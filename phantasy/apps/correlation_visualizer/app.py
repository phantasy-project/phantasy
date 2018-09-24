#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_app import Ui_MainWindow
#from .app_help import HelpDialog
#from .icons import tv_icon
from phantasy_ui.templates import BaseAppForm

import numpy as np

from PyQt5.QtGui import QDoubleValidator

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest

from .utils import PVElement
from .utils import PVElementReadonly
from .utils import delayed_exec


class CorrelationVisualizerWindow(BaseAppForm, Ui_MainWindow):

    # scan log
    scanlogUpdated = pyqtSignal('QString')

    def __init__(self, version):
        super(CorrelationVisualizerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Correlation Visualizer")
        # self.setWindowIcon(QIcon(QPixmap(icon)))

        # set app properties
        self.setAppTitle("Correlation Visualizer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Correlation Visualizer</h4>
            <p>This app is created to visualize the correlation between
            selected parameters, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # timers
        self.init_timers()

        # daq ctrl btns
        self.start_btn.clicked.connect(self.on_click_start_btn)
        self.stop_btn.clicked.connect(self.on_click_stop_btn)
        self.retake_btn.clicked.connect(self.on_click_retake_btn)
        self.pause_btn.clicked.connect(self.on_click_pause_btn)

        # events
        self.niter_spinBox.valueChanged.connect(self.set_scan_daq)
        self.nshot_spinBox.valueChanged.connect(self.set_scan_daq)
        self.waitsec_dSpinBox.valueChanged.connect(self.set_scan_daq)
        self.scanrate_dSpinBox.valueChanged.connect(self.set_scan_daq)
        self.show_scan_data_btn.clicked.connect(self.show_scan_outdata)

        # signals & slots
        self.scanlogUpdated.connect(self.scan_log_textEdit.append)

        # alter vars
        self.scan_vars_put_lineEdit.returnPressed.connect(self.set_alter_vars)
        self.scan_vars_get_lineEdit.returnPressed.connect(self.set_alter_vars)

        # alter range
        self.lower_limit_lineEdit.returnPressed.connect(self.set_alter_range)
        self.upper_limit_lineEdit.returnPressed.connect(self.set_alter_range)

        # monitor vars
        self.monitor_vars_lineEdit.returnPressed.connect(self.set_monitor_vars)

        # scan_vars_type_cbb / monitor_vars_type_cbb
        # 'PV' for generic PV strings;
        # 'Element' for high-level element from PHANTASY
        self.scan_vars_type_cbb.currentTextChanged['QString'].connect(self.on_select_alter_vars_type)
        self.monitor_vars_type_cbb.currentTextChanged['QString'].connect(self.on_select_monitor_vars_type)

        # copy_pvname_btn, if copy scan put pv string as get pv
        self.copy_pvname_btn.clicked.connect(self.on_copy_pvname)

        # UI post_init
        self._post_init_ui()

    @pyqtSlot()
    def show_scan_outdata(self):
        """Show scan output data.
        """
        print(self.scan_out_all)
        np.save('/tmp/scan_data.npy', self.scan_out_all)

    @pyqtSlot()
    def on_copy_pvname(self):
        """If copying text from *scan_vars_put_lineEdit* to
        *scan_vars_get_lineEdit*.
        """
        self.scan_vars_get_lineEdit.setText(self.scan_vars_put_lineEdit.text())

    def _post_init_ui(self):
        """post init ui
        """
        self.on_select_alter_vars_type(self.scan_vars_type_cbb.currentText())
        self.on_select_monitor_vars_type(self.monitor_vars_type_cbb.currentText())

        # validators
        self.lower_limit_lineEdit.setValidator(QDoubleValidator())
        self.upper_limit_lineEdit.setValidator(QDoubleValidator())

        # init scan config
        self.init_scan_config()

        # btn's status
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.retake_btn.setEnabled(False)

    @pyqtSlot('QString')
    def on_select_monitor_vars_type(self, val):
        """Select type for monitor var type
        """
        if val == 'Element':
            # do not accept input
            self.monitor_vars_lineEdit.setEnabled(False)
            self.select_monitor_elems_btn.setEnabled(True)
        else:
            self.monitor_vars_lineEdit.setEnabled(True)
            self.select_monitor_elems_btn.setEnabled(False)

    @pyqtSlot('QString')
    def on_select_alter_vars_type(self, val):
        """Select type for alter var type
        """
        if val == 'Element':
            # put and get boxes do not accept input
            self.scan_vars_put_lineEdit.setEnabled(False)
            self.scan_vars_get_lineEdit.setEnabled(False)
            self.copy_pvname_btn.setEnabled(False)
            self.select_scan_elems_btn.setEnabled(True)
        else:
            self.scan_vars_get_lineEdit.setEnabled(True)
            self.scan_vars_put_lineEdit.setEnabled(True)
            self.copy_pvname_btn.setEnabled(True)
            self.select_scan_elems_btn.setEnabled(False)

    @pyqtSlot()
    def set_monitor_vars(self):
        """Set DAQ interface for vars to be monitored.
        """
        getPV_str = self.monitor_vars_lineEdit.text()
        if getPV_str == '':
            return

        self.monitor_var_elem = PVElementReadonly(getPV_str)
        self.delayed_check_pv_status(self.monitor_var_elem)

    @pyqtSlot()
    def set_alter_vars(self):
        """Set DAQ interface for vars to be altered.
        """
        putPV_str = self.scan_vars_put_lineEdit.text()
        getPV_str = self.scan_vars_get_lineEdit.text()
        if putPV_str == '' or getPV_str == '':
            return

        self.alter_var_elem = PVElement(putPV_str, getPV_str)
        self.delayed_check_pv_status(self.alter_var_elem)

    @pyqtSlot()
    def set_alter_range(self):
        """Set scan alter vars range.

        *alter_range_array* : array to iterately alter
        """
        smin_str = self.lower_limit_lineEdit.text()
        smax_str = self.upper_limit_lineEdit.text()
        if smin_str == '' or smax_str == '':
            return

        try:
            smin, smax = float(smin_str), float(smax_str)
            assert smin < smax
        except AssertionError:
            QMessageBox.warning(self, "Warning",
                    "Lower limit must be less than upper limit.",
                    QMessageBox.Ok)
            self.lower_limit_lineEdit.setText(str(smax))
            self.upper_limit_lineEdit.setText(str(smin))
        else:
            self.alter_range_array = np.linspace(
                smin, smax, self.scan_iternum_val)

    def set_scan_outdata(self):
        """Set storage for the data yield from scan.
        """
        # pre-allocated array for every iteration
        self.scan_out_per_iter = np.zeros((self.scan_shotnum_val, 2))
        # pre-allocated array for all the iteration
        # shape: niter, nshot, ndim (2)
        self.scan_out_all = np.asarray([
            [[np.nan, np.nan]] * self.scan_shotnum_val
            ] * self.scan_iternum_val
        )

        # set current index at altered, i.e. self.alter_range_array
        self.current_alter_index = 0

    def init_scan_config(self):
        """Initialize scan configurations, including:
        1. Scan vars: the vars to be altered and
           the ones used as monitoring purpose.
        2. Scan range
        3. DAQ settings
        4. Scan data out settings
        """
        # vars to be altered:
        # scan_vars_type_cbb: PV or Element
        self.set_alter_vars()

        # vars to be monitored:
        # monitor_vars_type_cbb: PV or Element
        self.set_monitor_vars()

        # scan daq params
        self.set_scan_daq()

        # scan range
        self.set_alter_range()

        # scan output data
        self.set_scan_outdata()

    @pyqtSlot()
    def on_click_start_btn(self):
        """Start a new scan routine, initialize everything.
        """
        # initialize configuration for scan routine
        self.init_scan_config()

        # reset scan log
        self.scan_log_textEdit.clear()
        self.scanlogUpdated.emit("Starting scan...")

        # reset scan_plot_widget

        # start scan
        self.scantimer.start(self.scantimer_deltmsec)

        # update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)
        self.retake_btn.setEnabled(True)

    @pyqtSlot()
    def on_click_stop_btn(self):
        """Stop scan routine, can only start again.
        """
        self.scantimer.stop()
        self.daqtimer.stop()
        # publish summary info in scan log
        self.scanlogUpdated.emit("Scan routine stopped.")

        # update UI
        self.stop_btn.setEnabled(False)
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.retake_btn.setEnabled(True)

    @pyqtSlot()
    def on_click_pause_btn(self):
        """Pause scan routine.
        """
        if self.sender().text() == 'Pause':
            self.pause_btn.setText('Resume')
            # pause action
        else:
            self.pause_btn.setText('Pause')
            # resume action
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.retake_btn.setEnabled(True)

    @pyqtSlot()
    def on_click_retake_btn(self):
        """Re-scan with selected points.
        """
        self.retake_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)

    def init_timers(self):
        """Initialize timers for DAQ and SCAN control.
        """
        self.daqtimer = QTimer()
        self.scantimer = QTimer()
        self.daqtimer.timeout.connect(self.on_daqtimer_timeout)
        self.scantimer.timeout.connect(self.on_scantimer_timeout)

    @pyqtSlot()
    def on_daqtimer_timeout(self):
        """DAQ within one scan iteration.
        """
        try:
            assert self.daq_cnt < self.scan_shotnum_val
        except AssertionError:
            # stop DAQ timer
            self.daqtimer.stop()

            # update scan log
            idx = self.current_alter_index_in_daq
            log = 'Iter: {0:>3d}/[{1:d}] is done, scan value: {2:>10.3f}.'.format(
                    idx + 1, self.scan_iternum_val, self.alter_range_array[idx])
            self.scanlogUpdated.emit(log)

            # debug only
            #print("-"*20)
            #print(self.current_alter_index_in_daq)
            #print(self.scan_out_per_iter)
            #print(self.scan_out_all)
            #print("-"*20)

            # push finish message
            if not self.scantimer.isActive():
                self.scanlogUpdated.emit("Scan routine finished.")

            # update figure

        else:
            self.scan_out_per_iter[self.daq_cnt, :] = \
                self.alter_var_elem.value, \
                self.monitor_var_elem.value

            # update data: scan_out_all
            self.scan_out_all[self.current_alter_index_in_daq, :, :] = self.scan_out_per_iter

            # next daq event
            self.daq_cnt += 1

    @pyqtSlot()
    def on_scantimer_timeout(self):
        """Update parameters for next scan iteration.
        """
        try:
            assert self.current_alter_index < self.scan_iternum_val
        except AssertionError:
            self.scantimer.stop()
            self.start_btn.setEnabled(True)
        else:
            # get the current value to be set
            current_alter_val = self.alter_range_array[self.current_alter_index]
            # make set/put operation
            self.alter_var_elem.value = current_alter_val

            # wait
            QTest.qWait(self.scan_waitmsec_val)

            # start DAQ
            self.start_daqtimer(self.daqtimer_deltmsec, self.current_alter_index)

            # to next alter value
            self.current_alter_index += 1

    def start_daqtimer(self, deltmsec, idx):
        """Start DAQ timer, current alter data *idx* must be reserved within
        the DAQ routine.

        Parameters
        ----------
        deltmsec : float
            Millisecond timeout interval for DAQ timer.
        idx : int
            Index of the current alter value.
        """
        self.current_alter_index_in_daq = idx
        self.daq_cnt = 0 # max: self.scan_shotnum_val
        self.daqtimer.start(deltmsec)

    @pyqtSlot()
    def set_scan_daq(self):
        """Set scan DAQ parameters, and timeout for DAQ and SCAN timers.
        """
        # total number of scan points
        self.scan_iternum_val = self.niter_spinBox.value()
        # time wait after every scan data setup, in msec
        self.scan_waitmsec_val = self.waitsec_dSpinBox.value() * 1000.0
        # total shot number for each scan iteration
        self.scan_shotnum_val = self.nshot_spinBox.value()
        # scan DAQ rate, in Hz
        self.scan_daqrate_val = self.scanrate_dSpinBox.value()

        # scan DAQ timer timeout interval, in msec
        self.daqtimer_deltmsec = 1000.0 / self.scan_daqrate_val

        # SCAN timer timeout interval (between iteration), in msec
        self.scantimer_deltmsec = self.scan_waitmsec_val + (
                self.scan_shotnum_val + 2) * self.daqtimer_deltmsec

        # debug
        print("iter:{iter}, shot#:{shot}, wait_t:{wt}, daq:{daq}".format(
            iter=self.scan_iternum_val, shot=self.scan_shotnum_val,
            wt=self.scan_waitmsec_val, daq=self.scan_daqrate_val))
        print("DAQ Timer interval: {}ms\nSCAN Timer interval: {} ms".format(
            self.daqtimer_deltmsec, self.scantimer_deltmsec))

    def delayed_check_pv_status(self, pvelem, delay=1000):
        """Check PV element connected or not.

        Parameters
        ----------
        pvelem : obj
            Instance of `epics.PV`, `PVElement`, `PVElementReadonly`.
        """
        def check_status(elem):
            if not elem.connected:
                r = QMessageBox.warning(self, "Warning",
                        "Cannot connect to the input PV(s).",
                        QMessageBox.Ok)
        QTimer.singleShot(delay, lambda : check_status(pvelem))
