#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QToolButton
import epics
import time

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.utils import uptime

from .ui.ui_app import Ui_MainWindow
from .app_vainfo import VAProcessInfoWidget
from .icons import va_icon


class VALauncherWindow(BaseAppForm, Ui_MainWindow):
    # va status changed, message to set, color of the string
    vaStatusChanged = pyqtSignal('QString', QColor)

    def __init__(self, version):
        super(VALauncherWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Virtual Accelerator Launcher")
        self.setWindowIcon(QIcon(QPixmap(va_icon)))

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

        # events
        # va status
        self.vaStatusChanged.connect(self.on_va_status_changed)
        # 0.001 * i -> 0.1% * i
        self.noise_slider.valueChanged.connect(
                lambda i:self.noise_label.setText("{:.1f}%".format(i*0.1)))
        self.noise_slider.valueChanged.connect(self.on_change_noise)

        # timer for uptime
        self.uptimer = QTimer(self)
        self.uptimer.timeout.connect(self.on_update_uptime)

        # post ui init
        self._post_ui_init()

    def _post_ui_init(self):
        # uptime label
        self.uptime_label.setText("00:00:00")

        # initialization, va config
        self.on_machine_changed(self.mach_comboBox.currentText())
        self.on_engine_changed(self.engine_comboBox.currentText())

        # disable all tools buttons
        self.enable_all_tools_buttons(False)

        # noise level
        self.noise_slider.valueChanged.emit(1)

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
        mach = self._mach
        run_cmd = self._run_cmd
        va = QProcess()
        self.va_process = va
        arguments = [run_cmd, '--mach', mach, '-v']
        va.start('/usr/local/bin/phytool', arguments)

        # start va
        va.started.connect(self.on_va_started)
        #va.errorOccurred.connect(self.on_error_occurred)

    def on_error_occurred(self, err):
        print("Error (code: {}) occurred...".format(err))

    @pyqtSlot('QString', QColor)
    def on_va_status_changed(self, s, color):
        self.va_status_label.setText(s)
        self.va_status_label.setStyleSheet(
                """QLabel {{
                    background-color:{c};
                    color: white;
                    border: 1px solid {c};
                    border-radius: 5px;
                    padding: 1px;
                }}""".format(c=color.name()))
        # noise pv
        self.noise_pv = epics.PV('VA:SVR:NOISE')

    @pyqtSlot()
    def on_va_started(self):
        """VA is started.
        """
        self.start_time = time.time()
        self.uptimer.start(1000)
        self.vaStatusChanged.emit("Running", QColor("#4E9A06"))
        self.enable_all_tools_buttons()

    @pyqtSlot()
    def on_stop_va(self):
        """Stop VA.
        """
        pid = self.va_process.processId()
        self.va_process.kill()
        print("VA ({}) is stopped...".format(pid))
        self.vaStatusChanged.emit("Stopped", QColor("#EF2929"))
        self.uptimer.stop()
        self.enable_all_tools_buttons(False)

    @pyqtSlot('QString')
    def on_machine_changed(self, s):
        """Machine is changed.
        """
        self._mach = s

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
        mach = self._mach
        p = QProcess(self)
        cmd = "/home/tong/.local/bin/jupyter-notebook"
        args = ["/home/tong/Dropbox/FRIB/work/phantasy-project/phantasy/phantasy/apps/quad_scan/tests/autofill_from_model.ipynb"]
        p.start(cmd, args)

    def enable_all_tools_buttons(self, enable=True):
        """Disable all buttons in tools groupbox.
        """
        for btn in self.tools_groupBox.findChildren(QToolButton):
            btn.setEnabled(enable)

    def closeEvent(self, e):
        try:
            self.on_stop_va()
            self.va_process.waitForFinished()
        except:
            pass
        self.close()

    @pyqtSlot(int)
    def on_change_noise(self, i):
        """Update VA noise level.
        """
        if self.noise_pv is not None and self.noise_pv.connected:
            v = i * 0.001
            self.noise_pv.put(v, wait=True)
