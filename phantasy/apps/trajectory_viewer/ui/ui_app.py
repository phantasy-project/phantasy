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
        MainWindow.resize(1507, 1153)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal,
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
            "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.h_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.h_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.h_splitter.setObjectName("h_splitter")
        self.v_splitter_1 = QtWidgets.QSplitter(self.h_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.v_splitter_1.sizePolicy().hasHeightForWidth())
        self.v_splitter_1.setSizePolicy(sizePolicy)
        self.v_splitter_1.setOrientation(QtCore.Qt.Vertical)
        self.v_splitter_1.setObjectName("v_splitter_1")
        self.groupBox_2 = QtWidgets.QGroupBox(self.v_splitter_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.matplotlibcurveWidget = MatplotlibCurveWidget(self.groupBox_2)
        self.matplotlibcurveWidget.setProperty("figureTightLayout", False)
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.gridLayout_2.addWidget(self.matplotlibcurveWidget, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.v_splitter_1)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.freq_dSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.freq_dSpinbox.setDecimals(1)
        self.freq_dSpinbox.setMinimum(0.1)
        self.freq_dSpinbox.setMaximum(10.0)
        self.freq_dSpinbox.setSingleStep(0.5)
        self.freq_dSpinbox.setProperty("value", 1.0)
        self.freq_dSpinbox.setObjectName("freq_dSpinbox")
        self.gridLayout.addWidget(self.freq_dSpinbox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(411, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 2)
        self.stop_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        self.stop_btn.setObjectName("stop_btn")
        self.gridLayout.addWidget(self.stop_btn, 1, 2, 1, 2)
        self.start_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(368, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.v_splitter_2 = QtWidgets.QSplitter(self.h_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.v_splitter_2.sizePolicy().hasHeightForWidth())
        self.v_splitter_2.setSizePolicy(sizePolicy)
        self.v_splitter_2.setMinimumSize(QtCore.QSize(400, 0))
        self.v_splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.v_splitter_2.setObjectName("v_splitter_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.v_splitter_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.select_elem_btn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_elem_btn.sizePolicy().hasHeightForWidth())
        self.select_elem_btn.setSizePolicy(sizePolicy)
        self.select_elem_btn.setObjectName("select_elem_btn")
        self.gridLayout_4.addWidget(self.select_elem_btn, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(599, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 2, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.groupBox_3)
        self.treeView.setObjectName("treeView")
        self.gridLayout_4.addWidget(self.treeView, 1, 0, 1, 3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.v_splitter_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.select_elem_btn_2 = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_elem_btn_2.sizePolicy().hasHeightForWidth())
        self.select_elem_btn_2.setSizePolicy(sizePolicy)
        self.select_elem_btn_2.setObjectName("select_elem_btn_2")
        self.gridLayout_3.addWidget(self.select_elem_btn_2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(560, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        self.treeView_2 = QtWidgets.QTreeView(self.groupBox_4)
        self.treeView_2.setObjectName("treeView_2")
        self.gridLayout_3.addWidget(self.treeView_2, 1, 0, 1, 3)
        self.gridLayout_5.addWidget(self.h_splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1507, 29))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Tools = QtWidgets.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon1)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon2)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon3)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionContents.setIcon(icon4)
        self.actionContents.setObjectName("actionContents")
        self.actionORM = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/matrix.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionORM.setIcon(icon5)
        self.actionORM.setObjectName("actionORM")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/load_lattice.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon6)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Tools.addAction(self.actionORM)
        self.menu_Tools.addAction(self.actionLoad_Lattice)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionContents.triggered.connect(MainWindow.onHelp)
        self.actionORM.triggered.connect(MainWindow.on_launch_orm)
        self.actionLoad_Lattice.triggered.connect(
            MainWindow.onLoadLatticeAction)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(
            _translate("MainWindow", "Data Visualization"))
        self.groupBox.setTitle(_translate("MainWindow", "DAQ Configuration"))
        self.label_3.setText(_translate("MainWindow", "Hz"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.label_2.setText(_translate("MainWindow", "Frequency"))
        self.label_5.setText(_translate("MainWindow", "Action"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Monitors"))
        self.label_4.setText(_translate("MainWindow", "Select BPMs"))
        self.select_elem_btn.setText(_translate("MainWindow", "Choose"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Correctors"))
        self.label_6.setText(_translate("MainWindow", "Select Correctors"))
        self.select_elem_btn_2.setText(_translate("MainWindow", "Choose"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionORM.setText(
            _translate("MainWindow", "Orbit Response Matrix"))
        self.actionORM.setShortcut(_translate("MainWindow", "Ctrl+Shift+M"))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))


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
