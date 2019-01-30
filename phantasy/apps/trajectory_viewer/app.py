#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QMessageBox

from functools import partial

from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.latticewidget import LatticeWidget

from .app_elem_selection import ElementSelectionWidget
from .app_help import HelpDialog
from .utils import apply_mplcurve_settings
from .ui.ui_app import Ui_MainWindow
from .utils import ElementListModel


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

        # post init
        self.post_init()

        # events
        self.start_btn.clicked.connect(self.start_daq)
        self.start_btn.clicked.connect(self.start_btn.setEnabled)
        self.start_btn.clicked.connect(lambda x:self.stop_btn.setEnabled(not x))
        self.stop_btn.clicked.connect(self.stop_daq)
        self.stop_btn.clicked.connect(self.stop_btn.setEnabled)
        self.stop_btn.clicked.connect(lambda x:self.start_btn.setEnabled(not x))

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

        self.daq_timer = QTimer()
        self.daq_timer.timeout.connect(self.on_daq_update)

    @pyqtSlot()
    def on_select_elements(self, mode, dtype_list):
        """Select devices.
        """
        if self.__mp is None:
            QMessageBox.warning(self, "Select Element",
                    "Cannot find loaded lattice, try to load first, either by clicking Tools --> Load Lattice or Ctrl + Shift + L.",
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

        # lattice load window
        self._lattice_load_window = None
        # elem selection widget, key: 'bpm' and 'cor'
        self._elem_sel_widgets = {}

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        # add another curve to matplotlibcurveWidget
        self.matplotlibcurveWidget.add_curve()
        # initial values
        self._bpms = []
        self._daqfreq = 1.0

        # load default figure config
        apply_mplcurve_settings(self.matplotlibcurveWidget)

    @pyqtSlot(list)
    def on_update_elems(self, mode, enames):
        """Selected element names list updated, mode: 'bpm'/'cor'
        """
        #print(mode, len(enames))
        tv = getattr(self, "{}s_treeView".format(mode))
        #print(mode, tv.objectName(), len(enames))
        model = ElementListModel(tv, self.__mp, enames)
        model.set_model()

    @pyqtSlot(QVariant)
    def update_lattice(self, o):
        self.__mp = o
        self.latticeChanged.emit(o)

    @pyqtSlot()
    def start_daq(self):
        self.daq_timer.start(1000.0/self._daqfreq)

    @pyqtSlot()
    def stop_daq(self):
        self.daq_timer.stop()

    @pyqtSlot()
    def on_daq_update(self):
        """Update DAQ and show data.
        """
        if self._bpms == []:
            return
        xdata = [elem.sb for elem in self._bpms]
        line0_ydata = [elem.X*1e3 for elem in self._bpms]
        line1_ydata = [elem.Y*1e3 for elem in self._bpms]
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


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = TrajectoryViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
