# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(944, 316)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cv_btn = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/cv.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.cv_btn.setIcon(icon1)
        self.cv_btn.setIconSize(QtCore.QSize(128, 128))
        self.cv_btn.setAutoRaise(True)
        self.cv_btn.setObjectName("cv_btn")
        self.horizontalLayout.addWidget(self.cv_btn)
        self.qs_btn = QtWidgets.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/qs.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.qs_btn.setIcon(icon2)
        self.qs_btn.setIconSize(QtCore.QSize(128, 128))
        self.qs_btn.setAutoRaise(True)
        self.qs_btn.setObjectName("qs_btn")
        self.horizontalLayout.addWidget(self.qs_btn)
        self.ws_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ws_btn.sizePolicy().hasHeightForWidth())
        self.ws_btn.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/ws.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.ws_btn.setIcon(icon3)
        self.ws_btn.setIconSize(QtCore.QSize(128, 128))
        self.ws_btn.setAutoRaise(True)
        self.ws_btn.setObjectName("ws_btn")
        self.horizontalLayout.addWidget(self.ws_btn)
        self.va_btn = QtWidgets.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/va.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.va_btn.setIcon(icon4)
        self.va_btn.setIconSize(QtCore.QSize(128, 128))
        self.va_btn.setAutoRaise(True)
        self.va_btn.setObjectName("va_btn")
        self.horizontalLayout.addWidget(self.va_btn)
        self.tv_btn = QtWidgets.QToolButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/tv.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.tv_btn.setIcon(icon5)
        self.tv_btn.setIconSize(QtCore.QSize(128, 128))
        self.tv_btn.setAutoRaise(True)
        self.tv_btn.setObjectName("tv_btn")
        self.horizontalLayout.addWidget(self.tv_btn)
        self.un_btn = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/un.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.un_btn.setIcon(icon6)
        self.un_btn.setIconSize(QtCore.QSize(128, 128))
        self.un_btn.setAutoRaise(True)
        self.un_btn.setObjectName("un_btn")
        self.horizontalLayout.addWidget(self.un_btn)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.add_btn = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/add.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.add_btn.setIcon(icon7)
        self.add_btn.setIconSize(QtCore.QSize(24, 24))
        self.add_btn.setAutoRaise(True)
        self.add_btn.setObjectName("add_btn")
        self.verticalLayout.addWidget(self.add_btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.add_btn.clicked.connect(MainWindow.on_add_launcher)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cv_btn.setText(_translate("MainWindow", "..."))
        self.qs_btn.setText(_translate("MainWindow", "..."))
        self.ws_btn.setText(_translate("MainWindow", "..."))
        self.va_btn.setText(_translate("MainWindow", "..."))
        self.tv_btn.setText(_translate("MainWindow", "..."))
        self.un_btn.setText(_translate("MainWindow", "..."))
        self.add_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Add a new button as app launcher.</p></body></html>"
            ))
        self.add_btn.setText(_translate("MainWindow", "..."))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
