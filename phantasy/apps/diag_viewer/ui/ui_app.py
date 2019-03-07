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
        MainWindow.resize(1830, 1233)
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
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.machine_cbb = QtWidgets.QComboBox(self.centralwidget)
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
        self.gridLayout_2.addWidget(self.machine_cbb, 0, 1, 1, 1)
        self.mebt_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt_chkbox.setSizePolicy(sizePolicy)
        self.mebt_chkbox.setObjectName("mebt_chkbox")
        self.gridLayout_2.addWidget(self.mebt_chkbox, 0, 4, 1, 1)
        self.device_type_cbb = QtWidgets.QComboBox(self.centralwidget)
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
        self.gridLayout_2.addWidget(self.device_type_cbb, 0, 8, 1, 1)
        self.mebt2fs1a_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt2fs1a_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt2fs1a_chkbox.setSizePolicy(sizePolicy)
        self.mebt2fs1a_chkbox.setObjectName("mebt2fs1a_chkbox")
        self.gridLayout_2.addWidget(self.mebt2fs1a_chkbox, 0, 5, 1, 1)
        self.daq_hbox = QtWidgets.QHBoxLayout()
        self.daq_hbox.setObjectName("daq_hbox")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.daq_hbox.addWidget(self.label_11)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.daq_hbox.addWidget(self.line_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.freq_dSpinbox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.freq_dSpinbox.setDecimals(1)
        self.freq_dSpinbox.setMinimum(0.0)
        self.freq_dSpinbox.setMaximum(10.0)
        self.freq_dSpinbox.setSingleStep(0.5)
        self.freq_dSpinbox.setProperty("value", 1.0)
        self.freq_dSpinbox.setObjectName("freq_dSpinbox")
        self.gridLayout.addWidget(self.freq_dSpinbox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/start.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.start_btn.setIcon(icon)
        self.start_btn.setIconSize(QtCore.QSize(24, 24))
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 1, 1, 1, 1)
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon1)
        self.stop_btn.setIconSize(QtCore.QSize(24, 24))
        self.stop_btn.setObjectName("stop_btn")
        self.gridLayout.addWidget(self.stop_btn, 1, 2, 1, 1)
        self.daq_hbox.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.daq_hbox, 2, 12, 1, 1)
        self.load_pb = QtWidgets.QProgressBar(self.centralwidget)
        self.load_pb.setMaximum(0)
        self.load_pb.setProperty("value", -1)
        self.load_pb.setObjectName("load_pb")
        self.gridLayout_2.addWidget(self.load_pb, 0, 10, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 7, 1, 1)
        self.matplotlibbarWidget = MatplotlibBarWidget(self.centralwidget)
        self.matplotlibbarWidget.setObjectName("matplotlibbarWidget")
        self.gridLayout_2.addWidget(self.matplotlibbarWidget, 1, 0, 1, 13)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.mebt2fs1b_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt2fs1b_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt2fs1b_chkbox.setSizePolicy(sizePolicy)
        self.mebt2fs1b_chkbox.setObjectName("mebt2fs1b_chkbox")
        self.gridLayout_2.addWidget(self.mebt2fs1b_chkbox, 0, 6, 1, 1)
        self.load_btn = QtWidgets.QToolButton(self.centralwidget)
        self.load_btn.setObjectName("load_btn")
        self.gridLayout_2.addWidget(self.load_btn, 0, 9, 1, 1)
        self.lebt_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lebt_chkbox.sizePolicy().hasHeightForWidth())
        self.lebt_chkbox.setSizePolicy(sizePolicy)
        self.lebt_chkbox.setObjectName("lebt_chkbox")
        self.gridLayout_2.addWidget(self.lebt_chkbox, 0, 3, 1, 1)
        self.load_status_lbl = QtWidgets.QLabel(self.centralwidget)
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
        self.gridLayout_2.addWidget(self.load_status_lbl, 0, 12, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1830, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon2)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon3)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon4)
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
        self.load_btn.clicked.connect(MainWindow.on_load_devices)
        self.device_type_cbb.currentTextChanged['QString'].connect(
            MainWindow.on_device_type_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Machine"))
        self.machine_cbb.setItemText(0, _translate("MainWindow", "FRIB"))
        self.machine_cbb.setItemText(1, _translate("MainWindow", "VA_LS1FS1"))
        self.mebt_chkbox.setText(_translate("MainWindow", "MEBT"))
        self.device_type_cbb.setItemText(0, _translate("MainWindow", "BCM"))
        self.device_type_cbb.setItemText(1, _translate("MainWindow", "BPM"))
        self.mebt2fs1a_chkbox.setText(_translate("MainWindow", "MEBT2FS1A"))
        self.label_11.setText(_translate("MainWindow", "DAQ"))
        self.label_2.setText(_translate("MainWindow", "Frequency"))
        self.label_3.setText(_translate("MainWindow", "Hz"))
        self.label_5.setText(_translate("MainWindow", "Action"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_7.setText(_translate("MainWindow", "Device Type"))
        self.label_4.setText(_translate("MainWindow", "Segments"))
        self.mebt2fs1b_chkbox.setText(_translate("MainWindow", "MEBT2FS1B"))
        self.load_btn.setText(_translate("MainWindow", "Load"))
        self.lebt_chkbox.setText(_translate("MainWindow", "LEBT"))
        self.load_status_lbl.setText(
            _translate("MainWindow", "Device Loading Ready?"))
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
