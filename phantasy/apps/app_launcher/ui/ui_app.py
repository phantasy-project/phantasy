# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
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
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setStyleSheet("")
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_lbl = QtWidgets.QLabel(self.centralwidget)
        self.title_lbl.setStyleSheet("QLabel {\n"
                                     "    border: 0.5px solid gray;\n"
                                     "    border-radius: 3px;\n"
                                     "    padding: 5px 10px 5px 10px;\n"
                                     "    background-color: white;\n"
                                     "    color: blue;\n"
                                     "}")
        self.title_lbl.setText("")
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setObjectName("title_lbl")
        self.horizontalLayout.addWidget(self.title_lbl)
        self.enable_debug_btn = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/log.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.enable_debug_btn.setIcon(icon1)
        self.enable_debug_btn.setIconSize(QtCore.QSize(24, 24))
        self.enable_debug_btn.setCheckable(True)
        self.enable_debug_btn.setAutoRaise(True)
        self.enable_debug_btn.setObjectName("enable_debug_btn")
        self.horizontalLayout.addWidget(self.enable_debug_btn)
        self.show_log_btn = QtWidgets.QToolButton(self.centralwidget)
        self.show_log_btn.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/show.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.show_log_btn.setIcon(icon2)
        self.show_log_btn.setIconSize(QtCore.QSize(24, 24))
        self.show_log_btn.setAutoRaise(True)
        self.show_log_btn.setObjectName("show_log_btn")
        self.horizontalLayout.addWidget(self.show_log_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 34))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tableView.doubleClicked['QModelIndex'].connect(
            MainWindow.on_launch_app)
        self.enable_debug_btn.toggled['bool'].connect(
            MainWindow.on_enable_debug)
        self.show_log_btn.clicked.connect(MainWindow.on_show_log)
        self.enable_debug_btn.toggled['bool'].connect(
            self.show_log_btn.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.enable_debug_btn.setToolTip(
            _translate("MainWindow", "Enable log messages capture"))
        self.enable_debug_btn.setText(_translate("MainWindow", "Debug"))
        self.show_log_btn.setToolTip(
            _translate("MainWindow", "Show log messages"))
        self.show_log_btn.setText(_translate("MainWindow", "Show Log"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
