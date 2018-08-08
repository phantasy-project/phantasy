# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
import time

from .ui_app import Ui_mainWindow
from .app_pref import PrefDialog
from .utils import get_service_status


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

        # remove widgets border in statusbar
        self.setStyleSheet("QStatusBar::item { border: 0px solid black };")

        # vars
        self._url, self._port = self.webView.url().toString().rstrip(
            '/').rsplit(':', 1)
        self._pageZoom = self.webView.zoomFactor() * 100

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

    @pyqtSlot(bool)
    def slot_test(self, e):
        print(self.sender().text())

    def get_base_url(self):
        return '{}:{}'.format(self._url, self._port)

    def closeEvent(self, e):
        r = QMessageBox.warning(self, "Warning", "Exit this application?",
                                QMessageBox.Cancel | QMessageBox.Yes,
                                QMessageBox.Cancel)
        if r == QMessageBox.Yes:
            self.timer.stop()
            self.ui_refresher.terminate()
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
        QMessageBox.about(self, 'UNICORN Application',
                          'This is the UI for UNICORN.')

    def onPreferences(self):
        d = PrefDialog(self)
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
