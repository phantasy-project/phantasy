# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

from .ui_app import Ui_mainWindow
from .app_pref import PrefDialog

DT_FMT = 'yyyy-MM-dd HH:mm:ss t'

class UnicornApp(QMainWindow, Ui_mainWindow):

    # signal for label: 'clock_sb'
    clockTicking = pyqtSignal('QString')

    def __init__(self, version):
        super(UnicornApp, self).__init__()
        
        self._version = version

        # UI
        self.setupUi(self)
        self.setWindowTitle("UNICORN Application")

        # remove widgets border in statusbar
        self.setStyleSheet("QStatusBar::item { border: 0px solid black };")

        # create statusBar
        self.statusBar = self.create_statusbar()
        self.setStatusBar(self.statusBar)
        self.clock_sb.setText(self.get_current_time())

        # vars
        self._url, self._port = self.webView.url().toString().rstrip('/').rsplit(':', 1)
        self._pageZoom = self.webView.zoomFactor() * 100

        # clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_clockticking)
        self.timer.start(1000)

        # events
        self.clockTicking['QString'].connect(self.clock_sb.setText)

    def get_base_url(self):
        return '{}:{}'.format(self._url, self._port)

    def closeEvent(self, e):
        r = QMessageBox.warning(self, "Warning",
                "Exit this application?",
                QMessageBox.Cancel | QMessageBox.Yes,
                QMessageBox.Cancel)
        if r == QMessageBox.Yes:
            self.timer.stop()
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
        self.webView.setZoomFactor(self._pageZoom/100.0)

    def on_clockticking(self):
        self.clockTicking.emit(self.get_current_time())

    def get_current_time(self):
        return QDateTime().currentDateTime().toString(DT_FMT)

    def create_statusbar(self):
        sb = QStatusBar(self)
        #sb.showMessage("Ready")
        app_title = QLabel("UNICORN App (Version: {})".format(self._version))
        app_title.setAlignment(Qt.AlignLeft)

        self.clock_sb = clock_sb = QLabel(sb)
        clock_sb.setAlignment(Qt.AlignRight)
        
        sb.addWidget(app_title)
        sb.addWidget(self.clock_sb, 1)
        return sb
        

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = UnicornApp(version='1.0')
    w.show()

    sys.exit(app.exec_())
