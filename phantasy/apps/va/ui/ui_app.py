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
        MainWindow.resize(750, 444)
        MainWindow.setStyleSheet(
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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.config_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.config_groupBox.setObjectName("config_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.config_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.config_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mach_comboBox = QtWidgets.QComboBox(self.config_groupBox)
        self.mach_comboBox.setObjectName("mach_comboBox")
        self.gridLayout.addWidget(self.mach_comboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.config_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.engine_comboBox = QtWidgets.QComboBox(self.config_groupBox)
        self.engine_comboBox.setObjectName("engine_comboBox")
        self.engine_comboBox.addItem("")
        self.engine_comboBox.addItem("")
        self.gridLayout.addWidget(self.engine_comboBox, 0, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.config_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.segm_comboBox = QtWidgets.QComboBox(self.config_groupBox)
        self.segm_comboBox.setObjectName("segm_comboBox")
        self.gridLayout.addWidget(self.segm_comboBox, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.config_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.prefix_comboBox = QtWidgets.QComboBox(self.config_groupBox)
        self.prefix_comboBox.setEditable(True)
        self.prefix_comboBox.setObjectName("prefix_comboBox")
        self.prefix_comboBox.addItem("")
        self.prefix_comboBox.addItem("")
        self.gridLayout.addWidget(self.prefix_comboBox, 1, 3, 1, 1)
        self.localonly_chkbox = QtWidgets.QCheckBox(self.config_groupBox)
        self.localonly_chkbox.setObjectName("localonly_chkbox")
        self.gridLayout.addWidget(self.localonly_chkbox, 2, 2, 1, 2)
        self.gridLayout_2.addWidget(self.config_groupBox, 0, 0, 1, 1)
        self.control_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.control_groupBox.sizePolicy().hasHeightForWidth())
        self.control_groupBox.setSizePolicy(sizePolicy)
        self.control_groupBox.setObjectName("control_groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.control_groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.control_groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.noise_slider = QtWidgets.QSlider(self.control_groupBox)
        self.noise_slider.setEnabled(False)
        self.noise_slider.setStyleSheet(
            "QSlider::groove:horizontal {\n"
            "border: 1px solid #bbb;\n"
            "background: white;\n"
            "height: 12px;\n"
            "border-radius: 4px;\n"
            "}\n"
            "\n"
            "QSlider::sub-page:horizontal {\n"
            "background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
            "    stop: 0 #10BAF0, stop: 1 #10BAF0);\n"
            "background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
            "    stop: 0 #10BAF0, stop: 1 #10BAF0);\n"
            "border: 1px solid #777;\n"
            "height: 10px;\n"
            "border-radius: 4px;\n"
            "}\n"
            "\n"
            "QSlider::add-page:horizontal {\n"
            "background: #fff;\n"
            "border: 1px solid #777;\n"
            "height: 10px;\n"
            "border-radius: 4px;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal {\n"
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
            "    stop:0 #eee, stop:1 #ccc);\n"
            "border: 1px solid #777;\n"
            "width: 15px;\n"
            "margin-top: -2px;\n"
            "margin-bottom: -2px;\n"
            "border-radius: 4px;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:hover {\n"
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
            "    stop:0 #fff, stop:1 #ddd);\n"
            "border: 1px solid #444;\n"
            "border-radius: 4px;\n"
            "}\n"
            "\n"
            "QSlider::sub-page:horizontal:disabled {\n"
            "background: #bbb;\n"
            "border-color: #999;\n"
            "}\n"
            "\n"
            "QSlider::add-page:horizontal:disabled {\n"
            "background: #eee;\n"
            "border-color: #999;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:disabled {\n"
            "background: #eee;\n"
            "border: 1px solid #aaa;\n"
            "border-radius: 4px;\n"
            "}")
        self.noise_slider.setMinimum(0)
        self.noise_slider.setMaximum(50)
        self.noise_slider.setProperty("value", 0)
        self.noise_slider.setOrientation(QtCore.Qt.Horizontal)
        self.noise_slider.setObjectName("noise_slider")
        self.horizontalLayout_3.addWidget(self.noise_slider)
        self.noise_label = QtWidgets.QLabel(self.control_groupBox)
        self.noise_label.setEnabled(False)
        self.noise_label.setObjectName("noise_label")
        self.horizontalLayout_3.addWidget(self.noise_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.va_status_label = QtWidgets.QLabel(self.control_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.va_status_label.sizePolicy().hasHeightForWidth())
        self.va_status_label.setSizePolicy(sizePolicy)
        self.va_status_label.setText("")
        self.va_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.va_status_label.setObjectName("va_status_label")
        self.horizontalLayout_2.addWidget(self.va_status_label)
        self.label_3 = QtWidgets.QLabel(self.control_groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.uptime_label = QtWidgets.QLabel(self.control_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.uptime_label.sizePolicy().hasHeightForWidth())
        self.uptime_label.setSizePolicy(sizePolicy)
        self.uptime_label.setStyleSheet("QLabel {\n"
                                        "    font-family: monospace;\n"
                                        "}")
        self.uptime_label.setAlignment(QtCore.Qt.AlignRight
                                       | QtCore.Qt.AlignTrailing
                                       | QtCore.Qt.AlignVCenter)
        self.uptime_label.setObjectName("uptime_label")
        self.horizontalLayout_2.addWidget(self.uptime_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addWidget(self.control_groupBox, 1, 0, 1, 1)
        self.tools_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tools_groupBox.sizePolicy().hasHeightForWidth())
        self.tools_groupBox.setSizePolicy(sizePolicy)
        self.tools_groupBox.setObjectName("tools_groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tools_groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_notebook_btn = QtWidgets.QToolButton(self.tools_groupBox)
        self.open_notebook_btn.setAutoRaise(True)
        self.open_notebook_btn.setObjectName("open_notebook_btn")
        self.horizontalLayout.addWidget(self.open_notebook_btn)
        self.va_info_btn = QtWidgets.QToolButton(self.tools_groupBox)
        self.va_info_btn.setAutoRaise(True)
        self.va_info_btn.setObjectName("va_info_btn")
        self.horizontalLayout.addWidget(self.va_info_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.tools_groupBox, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 30))
        self.menubar.setObjectName("menubar")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_File.addAction(self.actionE_xit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.mach_comboBox.currentTextChanged['QString'].connect(
            MainWindow.on_machine_changed)
        self.engine_comboBox.currentTextChanged['QString'].connect(
            MainWindow.on_engine_changed)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.va_info_btn.clicked.connect(MainWindow.on_view_va_info)
        self.open_notebook_btn.clicked.connect(MainWindow.on_launch_notebook)
        self.segm_comboBox.currentTextChanged['QString'].connect(
            MainWindow.on_segment_changed)
        self.prefix_comboBox.editTextChanged['QString'].connect(
            MainWindow.on_pvprefix_changed)
        self.localonly_chkbox.toggled['bool'].connect(MainWindow.on_localonly)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.mach_comboBox, self.segm_comboBox)
        MainWindow.setTabOrder(self.segm_comboBox, self.engine_comboBox)
        MainWindow.setTabOrder(self.engine_comboBox, self.prefix_comboBox)
        MainWindow.setTabOrder(self.prefix_comboBox, self.localonly_chkbox)
        MainWindow.setTabOrder(self.localonly_chkbox, self.noise_slider)
        MainWindow.setTabOrder(self.noise_slider, self.open_notebook_btn)
        MainWindow.setTabOrder(self.open_notebook_btn, self.va_info_btn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.config_groupBox.setTitle(
            _translate("MainWindow", "Configuration"))
        self.label.setText(_translate("MainWindow", "Machine"))
        self.label_2.setText(_translate("MainWindow", "Model Engine"))
        self.engine_comboBox.setItemText(0, _translate("MainWindow", "FLAME"))
        self.engine_comboBox.setItemText(1, _translate("MainWindow", "IMPACT"))
        self.label_6.setText(_translate("MainWindow", "Segment"))
        self.label_5.setText(_translate("MainWindow", "PV Prefix"))
        self.prefix_comboBox.setItemText(0, _translate("MainWindow", "None"))
        self.prefix_comboBox.setItemText(1, _translate("MainWindow", "VA"))
        self.localonly_chkbox.setText(
            _translate("MainWindow", "Limit CA Local Only"))
        self.control_groupBox.setTitle(_translate("MainWindow", "Control"))
        self.label_4.setText(_translate("MainWindow", "Noise Level"))
        self.noise_label.setText(_translate("MainWindow", "%"))
        self.label_3.setText(_translate("MainWindow", "Uptime"))
        self.uptime_label.setText(_translate("MainWindow", "00:00:00"))
        self.tools_groupBox.setTitle(_translate("MainWindow", "Tools"))
        self.open_notebook_btn.setText(_translate("MainWindow", "RUN-NB"))
        self.va_info_btn.setText(_translate("MainWindow", "VA Info"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
