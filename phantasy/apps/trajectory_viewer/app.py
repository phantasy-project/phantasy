#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDoubleValidator

from PyQt5.QtWidgets import QMessageBox

from functools import partial
from collections import OrderedDict

from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.latticewidget import LatticeWidget

from .app_elem_selection import ElementSelectionWidget
from .app_help import HelpDialog
from .utils import apply_mplcurve_settings
from .ui.ui_app import Ui_MainWindow
from .utils import ElementListModel

BPM_UNIT_FAC = {"mm": 1.0, "m": 1e3}


class TrajectoryViewerWindow(BaseAppForm, Ui_MainWindow):

    # curves
    lineChanged = pyqtSignal(int)
    xdataChanged = pyqtSignal(QVariant)
    ydataChanged = pyqtSignal(QVariant)

    # lattice is loaded
    latticeChanged = pyqtSignal(QVariant)

    def __init__(self, version):
        super(TrajectoryViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Trajectory Viewer")

        # set app properties
        self.setAppTitle("Trajectory Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Trajectory Viewer</h4>
            <p>This app is created to visualize the beam central
            trajectory of FRIB accelerator, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # events
        self.start_btn.clicked.connect(self.start_daq)
        self.stop_btn.clicked.connect(self.stop_daq)

        # select element btn: BPMs
        self.select_bpms_btn.clicked.connect(
                partial(self.on_select_elements, 'bpm', ["BPM"]))

        # select element btn:CORs
        self.select_cors_btn.clicked.connect(
                partial(self.on_select_elements, 'cor', ["HCOR", "VCOR"]))

        # DAQ freq
        self.freq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)

        # curve
        self.lineChanged.connect(self.matplotlibcurveWidget.setLineID)
        self.xdataChanged.connect(self.matplotlibcurveWidget.setXData)
        self.ydataChanged.connect(self.matplotlibcurveWidget.setYData)

        # xy limits
        self.__xylimits_lineEdits = (self.xmin_lineEdit,
                                     self.xmax_lineEdit,
                                     self.ymin_lineEdit,
                                     self.ymax_lineEdit)
        for o in self.__xylimits_lineEdits:
            o.setValidator(QDoubleValidator())
        self.xmin_lineEdit.textChanged.connect(
                lambda s: self.matplotlibcurveWidget.setXLimitMin(float(s)))
        self.xmax_lineEdit.textChanged.connect(
                lambda s: self.matplotlibcurveWidget.setXLimitMax(float(s)))
        self.ymin_lineEdit.textChanged.connect(
                lambda s: self.matplotlibcurveWidget.setYLimitMin(float(s)))
        self.ymax_lineEdit.textChanged.connect(
                lambda s: self.matplotlibcurveWidget.setYLimitMax(float(s)))

        # bpm unit
        self.bpm_unit_millimeter_rbtn.toggled.connect(
                partial(self.on_update_unit, "mm"))
        self.bpm_unit_meter_rbtn.toggled.connect(
                partial(self.on_update_unit, "m"))

        # bpm selection for monitoring
        self.use_all_bpms_rbtn.toggled.connect(
                partial(self.on_update_monitors, "all"))
        self.use_selected_bpms_rbtn.toggled.connect(
                partial(self.on_update_monitors, "selected"))

        # element selection for BPMs/CORs treeview
        self.select_all_bpms_btn.clicked.connect(
                partial(self.on_select_all_elems, "bpm"))
        self.inverse_bpm_selection_btn.clicked.connect(
                partial(self.on_inverse_current_elem_selection, "bpm"))
        self.select_all_cors_btn.clicked.connect(
                partial(self.on_select_all_elems, "cor"))
        self.inverse_cor_selection_btn.clicked.connect(
                partial(self.on_inverse_current_elem_selection, "cor"))

        # DAQ
        self.daq_timer = QTimer()
        self.daq_timer.timeout.connect(self.on_daq_update)

        # post init
        self.post_init()

    @pyqtSlot(bool)
    def on_update_monitors(self, strategy, f):
        """Use all or selected BPMs as monitors.
        """
        if not f:
            return
        model = self.bpms_treeView.model()
        if model is None:
            self._bpms = []
            return
        if strategy == "all":
            self._bpms = self.bpms_treeView.model().get_elements("all")
        else:
            self._bpms = self.bpms_treeView.model().get_elements("selected")

    @pyqtSlot(bool)
    def on_update_unit(self, unit, f):
        """Update BPM monitorings unit.
        """
        if f:
            self._bpm_unit = unit
            #print("BPM unit: {}".format(self._bpm_unit))

    @pyqtSlot()
    def on_select_elements(self, mode, dtype_list):
        """Select devices.
        """
        if self.__mp is None:
            QMessageBox.warning(self, "Select Element",
                    "Cannot find loaded lattice, try to load first, either by clicking Tools > Load Lattice or Ctrl+Shift+L.",
                    QMessageBox.Ok)
            return
        w = self._elem_sel_widgets.setdefault(mode,
                ElementSelectionWidget(self, self.__mp, dtypes=dtype_list))
        w.elementsSelected.connect(partial(self.on_update_elems, mode))
        w.show()

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    def post_init(self):
        #
        self.__mp = None
        self._bpm_unit = None
        self._bpms = None

        # lattice load window
        self._lattice_load_window = None
        # elem selection widget, key: 'bpm' and 'cor'
        self._elem_sel_widgets = {}

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        # add another curve to matplotlibcurveWidget
        self.matplotlibcurveWidget.add_curve()

        # bpm monitorings unit
        self.bpm_unit_millimeter_rbtn.setChecked(True)
        assert self._bpm_unit == "mm"

        # selection of bpms for monitoring
        self.use_selected_bpms_rbtn.setChecked(True)
        assert self._bpms == []

        # DAQ
        self._daqfreq = 1.0

        # load default figure config
        apply_mplcurve_settings(self.matplotlibcurveWidget)

    @pyqtSlot(OrderedDict)
    def on_elem_selection_updated(self, mode, d):
        # BPMs selection (bpms_treeView) is updated.
        # 1. trigger the update of self._bpms
        # 2. update monitors viz
        for o in (self.use_selected_bpms_rbtn, self.use_all_bpms_rbtn):
            o.toggled.emit(o.isChecked())

        #print(self._bpms, len(self._bpms))
        model = getattr(self, '{}s_treeView'.format(mode)).model()
        print("Selection is updated: ", model._selected_elements)

    @pyqtSlot()
    def on_select_all_elems(self, mode):
        """Select all BPMs/CORs in *mode*s_treeView.
        """
        try:
            print("Select All {}s".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self, mode):
        """Inverse current BPM/COR selection in *mode*s_treeView.
        """
        try:
            print("Inverse {} selection".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot(list)
    def on_update_elems(self, mode, enames):
        """Selected element names list updated, mode: 'bpm'/'cor'
        """
        #print(mode, len(enames))
        tv = getattr(self, "{}s_treeView".format(mode))
        #print(mode, tv.objectName(), len(enames))
        model = ElementListModel(tv, self.__mp, enames)
        model.set_model()

        # bpm/cor elementlistmodel
        tv.model().elementSelected.connect(partial(self.on_elem_selection_updated, mode))

    @pyqtSlot(QVariant)
    def update_lattice(self, o):
        self.__mp = o
        self.latticeChanged.emit(o)

    @pyqtSlot()
    def start_daq(self):
        # check if BPMs are selected from lattice.
        if self.not_selected_bpms():
            QMessageBox.warning(self, "DAQ Warning",
                    "BPMs are not found, Choose Monitors first.", QMessageBox.Ok)
            return
        # start DAQ
        self.daq_timer.start(1000.0/self._daqfreq)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    @pyqtSlot()
    def stop_daq(self):
        self.daq_timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    @pyqtSlot()
    def on_daq_update(self):
        """Update DAQ and show data.
        """
        ufac = BPM_UNIT_FAC[self._bpm_unit]

        if self._bpms == []:
            return
        xdata = [elem.sb for elem in self._bpms]
        line0_ydata = [elem.X * ufac for elem in self._bpms]
        line1_ydata = [elem.Y * ufac for elem in self._bpms]
        self.xdataChanged.emit(xdata)
        self.ydataChanged.emit(line0_ydata)
        self.lineChanged.emit(1)
        self.xdataChanged.emit(xdata)
        self.ydataChanged.emit(line1_ydata)
        self.lineChanged.emit(0)

    @pyqtSlot()
    def onHelp(self):
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    @pyqtSlot()
    def on_launch_orm(self):
        """Launch ORM app.
        """
        from phantasy.apps.orm import OrbitResponseMatrixWindow
        from phantasy.apps.orm import __version__

        self.orm_window = OrbitResponseMatrixWindow(__version__)
        self.orm_window.show()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
        self._lattice_load_window.show()
        self._lattice_load_window.latticeChanged.connect(self.update_lattice)
        # reset element selection widgets
        self._elem_sel_widgets = {}

    def not_selected_bpms(self):
        """Test if BPMs are selected or not.
        """
        return self.bpms_treeView.model() is None

    @pyqtSlot(bool)
    def on_auto_xyscale(self, f):
        """Set auto xyscale or not
        """
        if f: # auto scale
            p = self.matplotlibcurveWidget
            xmin, xmax = p.get_xlim()
            ymin, ymax = p.get_ylim()
            self.xmin_lineEdit.setText("{0:.3g}".format(xmin))
            self.xmax_lineEdit.setText("{0:.3g}".format(xmax))
            self.ymin_lineEdit.setText("{0:.3g}".format(ymin))
            self.ymax_lineEdit.setText("{0:.3g}".format(ymax))
            for o in self.__xylimits_lineEdits:
                o.setEnabled(False)
        else:
            for o in self.__xylimits_lineEdits:
                o.setEnabled(True)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = TrajectoryViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
