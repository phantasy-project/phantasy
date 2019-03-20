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
        MainWindow.resize(1700, 1031)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.matplotlibbarWidget = MatplotlibBarWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.matplotlibbarWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibbarWidget.setSizePolicy(sizePolicy)
        self.matplotlibbarWidget.setProperty("figureBarWidth", 0.8)
        self.matplotlibbarWidget.setObjectName("matplotlibbarWidget")
        self.horizontalLayout_3.addWidget(self.matplotlibbarWidget)
        self.groupBox_4 = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(400, 0))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.select_all_elems_btn = QtWidgets.QToolButton(self.groupBox_4)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/select-all.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.select_all_elems_btn.setIcon(icon1)
        self.select_all_elems_btn.setIconSize(QtCore.QSize(20, 20))
        self.select_all_elems_btn.setObjectName("select_all_elems_btn")
        self.horizontalLayout_2.addWidget(self.select_all_elems_btn)
        self.inverse_selection_btn = QtWidgets.QToolButton(self.groupBox_4)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/invert-selection.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.inverse_selection_btn.setIcon(icon2)
        self.inverse_selection_btn.setIconSize(QtCore.QSize(20, 20))
        self.inverse_selection_btn.setObjectName("inverse_selection_btn")
        self.horizontalLayout_2.addWidget(self.inverse_selection_btn)
        self.field_cbb = QtWidgets.QComboBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.field_cbb.sizePolicy().hasHeightForWidth())
        self.field_cbb.setSizePolicy(sizePolicy)
        self.field_cbb.setObjectName("field_cbb")
        self.horizontalLayout_2.addWidget(self.field_cbb)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.choose_elems_btn = QtWidgets.QPushButton(self.groupBox_4)
        self.choose_elems_btn.setIconSize(QtCore.QSize(20, 20))
        self.choose_elems_btn.setObjectName("choose_elems_btn")
        self.horizontalLayout_2.addWidget(self.choose_elems_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.devices_treeView = QtWidgets.QTreeView(self.groupBox_4)
        self.devices_treeView.setObjectName("devices_treeView")
        self.verticalLayout_2.addWidget(self.devices_treeView)
        self.verticalLayout.addWidget(self.splitter)
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
        self.daqfreq_dSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.daqfreq_dSpinbox.sizePolicy().hasHeightForWidth())
        self.daqfreq_dSpinbox.setSizePolicy(sizePolicy)
        self.daqfreq_dSpinbox.setDecimals(1)
        self.daqfreq_dSpinbox.setMinimum(0.0)
        self.daqfreq_dSpinbox.setMaximum(10.0)
        self.daqfreq_dSpinbox.setSingleStep(0.5)
        self.daqfreq_dSpinbox.setProperty("value", 1.0)
        self.daqfreq_dSpinbox.setObjectName("daqfreq_dSpinbox")
        self.horizontalLayout.addWidget(self.daqfreq_dSpinbox)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.daq_nshot_sbox = QtWidgets.QSpinBox(self.groupBox_3)
        self.daq_nshot_sbox.setSuffix("")
        self.daq_nshot_sbox.setMinimum(1)
        self.daq_nshot_sbox.setMaximum(3000)
        self.daq_nshot_sbox.setObjectName("daq_nshot_sbox")
        self.horizontalLayout.addWidget(self.daq_nshot_sbox)
        self.daq_status_lbl = QtWidgets.QLabel(self.groupBox_3)
        self.daq_status_lbl.setText("")
        self.daq_status_lbl.setPixmap(QtGui.QPixmap(":/icons/inactive.png"))
        self.daq_status_lbl.setObjectName("daq_status_lbl")
        self.horizontalLayout.addWidget(self.daq_status_lbl)
        self.viz_cnt_lbl = QtWidgets.QLabel(self.groupBox_3)
        self.viz_cnt_lbl.setObjectName("viz_cnt_lbl")
        self.horizontalLayout.addWidget(self.viz_cnt_lbl)
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
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/start.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.start_btn.setIcon(icon3)
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon4)
        self.stop_btn.setIconSize(QtCore.QSize(24, 24))
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout.addWidget(self.stop_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/load.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.reset_figure_btn.setIcon(icon5)
        self.reset_figure_btn.setIconSize(QtCore.QSize(16, 16))
        self.reset_figure_btn.setObjectName("reset_figure_btn")
        self.gridLayout.addWidget(self.reset_figure_btn, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1700, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon6)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon7)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon8)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/load_lattice.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon9)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuTools.addAction(self.actionLoad_Lattice)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.id_as_x_rbtn.toggled['bool'].connect(
            MainWindow.on_apply_id_as_xdata)
        self.pos_as_x_rbtn.toggled['bool'].connect(
            MainWindow.on_apply_pos_as_xdata)
        self.start_btn.clicked.connect(MainWindow.on_daq_start)
        self.stop_btn.clicked.connect(MainWindow.on_daq_stop)
        self.reset_figure_btn.clicked.connect(MainWindow.on_init_dataviz)
        self.annote_height_chkbox.toggled['bool'].connect(
            MainWindow.on_annote_height)
        self.actionLoad_Lattice.triggered.connect(
            MainWindow.onLoadLatticeAction)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Data Visualization"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Devices"))
        self.select_all_elems_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.select_all_elems_btn.setText(
            _translate("MainWindow", "Select All"))
        self.inverse_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.inverse_selection_btn.setText(
            _translate("MainWindow", "Inverse Selection"))
        self.choose_elems_btn.setText(_translate("MainWindow", "Choose"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Control Panel"))
        self.label_2.setText(_translate("MainWindow", "Frequency"))
        self.daqfreq_dSpinbox.setSuffix(_translate("MainWindow", " Hz"))
        self.label.setText(_translate("MainWindow", "Shot Number"))
        self.viz_cnt_lbl.setText(_translate("MainWindow", "0"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_11.setText(_translate("MainWindow", "X-Axis"))
        self.id_as_x_rbtn.setText(_translate("MainWindow", "ID"))
        self.pos_as_x_rbtn.setText(_translate("MainWindow", "Position"))
        self.annote_height_chkbox.setText(
            _translate("MainWindow", "Height Annotation"))
        self.label_5.setText(_translate("MainWindow", "DataViz"))
        self.label_6.setText(_translate("MainWindow", "DAQ"))
        self.reset_figure_btn.setToolTip(
            _translate(
                "MainWindow",
                "Reset figure is always required after changing any configuration."
            ))
        self.reset_figure_btn.setText(_translate("MainWindow", "Reset"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))


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
