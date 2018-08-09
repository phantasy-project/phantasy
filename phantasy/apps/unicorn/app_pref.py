# -*- coding: utf-8 -*-

import time
import requests
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from .ui_app_pref import Ui_Dialog
from .utils import get_service_status
from .utils import init_unicorn_database


class PrefDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(PrefDialog, self).__init__()
        self.parent = parent
        self.setupUi(self)

        # set url and port
        self.lineEdit_url.setText(self.parent._url)
        self.lineEdit_port.setText(self.parent._port)
        # set pagezoom
        self.pageZoom.setCurrentText('{}%'.format(int(self.parent._pageZoom)))

        # refresher (UI)
        self.refresher = Refresher(self)
        self.refresher.srv_ctrl_btn_signal.connect(self.set_btn_style)
        self.refresher.start()

        # events
        self.btn_box.accepted.connect(self.on_accept_btn_box)
        self.btn_box.rejected.connect(self.on_reject_btn_box)
        self.srv_ctrl_btn.clicked.connect(self.srv_control)
        self.srv_data_btn.clicked.connect(self.init_database)

    def on_accept_btn_box(self):
        # url
        url, port = self.lineEdit_url.text(), self.lineEdit_port.text()
        base_url = url.rstrip('/') + ':' + port
        #if base_url != self.parent.get_base_url():
        self.parent._url = url
        self.parent._port = port
        self.parent.update_url(QUrl(base_url))

        # pageZoom
        self.parent._pageZoom = float(
            self.pageZoom.currentText().split('%')[0])
        self.parent.update_pageZoom()
        self.close()

    def on_reject_btn_box(self):
        self.close()

    def srv_control(self, e):
        sender = self.sender()
        url, port = self.lineEdit_url.text().rstrip('/'), self.lineEdit_port.text()
        if sender.text() == 'START':
            _start_unicorn_service(url, port)
            self.refresher.restart()
        else:
            _stop_unicorn_service(url, port)
            self.refresher.restart()

    def set_btn_style(self, s):
        btn = self.srv_ctrl_btn
        btn.setText(s)
        if s == 'STOP':
            btn.setStyleSheet(
                    "QPushButton {\n"
                    "    color: rgb(0, 170, 0);\n"
                    "  font-weight: bold;\n"
                    "}")
        else:
            btn.setStyleSheet(
                    "QPushButton {\n"
                    "  color: rgb(255, 0, 0);\n"
                    "  font-weight: bold;\n"
                    "}")

    def closeEvent(self, e):
        self.refresher.terminate()

    def init_database(self, e):
        init_unicorn_database()


class Refresher(QThread):
    srv_ctrl_btn_signal = pyqtSignal('QString')  # for control btn label
    def __init__(self, parent=None):
        super(Refresher, self).__init__(parent)
        self.parent = parent
        self.run_flag = True

    def run(self):
        while self.run_flag:
            if get_service_status(self.parent.parent.get_base_url()) == "Running":
                self.srv_ctrl_btn_signal.emit("STOP")
            else:
                self.srv_ctrl_btn_signal.emit("START")
            self.run_flag = False

    def restart(self):
        self.run_flag = True
        self.start()


def _start_unicorn_service(url, port):
    import subprocess
    cmdline = ["unicorn-admin", "run", port]
    app_process = subprocess.Popen(cmdline)


def _stop_unicorn_service(url, port):
    base_url = "{}:{}".format(url, port)
    try:
        requests.post("{}/shutdown".format(base_url))
    except requests.ConnectionError:
        print("Service is not running...")
    finally:
        print("Service is shutting down...")
