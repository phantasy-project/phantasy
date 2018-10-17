# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QKeySequence
import time
import random

from .ui_app import Ui_mainWindow
from .app_pref import PrefDialog
from .app_help import HelpDialog
from .utils import get_service_status
from .utils import start_unicorn_service
from .utils import stop_unicorn_service
from .resources import unicorn_icon
from .resources import zoom_in_icon
from .resources import zoom_out_icon
from .resources import back_icon
from .resources import forward_icon
from .resources import quit_icon
from .resources import home_icon

from .utils import PORT_RANGE


DT_FMT = 'yyyy-MM-dd HH:mm:ss t'

class UnicornApp(QMainWindow, Ui_mainWindow):

    # signal for label: 'clock_sb'
    clock_ticking_signal = pyqtSignal('QString')

    def __init__(self, version):
        super(UnicornApp, self).__init__()

        self._version = version

        # UI
        self.setupUi(self)
        self.setWindowTitle("UNICORN Application")

        # toolbar
        self.setup_toolbar()

        # icon
        self.setWindowIcon(QIcon(QPixmap(unicorn_icon)))

        # remove widgets border in statusbar
        self.setStyleSheet("QStatusBar::item { border: 0px solid black };")

        # vars
        self._url, self._port = self.webView.url().toString().rstrip(
            '/').rsplit(':', 1)
        self._port = str(random.randint(*PORT_RANGE))
        self._pageZoom = self.webView.zoomFactor() * 100
        # startup service
        self._startup_unicorn()

        # create statusBar
        self.statusBar = self.create_statusbar()
        self.setStatusBar(self.statusBar)
        self.clock_sb.setText(self.get_current_time())

        # clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_clockticking)
        self.timer.start(1000)

        # events
        self.clock_ticking_signal['QString'].connect(self.clock_sb.setText)

        #
        self.ui_refresher = Refresher(self)
        self.ui_refresher.srv_status_signal.connect(self.set_srv_status)
        self.ui_refresher.start()

        # shortcuts
        zoom0 = QShortcut(QKeySequence("Ctrl+0"), self)
        zoom0.activated.connect(self.zoom_reset)

    @pyqtSlot(bool)
    def slot_test(self, e):
        print(self.sender().text())

    def get_base_url(self, port=None):
        port = self._port if port is None else port
        return '{}:{}'.format(self._url, port)

    def closeEvent(self, e):
        r = QMessageBox.warning(self, "Warning", "Exit this application?",
                                QMessageBox.Cancel | QMessageBox.Yes,
                                QMessageBox.Cancel)
        if r == QMessageBox.Yes:
            self.timer.stop()
            self.ui_refresher.terminate()
            self._terminate_unicorn()
            e.accept()
        else:
            e.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backspace:
            self.webView.back()
        elif e.key() == Qt.Key_F5:
            self.webView.reload()

    def onAboutQt(self):
        QMessageBox.aboutQt(self)

    def onAbout(self):
        app_info = '''
        <html>
        <h4>About Unicorn App</h4>
        <p>Unicorn App is a GUI application, built upon PyQt5,
        current running version is {}.
        </p>
        <p>
        UNICORN is a web service to be used as an interpreter for the
        units between engineering and physics fields, on the accelerator
        system.
        </p>
        <p>The detailed information could be reached at Help page of UNICORN.</p>
        <p>This app features easy access and control to UNICORN service.</p>
        <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
        </html>
        '''.format(self._version)
        QMessageBox.about(self, 'About UNICORN App', app_info)

    def onPreferences(self):
        d = PrefDialog(self)
        d.exec_()

    def onHelp(self):
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    def update_url(self, url):
        self.webView.setUrl(url)

    def update_pageZoom(self):
        self.webView.setZoomFactor(self._pageZoom / 100.0)

    def on_clockticking(self):
        self.clock_ticking_signal.emit(self.get_current_time())

    def get_current_time(self):
        return QDateTime().currentDateTime().toString(DT_FMT)

    def create_statusbar(self):
        sb = QStatusBar(self)
        # app title
        app_title = QLabel(
                "UNICORN App (Version: {})".format(self._version), sb)
        app_title.setAlignment(Qt.AlignLeft)

        # service status
        base_url = self.get_base_url()
        self.srv_status = srv_status = QLabel(sb)
        srv_status.setAlignment(Qt.AlignCenter)

        # clock
        self.clock_sb = clock_sb = QLabel(sb)
        clock_sb.setAlignment(Qt.AlignRight)

        #
        sb.addWidget(app_title, 1)
        sb.addWidget(srv_status, 1)
        sb.addWidget(self.clock_sb, 1)
        return sb

    @pyqtSlot('QString')
    def set_srv_status(self, s):
        self.srv_status.setText("[ {} ] {}".format(s,self.get_base_url()))
        if s == 'Running':
            self.srv_status.setStyleSheet(
                    "QLabel {\n"
                    "    background-color: rgb(0, 170, 0);\n"
                    "    color: rgb(255, 255, 255);\n"
                    "    font-weight: bold;\n"
                    "}")
        else:
            self.srv_status.setStyleSheet(
                    "QLabel {\n"
                    "    background-color: rgb(255, 0, 0);\n"
                    "    color: rgb(255, 255, 255);\n"
                    "    font-weight: bold;\n"
                    "}")

    def _terminate_unicorn(self):
        # shutdown unicorn web service
        base_url = self.get_base_url()
        if get_service_status(base_url) == "Running":
            stop_unicorn_service(self._url, self._port)
        else:
            print("Unicorn service is terminated.")

    def _startup_unicorn(self):
        # startup unicorn service at random port
        base_url = self.get_base_url()
        if get_service_status(base_url) == "Not Running":
            start_unicorn_service(self._url, self._port)
            time.sleep(1.0)
        else:
            QMessageBox.information(self, "Start Unicorn Service",
                    "UNICORN service is already running at {}.".format(base_url),
                    QMessageBox.Ok)
        self.webView.setUrl(QUrl(base_url))

    @pyqtSlot()
    def zoom_in(self):
        if self._pageZoom < 200:
            self._pageZoom += 5
            self.webView.setZoomFactor(self._pageZoom / 100)

    @pyqtSlot()
    def zoom_out(self):
        if self._pageZoom > 50:
            self._pageZoom -= 5
            self.webView.setZoomFactor(self._pageZoom / 100)

    @pyqtSlot()
    def zoom_reset(self):
        self._pageZoom = 100
        self.webView.setZoomFactor(self._pageZoom / 100)

    def setup_toolbar(self):
        """Set up toolbar"""
        # exit tool
        exitTool = QAction(QIcon(QPixmap(quit_icon)), 'Exit', self)
        exitTool.triggered.connect(self.close)

        # zoom in tool
        zoomInTool = QAction(QIcon(QPixmap(zoom_in_icon)), 'Zoom In', self)
        zoomInTool.setShortcut(QKeySequence.ZoomIn)
        zoomInTool.triggered.connect(self.zoom_in)

        # zoom out tool
        zoomOutTool = QAction(QIcon(QPixmap(zoom_out_icon)), 'Zoom Out', self)
        zoomOutTool.setShortcut(QKeySequence.ZoomOut)
        zoomOutTool.triggered.connect(self.zoom_out)

        # home tool
        homeTool = QAction(QIcon(QPixmap(home_icon)), 'Home Page', self)
        homeTool.setShortcut('Ctrl+h')
        homeTool.triggered.connect(lambda: self.webView.setUrl(QUrl(self.get_base_url())))

        # back view
        backTool = QAction(QIcon(QPixmap(back_icon)), 'Back', self)
        backTool.setShortcut(QKeySequence.Back)
        backTool.triggered.connect(lambda x: self.webView.back())

        # forward view
        forwardTool = QAction(QIcon(QPixmap(forward_icon)), 'Forward', self)
        forwardTool.setShortcut(QKeySequence.Forward)
        forwardTool.triggered.connect(lambda x: self.webView.forward())

        # set toolbar
        self.toolBar.addAction(homeTool)
        self.toolBar.addSeparator()
        self.toolBar.addAction(zoomInTool)
        self.toolBar.addAction(zoomOutTool)
        self.toolBar.addAction(backTool)
        self.toolBar.addAction(forwardTool)
        self.toolBar.addSeparator()
        self.toolBar.addAction(exitTool)

class Refresher(QThread):
    srv_status_signal = pyqtSignal('QString')    # for service status
    def __init__(self, parent=None):
        super(Refresher, self).__init__(parent)
        self.parent = parent
        self.run_flag = True

    def run(self):
        while self.run_flag:
            if get_service_status(self.parent.get_base_url()) == "Running":
                self.srv_status_signal.emit("Running")
            else:
                self.srv_status_signal.emit("Not Running")
            time.sleep(30)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = UnicornApp(version='1.0')
    w.show()

    sys.exit(app.exec_())
