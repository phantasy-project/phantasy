#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_app import Ui_MainWindow
from .app_help import HelpDialog
from phantasy_ui.templates import BaseAppForm

from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer


class TrajectoryViewerWindow(BaseAppForm, Ui_MainWindow):

    lineChanged = pyqtSignal(int)
    xdataChanged = pyqtSignal(QVariant)
    ydataChanged = pyqtSignal(QVariant)
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
        # DAQ freq
        self.freq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)
        # curve
        self.lineChanged.connect(self.matplotlibcurveWidget.setLineID)
        self.xdataChanged.connect(self.matplotlibcurveWidget.setXData)
        self.ydataChanged.connect(self.matplotlibcurveWidget.setYData)

        self.daq_timer = QTimer()
        self.daq_timer.timeout.connect(self.on_daq_update)

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    def post_init(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        # add another curve to matplotlibcurveWidget
        self.matplotlibcurveWidget.add_curve()
        # initial values
        self._bpms = []
        self._daqfreq = 1.0

    @pyqtSlot(QVariant)
    def onLatticeChanged(self, o):
        all_bpms = o.get_elements(type='BPM')
        if all_bpms:
            self._bpms = all_bpms

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

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = TrajectoryViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
