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
        MainWindow.resize(1200, 900)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/tv_icon.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
            "}\n"
            "\n"
            "QLineEdit {\n"
            "    border: 0.5px solid gray;\n"
            "    padding: 1 5px;\n"
            "    border-radius: 3px;\n"
            "}")
        MainWindow.setIconSize(QtCore.QSize(36, 36))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.operation_mode_cbb = QtWidgets.QComboBox(self.centralwidget)
        self.operation_mode_cbb.setObjectName("operation_mode_cbb")
        self.operation_mode_cbb.addItem("")
        self.operation_mode_cbb.addItem("")
        self.horizontalLayout.addWidget(self.operation_mode_cbb)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.run_btn = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.run_btn.setIcon(icon1)
        self.run_btn.setIconSize(QtCore.QSize(24, 24))
        self.run_btn.setObjectName("run_btn")
        self.horizontalLayout.addWidget(self.run_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.cors_gbox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cors_gbox.sizePolicy().hasHeightForWidth())
        self.cors_gbox.setSizePolicy(sizePolicy)
        self.cors_gbox.setObjectName("cors_gbox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.cors_gbox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.cors_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.wait_time_dspinbox = QtWidgets.QDoubleSpinBox(self.cors_gbox)
        self.wait_time_dspinbox.setDecimals(1)
        self.wait_time_dspinbox.setMaximum(10.0)
        self.wait_time_dspinbox.setSingleStep(0.5)
        self.wait_time_dspinbox.setProperty("value", 1.0)
        self.wait_time_dspinbox.setObjectName("wait_time_dspinbox")
        self.horizontalLayout_3.addWidget(self.wait_time_dspinbox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.refresh_cors_btn = QtWidgets.QToolButton(self.cors_gbox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/refresh.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.refresh_cors_btn.setIcon(icon2)
        self.refresh_cors_btn.setIconSize(QtCore.QSize(24, 24))
        self.refresh_cors_btn.setObjectName("refresh_cors_btn")
        self.horizontalLayout_3.addWidget(self.refresh_cors_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.cors_gbox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.alter_start_lineEdit = QtWidgets.QLineEdit(self.cors_gbox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_start_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_start_lineEdit.setSizePolicy(sizePolicy)
        self.alter_start_lineEdit.setObjectName("alter_start_lineEdit")
        self.horizontalLayout_2.addWidget(self.alter_start_lineEdit)
        self.label_4 = QtWidgets.QLabel(self.cors_gbox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.alter_stop_lineEdit = QtWidgets.QLineEdit(self.cors_gbox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_stop_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_stop_lineEdit.setSizePolicy(sizePolicy)
        self.alter_stop_lineEdit.setObjectName("alter_stop_lineEdit")
        self.horizontalLayout_2.addWidget(self.alter_stop_lineEdit)
        self.label_5 = QtWidgets.QLabel(self.cors_gbox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.alter_steps_lineEdit = QtWidgets.QLineEdit(self.cors_gbox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_steps_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_steps_lineEdit.setSizePolicy(sizePolicy)
        self.alter_steps_lineEdit.setObjectName("alter_steps_lineEdit")
        self.horizontalLayout_2.addWidget(self.alter_steps_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.cors_treeView = QtWidgets.QTreeView(self.cors_gbox)
        self.cors_treeView.setObjectName("cors_treeView")
        self.verticalLayout.addWidget(self.cors_treeView)
        self.monitors_gbox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.monitors_gbox.sizePolicy().hasHeightForWidth())
        self.monitors_gbox.setSizePolicy(sizePolicy)
        self.monitors_gbox.setObjectName("monitors_gbox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.monitors_gbox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.refresh_bpms_btn = QtWidgets.QToolButton(self.monitors_gbox)
        self.refresh_bpms_btn.setIcon(icon2)
        self.refresh_bpms_btn.setIconSize(QtCore.QSize(24, 24))
        self.refresh_bpms_btn.setObjectName("refresh_bpms_btn")
        self.horizontalLayout_4.addWidget(self.refresh_bpms_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.monitors_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.monitor_fields_cbb = QtWidgets.QComboBox(self.monitors_gbox)
        self.monitor_fields_cbb.setObjectName("monitor_fields_cbb")
        self.monitor_fields_cbb.addItem("")
        self.monitor_fields_cbb.addItem("")
        self.monitor_fields_cbb.addItem("")
        self.horizontalLayout_5.addWidget(self.monitor_fields_cbb)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.bpms_treeView = QtWidgets.QTreeView(self.monitors_gbox)
        self.bpms_treeView.setObjectName("bpms_treeView")
        self.verticalLayout_3.addWidget(self.bpms_treeView)
        self.log_gbox = QtWidgets.QGroupBox(self.splitter_2)
        self.log_gbox.setMinimumSize(QtCore.QSize(0, 100))
        self.log_gbox.setObjectName("log_gbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.log_gbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.log_textEdit = QtWidgets.QTextEdit(self.log_gbox)
        self.log_textEdit.setObjectName("log_textEdit")
        self.gridLayout_3.addWidget(self.log_textEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.load_lattice_tool = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/load_lattice.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.load_lattice_tool.setIcon(icon3)
        self.load_lattice_tool.setObjectName("load_lattice_tool")
        self.measure_tool = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/measure.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.measure_tool.setIcon(icon4)
        self.measure_tool.setObjectName("measure_tool")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon5)
        self.actionAbout.setObjectName("actionAbout")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon6)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionContents.setIcon(icon7)
        self.actionContents.setObjectName("actionContents")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon8)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menuFile.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Edit.addAction(self.measure_tool)
        self.menu_Edit.addAction(self.load_lattice_tool)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.run_btn.clicked.connect(MainWindow.on_measure_orm)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Measurement Source"))
        self.operation_mode_cbb.setItemText(0, _translate(
            "MainWindow", "Live"))
        self.operation_mode_cbb.setItemText(1, _translate(
            "MainWindow", "Model"))
        self.run_btn.setText(_translate("MainWindow", "..."))
        self.cors_gbox.setTitle(_translate("MainWindow", "Correctors"))
        self.label_2.setText(_translate("MainWindow", "Additional Wait Time"))
        self.refresh_cors_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Refresh the elements</p></body></html>")
        )
        self.refresh_cors_btn.setText(_translate("MainWindow", "refresh"))
        self.label_3.setText(_translate("MainWindow", "Alter Range"))
        self.alter_start_lineEdit.setText(_translate("MainWindow", "-0.003"))
        self.label_4.setText(_translate("MainWindow", "To"))
        self.alter_stop_lineEdit.setText(_translate("MainWindow", "0.003"))
        self.label_5.setText(_translate("MainWindow", "N"))
        self.alter_steps_lineEdit.setText(_translate("MainWindow", "5"))
        self.monitors_gbox.setTitle(_translate("MainWindow", "Monitors"))
        self.refresh_bpms_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Refresh the elements</p></body></html>")
        )
        self.refresh_bpms_btn.setText(_translate("MainWindow", "refresh"))
        self.label_6.setText(_translate("MainWindow", "Fields to Monitor"))
        self.monitor_fields_cbb.setItemText(0, _translate("MainWindow", "X&Y"))
        self.monitor_fields_cbb.setItemText(1, _translate("MainWindow", "X"))
        self.monitor_fields_cbb.setItemText(2, _translate("MainWindow", "Y"))
        self.log_gbox.setTitle(_translate("MainWindow", "Log"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.load_lattice_tool.setText(
            _translate("MainWindow", "Load Lattice"))
        self.measure_tool.setText(_translate("MainWindow", "measure"))
        self.measure_tool.setIconText(_translate("MainWindow", "Measure ORM"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
