#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QProcessEnvironment
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
import epics
import time
import os
from functools import partial

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.utils import uptime

from .ui.ui_app import Ui_MainWindow
from .app_vainfo import VAProcessInfoWidget

CURDIR = os.path.dirname(__file__)

MACHINE_DICT = {
    'VA_LEBT': ('LEBT',),
    'VA_MEBT': ('MEBT',),
    #'VA_LS1FS1': ('LINAC', 'LS1', 'FS1',),
    'VA_LS1FS1': ('LINAC',),
}

MACHINE_LIST = sorted(list(MACHINE_DICT.keys()))

# MPS status
MPS_STATUS = ["Fault", "Disable", "Monitor", "Enable"]
MPS_ENABLE = MPS_STATUS.index("Enable")
MPS_FAULT = MPS_STATUS.index("Fault")
MPS_DISABLE = MPS_STATUS.index("Disable")
MPS_MONITOR = MPS_STATUS.index("Monitor")

#
TIME_OUT = 20


class VALauncherWindow(BaseAppForm, Ui_MainWindow):
    # va status changed, message to set, color of the string
    vaStatusChanged = pyqtSignal('QString', QColor)

    # pv is connected or not
    pv_connected = pyqtSignal(bool)

    #
    start_timeout = pyqtSignal()

    def __init__(self, version):
        super(VALauncherWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Virtual Accelerator Launcher")

        # set app properties
        self.setAppTitle("VA Launcher")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Virtual Accelerator Launcher</h4>
            <p>Start virtual accelerators of FRIB for app development,
            current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # initialize va_process
        self.va_process = None

        # va process info widget
        self._va_info_widget = None

        # noise pv
        self.noise_pv = None
        self._noise_pv_name = 'VA:SVR:NOISE'

        # mps status pv
        self.mps_pv = None
        self._mps_pv_name = 'VA:SVR:MpsStatus'

        # pv prefix
        self._prefix = None

        # CA local only
        self._ca_local_only = False

        # events
        # pv conn
        self.pv_connected.connect(self.on_pv_connected)
        # va status
        self.vaStatusChanged.connect(self.on_va_status_changed)
        # 0.001 * i -> 0.1% * i
        self.noise_slider.valueChanged.connect(
                lambda i:self.noise_label.setText("{:.1f}%".format(i*0.1)))
        self.noise_slider.valueChanged.connect(self.on_change_noise)

        # mps status
        self.mps_fault_radiobtn.toggled[bool].connect(
                partial(self.on_change_mps, "Fault")),
        self.mps_disable_radiobtn.toggled[bool].connect(
                partial(self.on_change_mps, "Disable"))
        self.mps_monitor_radiobtn.toggled[bool].connect(
                partial(self.on_change_mps, "Monitor"))
        self.mps_enable_radiobtn.toggled[bool].connect(
                partial(self.on_change_mps, "Enable"))

        # timer for uptime
        self.uptimer = QTimer(self)
        self.uptimer.timeout.connect(self.on_update_uptime)

        # post ui init
        self._post_ui_init()

    def _post_ui_init(self):
        # fill out mach/segm combobox
        self.mach_comboBox.clear()
        self.mach_comboBox.addItems(MACHINE_LIST)
        self.mach_comboBox.setCurrentText(MACHINE_LIST[0])
        self.mach_comboBox.currentTextChanged.emit(MACHINE_LIST[0])

        # toolbar for featured buttons
        self._setup_toolbar()

        # uptime label
        self.uptime_label.setText("00:00:00")

        # initialization, va config
        self.on_machine_changed(self.mach_comboBox.currentText())
        self.on_engine_changed(self.engine_comboBox.currentText())

        # disable all other tools
        self.enable_all_tools(False)

        #
        #self.mach_comboBox.setEditable(False)
        #self.segm_comboBox.setEditable(False)
        self.mach_comboBox.setEditable(True)
        self.segm_comboBox.setEditable(True)

    def _setup_toolbar(self):
        # va run tool
        self.va_run_tool.setToolTip("Run Virtual Accelerator")

        # va stop tool
        self.va_stop_tool.setToolTip("Stop Virtual Accelerator")

        # notebook tool
        self.nb_tool.setToolTip("Launch Jupyter-Notebook")

        # va info tool
        self.va_info_tool.setToolTip("Show VA Running Status")

        # initial visibility
        self.va_run_tool.setEnabled(True)
        self.va_stop_tool.setEnabled(False)

    @pyqtSlot()
    def on_update_uptime(self):
        """Update uptime box.
        """
        up_secs = time.time() - self.start_time
        self.uptime_label.setText(uptime(up_secs))

    @pyqtSlot()
    def on_run_va(self):
        """Run VA.
        """
        env = QProcessEnvironment.systemEnvironment()
        k = 'PHANTASY_CONFIG_DIR'
        if k not in env.keys():
            env.insert(k, '/usr/lib/phantasy-machines')
        mach = self._mach
        segm = self._segm
        run_cmd = self._run_cmd
        prefix = self._prefix
        #
        va = QProcess()
        va.setProcessEnvironment(env)
        self.va_process = va
        arguments = [run_cmd, '--mach', mach, '--subm', segm]
        if prefix is not None and prefix not in ('', 'NONE'):
            arguments.extend(['--pv-prefix', prefix])
            self._noise_pv_name = "{}:SVR:NOISE".format(prefix)
            self._mps_pv_name = "{}:SVR:MpsStatus".format(prefix)
        if self._ca_local_only:
            arguments.append("-l")
        va.start('phytool', arguments)

        # start va
        va.started.connect(self.on_va_started)
        #va.errorOccurred.connect(self.on_error_occurred)
        #
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.on_tick_startup)
        self._timer_start = time.time()
        self._timer.start(1000)
        self.start_timeout.connect(self.on_startup_timeout)
        self.msg_box = QMessageBox(self)
        self.msg_box.setWindowTitle("VA Launcher")
        self.msg_box.setText("Virtual Accelerator is starting...")
        self.msg_box.exec_()

    def on_error_occurred(self, err):
        print("Error (code: {}) occurred...".format(err))

    def on_tick_startup(self):
        dt = time.time() - self._timer_start
        if dt >= TIME_OUT:
            self.start_timeout.emit()
            self._timer.stop()
        else:
            self.msg_box.setText(
                "Virtual Accelerator is starting... ({}s)".format(int(dt)))

    def on_startup_timeout(self):
        self.msg_box.close()
        QMessageBox.warning(self, "VA Launcher",
                "Virtual Accelerator Starting Up Timeout (20s). Please try again.",
                QMessageBox.Ok)

    @pyqtSlot('QString', QColor)
    def on_va_status_changed(self, s, color):
        self.va_status_label.setText(s)
        self.va_status_label.setStyleSheet(
                """QLabel {{
                    background-color:{c};
                    color: white;
                    border: 1px solid {c};
                    border-radius: 5px;
                    padding: 2px;
                }}""".format(c=color.name()))

    @pyqtSlot()
    def on_va_started(self):
        """VA is started.
        """
        # noise pv
        self.noise_pv = epics.PV(self._noise_pv_name,
            connection_callback=partial(self.__on_connection_changed, name="noise"),
            callback=partial(self.__on_value_changed, name="noise"))
        # mps status pv
        self.mps_pv = epics.PV(self._mps_pv_name,
            connection_callback=partial(self.__on_connection_changed, name="mps"),
            callback=partial(self.__on_value_changed, name="mps"))

    def update_widgets_visibility(self, status="STARTED"):
        """Enable/Disable widgets when VA is STARTED or STOPPED.
        """
        if status == 'STARTED':
            # enable tool buttons panel
            # enable VA STOP, disable VA START
            # disable VA configuration panel
            self.enable_all_tools()
            self.va_run_tool.setEnabled(False)
            self.va_stop_tool.setEnabled(True)
            self.config_groupBox.setEnabled(False)
        elif status == 'STOPPED':
            # disable tool buttons panel
            # disable VA STOP, enable VA START
            # enable VA configuration panel
            self.enable_all_tools(False)
            self.va_run_tool.setEnabled(True)
            self.va_stop_tool.setEnabled(False)
            self.config_groupBox.setEnabled(True)

    @pyqtSlot()
    def on_stop_va(self):
        """Stop VA.
        """
        pid = self.va_process.processId()
        self.va_process.kill()
        print("VA ({}) is stopped...".format(pid))

    @pyqtSlot('QString')
    def on_machine_changed(self, s):
        """Machine is changed, update segm_combob items.
        """
        try:
            self._mach = s
            self.segm_comboBox.currentTextChanged.disconnect()
            self.segm_comboBox.clear()
            self.segm_comboBox.currentTextChanged.connect(self.on_segment_changed)
            seg_names = MACHINE_DICT[s]
            self.segm_comboBox.addItems(seg_names)
            self.segm_comboBox.setCurrentText(seg_names[0])
        except:
            pass

    @pyqtSlot('QString')
    def on_segment_changed(self, s):
        """Segment is changed.
        """
        self._segm = s

    @pyqtSlot('QString')
    def on_pvprefix_changed(self, s):
        """PV string prefix is changed.
        """
        self._prefix = s.upper()

    @pyqtSlot('QString')
    def on_engine_changed(self, s):
        self._engine = s
        self._run_cmd = '{}-vastart'.format(s.lower())

    @pyqtSlot()
    def on_view_va_info(self):
        """VA info tool button: view va process information.
        """
        if self.va_process is None:
            return

        if self._va_info_widget is None:
            w = VAProcessInfoWidget(self.va_process.processId())
            self._va_info_widget = w
        self._va_info_widget.show_widget()

    @pyqtSlot()
    def on_launch_notebook(self):
        """Notebook tool button: launch jupyter notebook with predefined
        python environment.
        """
        obj = self.sender()
        def on_nb_started():
            obj.setText("STOP-NB")
            obj.setIcon(QIcon(QPixmap(":/icons/notebook_stop.png")))
            obj.setToolTip("Stop Jupyter-notebook")

        if obj.text() == "RUN-NB":
            mach = self._mach
            self.nb_p = p = QProcess(self)
            cmd = "jupyter-notebook"
            nbfile = os.path.join(CURDIR, 'nb', "{}.ipynb".format(self._mach))
            args = []
            if os.path.isfile(nbfile):
                args.append(nbfile)
            p.start(cmd, args)
            p.started.connect(on_nb_started)
        elif obj.text() == "STOP-NB":
            self.nb_p.kill()
            obj.setText("RUN-NB")
            obj.setIcon(QIcon(QPixmap(":/icons/notebook_run.png")))
            obj.setToolTip("Launch Jupyter-notebook")

    def enable_all_tools(self, enable=True):
        """Enable/disable all tools, except RUN/STOP VA tools.
        """
        [t.setEnabled(enable) for t in (self.nb_tool, self.va_info_tool)]

    def closeEvent(self, e):
        try:
            self.on_stop_va()
            self.va_process.waitForFinished()
        except:
            pass
        BaseAppForm.closeEvent(self, e)

    @pyqtSlot(int)
    def on_change_noise(self, i):
        """Update VA noise level.
        """
        if self.noise_pv is not None and self.noise_pv.connected:
            v = i * 0.001
            self.noise_pv.put(v, wait=True)

    @pyqtSlot(bool)
    def on_change_mps(self, status, f):
        if f:
            self.mps_pv.put(status)

    @pyqtSlot(bool)
    def on_localonly(self, f):
        """CA localhost only or not.
        """
        self._ca_local_only = f

    def __on_connection_changed(self, name="noise", pvname=None, conn=None, **kws):
        self.pv_connected.emit(conn)
        if name == "mps" and conn:
            self.mps_pvname_lbl.setText(self._mps_pv_name)

    def __on_value_changed(self, name="noise", pvname=None, value=None, host=None, **kws):
        if name == "noise":
            v = int(value / 0.001)
            self.noise_slider.setValue(v)
        else:
            # mps
            if value == MPS_ENABLE:
                self.mps_enable_radiobtn.setChecked(True)
            elif value == MPS_FAULT:
                self.mps_fault_radiobtn.setChecked(True)
            elif value == MPS_MONITOR:
                self.mps_monitor_radiobtn.setChecked(True)
            elif value == MPS_ENABLE:
                self.mps_enable_radiobtn.setChecked(True)

    @pyqtSlot(bool)
    def on_pv_connected(self, conn):
        """PV is connected or not.
        """
        self._timer.stop()
        self.enable_noise_controls(conn)
        self.enable_mps_controls(conn)
        if conn:
            # reset VAProcessInfoWidget
            self._va_info_widget = None
            #
            self.va_name_label.setText(
                "{}/{}, PV prefixed with {}".format(
                    self._mach, self._segm, self._prefix))
            if self._prefix == 'NONE' or self._prefix is None:
                self.va_name_label.setToolTip(
                    "PV prefixed with default one, e.g. 'VA'")
            else:
                self.va_name_label.setToolTip('')
            #
            self.vaStatusChanged.emit("Running", QColor("#4E9A06"))
            self.update_widgets_visibility(status="STARTED")
            self.start_time = time.time()
            self.uptimer.start(1000)
            #
            self.msg_box.close()
        else:
            self.vaStatusChanged.emit("Stopped", QColor("#EF2929"))
            self.update_widgets_visibility(status="STOPPED")
            self.uptimer.stop()

    def enable_noise_controls(self, enable=True):
        """Enable controls for noise or not.
        """
        for o in (self.noise_slider, self.noise_label):
            o.setEnabled(enable)

    def enable_mps_controls(self, enable=True):
        """Enable controls for mps status or not.
        """
        for o in (self.mps_fault_radiobtn, self.mps_disable_radiobtn,
                  self.mps_monitor_radiobtn, self.mps_enable_radiobtn,
                  self.mps_pvname_lbl):
            o.setEnabled(enable)

    def sizeHint(self):
        return QSize(600, 300)
