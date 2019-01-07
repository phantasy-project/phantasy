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
        MainWindow.resize(1425, 1051)
        MainWindow.setStyleSheet("QLineEdit {\n"
                                 "    border: 0.5px solid gray;\n"
                                 "    padding: 0 5px;\n"
                                 "    border-radius: 5px;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.controls_groupBox = QtWidgets.QGroupBox(self.splitter_2)
        self.controls_groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
            "   */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1.5ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 0.5ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}")
        self.controls_groupBox.setObjectName("controls_groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.controls_groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 10, 1, 1)
        self.dtype_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.dtype_lineEdit.setStyleSheet("")
        self.dtype_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dtype_lineEdit.setReadOnly(True)
        self.dtype_lineEdit.setObjectName("dtype_lineEdit")
        self.gridLayout_3.addWidget(self.dtype_lineEdit, 2, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 8, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 8, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 3, 1, 2)
        self.offset1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset1_lineEdit.setStyleSheet("")
        self.offset1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset1_lineEdit.setObjectName("offset1_lineEdit")
        self.gridLayout_3.addWidget(self.offset1_lineEdit, 3, 5, 1, 1)
        self.coord_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.coord_lineEdit.setStyleSheet("")
        self.coord_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coord_lineEdit.setReadOnly(True)
        self.coord_lineEdit.setObjectName("coord_lineEdit")
        self.gridLayout_3.addWidget(self.coord_lineEdit, 2, 7, 1, 1)
        self.pm_names_cbb = QtWidgets.QComboBox(self.controls_groupBox)
        self.pm_names_cbb.setStyleSheet("QComboBox {\n"
                                        "    font-family: monospace;\n"
                                        "}")
        self.pm_names_cbb.setObjectName("pm_names_cbb")
        self.gridLayout_3.addWidget(self.pm_names_cbb, 0, 3, 1, 4)
        self.label_4 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 6, 1, 1)
        self.line = QtWidgets.QFrame(self.controls_groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 12)
        self.start_pos1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.start_pos1_lineEdit.setStyleSheet("")
        self.start_pos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.start_pos1_lineEdit.setObjectName("start_pos1_lineEdit")
        self.gridLayout_3.addWidget(self.start_pos1_lineEdit, 2, 9, 1, 1)
        self.label = QtWidgets.QLabel(self.controls_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.start_pos2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.start_pos2_lineEdit.setStyleSheet("")
        self.start_pos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.start_pos2_lineEdit.setObjectName("start_pos2_lineEdit")
        self.gridLayout_3.addWidget(self.start_pos2_lineEdit, 2, 11, 1, 1)
        self.stop_pos2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.stop_pos2_lineEdit.setStyleSheet("")
        self.stop_pos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stop_pos2_lineEdit.setObjectName("stop_pos2_lineEdit")
        self.gridLayout_3.addWidget(self.stop_pos2_lineEdit, 3, 11, 1, 1)
        self.offset3_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset3_lineEdit.setStyleSheet("")
        self.offset3_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset3_lineEdit.setObjectName("offset3_lineEdit")
        self.gridLayout_3.addWidget(self.offset3_lineEdit, 3, 7, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 10, 1, 1)
        self.stop_pos1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.stop_pos1_lineEdit.setStyleSheet("")
        self.stop_pos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stop_pos1_lineEdit.setObjectName("stop_pos1_lineEdit")
        self.gridLayout_3.addWidget(self.stop_pos1_lineEdit, 3, 9, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.controls_groupBox)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 4, 11, 1, 1)
        self.offset2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset2_lineEdit.setStyleSheet("")
        self.offset2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset2_lineEdit.setObjectName("offset2_lineEdit")
        self.gridLayout_3.addWidget(self.offset2_lineEdit, 3, 6, 1, 1)
        self.pm_detail_btn = QtWidgets.QToolButton(self.controls_groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/browse.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pm_detail_btn.setIcon(icon)
        self.pm_detail_btn.setAutoRaise(True)
        self.pm_detail_btn.setObjectName("pm_detail_btn")
        self.gridLayout_3.addWidget(self.pm_detail_btn, 0, 7, 1, 1)
        self.label_2.raise_()
        self.label.raise_()
        self.pm_names_cbb.raise_()
        self.label_3.raise_()
        self.dtype_lineEdit.raise_()
        self.coord_lineEdit.raise_()
        self.label_4.raise_()
        self.line.raise_()
        self.label_5.raise_()
        self.start_pos1_lineEdit.raise_()
        self.label_6.raise_()
        self.start_pos2_lineEdit.raise_()
        self.stop_pos2_lineEdit.raise_()
        self.stop_pos1_lineEdit.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.offset1_lineEdit.raise_()
        self.offset2_lineEdit.raise_()
        self.offset3_lineEdit.raise_()
        self.pm_detail_btn.raise_()
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
            "   */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1.5ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 0.5ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.matplotlibcurveWidget = MatplotlibCurveWidget(self.groupBox)
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.gridLayout_2.addWidget(self.matplotlibcurveWidget, 0, 0, 1, 1)
        self.matplotlibcurveWidget.raise_()
        self.controls_groupBox.raise_()
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_2.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
            "   */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1.5ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 0.5ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1425, 30))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Config = QtWidgets.QMenu(self.menubar)
        self.menu_Config.setObjectName("menu_Config")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionLoad_Configuration = QtWidgets.QAction(MainWindow)
        self.actionLoad_Configuration.setObjectName("actionLoad_Configuration")
        self.actionSave_Configuration = QtWidgets.QAction(MainWindow)
        self.actionSave_Configuration.setObjectName("actionSave_Configuration")
        self.actionSaveAs_Configuration = QtWidgets.QAction(MainWindow)
        self.actionSaveAs_Configuration.setObjectName(
            "actionSaveAs_Configuration")
        self.actionReload_Configuration = QtWidgets.QAction(MainWindow)
        self.actionReload_Configuration.setObjectName(
            "actionReload_Configuration")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Config.addAction(self.actionReload_Configuration)
        self.menu_Config.addAction(self.actionSave_Configuration)
        self.menu_Config.addAction(self.actionLoad_Configuration)
        self.menu_Config.addAction(self.actionSaveAs_Configuration)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Config.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionContents.triggered.connect(MainWindow.onHelp)
        self.pm_detail_btn.clicked.connect(MainWindow.on_show_device_details)
        self.actionLoad_Configuration.triggered.connect(
            MainWindow.on_loadfrom_config)
        self.actionSave_Configuration.triggered.connect(
            MainWindow.on_save_config)
        self.actionSaveAs_Configuration.triggered.connect(
            MainWindow.on_saveas_config)
        self.actionReload_Configuration.triggered.connect(
            MainWindow.on_reload_config)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.controls_groupBox.setTitle(_translate("MainWindow", "Controls"))
        self.label_3.setText(_translate("MainWindow", "Type"))
        self.label_6.setText(_translate("MainWindow", "Start Pos (Fork2)"))
        self.label_2.setText(_translate("MainWindow", "Configuration"))
        self.label_8.setText(_translate("MainWindow", "Stop Pos (Fork2)"))
        self.label_5.setText(_translate("MainWindow", "Start Pos (Fork1)"))
        self.label_9.setText(_translate("MainWindow", "Wire Offsets"))
        self.label_4.setText(_translate("MainWindow", "Coordinate"))
        self.label.setText(_translate("MainWindow", "Select Device"))
        self.label_7.setText(_translate("MainWindow", "Stop Pos (Fork2)"))
        self.pushButton.setText(_translate("MainWindow", "START"))
        self.pm_detail_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show device details</p></body></html>"))
        self.pm_detail_btn.setText(_translate("MainWindow", "..."))
        self.groupBox.setTitle(_translate("MainWindow", "Data Plot"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Data Analysis"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Config.setTitle(_translate("MainWindow", "Configuration"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionLoad_Configuration.setText(
            _translate("MainWindow", "Load From"))
        self.actionSave_Configuration.setText(_translate("MainWindow", "Save"))
        self.actionSaveAs_Configuration.setText(
            _translate("MainWindow", "Save As"))
        self.actionReload_Configuration.setText(
            _translate("MainWindow", "Reload"))


from mpl4qt.widgets.mplcurvewidget import MatplotlibCurveWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
