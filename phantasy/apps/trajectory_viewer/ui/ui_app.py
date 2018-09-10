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
        MainWindow.resize(1227, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("QLabel {\n"
                                 "    font-weight: bold;\n"
                                 "    font-size: 20pt;\n"
                                 "}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.latticeWidget = LatticeWidget(self.centralwidget)
        self.latticeWidget.setObjectName("latticeWidget")
        self.horizontalLayout.addWidget(self.latticeWidget)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 2ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 1ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "}")
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setContentsMargins(9, 9, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.select_elem_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_elem_btn.sizePolicy().hasHeightForWidth())
        self.select_elem_btn.setSizePolicy(sizePolicy)
        self.select_elem_btn.setObjectName("select_elem_btn")
        self.gridLayout_2.addWidget(self.select_elem_btn, 1, 1, 1, 3)
        self.stop_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        self.stop_btn.setObjectName("stop_btn")
        self.gridLayout_2.addWidget(self.stop_btn, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 2)
        self.freq_dSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.freq_dSpinbox.setDecimals(1)
        self.freq_dSpinbox.setMinimum(0.1)
        self.freq_dSpinbox.setMaximum(10.0)
        self.freq_dSpinbox.setSingleStep(0.5)
        self.freq_dSpinbox.setProperty("value", 1.0)
        self.freq_dSpinbox.setObjectName("freq_dSpinbox")
        self.gridLayout_2.addWidget(self.freq_dSpinbox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout_2.addWidget(self.start_btn, 2, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 4, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.matplotlibcurveWidget = MatplotlibCurveWidget(self.centralwidget)
        self.matplotlibcurveWidget.setProperty("figureTightLayout", True)
        self.matplotlibcurveWidget.setProperty("figureDPI", 100)
        self.matplotlibcurveWidget.setProperty("figureBackgroundColor",
                                               QtGui.QColor(237, 236, 235))
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.verticalLayout.addWidget(self.matplotlibcurveWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1227, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.latticeWidget.latticeChanged['QVariant'].connect(
            MainWindow.onLatticeChanged)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Trajectory Viewer"))
        self.groupBox.setTitle(_translate("MainWindow", "Control Panel"))
        self.label_4.setText(_translate("MainWindow", "Select Devices"))
        self.label_5.setText(_translate("MainWindow", "DAQ Action"))
        self.select_elem_btn.setText(_translate("MainWindow", "Choose"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_3.setText(_translate("MainWindow", "Hz"))
        self.label_2.setText(_translate("MainWindow", "DAQ Frequency"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))


from mpl4qt.widgets.mplcurvewidget import MatplotlibCurveWidget
from phantasy_ui.widgets.latticewidget import LatticeWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
