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
from .utils import start_unicorn_service
from .utils import stop_unicorn_service
from .utils import PORT_RANGE


class PrefDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(PrefDialog, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle('Preferences')

        # set url and port
        self.lineEdit_url.setText(self.parent._url)
        self.lineEdit_port.setText(self.parent._port)

        # refresher (UI)
        self.refresher = Refresher(self)
        self.refresher.srv_ctrl_btn_signal.connect(self.set_btn_style)
        self.refresher.start()

        # events
        self.btn_box.accepted.connect(self.on_accept_btn_box)
        self.btn_box.rejected.connect(self.on_reject_btn_box)
        self.srv_ctrl_btn.clicked.connect(self.srv_control)
        self.srv_db_reset_btn.clicked.connect(self.init_database)
        self.get_all_srv_status_btn.clicked.connect(self.get_all_srv_status)
        self.clean_all_srv_btn.clicked.connect(self.clean_all_srv)
        self.popup_browser_btn.clicked.connect(self.popup_browser)
        self.pageZoom_slider.valueChanged.connect(
                lambda x:self.pageZoom_lbl.setText("{} %".format(x)))

        # set pagezoom
        self.pageZoom_slider.setValue(self.parent._pageZoom)

    def on_accept_btn_box(self):
        # url
        url, port = self.lineEdit_url.text(), self.lineEdit_port.text()
        base_url = url.rstrip('/') + ':' + port
        #if base_url != self.parent.get_base_url():
        self.parent._url = url
        self.parent._port = port
        self.parent.update_url(QUrl(base_url))

        # pageZoom
        self.parent._pageZoom = self.pageZoom_slider.value()
        self.parent.update_pageZoom()
        self.close()

    def on_reject_btn_box(self):
        self.close()

    def srv_control(self, e):
        sender = self.sender()
        url, port = self.lineEdit_url.text().rstrip('/'), self.lineEdit_port.text()
        if sender.text() == 'START':
            start_unicorn_service(url, port)
            self.refresher.restart()
        else:
            stop_unicorn_service(url, port)
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
        # initialize database with default one from unicorn-webapp
        init_unicorn_database()

    def clean_all_srv(self, e):
        # clean up all alive services
        urls = self.textEdit_srv_info.toPlainText().split('\n')
        current_port = self.parent._port
        for url in urls:
            u, p = url.rstrip('/').rsplit(':', 1)
            if p != current_port:
                stop_unicorn_service(u, p)

    def get_all_srv_status(self, e):
        # get all alive services
        self.textEdit_srv_info.clear()
        srv_checker = SrvStatusChecker(self)
        srv_checker.srv_info_signal.connect(self.textEdit_srv_info.append)
        srv_checker.start()

    def popup_browser(self, e):
        # pop up browser
        import subprocess
        url = self.parent.get_base_url()
        cmdline = 'x-www-browser {}'.format(url)
        subprocess.Popen(cmdline.split())


class SrvStatusChecker(QThread):
    """Check the status of all possible urls.
    """
    srv_info_signal = pyqtSignal('QString')
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.parent = parent

    def run(self):
        min_port, max_port = PORT_RANGE
        for i in range(min_port, max_port + 1):
            base_url = self.parent.parent.get_base_url(i)
            if get_service_status(base_url) == "Running":
                self.srv_info_signal.emit(base_url)


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
