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
        MainWindow.resize(1779, 1123)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.scan_groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.scan_groupBox.sizePolicy().hasHeightForWidth())
        self.scan_groupBox.setSizePolicy(sizePolicy)
        self.scan_groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
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
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "}")
        self.scan_groupBox.setObjectName("scan_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.scan_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.scan_verticalLayout = QtWidgets.QVBoxLayout()
        self.scan_verticalLayout.setObjectName("scan_verticalLayout")
        self.scan_gridLayout = QtWidgets.QGridLayout()
        self.scan_gridLayout.setObjectName("scan_gridLayout")
        self.scan_vars_get_lineEdit = QtWidgets.QLineEdit(self.scan_groupBox)
        self.scan_vars_get_lineEdit.setObjectName("scan_vars_get_lineEdit")
        self.scan_gridLayout.addWidget(self.scan_vars_get_lineEdit, 1, 1, 1, 3)
        self.scan_range_set_btn = QtWidgets.QPushButton(self.scan_groupBox)
        self.scan_range_set_btn.setObjectName("scan_range_set_btn")
        self.scan_gridLayout.addWidget(self.scan_range_set_btn, 3, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.scan_groupBox)
        self.label_8.setObjectName("label_8")
        self.scan_gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.scan_groupBox)
        self.label_9.setObjectName("label_9")
        self.scan_gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.scan_groupBox)
        self.label_10.setObjectName("label_10")
        self.scan_gridLayout.addWidget(self.label_10, 3, 2, 1, 1)
        self.lower_limit_lineEdit = QtWidgets.QLineEdit(self.scan_groupBox)
        self.lower_limit_lineEdit.setPlaceholderText("")
        self.lower_limit_lineEdit.setObjectName("lower_limit_lineEdit")
        self.scan_gridLayout.addWidget(self.lower_limit_lineEdit, 3, 1, 1, 1)
        self.upper_limit_lineEdit = QtWidgets.QLineEdit(self.scan_groupBox)
        self.upper_limit_lineEdit.setPlaceholderText("")
        self.upper_limit_lineEdit.setObjectName("upper_limit_lineEdit")
        self.scan_gridLayout.addWidget(self.upper_limit_lineEdit, 3, 3, 1, 1)
        self.select_scan_elems_btn = QtWidgets.QPushButton(self.scan_groupBox)
        self.select_scan_elems_btn.setObjectName("select_scan_elems_btn")
        self.scan_gridLayout.addWidget(self.select_scan_elems_btn, 2, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.scan_groupBox)
        self.label_11.setObjectName("label_11")
        self.scan_gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.scan_groupBox)
        self.label_13.setObjectName("label_13")
        self.scan_gridLayout.addWidget(self.label_13, 1, 0, 1, 1)
        self.scan_vars_type_cbb = QtWidgets.QComboBox(self.scan_groupBox)
        self.scan_vars_type_cbb.setObjectName("scan_vars_type_cbb")
        self.scan_vars_type_cbb.addItem("")
        self.scan_vars_type_cbb.addItem("")
        self.scan_gridLayout.addWidget(self.scan_vars_type_cbb, 2, 1, 1, 1)
        self.scan_vars_put_lineEdit = QtWidgets.QLineEdit(self.scan_groupBox)
        self.scan_vars_put_lineEdit.setPlaceholderText("")
        self.scan_vars_put_lineEdit.setObjectName("scan_vars_put_lineEdit")
        self.scan_gridLayout.addWidget(self.scan_vars_put_lineEdit, 0, 1, 1, 3)
        self.monitor_vars_type_cbb = QtWidgets.QComboBox(self.scan_groupBox)
        self.monitor_vars_type_cbb.setObjectName("monitor_vars_type_cbb")
        self.monitor_vars_type_cbb.addItem("")
        self.monitor_vars_type_cbb.addItem("")
        self.scan_gridLayout.addWidget(self.monitor_vars_type_cbb, 5, 1, 1, 1)
        self.select_monitor_elems_btn = QtWidgets.QPushButton(
            self.scan_groupBox)
        self.select_monitor_elems_btn.setObjectName("select_monitor_elems_btn")
        self.scan_gridLayout.addWidget(self.select_monitor_elems_btn, 5, 3, 1,
                                       1)
        self.monitor_vars_lineEdit = QtWidgets.QLineEdit(self.scan_groupBox)
        self.monitor_vars_lineEdit.setPlaceholderText("")
        self.monitor_vars_lineEdit.setObjectName("monitor_vars_lineEdit")
        self.scan_gridLayout.addWidget(self.monitor_vars_lineEdit, 4, 1, 1, 3)
        self.copy_pvname_btn = QtWidgets.QPushButton(self.scan_groupBox)
        self.copy_pvname_btn.setObjectName("copy_pvname_btn")
        self.scan_gridLayout.addWidget(self.copy_pvname_btn, 1, 4, 1, 1)
        self.scan_verticalLayout.addLayout(self.scan_gridLayout)
        self.scanlog_verticalLayout = QtWidgets.QVBoxLayout()
        self.scanlog_verticalLayout.setObjectName("scanlog_verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line_2 = QtWidgets.QFrame(self.scan_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.label_12 = QtWidgets.QLabel(self.scan_groupBox)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        self.line_3 = QtWidgets.QFrame(self.scan_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.line_3)
        self.scanlog_verticalLayout.addLayout(self.horizontalLayout_2)
        self.scan_log_textEdit = QtWidgets.QTextEdit(self.scan_groupBox)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.scan_log_textEdit.setFont(font)
        self.scan_log_textEdit.setObjectName("scan_log_textEdit")
        self.scanlog_verticalLayout.addWidget(self.scan_log_textEdit)
        self.scan_verticalLayout.addLayout(self.scanlog_verticalLayout)
        self.gridLayout.addLayout(self.scan_verticalLayout, 0, 0, 1, 1)
        self.daq_groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.daq_groupBox.sizePolicy().hasHeightForWidth())
        self.daq_groupBox.setSizePolicy(sizePolicy)
        self.daq_groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
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
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "}")
        self.daq_groupBox.setObjectName("daq_groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.daq_groupBox)
        self.gridLayout_2.setContentsMargins(-1, 20, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.nshot_spinBox = QtWidgets.QSpinBox(self.daq_groupBox)
        self.nshot_spinBox.setMinimum(1)
        self.nshot_spinBox.setProperty("value", 5)
        self.nshot_spinBox.setObjectName("nshot_spinBox")
        self.gridLayout_2.addWidget(self.nshot_spinBox, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.niter_spinBox = QtWidgets.QSpinBox(self.daq_groupBox)
        self.niter_spinBox.setMinimum(1)
        self.niter_spinBox.setProperty("value", 10)
        self.niter_spinBox.setObjectName("niter_spinBox")
        self.gridLayout_2.addWidget(self.niter_spinBox, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 4, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        self.start_btn.setObjectName("start_btn")
        self.horizontalLayout.addWidget(self.start_btn)
        self.pause_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pause_btn.sizePolicy().hasHeightForWidth())
        self.pause_btn.setSizePolicy(sizePolicy)
        self.pause_btn.setObjectName("pause_btn")
        self.horizontalLayout.addWidget(self.pause_btn)
        self.stop_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout.addWidget(self.stop_btn)
        self.retake_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.retake_btn.sizePolicy().hasHeightForWidth())
        self.retake_btn.setSizePolicy(sizePolicy)
        self.retake_btn.setObjectName("retake_btn")
        self.horizontalLayout.addWidget(self.retake_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 0, 1, 3)
        self.waitsec_dSpinBox = QtWidgets.QDoubleSpinBox(self.daq_groupBox)
        self.waitsec_dSpinBox.setSingleStep(0.5)
        self.waitsec_dSpinBox.setProperty("value", 1.0)
        self.waitsec_dSpinBox.setObjectName("waitsec_dSpinBox")
        self.gridLayout_2.addWidget(self.waitsec_dSpinBox, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.scanrate_dSpinBox = QtWidgets.QDoubleSpinBox(self.daq_groupBox)
        self.scanrate_dSpinBox.setDecimals(1)
        self.scanrate_dSpinBox.setMinimum(0.1)
        self.scanrate_dSpinBox.setMaximum(20.0)
        self.scanrate_dSpinBox.setProperty("value", 1.0)
        self.scanrate_dSpinBox.setObjectName("scanrate_dSpinBox")
        self.gridLayout_2.addWidget(self.scanrate_dSpinBox, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.daq_groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.plot_groupBox = QtWidgets.QGroupBox(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_groupBox.sizePolicy().hasHeightForWidth())
        self.plot_groupBox.setSizePolicy(sizePolicy)
        self.plot_groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
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
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "}")
        self.plot_groupBox.setObjectName("plot_groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.plot_groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scan_plot_widget = MatplotlibErrorbarWidget(self.plot_groupBox)
        self.scan_plot_widget.setFigureAutoScale(True)
        self.scan_plot_widget.setObjectName("scan_plot_widget")
        self.verticalLayout_3.addWidget(self.scan_plot_widget)
        self.save_data_btn = QtWidgets.QPushButton(self.plot_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.save_data_btn.sizePolicy().hasHeightForWidth())
        self.save_data_btn.setSizePolicy(sizePolicy)
        self.save_data_btn.setObjectName("save_data_btn")
        self.verticalLayout_3.addWidget(self.save_data_btn)
        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1779, 32))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionQuad_Scan = QtWidgets.QAction(MainWindow)
        self.actionQuad_Scan.setObjectName("actionQuad_Scan")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuTools.addAction(self.actionQuad_Scan)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionQuad_Scan.triggered.connect(MainWindow.onQuadScanAction)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.scan_groupBox.setTitle(
            _translate("MainWindow", "Scan Configuration"))
        self.scan_vars_get_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Variables to scan, if selected \'PV\' mode, input readback PV name.</p></body></html>"
            ))
        self.scan_vars_get_lineEdit.setText(
            _translate("MainWindow", "VA:LS1_BTS:QH_D1942:I_RD"))
        self.scan_range_set_btn.setText(_translate("MainWindow", "Range"))
        self.label_8.setText(_translate("MainWindow", "Alter Vars (set)"))
        self.label_9.setText(_translate("MainWindow", "Alter Ranges"))
        self.label_10.setText(_translate("MainWindow", "To"))
        self.lower_limit_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Lower limit of scan range</p></body></html>"
            ))
        self.lower_limit_lineEdit.setText(_translate("MainWindow", "-100"))
        self.upper_limit_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Up limit of scan range</p></body></html>"
            ))
        self.upper_limit_lineEdit.setText(_translate("MainWindow", "100"))
        self.select_scan_elems_btn.setText(_translate("MainWindow", "Select"))
        self.label_11.setText(_translate("MainWindow", "Monitor Vars"))
        self.label_13.setText(_translate("MainWindow", "Alter Vars (get)"))
        self.scan_vars_type_cbb.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Type of scan variables: PV or Element</p></body></html>"
            ))
        self.scan_vars_type_cbb.setItemText(0, _translate("MainWindow", "PV"))
        self.scan_vars_type_cbb.setItemText(1,
                                            _translate("MainWindow",
                                                       "Element"))
        self.scan_vars_put_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Variables to scan, if selected \'PV\' mode, input setpoint PV name.</p></body></html>"
            ))
        self.scan_vars_put_lineEdit.setText(
            _translate("MainWindow", "VA:LS1_BTS:QH_D1942:I_CSET"))
        self.monitor_vars_type_cbb.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Type of monitor variables: PV or Element</p></body></html>"
            ))
        self.monitor_vars_type_cbb.setItemText(0, _translate(
            "MainWindow", "PV"))
        self.monitor_vars_type_cbb.setItemText(1,
                                               _translate(
                                                   "MainWindow", "Element"))
        self.select_monitor_elems_btn.setText(
            _translate("MainWindow", "Select"))
        self.monitor_vars_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Variables to monitor</p></body></html>")
        )
        self.monitor_vars_lineEdit.setText(
            _translate("MainWindow", "VA:LS1_BTS:PM_D2056:XRMS_RD"))
        self.copy_pvname_btn.setText(_translate("MainWindow", "Copy"))
        self.label_12.setText(_translate("MainWindow", "Event Log"))
        self.daq_groupBox.setTitle(
            _translate("MainWindow", "DAQ Configuration"))
        self.label_5.setText(_translate("MainWindow", "per iteration"))
        self.label_3.setText(_translate("MainWindow", "Wait Time"))
        self.label_4.setText(_translate("MainWindow", "Second"))
        self.label_7.setText(_translate("MainWindow", "Scan Rate"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.pause_btn.setText(_translate("MainWindow", "Pause"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.retake_btn.setText(_translate("MainWindow", "Retake"))
        self.label_2.setText(_translate("MainWindow", "Shot Number"))
        self.label_6.setText(_translate("MainWindow", "Hz"))
        self.label.setText(_translate("MainWindow", "Iteration Number"))
        self.plot_groupBox.setTitle(
            _translate("MainWindow", "Correlation Plot"))
        self.save_data_btn.setText(_translate("MainWindow", "Save Data"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionQuad_Scan.setText(
            _translate("MainWindow", "Quad Scan Analysis"))


from mpl4qt.widgets.mplerrorbarwidget import MatplotlibErrorbarWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
