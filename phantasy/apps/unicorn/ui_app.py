# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setStyleSheet(
            "QWidget {\n"
            "    background: rgb(255, 255, 255);\n"
            "}")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webView = QtWebKitWidgets.QWebView(self.centralwidget)
        self.webView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setMinimumSize(QtCore.QSize(1024, 768))
        self.webView.setBaseSize(QtCore.QSize(1024, 768))
        self.webView.setUrl(QtCore.QUrl("http://127.0.0.1:5000/"))
        self.webView.setZoomFactor(1.25)
        self.webView.setRenderHints(QtGui.QPainter.Antialiasing |
                                    QtGui.QPainter.HighQualityAntialiasing |
                                    QtGui.QPainter.SmoothPixmapTransform |
                                    QtGui.QPainter.TextAntialiasing)
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 34))
        self.menubar.setObjectName("menubar")
        self.menuPreferences = QtWidgets.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        mainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtWidgets.QAction(mainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionExit = QtWidgets.QAction(mainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout_Qt = QtWidgets.QAction(mainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menuPreferences.addAction(self.actionPreferences)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionAbout_Qt)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(mainWindow)
        self.actionAbout_Qt.triggered.connect(mainWindow.onAboutQt)
        self.actionExit.triggered.connect(mainWindow.close)
        self.actionAbout.triggered.connect(mainWindow.onAbout)
        self.actionPreferences.triggered.connect(mainWindow.onPreferences)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(
            _translate("mainWindow", "UNICORN Application"))
        self.menuPreferences.setTitle(_translate("mainWindow", "Edit"))
        self.menuAbout.setTitle(_translate("mainWindow", "Help"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.actionAbout.setText(_translate("mainWindow", "About"))
        self.actionAbout.setShortcut(_translate("mainWindow", "Ctrl+A"))
        self.actionPreferences.setText(_translate("mainWindow", "Preferences"))
        self.actionPreferences.setShortcut(
            _translate("mainWindow", "Ctrl+Shift+P"))
        self.actionExit.setText(_translate("mainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("mainWindow", "Ctrl+W"))
        self.actionAbout_Qt.setText(_translate("mainWindow", "About Qt"))


from PyQt5 import QtWebKitWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
