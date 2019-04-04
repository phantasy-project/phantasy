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
        MainWindow.resize(1920, 1440)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setMinimumSize(QtCore.QSize(200, 0))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.scan_groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.scan_groupBox.sizePolicy().hasHeightForWidth())
        self.scan_groupBox.setSizePolicy(sizePolicy)
        self.scan_groupBox.setStyleSheet(
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
        self.scan_groupBox.setObjectName("scan_groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scan_groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(self.scan_groupBox)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.alter_elem_lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_elem_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_elem_lineEdit.setSizePolicy(sizePolicy)
        self.alter_elem_lineEdit.setText("")
        self.alter_elem_lineEdit.setReadOnly(True)
        self.alter_elem_lineEdit.setObjectName("alter_elem_lineEdit")
        self.gridLayout_2.addWidget(self.alter_elem_lineEdit, 0, 1, 1, 3)
        self.lower_limit_lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lower_limit_lineEdit.sizePolicy().hasHeightForWidth())
        self.lower_limit_lineEdit.setSizePolicy(sizePolicy)
        self.lower_limit_lineEdit.setPlaceholderText("")
        self.lower_limit_lineEdit.setObjectName("lower_limit_lineEdit")
        self.gridLayout_2.addWidget(self.lower_limit_lineEdit, 1, 1, 1, 1)
        self.select_monitor_elem_btn = QtWidgets.QPushButton(self.widget)
        self.select_monitor_elem_btn.setAutoDefault(True)
        self.select_monitor_elem_btn.setObjectName("select_monitor_elem_btn")
        self.gridLayout_2.addWidget(self.select_monitor_elem_btn, 2, 6, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.auto_show_extra_chkbox = QtWidgets.QCheckBox(self.widget)
        self.auto_show_extra_chkbox.setObjectName("auto_show_extra_chkbox")
        self.horizontalLayout_5.addWidget(self.auto_show_extra_chkbox)
        self.show_extra_monitors_btn = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_extra_monitors_btn.sizePolicy().hasHeightForWidth())
        self.show_extra_monitors_btn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/show.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.show_extra_monitors_btn.setIcon(icon1)
        self.show_extra_monitors_btn.setIconSize(QtCore.QSize(24, 24))
        self.show_extra_monitors_btn.setAutoRaise(True)
        self.show_extra_monitors_btn.setObjectName("show_extra_monitors_btn")
        self.horizontalLayout_5.addWidget(self.show_extra_monitors_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 3, 3, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.enable_arbitary_array_chkbox = QtWidgets.QCheckBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.enable_arbitary_array_chkbox.sizePolicy().hasHeightForWidth())
        self.enable_arbitary_array_chkbox.setSizePolicy(sizePolicy)
        self.enable_arbitary_array_chkbox.setText("")
        self.enable_arbitary_array_chkbox.setObjectName(
            "enable_arbitary_array_chkbox")
        self.horizontalLayout_6.addWidget(self.enable_arbitary_array_chkbox)
        self.alter_array_btn = QtWidgets.QPushButton(self.widget)
        self.alter_array_btn.setObjectName("alter_array_btn")
        self.horizontalLayout_6.addWidget(self.alter_array_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 1, 6, 1, 1)
        self.upper_limit_lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.upper_limit_lineEdit.sizePolicy().hasHeightForWidth())
        self.upper_limit_lineEdit.setSizePolicy(sizePolicy)
        self.upper_limit_lineEdit.setPlaceholderText("")
        self.upper_limit_lineEdit.setObjectName("upper_limit_lineEdit")
        self.gridLayout_2.addWidget(self.upper_limit_lineEdit, 1, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.select_alter_elem_btn = QtWidgets.QPushButton(self.widget)
        self.select_alter_elem_btn.setAutoDefault(True)
        self.select_alter_elem_btn.setObjectName("select_alter_elem_btn")
        self.gridLayout_2.addWidget(self.select_alter_elem_btn, 0, 6, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.extra_monitors_counter_lbl = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.extra_monitors_counter_lbl.sizePolicy().hasHeightForWidth())
        self.extra_monitors_counter_lbl.setSizePolicy(sizePolicy)
        self.extra_monitors_counter_lbl.setObjectName(
            "extra_monitors_counter_lbl")
        self.gridLayout_2.addWidget(self.extra_monitors_counter_lbl, 3, 1, 1,
                                    2)
        self.monitor_elem_lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.monitor_elem_lineEdit.sizePolicy().hasHeightForWidth())
        self.monitor_elem_lineEdit.setSizePolicy(sizePolicy)
        self.monitor_elem_lineEdit.setText("")
        self.monitor_elem_lineEdit.setReadOnly(True)
        self.monitor_elem_lineEdit.setObjectName("monitor_elem_lineEdit")
        self.gridLayout_2.addWidget(self.monitor_elem_lineEdit, 2, 1, 1, 3)
        self.label_11 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 1, 2, 1, 1)
        self.select_more_monitor_elems_btn = QtWidgets.QPushButton(self.widget)
        self.select_more_monitor_elems_btn.setAutoDefault(True)
        self.select_more_monitor_elems_btn.setObjectName(
            "select_more_monitor_elems_btn")
        self.gridLayout_2.addWidget(self.select_more_monitor_elems_btn, 3, 6,
                                    1, 1)
        self.verticalLayout_3.addWidget(self.widget)
        self.line_4 = QtWidgets.QFrame(self.scan_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_3.addWidget(self.line_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_12 = QtWidgets.QLabel(self.scan_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.inc_fontsize_tbtn = QtWidgets.QToolButton(self.scan_groupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/increase-font.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.inc_fontsize_tbtn.setIcon(icon2)
        self.inc_fontsize_tbtn.setAutoRaise(True)
        self.inc_fontsize_tbtn.setObjectName("inc_fontsize_tbtn")
        self.horizontalLayout_2.addWidget(self.inc_fontsize_tbtn)
        self.dec_fontsize_tbtn = QtWidgets.QToolButton(self.scan_groupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/decrease-font.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.dec_fontsize_tbtn.setIcon(icon3)
        self.dec_fontsize_tbtn.setAutoRaise(True)
        self.dec_fontsize_tbtn.setObjectName("dec_fontsize_tbtn")
        self.horizontalLayout_2.addWidget(self.dec_fontsize_tbtn)
        self.clear_log_tbtn = QtWidgets.QToolButton(self.scan_groupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/clean.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.clear_log_tbtn.setIcon(icon4)
        self.clear_log_tbtn.setAutoRaise(True)
        self.clear_log_tbtn.setObjectName("clear_log_tbtn")
        self.horizontalLayout_2.addWidget(self.clear_log_tbtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.scan_log_textEdit = QtWidgets.QTextEdit(self.scan_groupBox)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.scan_log_textEdit.setFont(font)
        self.scan_log_textEdit.setReadOnly(True)
        self.scan_log_textEdit.setObjectName("scan_log_textEdit")
        self.verticalLayout_2.addWidget(self.scan_log_textEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.daq_groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.daq_groupBox.sizePolicy().hasHeightForWidth())
        self.daq_groupBox.setSizePolicy(sizePolicy)
        self.daq_groupBox.setStyleSheet(
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
        self.daq_groupBox.setObjectName("daq_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.daq_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.niter_label = QtWidgets.QLabel(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.niter_label.sizePolicy().hasHeightForWidth())
        self.niter_label.setSizePolicy(sizePolicy)
        self.niter_label.setObjectName("niter_label")
        self.gridLayout.addWidget(self.niter_label, 0, 0, 1, 1)
        self.niter_spinBox = QtWidgets.QSpinBox(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.niter_spinBox.sizePolicy().hasHeightForWidth())
        self.niter_spinBox.setSizePolicy(sizePolicy)
        self.niter_spinBox.setMinimum(1)
        self.niter_spinBox.setMaximum(9999)
        self.niter_spinBox.setProperty("value", 10)
        self.niter_spinBox.setObjectName("niter_spinBox")
        self.gridLayout.addWidget(self.niter_spinBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.nshot_spinBox = QtWidgets.QSpinBox(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.nshot_spinBox.sizePolicy().hasHeightForWidth())
        self.nshot_spinBox.setSizePolicy(sizePolicy)
        self.nshot_spinBox.setMinimum(1)
        self.nshot_spinBox.setMaximum(9999)
        self.nshot_spinBox.setProperty("value", 5)
        self.nshot_spinBox.setObjectName("nshot_spinBox")
        self.gridLayout.addWidget(self.nshot_spinBox, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.waitsec_dSpinBox = QtWidgets.QDoubleSpinBox(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.waitsec_dSpinBox.sizePolicy().hasHeightForWidth())
        self.waitsec_dSpinBox.setSizePolicy(sizePolicy)
        self.waitsec_dSpinBox.setSingleStep(0.5)
        self.waitsec_dSpinBox.setProperty("value", 2.0)
        self.waitsec_dSpinBox.setObjectName("waitsec_dSpinBox")
        self.gridLayout.addWidget(self.waitsec_dSpinBox, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.scanrate_dSpinBox = QtWidgets.QDoubleSpinBox(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scanrate_dSpinBox.sizePolicy().hasHeightForWidth())
        self.scanrate_dSpinBox.setSizePolicy(sizePolicy)
        self.scanrate_dSpinBox.setDecimals(1)
        self.scanrate_dSpinBox.setMinimum(0.1)
        self.scanrate_dSpinBox.setMaximum(20.0)
        self.scanrate_dSpinBox.setProperty("value", 1.0)
        self.scanrate_dSpinBox.setObjectName("scanrate_dSpinBox")
        self.gridLayout.addWidget(self.scanrate_dSpinBox, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.daq_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 2, 1, 1)
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
        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mps_status_btn = QtWidgets.QToolButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mps_status_btn.sizePolicy().hasHeightForWidth())
        self.mps_status_btn.setSizePolicy(sizePolicy)
        self.mps_status_btn.setMinimumSize(QtCore.QSize(36, 36))
        self.mps_status_btn.setMaximumSize(QtCore.QSize(36, 36))
        self.mps_status_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/mps_skipped.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.mps_status_btn.setIcon(icon5)
        self.mps_status_btn.setIconSize(QtCore.QSize(36, 36))
        self.mps_status_btn.setAutoRaise(True)
        self.mps_status_btn.setObjectName("mps_status_btn")
        self.horizontalLayout_3.addWidget(self.mps_status_btn)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.line_2 = QtWidgets.QFrame(self.daq_groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        self.start_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        self.start_btn.setAutoDefault(True)
        self.start_btn.setObjectName("start_btn")
        self.horizontalLayout_3.addWidget(self.start_btn)
        self.pause_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pause_btn.sizePolicy().hasHeightForWidth())
        self.pause_btn.setSizePolicy(sizePolicy)
        self.pause_btn.setAutoDefault(True)
        self.pause_btn.setObjectName("pause_btn")
        self.horizontalLayout_3.addWidget(self.pause_btn)
        self.stop_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        self.stop_btn.setAutoDefault(True)
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout_3.addWidget(self.stop_btn)
        self.retake_btn = QtWidgets.QPushButton(self.daq_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.retake_btn.sizePolicy().hasHeightForWidth())
        self.retake_btn.setSizePolicy(sizePolicy)
        self.retake_btn.setAutoDefault(True)
        self.retake_btn.setObjectName("retake_btn")
        self.horizontalLayout_3.addWidget(self.retake_btn)
        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 3)
        self.plot_groupBox = QtWidgets.QGroupBox(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_groupBox.sizePolicy().hasHeightForWidth())
        self.plot_groupBox.setSizePolicy(sizePolicy)
        self.plot_groupBox.setToolTip("")
        self.plot_groupBox.setStyleSheet(
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
        self.plot_groupBox.setObjectName("plot_groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.plot_groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scan_plot_widget = MatplotlibErrorbarWidget(self.plot_groupBox)
        self.scan_plot_widget.setFigureMTicksToggle(True)
        self.scan_plot_widget.setFigureGridToggle(True)
        self.scan_plot_widget.setProperty("figureBackgroundColor",
                                          QtGui.QColor(240, 240, 240))
        self.scan_plot_widget.setFigureAutoScale(True)
        self.scan_plot_widget.setObjectName("scan_plot_widget")
        self.verticalLayout.addWidget(self.scan_plot_widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.autoscale_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/auto-scale.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.autoscale_tbtn.setIcon(icon6)
        self.autoscale_tbtn.setCheckable(True)
        self.autoscale_tbtn.setChecked(False)
        self.autoscale_tbtn.setAutoRaise(True)
        self.autoscale_tbtn.setObjectName("autoscale_tbtn")
        self.horizontalLayout.addWidget(self.autoscale_tbtn)
        self.save_data_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/save_figure.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.save_data_tbtn.setIcon(icon7)
        self.save_data_tbtn.setAutoRaise(True)
        self.save_data_tbtn.setObjectName("save_data_tbtn")
        self.horizontalLayout.addWidget(self.save_data_tbtn)
        self.auto_title_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/title.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.auto_title_tbtn.setIcon(icon8)
        self.auto_title_tbtn.setAutoRaise(True)
        self.auto_title_tbtn.setObjectName("auto_title_tbtn")
        self.horizontalLayout.addWidget(self.auto_title_tbtn)
        self.auto_labels_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/xylabel.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.auto_labels_tbtn.setIcon(icon9)
        self.auto_labels_tbtn.setAutoRaise(True)
        self.auto_labels_tbtn.setObjectName("auto_labels_tbtn")
        self.horizontalLayout.addWidget(self.auto_labels_tbtn)
        self.moveto_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/moveto.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.moveto_tbtn.setIcon(icon10)
        self.moveto_tbtn.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.moveto_tbtn.setAutoRaise(True)
        self.moveto_tbtn.setArrowType(QtCore.Qt.NoArrow)
        self.moveto_tbtn.setObjectName("moveto_tbtn")
        self.horizontalLayout.addWidget(self.moveto_tbtn)
        self.set_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(
            QtGui.QPixmap(":/icons/set.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.set_tbtn.setIcon(icon11)
        self.set_tbtn.setAutoRaise(True)
        self.set_tbtn.setObjectName("set_tbtn")
        self.horizontalLayout.addWidget(self.set_tbtn)
        self.view_selected_pts_tbtn = QtWidgets.QToolButton(self.plot_groupBox)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(
            QtGui.QPixmap(":/icons/points.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.view_selected_pts_tbtn.setIcon(icon12)
        self.view_selected_pts_tbtn.setPopupMode(
            QtWidgets.QToolButton.MenuButtonPopup)
        self.view_selected_pts_tbtn.setAutoRaise(True)
        self.view_selected_pts_tbtn.setObjectName("view_selected_pts_tbtn")
        self.horizontalLayout.addWidget(self.view_selected_pts_tbtn)
        self.line_3 = QtWidgets.QFrame(self.plot_groupBox)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.label_13 = QtWidgets.QLabel(self.plot_groupBox)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.xdata_cbb = QtWidgets.QComboBox(self.plot_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.xdata_cbb.sizePolicy().hasHeightForWidth())
        self.xdata_cbb.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.xdata_cbb.setFont(font)
        self.xdata_cbb.setObjectName("xdata_cbb")
        self.horizontalLayout.addWidget(self.xdata_cbb)
        self.label_14 = QtWidgets.QLabel(self.plot_groupBox)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout.addWidget(self.label_14)
        self.ydata_cbb = QtWidgets.QComboBox(self.plot_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ydata_cbb.sizePolicy().hasHeightForWidth())
        self.ydata_cbb.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.ydata_cbb.setFont(font)
        self.ydata_cbb.setObjectName("ydata_cbb")
        self.horizontalLayout.addWidget(self.ydata_cbb)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menu_Scan = QtWidgets.QMenu(self.menubar)
        self.menu_Scan.setObjectName("menu_Scan")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon13)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(
            QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionContents.setIcon(icon14)
        self.actionContents.setObjectName("actionContents")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon15)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon16)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionQuad_Scan = QtWidgets.QAction(MainWindow)
        self.actionQuad_Scan.setObjectName("actionQuad_Scan")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(
            QtGui.QPixmap(":/icons/load_lattice.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon17)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.actionMPS_guardian = QtWidgets.QAction(MainWindow)
        self.actionMPS_guardian.setCheckable(True)
        self.actionMPS_guardian.setObjectName("actionMPS_guardian")
        self.actionSave_Task = QtWidgets.QAction(MainWindow)
        self.actionSave_Task.setObjectName("actionSave_Task")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIcon(icon7)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad_Task = QtWidgets.QAction(MainWindow)
        self.actionLoad_Task.setObjectName("actionLoad_Task")
        self.menu_File.addAction(self.actionSave)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuTools.addAction(self.actionQuad_Scan)
        self.menuTools.addAction(self.actionLoad_Lattice)
        self.menuTools.addAction(self.actionMPS_guardian)
        self.menu_Scan.addAction(self.actionSave_Task)
        self.menu_Scan.addAction(self.actionLoad_Task)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Scan.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionQuad_Scan.triggered.connect(MainWindow.onQuadScanAction)
        self.actionContents.triggered.connect(MainWindow.onHelp)
        self.actionLoad_Lattice.triggered.connect(
            MainWindow.onLoadLatticeAction)
        self.actionMPS_guardian.toggled['bool'].connect(
            MainWindow.onEnableMPSGuardian)
        self.mps_status_btn.clicked.connect(MainWindow.on_config_mps)
        self.autoscale_tbtn.toggled['bool'].connect(
            self.scan_plot_widget.setFigureAutoScale)
        self.scan_plot_widget.autoScaleOnUpdated['bool'].connect(
            self.autoscale_tbtn.setChecked)
        self.actionSave.triggered.connect(MainWindow.on_save_data)
        self.actionSave_Task.triggered.connect(MainWindow.on_save_task)
        self.actionLoad_Task.triggered.connect(MainWindow.on_load_task)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.alter_elem_lineEdit,
                               self.select_alter_elem_btn)
        MainWindow.setTabOrder(self.select_alter_elem_btn,
                               self.lower_limit_lineEdit)
        MainWindow.setTabOrder(self.lower_limit_lineEdit,
                               self.upper_limit_lineEdit)
        MainWindow.setTabOrder(self.upper_limit_lineEdit,
                               self.enable_arbitary_array_chkbox)
        MainWindow.setTabOrder(self.enable_arbitary_array_chkbox,
                               self.alter_array_btn)
        MainWindow.setTabOrder(self.alter_array_btn,
                               self.monitor_elem_lineEdit)
        MainWindow.setTabOrder(self.monitor_elem_lineEdit,
                               self.select_monitor_elem_btn)
        MainWindow.setTabOrder(self.select_monitor_elem_btn,
                               self.show_extra_monitors_btn)
        MainWindow.setTabOrder(self.show_extra_monitors_btn,
                               self.inc_fontsize_tbtn)
        MainWindow.setTabOrder(self.inc_fontsize_tbtn, self.dec_fontsize_tbtn)
        MainWindow.setTabOrder(self.dec_fontsize_tbtn, self.clear_log_tbtn)
        MainWindow.setTabOrder(self.clear_log_tbtn, self.scan_log_textEdit)
        MainWindow.setTabOrder(self.scan_log_textEdit, self.niter_spinBox)
        MainWindow.setTabOrder(self.niter_spinBox, self.nshot_spinBox)
        MainWindow.setTabOrder(self.nshot_spinBox, self.waitsec_dSpinBox)
        MainWindow.setTabOrder(self.waitsec_dSpinBox, self.scanrate_dSpinBox)
        MainWindow.setTabOrder(self.scanrate_dSpinBox, self.start_btn)
        MainWindow.setTabOrder(self.start_btn, self.pause_btn)
        MainWindow.setTabOrder(self.pause_btn, self.stop_btn)
        MainWindow.setTabOrder(self.stop_btn, self.retake_btn)
        MainWindow.setTabOrder(self.retake_btn, self.save_data_tbtn)
        MainWindow.setTabOrder(self.save_data_tbtn, self.auto_title_tbtn)
        MainWindow.setTabOrder(self.auto_title_tbtn, self.auto_labels_tbtn)
        MainWindow.setTabOrder(self.auto_labels_tbtn, self.moveto_tbtn)
        MainWindow.setTabOrder(self.moveto_tbtn, self.set_tbtn)
        MainWindow.setTabOrder(self.set_tbtn, self.view_selected_pts_tbtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.scan_groupBox.setTitle(
            _translate("MainWindow", "Scan Configuration"))
        self.label_8.setText(_translate("MainWindow", "Alter Element"))
        self.alter_elem_lineEdit.setPlaceholderText(
            _translate("MainWindow", "Click \'Select\' to set element"))
        self.lower_limit_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Start value of scan range</p></body></html>"
            ))
        self.lower_limit_lineEdit.setText(_translate("MainWindow", "0"))
        self.select_monitor_elem_btn.setText(
            _translate("MainWindow", "Select"))
        self.auto_show_extra_chkbox.setToolTip(
            _translate("MainWindow",
                       "Show Extra Monitors After Each Selection"))
        self.auto_show_extra_chkbox.setText(_translate("MainWindow", "Auto"))
        self.show_extra_monitors_btn.setText(_translate("MainWindow", "Show"))
        self.enable_arbitary_array_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Check to enable altering with arbitary array</p></body></html>"
            ))
        self.alter_array_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Set alter range by array</p></body></html>"
            ))
        self.alter_array_btn.setText(_translate("MainWindow", "Array"))
        self.upper_limit_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Stop value of scan range</p></body></html>"
            ))
        self.upper_limit_lineEdit.setText(_translate("MainWindow", "1"))
        self.label_9.setText(_translate("MainWindow", "Alter Range"))
        self.select_alter_elem_btn.setText(_translate("MainWindow", "Select"))
        self.label.setText(_translate("MainWindow", "Extra"))
        self.extra_monitors_counter_lbl.setText(
            _translate("MainWindow", "Monitors (0)"))
        self.monitor_elem_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Variables to monitor</p></body></html>")
        )
        self.monitor_elem_lineEdit.setPlaceholderText(
            _translate("MainWindow", "Click \'Select\' to set element"))
        self.label_11.setText(_translate("MainWindow", "Monitor"))
        self.label_10.setText(_translate("MainWindow", "To"))
        self.select_more_monitor_elems_btn.setText(
            _translate("MainWindow", "More"))
        self.label_12.setText(_translate("MainWindow", "Event Log"))
        self.inc_fontsize_tbtn.setText(_translate("MainWindow", "FS+"))
        self.dec_fontsize_tbtn.setText(_translate("MainWindow", "FS-"))
        self.clear_log_tbtn.setText(_translate("MainWindow", "Clear"))
        self.daq_groupBox.setTitle(
            _translate("MainWindow", "DAQ Configuration"))
        self.niter_label.setText(_translate("MainWindow", "Iteration Number"))
        self.niter_spinBox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total number of points to scan</p></body></html>"
            ))
        self.label_2.setText(_translate("MainWindow", "Shot Number"))
        self.nshot_spinBox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Number of records to be taken at each scan point</p></body></html>"
            ))
        self.label_5.setText(_translate("MainWindow", "per iteration"))
        self.label_3.setText(_translate("MainWindow", "Additional Wait Time"))
        self.waitsec_dSpinBox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Additional wait time after set new scan point</p></body></html>"
            ))
        self.label_4.setText(_translate("MainWindow", "Second"))
        self.label_7.setText(_translate("MainWindow", "Scan DAQ Rate"))
        self.scanrate_dSpinBox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Record number to be taken within one second.</p></body></html>"
            ))
        self.label_6.setText(_translate("MainWindow", "Hz"))
        self.mps_status_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>MPS guardian is not enabled</p></body></html>"
            ))
        self.start_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Start scan task</p></body></html>"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.pause_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Pause scan task, click again to resume</p></body></html>"
            ))
        self.pause_btn.setText(_translate("MainWindow", "Pause"))
        self.stop_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Stop current running scan task</p></body></html>"
            ))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.retake_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Re-do scan at selected points</p></body></html>"
            ))
        self.retake_btn.setText(_translate("MainWindow", "Retake"))
        self.plot_groupBox.setTitle(
            _translate("MainWindow", "Correlation Plot"))
        self.autoscale_tbtn.setText(_translate("MainWindow", "..."))
        self.save_data_tbtn.setText(_translate("MainWindow", "save_data"))
        self.auto_title_tbtn.setText(_translate("MainWindow", "auto_title"))
        self.auto_labels_tbtn.setText(_translate("MainWindow", "auto_labels"))
        self.moveto_tbtn.setText(_translate("MainWindow", "moveto"))
        self.set_tbtn.setText(_translate("MainWindow", "set"))
        self.view_selected_pts_tbtn.setText(_translate("MainWindow", "points"))
        self.label_13.setText(_translate("MainWindow", "X-Axis"))
        self.label_14.setText(_translate("MainWindow", "Y-Axis"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.menu_Scan.setTitle(_translate("MainWindow", "&Scan"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionQuad_Scan.setText(
            _translate("MainWindow", "Quad Scan Analysis"))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))
        self.actionMPS_guardian.setText(
            _translate("MainWindow", "MPS Guardian"))
        self.actionMPS_guardian.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Check to enable MPS Guardian</p></body></html>"
            ))
        self.actionMPS_guardian.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+M"))
        self.actionSave_Task.setText(_translate("MainWindow", "Save Task"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionLoad_Task.setText(_translate("MainWindow", "Load Task"))


from mpl4qt.widgets.mplerrorbarwidget import MatplotlibErrorbarWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
