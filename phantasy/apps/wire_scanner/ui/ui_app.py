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
        MainWindow.resize(1920, 1499)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/ws.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QLineEdit {\n"
                                 "    border: 0.5px solid gray;\n"
                                 "    padding: 1 5px;\n"
                                 "    border-radius: 3px;\n"
                                 "}")
        MainWindow.setIconSize(QtCore.QSize(64, 64))
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
        sizePolicy.setVerticalStretch(0)
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
        self.offset3_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset3_lineEdit.setStyleSheet("")
        self.offset3_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset3_lineEdit.setObjectName("offset3_lineEdit")
        self.gridLayout_3.addWidget(self.offset3_lineEdit, 3, 6, 1, 1)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.run_btn.setIcon(icon1)
        self.run_btn.setIconSize(QtCore.QSize(24, 24))
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.emstop_btn.setIcon(icon2)
        self.emstop_btn.setIconSize(QtCore.QSize(24, 24))
        self.emstop_btn.setAutoRaise(True)
        self.emstop_btn.setObjectName("emstop_btn")
        self.horizontalLayout_2.addWidget(self.emstop_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 4, 0, 1, 13)
        self.info_lbl = QtWidgets.QLabel(self.controls_groupBox)
        self.info_lbl.setStyleSheet("")
        self.info_lbl.setText("")
        self.info_lbl.setScaledContents(False)
        self.info_lbl.setObjectName("info_lbl")
        self.gridLayout_3.addWidget(self.info_lbl, 0, 5, 1, 1)
        self.offset1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset1_lineEdit.setStyleSheet("")
        self.offset1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset1_lineEdit.setObjectName("offset1_lineEdit")
        self.gridLayout_3.addWidget(self.offset1_lineEdit, 3, 3, 1, 1)
        self.coord_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.coord_lineEdit.setStyleSheet("")
        self.coord_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coord_lineEdit.setReadOnly(True)
        self.coord_lineEdit.setObjectName("coord_lineEdit")
        self.gridLayout_3.addWidget(self.coord_lineEdit, 2, 6, 1, 1)
        self.pm_names_cbb = QtWidgets.QComboBox(self.controls_groupBox)
        self.pm_names_cbb.setStyleSheet("QComboBox {\n"
                                        "    font-family: monospace;\n"
                                        "}")
        self.pm_names_cbb.setObjectName("pm_names_cbb")
        self.gridLayout_3.addWidget(self.pm_names_cbb, 0, 2, 1, 3)
        self.label_7 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 10, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 2, 1, 1)
        self.offset2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.offset2_lineEdit.setStyleSheet("")
        self.offset2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.offset2_lineEdit.setObjectName("offset2_lineEdit")
        self.gridLayout_3.addWidget(self.offset2_lineEdit, 3, 4, 1, 1)
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
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 10, 1, 1)
        self.stop_pos1_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.stop_pos1_lineEdit.setStyleSheet("")
        self.stop_pos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stop_pos1_lineEdit.setObjectName("stop_pos1_lineEdit")
        self.gridLayout_3.addWidget(self.stop_pos1_lineEdit, 3, 9, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 8, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.controls_groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.controls_groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 13)
        self.label_4 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 4, 1, 1)
        self.pm_detail_btn = QtWidgets.QToolButton(self.controls_groupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/browse.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pm_detail_btn.setIcon(icon3)
        self.pm_detail_btn.setIconSize(QtCore.QSize(20, 20))
        self.pm_detail_btn.setAutoRaise(True)
        self.pm_detail_btn.setObjectName("pm_detail_btn")
        self.gridLayout_3.addWidget(self.pm_detail_btn, 0, 6, 1, 1)
        self.start_pos2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.start_pos2_lineEdit.setStyleSheet("")
        self.start_pos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.start_pos2_lineEdit.setObjectName("start_pos2_lineEdit")
        self.gridLayout_3.addWidget(self.start_pos2_lineEdit, 2, 11, 1, 2)
        self.dtype_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.dtype_lineEdit.setStyleSheet("")
        self.dtype_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dtype_lineEdit.setReadOnly(True)
        self.dtype_lineEdit.setObjectName("dtype_lineEdit")
        self.gridLayout_3.addWidget(self.dtype_lineEdit, 2, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 8, 1, 1)
        self.advctrl_groupBox = QtWidgets.QGroupBox(self.controls_groupBox)
        self.advctrl_groupBox.setObjectName("advctrl_groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.advctrl_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.startpos2_lineEdit = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.startpos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.startpos2_lineEdit.setObjectName("startpos2_lineEdit")
        self.gridLayout_4.addWidget(self.startpos2_lineEdit, 2, 3, 1, 1)
        self.init_potentiometer_btn = QtWidgets.QPushButton(
            self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.init_potentiometer_btn.sizePolicy().hasHeightForWidth())
        self.init_potentiometer_btn.setSizePolicy(sizePolicy)
        self.init_potentiometer_btn.setObjectName("init_potentiometer_btn")
        self.gridLayout_4.addWidget(self.init_potentiometer_btn, 0, 0, 1, 1)
        self.enable_scan_btn = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.enable_scan_btn.sizePolicy().hasHeightForWidth())
        self.enable_scan_btn.setSizePolicy(sizePolicy)
        self.enable_scan_btn.setObjectName("enable_scan_btn")
        self.gridLayout_4.addWidget(self.enable_scan_btn, 0, 2, 1, 1)
        self.reset_interlock_btn = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.reset_interlock_btn.sizePolicy().hasHeightForWidth())
        self.reset_interlock_btn.setSizePolicy(sizePolicy)
        self.reset_interlock_btn.setObjectName("reset_interlock_btn")
        self.gridLayout_4.addWidget(self.reset_interlock_btn, 0, 3, 1, 1)
        self.init_motor_pos_btn = QtWidgets.QPushButton(self.advctrl_groupBox)
        self.init_motor_pos_btn.setObjectName("init_motor_pos_btn")
        self.gridLayout_4.addWidget(self.init_motor_pos_btn, 1, 0, 1, 1)
        self.set_bias_volt_btn = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.set_bias_volt_btn.sizePolicy().hasHeightForWidth())
        self.set_bias_volt_btn.setSizePolicy(sizePolicy)
        self.set_bias_volt_btn.setObjectName("set_bias_volt_btn")
        self.gridLayout_4.addWidget(self.set_bias_volt_btn, 0, 4, 1, 1)
        self.mode_btn = QtWidgets.QPushButton(self.advctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mode_btn.sizePolicy().hasHeightForWidth())
        self.mode_btn.setSizePolicy(sizePolicy)
        self.mode_btn.setObjectName("mode_btn")
        self.gridLayout_4.addWidget(self.mode_btn, 0, 5, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.advctrl_groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 1, 2, 1, 1)
        self.stoppos2_lineEdit = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.stoppos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stoppos2_lineEdit.setObjectName("stoppos2_lineEdit")
        self.gridLayout_4.addWidget(self.stoppos2_lineEdit, 2, 5, 1, 1)
        self.outlimit_lineEdit = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.outlimit_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.outlimit_lineEdit.setObjectName("outlimit_lineEdit")
        self.gridLayout_4.addWidget(self.outlimit_lineEdit, 1, 3, 1, 1)
        self.set_scan_range_btn = QtWidgets.QPushButton(self.advctrl_groupBox)
        self.set_scan_range_btn.setObjectName("set_scan_range_btn")
        self.gridLayout_4.addWidget(self.set_scan_range_btn, 2, 0, 1, 1)
        self.startpos1_lineEdit = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.startpos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.startpos1_lineEdit.setObjectName("startpos1_lineEdit")
        self.gridLayout_4.addWidget(self.startpos1_lineEdit, 2, 2, 1, 1)
        self.stoppos1_lineEdit = QtWidgets.QLineEdit(self.advctrl_groupBox)
        self.stoppos1_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stoppos1_lineEdit.setObjectName("stoppos1_lineEdit")
        self.gridLayout_4.addWidget(self.stoppos1_lineEdit, 2, 4, 1, 1)
        self.gridLayout_3.addWidget(self.advctrl_groupBox, 5, 0, 1, 13)
        self.stop_pos2_lineEdit = QtWidgets.QLineEdit(self.controls_groupBox)
        self.stop_pos2_lineEdit.setStyleSheet("")
        self.stop_pos2_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stop_pos2_lineEdit.setObjectName("stop_pos2_lineEdit")
        self.gridLayout_3.addWidget(self.stop_pos2_lineEdit, 3, 11, 1, 2)
        self.label_36 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_36.setText("")
        self.label_36.setPixmap(QtGui.QPixmap(":/icons/dblrarr.png"))
        self.label_36.setScaledContents(False)
        self.label_36.setObjectName("label_36")
        self.gridLayout_3.addWidget(self.label_36, 0, 1, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.controls_groupBox)
        self.label_37.setText("")
        self.label_37.setPixmap(QtGui.QPixmap(":/icons/dblrarr.png"))
        self.label_37.setScaledContents(False)
        self.label_37.setObjectName("label_37")
        self.gridLayout_3.addWidget(self.label_37, 2, 1, 1, 1)
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
        self.info_lbl.raise_()
        self.label_36.raise_()
        self.label_37.raise_()
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
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
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(800, 0))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.matplotlibcurveWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibcurveWidget.setSizePolicy(sizePolicy)
        self.matplotlibcurveWidget.setProperty("figureLegendToggle", False)
        self.matplotlibcurveWidget.setFigureAutoScale(False)
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.gridLayout_2.addWidget(self.matplotlibcurveWidget, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.reset_xyscale_btn = QtWidgets.QPushButton(self.groupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/reset_scale.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.reset_xyscale_btn.setIcon(icon4)
        self.reset_xyscale_btn.setIconSize(QtCore.QSize(24, 24))
        self.reset_xyscale_btn.setObjectName("reset_xyscale_btn")
        self.horizontalLayout_3.addWidget(self.reset_xyscale_btn)
        self.legend_btn = QtWidgets.QPushButton(self.groupBox)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/label.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.legend_btn.setIcon(icon5)
        self.legend_btn.setIconSize(QtCore.QSize(24, 24))
        self.legend_btn.setCheckable(True)
        self.legend_btn.setObjectName("legend_btn")
        self.horizontalLayout_3.addWidget(self.legend_btn)
        self.grid_btn = QtWidgets.QPushButton(self.groupBox)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/grid.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.grid_btn.setIcon(icon6)
        self.grid_btn.setIconSize(QtCore.QSize(24, 24))
        self.grid_btn.setCheckable(True)
        self.grid_btn.setObjectName("grid_btn")
        self.horizontalLayout_3.addWidget(self.grid_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.hide_curve2_btn = QtWidgets.QToolButton(self.groupBox)
        self.hide_curve2_btn.setStyleSheet("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/u.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.hide_curve2_btn.setIcon(icon7)
        self.hide_curve2_btn.setIconSize(QtCore.QSize(24, 24))
        self.hide_curve2_btn.setCheckable(True)
        self.hide_curve2_btn.setAutoRaise(True)
        self.hide_curve2_btn.setObjectName("hide_curve2_btn")
        self.horizontalLayout_3.addWidget(self.hide_curve2_btn)
        self.hide_curve1_btn = QtWidgets.QToolButton(self.groupBox)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/v.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.hide_curve1_btn.setIcon(icon8)
        self.hide_curve1_btn.setIconSize(QtCore.QSize(24, 24))
        self.hide_curve1_btn.setCheckable(True)
        self.hide_curve1_btn.setAutoRaise(True)
        self.hide_curve1_btn.setObjectName("hide_curve1_btn")
        self.horizontalLayout_3.addWidget(self.hide_curve1_btn)
        self.hide_curve3_btn = QtWidgets.QToolButton(self.groupBox)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/w.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.hide_curve3_btn.setIcon(icon9)
        self.hide_curve3_btn.setIconSize(QtCore.QSize(24, 24))
        self.hide_curve3_btn.setCheckable(True)
        self.hide_curve3_btn.setAutoRaise(True)
        self.hide_curve3_btn.setObjectName("hide_curve3_btn")
        self.horizontalLayout_3.addWidget(self.hide_curve3_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plot_data_smoving_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_data_smoving_btn.sizePolicy().hasHeightForWidth())
        self.plot_data_smoving_btn.setSizePolicy(sizePolicy)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/line-chart.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.plot_data_smoving_btn.setIcon(icon10)
        self.plot_data_smoving_btn.setIconSize(QtCore.QSize(24, 24))
        self.plot_data_smoving_btn.setObjectName("plot_data_smoving_btn")
        self.horizontalLayout.addWidget(self.plot_data_smoving_btn)
        self.plot_data_sbeam_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_data_sbeam_btn.sizePolicy().hasHeightForWidth())
        self.plot_data_sbeam_btn.setSizePolicy(sizePolicy)
        self.plot_data_sbeam_btn.setIcon(icon10)
        self.plot_data_sbeam_btn.setIconSize(QtCore.QSize(24, 24))
        self.plot_data_sbeam_btn.setObjectName("plot_data_sbeam_btn")
        self.horizontalLayout.addWidget(self.plot_data_sbeam_btn)
        self.plot_data_subnoise_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_data_subnoise_btn.sizePolicy().hasHeightForWidth())
        self.plot_data_subnoise_btn.setSizePolicy(sizePolicy)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(
            QtGui.QPixmap(":/icons/minus.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.plot_data_subnoise_btn.setIcon(icon11)
        self.plot_data_subnoise_btn.setIconSize(QtCore.QSize(24, 24))
        self.plot_data_subnoise_btn.setObjectName("plot_data_subnoise_btn")
        self.horizontalLayout.addWidget(self.plot_data_subnoise_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(400, 0))
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
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_9.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.adv_analysis_groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.adv_analysis_groupBox.setObjectName("adv_analysis_groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.adv_analysis_groupBox)
        self.gridLayout_5.setHorizontalSpacing(9)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.adv_analysis_groupBox)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_5.addWidget(self.lineEdit_3, 6, 3, 1, 2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.adv_analysis_groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_5.addWidget(self.lineEdit_2, 5, 3, 1, 2)
        self.wpos1_left_lineEdit = QtWidgets.QLineEdit(
            self.adv_analysis_groupBox)
        self.wpos1_left_lineEdit.setObjectName("wpos1_left_lineEdit")
        self.gridLayout_5.addWidget(self.wpos1_left_lineEdit, 1, 3, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.adv_analysis_groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_5.addWidget(self.lineEdit, 4, 3, 1, 2)
        self.wpos2_right_lineEdit = QtWidgets.QLineEdit(
            self.adv_analysis_groupBox)
        self.wpos2_right_lineEdit.setObjectName("wpos2_right_lineEdit")
        self.gridLayout_5.addWidget(self.wpos2_right_lineEdit, 2, 4, 1, 1)
        self.wpos1_right_lineEdit = QtWidgets.QLineEdit(
            self.adv_analysis_groupBox)
        self.wpos1_right_lineEdit.setObjectName("wpos1_right_lineEdit")
        self.gridLayout_5.addWidget(self.wpos1_right_lineEdit, 1, 4, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        self.label_39.setObjectName("label_39")
        self.gridLayout_5.addWidget(self.label_39, 1, 1, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        self.label_40.setObjectName("label_40")
        self.gridLayout_5.addWidget(self.label_40, 3, 1, 1, 1)
        self.wpos2_left_lineEdit = QtWidgets.QLineEdit(
            self.adv_analysis_groupBox)
        self.wpos2_left_lineEdit.setObjectName("wpos2_left_lineEdit")
        self.gridLayout_5.addWidget(self.wpos2_left_lineEdit, 2, 3, 1, 1)
        self.wpos3_left_lineEdit = QtWidgets.QLineEdit(
            self.adv_analysis_groupBox)
        self.wpos3_left_lineEdit.setObjectName("wpos3_left_lineEdit")
        self.gridLayout_5.addWidget(self.wpos3_left_lineEdit, 3, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 2, 1, 1, 1)
        self.wpos3_right_lineEdit = QtWidgets.QLineEdit(
            self.adv_analysis_groupBox)
        self.wpos3_right_lineEdit.setObjectName("wpos3_right_lineEdit")
        self.gridLayout_5.addWidget(self.wpos3_right_lineEdit, 3, 4, 1, 1)
        self.plot_wpos1_btn = QtWidgets.QToolButton(self.adv_analysis_groupBox)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(
            QtGui.QPixmap(":/icons/show.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.plot_wpos1_btn.setIcon(icon12)
        self.plot_wpos1_btn.setIconSize(QtCore.QSize(24, 24))
        self.plot_wpos1_btn.setCheckable(True)
        self.plot_wpos1_btn.setAutoRaise(True)
        self.plot_wpos1_btn.setObjectName("plot_wpos1_btn")
        self.gridLayout_5.addWidget(self.plot_wpos1_btn, 1, 0, 1, 1)
        self.plot_wpos2_btn = QtWidgets.QToolButton(self.adv_analysis_groupBox)
        self.plot_wpos2_btn.setIcon(icon12)
        self.plot_wpos2_btn.setIconSize(QtCore.QSize(24, 24))
        self.plot_wpos2_btn.setCheckable(True)
        self.plot_wpos2_btn.setAutoRaise(True)
        self.plot_wpos2_btn.setObjectName("plot_wpos2_btn")
        self.gridLayout_5.addWidget(self.plot_wpos2_btn, 2, 0, 1, 1)
        self.plot_wpos3_btn = QtWidgets.QToolButton(self.adv_analysis_groupBox)
        self.plot_wpos3_btn.setIcon(icon12)
        self.plot_wpos3_btn.setIconSize(QtCore.QSize(24, 24))
        self.plot_wpos3_btn.setCheckable(True)
        self.plot_wpos3_btn.setAutoRaise(True)
        self.plot_wpos3_btn.setObjectName("plot_wpos3_btn")
        self.gridLayout_5.addWidget(self.plot_wpos3_btn, 3, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 4, 0, 1, 2)
        self.label_15 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 5, 0, 1, 2)
        self.label_16 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 6, 0, 1, 2)
        self.label_38 = QtWidgets.QLabel(self.adv_analysis_groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.gridLayout_5.addWidget(self.label_38, 0, 0, 1, 5)
        self.gridLayout_9.addWidget(self.adv_analysis_groupBox, 2, 0, 1, 3)
        self.data_filepath_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.data_filepath_lineEdit.setReadOnly(True)
        self.data_filepath_lineEdit.setObjectName("data_filepath_lineEdit")
        self.gridLayout_9.addWidget(self.data_filepath_lineEdit, 4, 0, 1, 3)
        self.label_35 = QtWidgets.QLabel(self.groupBox_2)
        self.label_35.setObjectName("label_35")
        self.gridLayout_9.addWidget(self.label_35, 3, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.data_path_locate_btn = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.data_path_locate_btn.sizePolicy().hasHeightForWidth())
        self.data_path_locate_btn.setSizePolicy(sizePolicy)
        self.data_path_locate_btn.setObjectName("data_path_locate_btn")
        self.horizontalLayout_5.addWidget(self.data_path_locate_btn)
        self.gridLayout_9.addLayout(self.horizontalLayout_5, 3, 1, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.analyze_btn = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analyze_btn.sizePolicy().hasHeightForWidth())
        self.analyze_btn.setSizePolicy(sizePolicy)
        self.analyze_btn.setObjectName("analyze_btn")
        self.horizontalLayout_4.addWidget(self.analyze_btn)
        self.adv_analysis_chkbox = QtWidgets.QCheckBox(self.groupBox_2)
        self.adv_analysis_chkbox.setObjectName("adv_analysis_chkbox")
        self.horizontalLayout_4.addWidget(self.adv_analysis_chkbox)
        self.analysis_progressbar = QtWidgets.QProgressBar(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysis_progressbar.sizePolicy().hasHeightForWidth())
        self.analysis_progressbar.setSizePolicy(sizePolicy)
        self.analysis_progressbar.setMaximum(0)
        self.analysis_progressbar.setProperty("value", -1)
        self.analysis_progressbar.setObjectName("analysis_progressbar")
        self.horizontalLayout_4.addWidget(self.analysis_progressbar)
        self.analyzed_status_lbl = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analyzed_status_lbl.sizePolicy().hasHeightForWidth())
        self.analyzed_status_lbl.setSizePolicy(sizePolicy)
        self.analyzed_status_lbl.setText("")
        self.analyzed_status_lbl.setObjectName("analyzed_status_lbl")
        self.horizontalLayout_4.addWidget(self.analyzed_status_lbl)
        self.sync_results_btn = QtWidgets.QToolButton(self.groupBox_2)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(
            QtGui.QPixmap(":/icons/sync.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.sync_results_btn.setIcon(icon13)
        self.sync_results_btn.setIconSize(QtCore.QSize(24, 24))
        self.sync_results_btn.setObjectName("sync_results_btn")
        self.horizontalLayout_4.addWidget(self.sync_results_btn)
        self.gridLayout_9.addLayout(self.horizontalLayout_4, 1, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem3, 8, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.fontsize_inc_btn = QtWidgets.QToolButton(self.groupBox_2)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(
            QtGui.QPixmap(":/icons/increase_fontsize.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.fontsize_inc_btn.setIcon(icon14)
        self.fontsize_inc_btn.setIconSize(QtCore.QSize(20, 20))
        self.fontsize_inc_btn.setAutoRaise(True)
        self.fontsize_inc_btn.setObjectName("fontsize_inc_btn")
        self.horizontalLayout_6.addWidget(self.fontsize_inc_btn)
        self.fontsize_dec_btn = QtWidgets.QToolButton(self.groupBox_2)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(
            QtGui.QPixmap(":/icons/decrease_fontsize.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.fontsize_dec_btn.setIcon(icon15)
        self.fontsize_dec_btn.setIconSize(QtCore.QSize(20, 20))
        self.fontsize_dec_btn.setAutoRaise(True)
        self.fontsize_dec_btn.setObjectName("fontsize_dec_btn")
        self.horizontalLayout_6.addWidget(self.fontsize_dec_btn)
        self.gridLayout_9.addLayout(self.horizontalLayout_6, 5, 0, 1, 3)
        self.results_wires_gb = QtWidgets.QGroupBox(self.groupBox_2)
        self.results_wires_gb.setObjectName("results_wires_gb")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.results_wires_gb)
        self.gridLayout_6.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_17 = QtWidgets.QLabel(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_6.addWidget(self.label_17, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_6.addWidget(self.label_18, 0, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_6.addWidget(self.label_19, 0, 3, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_6.addWidget(self.label_20, 1, 0, 1, 1)
        self.w11_sum_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w11_sum_lineEdit.sizePolicy().hasHeightForWidth())
        self.w11_sum_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w11_sum_lineEdit.setFont(font)
        self.w11_sum_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w11_sum_lineEdit.setReadOnly(True)
        self.w11_sum_lineEdit.setObjectName("w11_sum_lineEdit")
        self.gridLayout_6.addWidget(self.w11_sum_lineEdit, 1, 1, 1, 1)
        self.w21_sum_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w21_sum_lineEdit.sizePolicy().hasHeightForWidth())
        self.w21_sum_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w21_sum_lineEdit.setFont(font)
        self.w21_sum_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w21_sum_lineEdit.setReadOnly(True)
        self.w21_sum_lineEdit.setObjectName("w21_sum_lineEdit")
        self.gridLayout_6.addWidget(self.w21_sum_lineEdit, 1, 2, 1, 1)
        self.w22_sum_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w22_sum_lineEdit.sizePolicy().hasHeightForWidth())
        self.w22_sum_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w22_sum_lineEdit.setFont(font)
        self.w22_sum_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w22_sum_lineEdit.setReadOnly(True)
        self.w22_sum_lineEdit.setObjectName("w22_sum_lineEdit")
        self.gridLayout_6.addWidget(self.w22_sum_lineEdit, 1, 3, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout_6.addWidget(self.label_21, 2, 0, 1, 1)
        self.w11_center_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w11_center_lineEdit.sizePolicy().hasHeightForWidth())
        self.w11_center_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w11_center_lineEdit.setFont(font)
        self.w11_center_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w11_center_lineEdit.setReadOnly(True)
        self.w11_center_lineEdit.setObjectName("w11_center_lineEdit")
        self.gridLayout_6.addWidget(self.w11_center_lineEdit, 2, 1, 1, 1)
        self.w21_center_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w21_center_lineEdit.sizePolicy().hasHeightForWidth())
        self.w21_center_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w21_center_lineEdit.setFont(font)
        self.w21_center_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w21_center_lineEdit.setReadOnly(True)
        self.w21_center_lineEdit.setObjectName("w21_center_lineEdit")
        self.gridLayout_6.addWidget(self.w21_center_lineEdit, 2, 2, 1, 1)
        self.w22_center_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w22_center_lineEdit.sizePolicy().hasHeightForWidth())
        self.w22_center_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w22_center_lineEdit.setFont(font)
        self.w22_center_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w22_center_lineEdit.setReadOnly(True)
        self.w22_center_lineEdit.setObjectName("w22_center_lineEdit")
        self.gridLayout_6.addWidget(self.w22_center_lineEdit, 2, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.gridLayout_6.addWidget(self.label_22, 3, 0, 1, 1)
        self.w11_rms_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w11_rms_lineEdit.sizePolicy().hasHeightForWidth())
        self.w11_rms_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w11_rms_lineEdit.setFont(font)
        self.w11_rms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w11_rms_lineEdit.setReadOnly(True)
        self.w11_rms_lineEdit.setObjectName("w11_rms_lineEdit")
        self.gridLayout_6.addWidget(self.w11_rms_lineEdit, 3, 1, 1, 1)
        self.w21_rms_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w21_rms_lineEdit.sizePolicy().hasHeightForWidth())
        self.w21_rms_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w21_rms_lineEdit.setFont(font)
        self.w21_rms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w21_rms_lineEdit.setReadOnly(True)
        self.w21_rms_lineEdit.setObjectName("w21_rms_lineEdit")
        self.gridLayout_6.addWidget(self.w21_rms_lineEdit, 3, 2, 1, 1)
        self.w22_rms_lineEdit = QtWidgets.QLineEdit(self.results_wires_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w22_rms_lineEdit.sizePolicy().hasHeightForWidth())
        self.w22_rms_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.w22_rms_lineEdit.setFont(font)
        self.w22_rms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.w22_rms_lineEdit.setReadOnly(True)
        self.w22_rms_lineEdit.setObjectName("w22_rms_lineEdit")
        self.gridLayout_6.addWidget(self.w22_rms_lineEdit, 3, 3, 1, 1)
        self.gridLayout_9.addWidget(self.results_wires_gb, 6, 0, 1, 3)
        self.results_beam_gb = QtWidgets.QGroupBox(self.groupBox_2)
        self.results_beam_gb.setObjectName("results_beam_gb")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.results_beam_gb)
        self.gridLayout_7.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_30 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_30.setObjectName("label_30")
        self.gridLayout_7.addWidget(self.label_30, 3, 0, 1, 1)
        self.xrms90_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.xrms90_lineEdit.setFont(font)
        self.xrms90_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.xrms90_lineEdit.setReadOnly(True)
        self.xrms90_lineEdit.setObjectName("xrms90_lineEdit")
        self.gridLayout_7.addWidget(self.xrms90_lineEdit, 3, 1, 1, 1)
        self.cxy99_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.cxy99_lineEdit.setFont(font)
        self.cxy99_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.cxy99_lineEdit.setReadOnly(True)
        self.cxy99_lineEdit.setObjectName("cxy99_lineEdit")
        self.gridLayout_7.addWidget(self.cxy99_lineEdit, 6, 3, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout_7.addWidget(self.label_31, 7, 2, 1, 1)
        self.urms_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.urms_lineEdit.setFont(font)
        self.urms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.urms_lineEdit.setReadOnly(True)
        self.urms_lineEdit.setObjectName("urms_lineEdit")
        self.gridLayout_7.addWidget(self.urms_lineEdit, 2, 3, 1, 1)
        self.xrms_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.xrms_lineEdit.setFont(font)
        self.xrms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.xrms_lineEdit.setReadOnly(True)
        self.xrms_lineEdit.setObjectName("xrms_lineEdit")
        self.gridLayout_7.addWidget(self.xrms_lineEdit, 2, 1, 1, 1)
        self.vrms_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.vrms_lineEdit.setFont(font)
        self.vrms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vrms_lineEdit.setReadOnly(True)
        self.vrms_lineEdit.setObjectName("vrms_lineEdit")
        self.gridLayout_7.addWidget(self.vrms_lineEdit, 2, 4, 1, 1)
        self.yrms90_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.yrms90_lineEdit.setFont(font)
        self.yrms90_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.yrms90_lineEdit.setReadOnly(True)
        self.yrms90_lineEdit.setObjectName("yrms90_lineEdit")
        self.gridLayout_7.addWidget(self.yrms90_lineEdit, 3, 2, 1, 1)
        self.urms90_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.urms90_lineEdit.setFont(font)
        self.urms90_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.urms90_lineEdit.setReadOnly(True)
        self.urms90_lineEdit.setObjectName("urms90_lineEdit")
        self.gridLayout_7.addWidget(self.urms90_lineEdit, 3, 3, 1, 1)
        self.vrms90_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.vrms90_lineEdit.setFont(font)
        self.vrms90_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vrms90_lineEdit.setReadOnly(True)
        self.vrms90_lineEdit.setObjectName("vrms90_lineEdit")
        self.gridLayout_7.addWidget(self.vrms90_lineEdit, 3, 4, 1, 1)
        self.uc_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.uc_lineEdit.setFont(font)
        self.uc_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.uc_lineEdit.setReadOnly(True)
        self.uc_lineEdit.setObjectName("uc_lineEdit")
        self.gridLayout_7.addWidget(self.uc_lineEdit, 1, 3, 1, 1)
        self.xc_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.xc_lineEdit.setFont(font)
        self.xc_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.xc_lineEdit.setReadOnly(True)
        self.xc_lineEdit.setObjectName("xc_lineEdit")
        self.gridLayout_7.addWidget(self.xc_lineEdit, 1, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_27.setObjectName("label_27")
        self.gridLayout_7.addWidget(self.label_27, 1, 0, 1, 1)
        self.xrms99_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.xrms99_lineEdit.setFont(font)
        self.xrms99_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.xrms99_lineEdit.setReadOnly(True)
        self.xrms99_lineEdit.setObjectName("xrms99_lineEdit")
        self.gridLayout_7.addWidget(self.xrms99_lineEdit, 4, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.gridLayout_7.addWidget(self.label_23, 0, 1, 1, 1)
        self.vrms99_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.vrms99_lineEdit.setFont(font)
        self.vrms99_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vrms99_lineEdit.setReadOnly(True)
        self.vrms99_lineEdit.setObjectName("vrms99_lineEdit")
        self.gridLayout_7.addWidget(self.vrms99_lineEdit, 4, 4, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_29.setObjectName("label_29")
        self.gridLayout_7.addWidget(self.label_29, 6, 0, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_33.setAlignment(QtCore.Qt.AlignCenter)
        self.label_33.setObjectName("label_33")
        self.gridLayout_7.addWidget(self.label_33, 7, 3, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_32.setObjectName("label_32")
        self.gridLayout_7.addWidget(self.label_32, 4, 0, 1, 1)
        self.yrms99_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.yrms99_lineEdit.setFont(font)
        self.yrms99_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.yrms99_lineEdit.setReadOnly(True)
        self.yrms99_lineEdit.setObjectName("yrms99_lineEdit")
        self.gridLayout_7.addWidget(self.yrms99_lineEdit, 4, 2, 1, 1)
        self.cxy_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.cxy_lineEdit.setFont(font)
        self.cxy_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.cxy_lineEdit.setReadOnly(True)
        self.cxy_lineEdit.setObjectName("cxy_lineEdit")
        self.gridLayout_7.addWidget(self.cxy_lineEdit, 6, 1, 1, 1)
        self.cxy90_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.cxy90_lineEdit.setFont(font)
        self.cxy90_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.cxy90_lineEdit.setReadOnly(True)
        self.cxy90_lineEdit.setObjectName("cxy90_lineEdit")
        self.gridLayout_7.addWidget(self.cxy90_lineEdit, 6, 2, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.gridLayout_7.addWidget(self.label_24, 0, 2, 1, 1)
        self.urms99_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.urms99_lineEdit.setFont(font)
        self.urms99_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.urms99_lineEdit.setReadOnly(True)
        self.urms99_lineEdit.setObjectName("urms99_lineEdit")
        self.gridLayout_7.addWidget(self.urms99_lineEdit, 4, 3, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.gridLayout_7.addWidget(self.label_25, 0, 3, 1, 1)
        self.vc_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.vc_lineEdit.setFont(font)
        self.vc_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.vc_lineEdit.setReadOnly(True)
        self.vc_lineEdit.setObjectName("vc_lineEdit")
        self.gridLayout_7.addWidget(self.vc_lineEdit, 1, 4, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_28.setObjectName("label_28")
        self.gridLayout_7.addWidget(self.label_28, 2, 0, 1, 1)
        self.yc_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.yc_lineEdit.setFont(font)
        self.yc_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.yc_lineEdit.setReadOnly(True)
        self.yc_lineEdit.setObjectName("yc_lineEdit")
        self.gridLayout_7.addWidget(self.yc_lineEdit, 1, 2, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.gridLayout_7.addWidget(self.label_26, 0, 4, 1, 1)
        self.yrms_lineEdit = QtWidgets.QLineEdit(self.results_beam_gb)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.yrms_lineEdit.setFont(font)
        self.yrms_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.yrms_lineEdit.setReadOnly(True)
        self.yrms_lineEdit.setObjectName("yrms_lineEdit")
        self.gridLayout_7.addWidget(self.yrms_lineEdit, 2, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.results_beam_gb)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_7.addWidget(self.line_2, 5, 0, 1, 5)
        self.label_34 = QtWidgets.QLabel(self.results_beam_gb)
        self.label_34.setAlignment(QtCore.Qt.AlignCenter)
        self.label_34.setObjectName("label_34")
        self.gridLayout_7.addWidget(self.label_34, 7, 1, 1, 1)
        self.gridLayout_9.addWidget(self.results_beam_gb, 7, 0, 1, 3)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 30))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Config = QtWidgets.QMenu(self.menubar)
        self.menu_Config.setObjectName("menu_Config")
        self.menu_Data = QtWidgets.QMenu(self.menubar)
        self.menu_Data.setToolTipsVisible(True)
        self.menu_Data.setObjectName("menu_Data")
        self.menuDe_vice = QtWidgets.QMenu(self.menubar)
        self.menuDe_vice.setObjectName("menuDe_vice")
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
        self.actionSync = QtWidgets.QAction(MainWindow)
        self.actionSync.setIcon(icon13)
        self.actionSync.setObjectName("actionSync")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(
            QtGui.QPixmap(":/icons/load.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionLoad.setIcon(icon16)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(
            QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionSave.setIcon(icon17)
        self.actionSave.setObjectName("actionSave")
        self.actionLocate_Configuration = QtWidgets.QAction(MainWindow)
        self.actionLocate_Configuration.setObjectName(
            "actionLocate_Configuration")
        self.actionDAT2JSON = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(
            QtGui.QPixmap(":/icons/json.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionDAT2JSON.setIcon(icon18)
        self.actionDAT2JSON.setObjectName("actionDAT2JSON")
        self.actionTo_MicroAmp = QtWidgets.QAction(MainWindow)
        self.actionTo_MicroAmp.setCheckable(True)
        self.actionTo_MicroAmp.setObjectName("actionTo_MicroAmp")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Config.addAction(self.actionReload_Configuration)
        self.menu_Config.addAction(self.actionSave_Configuration)
        self.menu_Config.addAction(self.actionLoad_Configuration)
        self.menu_Config.addAction(self.actionSaveAs_Configuration)
        self.menu_Config.addSeparator()
        self.menu_Config.addAction(self.actionLocate_Configuration)
        self.menu_Data.addAction(self.actionSync)
        self.menu_Data.addAction(self.actionLoad)
        self.menu_Data.addAction(self.actionSave)
        self.menu_Data.addAction(self.actionDAT2JSON)
        self.menu_Data.addAction(self.actionTo_MicroAmp)
        self.menuDe_vice.addAction(self.actionSimulation_Mode)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Config.menuAction())
        self.menubar.addAction(self.menuDe_vice.menuAction())
        self.menubar.addAction(self.menu_Data.menuAction())
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
        self.actionSync.triggered.connect(MainWindow.on_sync_data)
        self.actionLoad.triggered.connect(MainWindow.on_load_data)
        self.actionSave.triggered.connect(MainWindow.on_save_data)
        self.actionLocate_Configuration.triggered.connect(
            MainWindow.on_locate_config)
        self.actionDAT2JSON.triggered.connect(MainWindow.on_dat2json)
        self.plot_data_smoving_btn.clicked.connect(MainWindow.on_plot_raw_data)
        self.plot_data_sbeam_btn.clicked.connect(
            MainWindow.on_plot_with_adjusted_pos)
        self.adv_analysis_chkbox.toggled['bool'].connect(
            MainWindow.on_show_advanced_analysis_panel)
        self.analyze_btn.clicked.connect(MainWindow.on_analyze_data)
        self.legend_btn.clicked['bool'].connect(
            self.matplotlibcurveWidget.setLegendToggle)
        self.init_potentiometer_btn.clicked.connect(
            MainWindow.on_init_potentimeter)
        self.enable_scan_btn.clicked.connect(MainWindow.on_enable_scan)
        self.reset_interlock_btn.clicked.connect(MainWindow.on_reset_interlock)
        self.set_bias_volt_btn.clicked.connect(MainWindow.on_set_bias_volt)
        self.mode_btn.clicked.connect(MainWindow.on_move)
        self.init_motor_pos_btn.clicked.connect(MainWindow.on_init_motor_pos)
        self.set_scan_range_btn.clicked.connect(MainWindow.on_set_scan_range)
        self.data_path_locate_btn.clicked.connect(
            MainWindow.on_locate_data_file)
        self.actionTo_MicroAmp.toggled['bool'].connect(
            MainWindow.on_amp_to_micro_amp)
        self.sync_results_btn.clicked.connect(
            MainWindow.on_sync_results_to_ioc)
        self.reset_xyscale_btn.clicked.connect(MainWindow.on_reset_xyscale)
        self.plot_wpos1_btn.toggled['bool'].connect(MainWindow.on_plot_wpos1)
        self.plot_wpos2_btn.toggled['bool'].connect(MainWindow.on_plot_wpos2)
        self.plot_wpos3_btn.toggled['bool'].connect(MainWindow.on_plot_wpos3)
        self.grid_btn.toggled['bool'].connect(
            self.matplotlibcurveWidget.setFigureGridToggle)
        self.plot_data_subnoise_btn.clicked.connect(
            MainWindow.on_plot_after_subnoise)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.controls_groupBox.setTitle(_translate("MainWindow", "Device"))
        self.run_btn.setText(_translate("MainWindow", "Run"))
        self.advctrl_chkbox.setText(_translate("MainWindow", "Advanced"))
        self.emstop_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Emergency Stop</p></body></html>"))
        self.emstop_btn.setText(_translate("MainWindow", "..."))
        self.label_7.setText(_translate("MainWindow", "Stop Pos (Fork2)"))
        self.label_9.setText(_translate("MainWindow", "Wire Offsets"))
        self.label.setText(_translate("MainWindow", "Select Device"))
        self.label_6.setText(_translate("MainWindow", "Start Pos (Fork2)"))
        self.label_8.setText(_translate("MainWindow", "Stop Pos (Fork2)"))
        self.label_3.setText(_translate("MainWindow", "Type"))
        self.label_2.setText(_translate("MainWindow", "Configuration"))
        self.label_4.setText(_translate("MainWindow", "Coordinate"))
        self.pm_detail_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show device details</p></body></html>"))
        self.pm_detail_btn.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "Start Pos (Fork1)"))
        self.advctrl_groupBox.setTitle(
            _translate("MainWindow", "Advanced Control"))
        self.startpos2_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Start position of fork2</p></body></html>"
            ))
        self.init_potentiometer_btn.setText(
            _translate("MainWindow", "Initialize Potentimeter"))
        self.enable_scan_btn.setText(_translate("MainWindow", "Enable Scan"))
        self.reset_interlock_btn.setText(
            _translate("MainWindow", "Reset Interlock"))
        self.init_motor_pos_btn.setText(
            _translate("MainWindow", "Initialize Motor"))
        self.set_bias_volt_btn.setText(
            _translate("MainWindow", "Set Bias Voltage"))
        self.mode_btn.setText(_translate("MainWindow", "Move"))
        self.label_10.setText(_translate("MainWindow", "Out Limit"))
        self.stoppos2_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Stop position of fork2</p></body></html>"
            ))
        self.outlimit_lineEdit.setText(_translate("MainWindow", "110"))
        self.set_scan_range_btn.setText(
            _translate("MainWindow", "Set Scan Range"))
        self.startpos1_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Start position of fork1</p></body></html>"
            ))
        self.stoppos1_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Stop position of fork1</p></body></html>"
            ))
        self.groupBox.setTitle(_translate("MainWindow", "Data Plot"))
        self.reset_xyscale_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Rest x and y scale</p></body></html>"))
        self.reset_xyscale_btn.setText(_translate("MainWindow", "Scale"))
        self.legend_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show/hide legend</p></body></html>"))
        self.legend_btn.setText(_translate("MainWindow", "Legend"))
        self.grid_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show/hide grid</p></body></html>"))
        self.grid_btn.setText(_translate("MainWindow", "Grid"))
        self.hide_curve2_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Press down to hide curve U</p></body></html>"
            ))
        self.hide_curve2_btn.setText(_translate("MainWindow", "U"))
        self.hide_curve1_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Press down to hide curve V</p></body></html>"
            ))
        self.hide_curve1_btn.setText(_translate("MainWindow", "V"))
        self.hide_curve3_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Press down to hide curve W (X ot Y).</p></body></html>"
            ))
        self.hide_curve3_btn.setText(_translate("MainWindow", "W"))
        self.plot_data_smoving_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Plot raw data (fork frame)</p></body></html>"
            ))
        self.plot_data_smoving_btn.setText(
            _translate("MainWindow", "Original"))
        self.plot_data_sbeam_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Convert position to beam frame</p></body></html>"
            ))
        self.plot_data_sbeam_btn.setText(_translate("MainWindow", "To Beam"))
        self.plot_data_subnoise_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Plot signals after noise substraction</p></body></html>"
            ))
        self.plot_data_subnoise_btn.setText(_translate("MainWindow", "Noise"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Data Analysis"))
        self.adv_analysis_groupBox.setTitle(
            _translate("MainWindow", "Advanced Analysis"))
        self.label_39.setText(_translate("MainWindow", "U-Wire"))
        self.label_40.setText(_translate("MainWindow", "W-Wire"))
        self.label_13.setText(_translate("MainWindow", "V-Wire"))
        self.plot_wpos1_btn.setText(_translate("MainWindow", "..."))
        self.plot_wpos2_btn.setText(_translate("MainWindow", "..."))
        self.plot_wpos3_btn.setText(_translate("MainWindow", "..."))
        self.label_14.setText(_translate("MainWindow", "Projection factor"))
        self.label_15.setText(_translate("MainWindow", "Threshold factor"))
        self.label_16.setText(_translate("MainWindow", "Abs range factor"))
        self.label_38.setText(_translate("MainWindow", "Position Ranges "))
        self.label_35.setText(_translate("MainWindow", "Data Path"))
        self.data_path_locate_btn.setText(_translate("MainWindow", "Locate"))
        self.analyze_btn.setText(_translate("MainWindow", "Analyze"))
        self.adv_analysis_chkbox.setText(_translate("MainWindow", "Advanced"))
        self.sync_results_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Push back analyzed results to device (XCEN, YCEN, XRMS, YRMS and CXY).</p></body></html>"
            ))
        self.sync_results_btn.setText(_translate("MainWindow", "..."))
        self.label_11.setText(_translate("MainWindow", "Results"))
        self.fontsize_inc_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Increase fontsize (CTRL + 0 to restore)</p></body></html>"
            ))
        self.fontsize_inc_btn.setText(_translate("MainWindow", "..."))
        self.fontsize_dec_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Decrease fontsize (CTRL + 0 to restore)</p></body></html>"
            ))
        self.fontsize_dec_btn.setText(_translate("MainWindow", "..."))
        self.results_wires_gb.setTitle(_translate("MainWindow", "Wires"))
        self.label_17.setText(_translate("MainWindow", "U"))
        self.label_18.setText(_translate("MainWindow", "V"))
        self.label_19.setText(_translate("MainWindow", "W"))
        self.label_20.setText(_translate("MainWindow", "Sum"))
        self.label_21.setText(_translate("MainWindow", "Center"))
        self.label_22.setText(_translate("MainWindow", "RMS"))
        self.results_beam_gb.setTitle(
            _translate("MainWindow", "Beam Parameters"))
        self.label_30.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>σ<span style=\" vertical-align:super;\">90%</span></p></body></html>"
            ))
        self.label_31.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>ρ<span style=\" vertical-align:sub;\">xy</span><span style=\" vertical-align:super;\">90%</span></p></body></html>"
            ))
        self.label_27.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>S<span style=\" vertical-align:sub;\">0</span></p></body></html>"
            ))
        self.label_23.setText(_translate("MainWindow", "X"))
        self.label_29.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>ρ<span style=\" vertical-align:sub;\">xy</span></p></body></html>"
            ))
        self.label_33.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>ρ<span style=\" vertical-align:sub;\">xy</span><span style=\" vertical-align:super;\">99%</span></p></body></html>"
            ))
        self.label_32.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>σ<span style=\" vertical-align:super;\">99%</span></p></body></html>"
            ))
        self.label_24.setText(_translate("MainWindow", "Y"))
        self.label_25.setText(_translate("MainWindow", "U"))
        self.label_28.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>&sigma;</p></body></html>"))
        self.label_26.setText(_translate("MainWindow", "V"))
        self.label_34.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>ρ<span style=\" vertical-align:sub;\">xy</span><span style=\" vertical-align:super;\">100%</span></p></body></html>"
            ))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Config.setTitle(_translate("MainWindow", "Configuration"))
        self.menu_Data.setTitle(_translate("MainWindow", "&Data"))
        self.menuDe_vice.setTitle(_translate("MainWindow", "De&vice"))
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
        self.actionSimulation_Mode.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+M"))
        self.actionSync.setText(_translate("MainWindow", "Sync"))
        self.actionSync.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Retrieve data from controls network</p></body></html>"
            ))
        self.actionSync.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionLoad.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Load data from file</p></body></html>"))
        self.actionLoad.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Save data to file</p></body></html>"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionLocate_Configuration.setText(
            _translate("MainWindow", "Locate"))
        self.actionDAT2JSON.setText(_translate("MainWindow", "Converter"))
        self.actionDAT2JSON.setToolTip(
            _translate("MainWindow",
                       "Convert .dat file to .json formatted data file."))
        self.actionDAT2JSON.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+C"))
        self.actionTo_MicroAmp.setText(_translate("MainWindow", "To MicroAmp"))
        self.actionTo_MicroAmp.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Convert signal from A to μA</p></body></html>"
            ))
        self.actionTo_MicroAmp.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+A"))


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
