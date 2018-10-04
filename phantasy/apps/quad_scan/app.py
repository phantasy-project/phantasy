#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant

from .ui.ui_app import Ui_MainWindow
from phantasy_ui.templates import BaseAppForm

from phantasy.apps.utils import get_open_filename
from phantasy.apps.correlation_visualizer.data import JSONDataSheet
from phantasy.apps.correlation_visualizer.data import ScanDataModel


class QuadScanWindow(BaseAppForm, Ui_MainWindow):

    # scan plot curve w/ errorbar
    curveUpdated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    def __init__(self, version):
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

        # data from app: Correlation Visualizer
        self.qs_data = None

        # events
        self.curveUpdated.connect(self.matplotliberrorbarWidget.update_curve)

    @pyqtSlot()
    def onOpen(self):
        """Open data sheet for quad scan, which is generated from
        'Correlation Visualizer' app.
        """
        filepath, ext = get_open_filename(self,
                filter="JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)")
        if ext.upper() == 'JSON':
            # process json data sheet
            self.qs_data = JSONDataSheet(filepath)
        elif ext.upper() == 'H5':
            # process h5 data sheet
            pass

        # present data
        self.update_ui_with_data(self.qs_data)

    def update_ui_with_data(self, data=None):
        """Present data in app.
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
        self.curveUpdated.emit(x, y, xerr, yerr)

