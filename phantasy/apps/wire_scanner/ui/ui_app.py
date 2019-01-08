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
        MainWindow.resize(1400, 1056)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.controls_groupBox = QtWidgets.QGroupBox(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.controls_groupBox.sizePolicy().hasHeightForWidth())
        self.controls_groupBox.setSizePolicy(sizePolicy)
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
        self.dtype_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.dtype_lineEdit.setStyleSheet("")
        self.dtype_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dtype_lineEdit.setReadOnly(True)
        self.dtype_lineEdit.setObjectName("dtype_lineEdit")
        self.gridLayout_3.addWidget(self.dtype_lineEdit, 2, 2, 1, 1)
        self.offset2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset2_lineEdit.setStyleSheet("")
        self.offset2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset2_lineEdit.setObjectName("offset2_lineEdit")
        self.gridLayout_3.addWidget(self.offset2_lineEdit, 3, 3, 1, 1)
        self.stop_pos2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.stop_pos2_lineEdit.setStyleSheet("")
        self.stop_pos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stop_pos2_lineEdit.setObjectName("stop_pos2_lineEdit")
        self.gridLayout_3.addWidget(self.stop_pos2_lineEdit, 3, 8, 1, 2)
        self.pm_detail_btn = QtWidgets.QToolButton(self.controls_groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/browse.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pm_detail_btn.setIcon(icon)
        self.pm_detail_btn.setAutoRaise(True)
        self.pm_detail_btn.setObjectName("pm_detail_btn")
        self.gridLayout_3.addWidget(self.pm_detail_btn, 0, 4, 1, 1)
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
        self.gridLayout_3.addWidget(self.start_pos2_lineEdit, 2, 8, 1, 2)
        self.start_pos1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.start_pos1_lineEdit.setStyleSheet("")
        self.start_pos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.start_pos1_lineEdit.setObjectName("start_pos1_lineEdit")
        self.gridLayout_3.addWidget(self.start_pos1_lineEdit, 2, 6, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 7, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 7, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 5, 1, 1)
        self.pm_names_cbb = QtWidgets.QComboBox(self.controls_groupBox)
        self.pm_names_cbb.setStyleSheet("QComboBox {\n"
                                        "    font-family: monospace;\n"
                                        "}")
        self.pm_names_cbb.setObjectName("pm_names_cbb")
        self.gridLayout_3.addWidget(self.pm_names_cbb, 0, 1, 1, 3)
        self.label_8 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 5, 1, 1)
        self.stop_pos1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.stop_pos1_lineEdit.setStyleSheet("")
        self.stop_pos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stop_pos1_lineEdit.setObjectName("stop_pos1_lineEdit")
        self.gridLayout_3.addWidget(self.stop_pos1_lineEdit, 3, 6, 1, 1)
        self.offset3_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset3_lineEdit.setStyleSheet("")
        self.offset3_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset3_lineEdit.setObjectName("offset3_lineEdit")
        self.gridLayout_3.addWidget(self.offset3_lineEdit, 3, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 3, 1, 1)
        self.coord_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.coord_lineEdit.setStyleSheet("")
        self.coord_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coord_lineEdit.setReadOnly(True)
        self.coord_lineEdit.setObjectName("coord_lineEdit")
        self.gridLayout_3.addWidget(self.coord_lineEdit, 2, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 1, 1, 1)
        self.offset1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset1_lineEdit.setStyleSheet("")
        self.offset1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset1_lineEdit.setObjectName("offset1_lineEdit")
        self.gridLayout_3.addWidget(self.offset1_lineEdit, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.controls_groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 10)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 6, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.run_btn = QtWidgets.QPushButton(self.controls_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.run_btn.sizePolicy().hasHeightForWidth())
        self.run_btn.setSizePolicy(sizePolicy)
        self.run_btn.setObjectName("run_btn")
        self.horizontalLayout_2.addWidget(self.run_btn)
        self.advctrl_chkbox = QtWidgets.QCheckBox(self.controls_groupBox)
        self.advctrl_chkbox.setObjectName("advctrl_chkbox")
        self.horizontalLayout_2.addWidget(self.advctrl_chkbox)
        self.run_progressbar = QtWidgets.QProgressBar(self.controls_groupBox)
        self.run_progressbar.setProperty("value", 24)
        self.run_progressbar.setObjectName("run_progressbar")
        self.horizontalLayout_2.addWidget(self.run_progressbar)
        self.emstop_btn = QtWidgets.QToolButton(self.controls_groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.emstop_btn.setIcon(icon1)
        self.emstop_btn.setIconSize(QtCore.QSize(24, 24))
        self.emstop_btn.setAutoRaise(True)
        self.emstop_btn.setObjectName("emstop_btn")
        self.horizontalLayout_2.addWidget(self.emstop_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 4, 0, 1, 10)
        self.advctrl_groupBox = QtWidgets.QGroupBox(self.controls_groupBox)
        self.advctrl_groupBox.setObjectName("advctrl_groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.advctrl_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.advctrl_groupBox)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 2, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_4.addWidget(self.lineEdit_2, 2, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_4.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_4.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_4.addWidget(self.pushButton_8, 0, 2, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.advctrl_groupBox)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_4.addWidget(self.pushButton_7, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_4.addWidget(self.pushButton_5, 0, 3, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_4.addWidget(self.pushButton_6, 0, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.advctrl_groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.advctrl_groupBox)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 2, 3, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_4.addWidget(self.lineEdit_5, 2, 4, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_4.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.advctrl_groupBox)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_4.addWidget(self.pushButton_4, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.advctrl_groupBox, 5, 0, 1, 10)
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
        self.advctrl_groupBox.raise_()
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 30))
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
        self.actionSimulation_Mode = QtWidgets.QAction(MainWindow)
        self.actionSimulation_Mode.setCheckable(True)
        self.actionSimulation_Mode.setObjectName("actionSimulation_Mode")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Config.addAction(self.actionReload_Configuration)
        self.menu_Config.addAction(self.actionSave_Configuration)
        self.menu_Config.addAction(self.actionLoad_Configuration)
        self.menu_Config.addAction(self.actionSaveAs_Configuration)
        self.menu_Config.addAction(self.actionSimulation_Mode)
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
        self.advctrl_chkbox.toggled['bool'].connect(
            MainWindow.on_show_advanced_ctrlpanel)
        self.run_btn.clicked.connect(MainWindow.on_run_device)
        self.actionSimulation_Mode.toggled['bool'].connect(
            MainWindow.on_enable_simulation_mode)
        self.emstop_btn.clicked.connect(MainWindow.on_emstop_device)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.controls_groupBox.setTitle(_translate("MainWindow", "Device"))
        self.pm_detail_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show device details</p></body></html>"))
        self.pm_detail_btn.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Select Device"))
        self.label_6.setText(_translate("MainWindow", "Start Pos (Fork2)"))
        self.label_7.setText(_translate("MainWindow", "Stop Pos (Fork2)"))
        self.label_3.setText(_translate("MainWindow", "Type"))
        self.label_5.setText(_translate("MainWindow", "Start Pos (Fork1)"))
        self.label_8.setText(_translate("MainWindow", "Stop Pos (Fork2)"))
        self.label_4.setText(_translate("MainWindow", "Coordinate"))
        self.label_9.setText(_translate("MainWindow", "Wire Offsets"))
        self.label_2.setText(_translate("MainWindow", "Configuration"))
        self.run_btn.setText(_translate("MainWindow", "Run"))
        self.advctrl_chkbox.setText(_translate("MainWindow", "Advanced"))
        self.emstop_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Emergency Stop</p></body></html>"))
        self.emstop_btn.setText(_translate("MainWindow", "..."))
        self.advctrl_groupBox.setTitle(
            _translate("MainWindow", "Advanced Control"))
        self.label_11.setText(_translate("MainWindow", "From"))
        self.pushButton_2.setText(
            _translate("MainWindow", "Initialize Potentimeter"))
        self.pushButton_3.setText(_translate("MainWindow", "Enable Scan"))
        self.pushButton_8.setText(_translate("MainWindow", "Reset Interlock"))
        self.pushButton_7.setText(_translate("MainWindow", "Initialize Motor"))
        self.pushButton_5.setText(_translate("MainWindow", "Set Bias Voltage"))
        self.pushButton_6.setText(_translate("MainWindow", "Move"))
        self.label_10.setText(_translate("MainWindow", "Out Limit"))
        self.label_12.setText(_translate("MainWindow", "To"))
        self.pushButton_4.setText(_translate("MainWindow", "Set Scan Range"))
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
        self.actionSimulation_Mode.setText(
            _translate("MainWindow", "Simulation Mode"))


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
