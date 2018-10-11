#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import lmfit

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDoubleValidator

from .ui.ui_app import Ui_MainWindow
from phantasy_ui.templates import BaseAppForm

from .utils import draw_beam_ellipse

from phantasy.apps.utils import get_open_filename
from phantasy.apps.correlation_visualizer.data import JSONDataSheet
from phantasy.apps.correlation_visualizer.data import ScanDataModel

LIGHT_SPEED = 299792458 # [m/s]
ION_ES = 9.31494e+08  # rest energy [eV/u]

# sample point for fitting curve
N_SAMPLE = 100


class QuadScanWindow(BaseAppForm, Ui_MainWindow):

    # scan plot curve w/ errorbar
    curveUpdated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # update fitting curve
    fitCurveChanged = pyqtSignal(QVariant, QVariant)

    def __init__(self, version, data=None):
        super(QuadScanWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Quadrupole Scan App")
        #self.setWindowIcon(QIcon(QPixmap(icon)))

        # set app properties
        self.setAppTitle("Quadrupole Scan App")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Quadrupole Scan App</h4>
            <p>This app is created to analyze the data from quadrupole
            scan, to calculate the beam transverse emittance and Twiss
            parameters, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # events
        self.curveUpdated.connect(self.matplotliberrorbarWidget.update_curve)

        # post init ui
        self.post_init_ui()

        # data from app: Correlation Visualizer
        # try to load data
        self.qs_data = data
        self.update_ui_with_data(self.qs_data)

    def post_init_ui(self):
        all_objs = self.beam_info_groupBox.findChildren(QLineEdit) \
                 + self.fitting_input_groupBox.findChildren(QLineEdit)
        for obj in all_objs:
            obj.setValidator(QDoubleValidator())

        # reset beam_ellipse_plot
        self.beam_ellipse_plot.axes.clear()
        self.beam_ellipse_plot.axes.axis('off')
        self.beam_ellipse_plot.update_figure()

        # data viz: matplotliberrorbarWidget
        # add one more curve for fitting
        self.matplotliberrorbarWidget.add_curve()
        # set the line label as 'Fitting'
        self.matplotliberrorbarWidget.setLineID(1)
        self.matplotliberrorbarWidget.setLineLabel("Fitting")
        self.matplotliberrorbarWidget.setLineID(0)
        self.matplotliberrorbarWidget.setFigureXlabel("Quad Gradient [T/m]")
        self.matplotliberrorbarWidget.setFigureYlabel("$\sigma^2\,\mathrm{[m^2]}$")
        # events
        self.fitCurveChanged[QVariant, QVariant].connect(self.update_fitting_curve)

    @pyqtSlot(QVariant, QVariant)
    def update_fitting_curve(self, x, y):
        """Update fitting line.
        """
        self.matplotliberrorbarWidget.setLineID(1)
        self.matplotliberrorbarWidget.setXData(x)
        self.matplotliberrorbarWidget.setYData(y)

    @pyqtSlot()
    def onOpen(self):
        """Open data sheet for quad scan, which is generated from
        'Correlation Visualizer' app.
        """
        filepath, ext = get_open_filename(self,
                filter="JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)")
        if filepath is None:
            return
        if ext.upper() == 'JSON':
            # process json data sheet
            self.qs_data = JSONDataSheet(filepath)
        elif ext.upper() == 'H5':
            # process h5 data sheet
            pass

        # present data
        self.update_ui_with_data(self.qs_data)

    def update_ui_with_data(self, data=None):
        """Present data.
        """
        if data is None:
            return

        data_ts_created = data['data']['created']
        task_duration_in_sec = data['task']['duration']
        data_shape = data['data']['shape']
        quad_name = data['devices']['quad']['name']
        monitor_names = [m['name'] for m in data['devices']['monitors']]
        scan_range = data['task']['scan_range']
        scan_data_model = ScanDataModel(np.asarray(data['data']['array']))

        # fillout lineEdits
        self.data_ts_created_lineEdit.setText(data_ts_created)
        self.task_duration_lineEdit.setText('{0:.2f}'.format(task_duration_in_sec))
        self.data_size_lineEdit.setText(
                "(niter:{s[0]} nshot:{s[1]} ndim:{s[2]})".format(s=data_shape))
        self.quad_name_lineEdit.setText(quad_name)
        self.monitor_names_lineEdit.setText(','.join(monitor_names))
        self.scan_range_lineEdit.setText('from {smin:.2f} to {smax:.2f} ({snum}) points'.format(
                smin=min(scan_range), smax=max(scan_range),
                snum=len(scan_range)))

        # show data on figure widget
        x, y = scan_data_model.get_xavg(), scan_data_model.get_yavg()
        xerr, yerr = scan_data_model.get_xerr(), scan_data_model.get_yerr()
        self.x, self.y = x, y**2
        self.matplotliberrorbarWidget.setEbLineID(0)
        self.matplotliberrorbarWidget.setLineID(0)
        self.curveUpdated.emit(x, y**2, xerr, yerr)

    @pyqtSlot()
    def on_fit_parabola(self):
        """Fit parabola curve with defined parameters.
        """
        ion_z = float(self.ref_IonZ_lineEdit.text())
        ion_beta = float(self.ref_beta_lineEdit.text())
        ion_w = float(self.ref_IonW_lineEdit.text())
        l_quad = float(self.quad_length_lineEdit.text())
        l_drift = float(self.distance_lineEdit.text())
        brho = ion_beta * ion_w / ion_z / LIGHT_SPEED
        bg = ion_beta * ion_w / ION_ES

        #
        a0 = float(self.coef_a_init_lineEdit.text())
        b0 = float(self.coef_b_init_lineEdit.text())
        c0 = float(self.coef_c_init_lineEdit.text())
        method = self.opt_method_comboBox.currentText()

        a, b, c, res = parabola_fitting(a0, b0, c0, self.x, self.y, method)

        (emit, nemit), (alpha, beta, gamma) = \
            single_quad_scan_analysis((a, b, c), l_quad, l_drift, brho, bg)

        # present results
        self.coef_a_final_lineEdit.setText('{0:.6g}'.format(a))
        self.coef_b_final_lineEdit.setText('{0:.6g}'.format(b))
        self.coef_c_final_lineEdit.setText('{0:.6g}'.format(c))
        self.resi_chisqr_lineEdit.setText('{0:.6g}'.format(res))

        self.emit_lineEdit.setText('{0:.6g}'.format(emit * 1e6))
        self.nemit_lineEdit.setText('{0:.6g}'.format(nemit * 1e6))
        self.twiss_alpha_lineEdit.setText('{0:.6g}'.format(alpha))
        self.twiss_beta_lineEdit.setText('{0:.6g}'.format(beta))
        self.twiss_gamma_lineEdit.setText('{0:.6g}'.format(gamma))

        # draw beam ellipse
        try:
            draw_beam_ellipse(self.beam_ellipse_plot.axes, alpha, beta, gamma, emit)
            self.beam_ellipse_plot.update_figure()
        except:
            QMessageBox.warning(self, "",
                    "Fatal error encountered.",
                    QMessageBox.Ok)

        # viz the fitting curve
        xx = np.linspace(self.x.min(), self.x.max(), N_SAMPLE)
        yy = (lambda x:a* x**2 + b * x + c)(xx)
        self.fitCurveChanged.emit(xx, yy)

    @pyqtSlot()
    def on_sync_coefs(self):
        """Sync the fitted ABC values to be the new set of initial settings.
        """
        self.coef_a_init_lineEdit.setText(self.coef_a_final_lineEdit.text())
        self.coef_b_init_lineEdit.setText(self.coef_b_final_lineEdit.text())
        self.coef_c_init_lineEdit.setText(self.coef_c_final_lineEdit.text())


def single_quad_scan_analysis(params, quad_length, drift_length,
                              rigidity, lorentz_energy):
    """Calculate the emittance and Twiss parameters from parabola coeffients
    and beam parameters.

    Parameters
    ----------
    params : tuple
        Tuple of a, b, c, from which parabola curve could be built as:
        f(G) = a * G^2 + b * G + c, where G is the quadrupole gradient in T/m.
    quad_length : float
        Quadrupole length in m.
    drift_length : float
        Drift between the beam size monitor and quadrupole, in m.
    rigidity : float
        Beam rigidity the quadrupole, as known as brho.
    lorentz_energy : float
        Relativistic lorentz factor of ion energy.

    Returns
    -------
    r : tuple
        Tuple of (geometrical emittance, normalized emittance),
        (alpha, beta, gamma), i.e. the first element is tuple of emittances,
        and the second element is tuple of Twiss parameters.
        Units: emittance: m.rad
    """
    a, b, c = params
    lq, d = quad_length, drift_length
    brho, bg = rigidity, lorentz_energy

    s11 = a * brho**2 / d / d / lq / lq
    s12 = (-b * brho - 2 * d * lq * s11) / (2 * d * d * lq)
    s22 = (c - s11 - 2 * d * s12) / d / d

    epsilon = (s11 * s22 - s12 ** 2) ** 0.5
    epsilon_n = epsilon * bg

    alpha, beta, gamma = -s12/epsilon, s11/epsilon, s22/epsilon

    return (epsilon, epsilon_n), (alpha, beta, gamma)


def parabola_fitting(a0, b0, c0, x, y, method):
    """Parabola curve fitting.
    """
    p = lmfit.Parameters()
    p.add('a', value=a0)
    p.add('b', value=b0)
    p.add('c', value=c0)

    def f(p, x, y):
        return p['a'] * x**2 + p['b'] * x + p['c'] - y

    res = lmfit.minimize(f, p, method, args=(x, y))

    a, b, c = res.params['a'].value, res.params['b'].value, res.params['c'].value

    return a, b, c, res.chisqr
