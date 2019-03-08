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
        MainWindow.resize(1645, 1031)
        MainWindow.setStyleSheet("QProgressBar {\n"
                                 "    border: 1px solid gray;\n"
                                 "    border-radius: 10px;\n"
                                 "}\n"
                                 "\n"
                                 "QProgressBar::chunk {\n"
                                 "    background-color: #05B8CC;\n"
                                 "    width: 20px;\n"
                                 "    margin: 0.5px;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.machine_cbb = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.machine_cbb.sizePolicy().hasHeightForWidth())
        self.machine_cbb.setSizePolicy(sizePolicy)
        self.machine_cbb.setObjectName("machine_cbb")
        self.machine_cbb.addItem("")
        self.machine_cbb.addItem("")
        self.horizontalLayout_2.addWidget(self.machine_cbb)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lebt_chkbox = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lebt_chkbox.sizePolicy().hasHeightForWidth())
        self.lebt_chkbox.setSizePolicy(sizePolicy)
        self.lebt_chkbox.setObjectName("lebt_chkbox")
        self.horizontalLayout_2.addWidget(self.lebt_chkbox)
        self.mebt_chkbox = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt_chkbox.setSizePolicy(sizePolicy)
        self.mebt_chkbox.setObjectName("mebt_chkbox")
        self.horizontalLayout_2.addWidget(self.mebt_chkbox)
        self.mebt2fs1a_chkbox = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt2fs1a_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt2fs1a_chkbox.setSizePolicy(sizePolicy)
        self.mebt2fs1a_chkbox.setObjectName("mebt2fs1a_chkbox")
        self.horizontalLayout_2.addWidget(self.mebt2fs1a_chkbox)
        self.mebt2fs1b_chkbox = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt2fs1b_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt2fs1b_chkbox.setSizePolicy(sizePolicy)
        self.mebt2fs1b_chkbox.setObjectName("mebt2fs1b_chkbox")
        self.horizontalLayout_2.addWidget(self.mebt2fs1b_chkbox)
        self.line = QtWidgets.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.device_type_cbb = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.device_type_cbb.sizePolicy().hasHeightForWidth())
        self.device_type_cbb.setSizePolicy(sizePolicy)
        self.device_type_cbb.setObjectName("device_type_cbb")
        self.device_type_cbb.addItem("")
        self.device_type_cbb.addItem("")
        self.horizontalLayout_2.addWidget(self.device_type_cbb)
        self.load_btn = QtWidgets.QPushButton(self.groupBox_2)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/load.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.load_btn.setIcon(icon)
        self.load_btn.setIconSize(QtCore.QSize(16, 16))
        self.load_btn.setObjectName("load_btn")
        self.horizontalLayout_2.addWidget(self.load_btn)
        self.load_status_lbl = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.load_status_lbl.sizePolicy().hasHeightForWidth())
        self.load_status_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(True)
        self.load_status_lbl.setFont(font)
        self.load_status_lbl.setObjectName("load_status_lbl")
        self.horizontalLayout_2.addWidget(self.load_status_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.load_pb = QtWidgets.QProgressBar(self.groupBox_2)
        self.load_pb.setMaximum(0)
        self.load_pb.setProperty("value", -1)
        self.load_pb.setObjectName("load_pb")
        self.horizontalLayout_2.addWidget(self.load_pb)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.matplotlibbarWidget = MatplotlibBarWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.matplotlibbarWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibbarWidget.setSizePolicy(sizePolicy)
        self.matplotlibbarWidget.setObjectName("matplotlibbarWidget")
        self.gridLayout_2.addWidget(self.matplotlibbarWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.freq_dSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.freq_dSpinbox.sizePolicy().hasHeightForWidth())
        self.freq_dSpinbox.setSizePolicy(sizePolicy)
        self.freq_dSpinbox.setDecimals(1)
        self.freq_dSpinbox.setMinimum(0.0)
        self.freq_dSpinbox.setMaximum(10.0)
        self.freq_dSpinbox.setSingleStep(0.5)
        self.freq_dSpinbox.setProperty("value", 1.0)
        self.freq_dSpinbox.setObjectName("freq_dSpinbox")
        self.horizontalLayout.addWidget(self.freq_dSpinbox)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.start_btn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/start.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.start_btn.setIcon(icon1)
        self.start_btn.setIconSize(QtCore.QSize(24, 24))
        self.start_btn.setObjectName("start_btn")
        self.horizontalLayout.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon2)
        self.stop_btn.setIconSize(QtCore.QSize(24, 24))
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout.addWidget(self.stop_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.field_cbb = QtWidgets.QComboBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.field_cbb.sizePolicy().hasHeightForWidth())
        self.field_cbb.setSizePolicy(sizePolicy)
        self.field_cbb.setObjectName("field_cbb")
        self.horizontalLayout_5.addWidget(self.field_cbb)
        self.line_3 = QtWidgets.QFrame(self.groupBox_3)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_5.addWidget(self.line_3)
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        self.id_as_x_rbtn = QtWidgets.QRadioButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.id_as_x_rbtn.sizePolicy().hasHeightForWidth())
        self.id_as_x_rbtn.setSizePolicy(sizePolicy)
        self.id_as_x_rbtn.setObjectName("id_as_x_rbtn")
        self.xaxis_data_group = QtWidgets.QButtonGroup(MainWindow)
        self.xaxis_data_group.setObjectName("xaxis_data_group")
        self.xaxis_data_group.addButton(self.id_as_x_rbtn)
        self.horizontalLayout_5.addWidget(self.id_as_x_rbtn)
        self.pos_as_x_rbtn = QtWidgets.QRadioButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_as_x_rbtn.sizePolicy().hasHeightForWidth())
        self.pos_as_x_rbtn.setSizePolicy(sizePolicy)
        self.pos_as_x_rbtn.setObjectName("pos_as_x_rbtn")
        self.xaxis_data_group.addButton(self.pos_as_x_rbtn)
        self.horizontalLayout_5.addWidget(self.pos_as_x_rbtn)
        self.line_4 = QtWidgets.QFrame(self.groupBox_3)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_5.addWidget(self.line_4)
        self.annote_height_chkbox = QtWidgets.QCheckBox(self.groupBox_3)
        self.annote_height_chkbox.setObjectName("annote_height_chkbox")
        self.horizontalLayout_5.addWidget(self.annote_height_chkbox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.reset_figure_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.reset_figure_btn.setIcon(icon)
        self.reset_figure_btn.setIconSize(QtCore.QSize(16, 16))
        self.reset_figure_btn.setObjectName("reset_figure_btn")
        self.gridLayout.addWidget(self.reset_figure_btn, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1645, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon3)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon5)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionLoad_All_BCM = QtWidgets.QAction(MainWindow)
        self.actionLoad_All_BCM.setObjectName("actionLoad_All_BCM")
        self.actionLoad_All_BPMs = QtWidgets.QAction(MainWindow)
        self.actionLoad_All_BPMs.setObjectName("actionLoad_All_BPMs")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.machine_cbb.currentTextChanged['QString'].connect(
            MainWindow.on_machine_changed)
        self.device_type_cbb.currentTextChanged['QString'].connect(
            MainWindow.on_device_type_changed)
        self.id_as_x_rbtn.toggled['bool'].connect(
            MainWindow.on_apply_id_as_xdata)
        self.pos_as_x_rbtn.toggled['bool'].connect(
            MainWindow.on_apply_pos_as_xdata)
        self.start_btn.clicked.connect(MainWindow.on_daq_start)
        self.stop_btn.clicked.connect(MainWindow.on_daq_stop)
        self.load_btn.clicked.connect(MainWindow.on_load_devices)
        self.reset_figure_btn.clicked.connect(MainWindow.on_init_dataviz)
        self.annote_height_chkbox.toggled['bool'].connect(
            MainWindow.on_annote_height)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Loading Devices"))
        self.label.setText(_translate("MainWindow", "Machine"))
        self.machine_cbb.setItemText(0, _translate("MainWindow", "FRIB"))
        self.machine_cbb.setItemText(1, _translate("MainWindow", "VA_LS1FS1"))
        self.label_4.setText(_translate("MainWindow", "Segments"))
        self.lebt_chkbox.setText(_translate("MainWindow", "LEBT"))
        self.mebt_chkbox.setText(_translate("MainWindow", "MEBT"))
        self.mebt2fs1a_chkbox.setText(_translate("MainWindow", "MEBT2FS1A"))
        self.mebt2fs1b_chkbox.setText(_translate("MainWindow", "MEBT2FS1B"))
        self.label_7.setText(_translate("MainWindow", "Device Type"))
        self.device_type_cbb.setItemText(0, _translate("MainWindow", "BCM"))
        self.device_type_cbb.setItemText(1, _translate("MainWindow", "BPM"))
        self.load_btn.setText(_translate("MainWindow", "Load"))
        self.load_status_lbl.setText(
            _translate("MainWindow", "Press Load Button To Load Devices"))
        self.groupBox.setTitle(_translate("MainWindow", "Data Visualization"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Control Panel"))
        self.label_2.setText(_translate("MainWindow", "Frequency"))
        self.label_3.setText(_translate("MainWindow", "Hz"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_8.setText(_translate("MainWindow", "Field"))
        self.label_11.setText(_translate("MainWindow", "X-Axis"))
        self.id_as_x_rbtn.setText(_translate("MainWindow", "ID"))
        self.pos_as_x_rbtn.setText(_translate("MainWindow", "Position"))
        self.annote_height_chkbox.setText(
            _translate("MainWindow", "Height Annotation"))
        self.label_5.setText(_translate("MainWindow", "DataViz"))
        self.label_6.setText(_translate("MainWindow", "DAQ"))
        self.reset_figure_btn.setText(_translate("MainWindow", "Reset"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionLoad_All_BCM.setText(
            _translate("MainWindow", "Load All BCMs"))
        self.actionLoad_All_BPMs.setText(
            _translate("MainWindow", "Load All BPMs"))


from mpl4qt.widgets.mplbarwidget import MatplotlibBarWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
