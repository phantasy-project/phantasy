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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setContentsMargins(10, -1, -1, -1)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ems_names_cbb = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ems_names_cbb.sizePolicy().hasHeightForWidth())
        self.ems_names_cbb.setSizePolicy(sizePolicy)
        self.ems_names_cbb.setStyleSheet("QComboBox {\n"
                                         "    font-family: monospace;\n"
                                         "}")
        self.ems_names_cbb.setObjectName("ems_names_cbb")
        self.horizontalLayout.addWidget(self.ems_names_cbb)
        self.info_lbl = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.info_lbl.sizePolicy().hasHeightForWidth())
        self.info_lbl.setSizePolicy(sizePolicy)
        self.info_lbl.setStyleSheet("")
        self.info_lbl.setScaledContents(False)
        self.info_lbl.setObjectName("info_lbl")
        self.horizontalLayout.addWidget(self.info_lbl)
        self.ems_detail_btn = QtWidgets.QToolButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ems_detail_btn.sizePolicy().hasHeightForWidth())
        self.ems_detail_btn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/view-details.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.ems_detail_btn.setIcon(icon)
        self.ems_detail_btn.setIconSize(QtCore.QSize(20, 20))
        self.ems_detail_btn.setAutoRaise(True)
        self.ems_detail_btn.setObjectName("ems_detail_btn")
        self.horizontalLayout.addWidget(self.ems_detail_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout.addWidget(self.label_14)
        self.ems_orientation_cbb = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ems_orientation_cbb.sizePolicy().hasHeightForWidth())
        self.ems_orientation_cbb.setSizePolicy(sizePolicy)
        self.ems_orientation_cbb.setStyleSheet("QComboBox {\n"
                                               "    font-family: monospace;\n"
                                               "}")
        self.ems_orientation_cbb.setObjectName("ems_orientation_cbb")
        self.ems_orientation_cbb.addItem("")
        self.ems_orientation_cbb.addItem("")
        self.horizontalLayout.addWidget(self.ems_orientation_cbb)
        self.run_btn = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
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
        self.horizontalLayout.addWidget(self.run_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.groupBox_2)
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
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                  | QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.splitter_3 = QtWidgets.QSplitter(self.groupBox_2)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.gridWidget = QtWidgets.QWidget(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gridWidget.sizePolicy().hasHeightForWidth())
        self.gridWidget.setSizePolicy(sizePolicy)
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setContentsMargins(8, 0, 0, 0)
        self.gridLayout_4.setHorizontalSpacing(10)
        self.gridLayout_4.setVerticalSpacing(12)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_16 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 7, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(13)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.length_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length_lineEdit.sizePolicy().hasHeightForWidth())
        self.length_lineEdit.setSizePolicy(sizePolicy)
        self.length_lineEdit.setReadOnly(True)
        self.length_lineEdit.setObjectName("length_lineEdit")
        self.horizontalLayout_4.addWidget(self.length_lineEdit)
        self.label_13 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.length1_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length1_lineEdit.sizePolicy().hasHeightForWidth())
        self.length1_lineEdit.setSizePolicy(sizePolicy)
        self.length1_lineEdit.setReadOnly(True)
        self.length1_lineEdit.setObjectName("length1_lineEdit")
        self.horizontalLayout_4.addWidget(self.length1_lineEdit)
        self.label_12 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.length2_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length2_lineEdit.sizePolicy().hasHeightForWidth())
        self.length2_lineEdit.setSizePolicy(sizePolicy)
        self.length2_lineEdit.setReadOnly(True)
        self.length2_lineEdit.setObjectName("length2_lineEdit")
        self.horizontalLayout_4.addWidget(self.length2_lineEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 1, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_6.setSpacing(13)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_20 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_6.addWidget(self.label_20)
        self.volt_begin_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_begin_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_begin_dsbox.setSizePolicy(sizePolicy)
        self.volt_begin_dsbox.setMinimum(-9999.0)
        self.volt_begin_dsbox.setMaximum(9999.0)
        self.volt_begin_dsbox.setObjectName("volt_begin_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_begin_dsbox)
        self.label_21 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_6.addWidget(self.label_21)
        self.volt_end_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_end_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_end_dsbox.setSizePolicy(sizePolicy)
        self.volt_end_dsbox.setMinimum(-9999.0)
        self.volt_end_dsbox.setMaximum(9999.0)
        self.volt_end_dsbox.setObjectName("volt_end_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_end_dsbox)
        self.label_22 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_6.addWidget(self.label_22)
        self.volt_step_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_step_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_step_dsbox.setSizePolicy(sizePolicy)
        self.volt_step_dsbox.setMinimum(-9999.0)
        self.volt_step_dsbox.setMaximum(9999.0)
        self.volt_step_dsbox.setObjectName("volt_step_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_step_dsbox)
        self.label_23 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_6.addWidget(self.label_23)
        self.volt_settling_time_dsbox = QtWidgets.QDoubleSpinBox(
            self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_settling_time_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_settling_time_dsbox.setSizePolicy(sizePolicy)
        self.volt_settling_time_dsbox.setDecimals(3)
        self.volt_settling_time_dsbox.setSingleStep(0.01)
        self.volt_settling_time_dsbox.setObjectName("volt_settling_time_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_settling_time_dsbox)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 7, 1, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(13)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.slit_thickness_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_thickness_lineEdit.sizePolicy().hasHeightForWidth())
        self.slit_thickness_lineEdit.setSizePolicy(sizePolicy)
        self.slit_thickness_lineEdit.setReadOnly(True)
        self.slit_thickness_lineEdit.setObjectName("slit_thickness_lineEdit")
        self.horizontalLayout_3.addWidget(self.slit_thickness_lineEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 4, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 5, 0, 1, 3)
        self.label_15 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(13)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_17 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_5.addWidget(self.label_17)
        self.pos_begin_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_begin_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_begin_dsbox.setSizePolicy(sizePolicy)
        self.pos_begin_dsbox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.pos_begin_dsbox.setMinimum(-9999.0)
        self.pos_begin_dsbox.setMaximum(9999.0)
        self.pos_begin_dsbox.setObjectName("pos_begin_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_begin_dsbox)
        self.label_18 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_5.addWidget(self.label_18)
        self.pos_end_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_end_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_end_dsbox.setSizePolicy(sizePolicy)
        self.pos_end_dsbox.setMinimum(-9999.0)
        self.pos_end_dsbox.setMaximum(9999.0)
        self.pos_end_dsbox.setObjectName("pos_end_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_end_dsbox)
        self.label_19 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_5.addWidget(self.label_19)
        self.pos_step_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_step_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_step_dsbox.setSizePolicy(sizePolicy)
        self.pos_step_dsbox.setSuffix("")
        self.pos_step_dsbox.setMinimum(-9999.0)
        self.pos_step_dsbox.setMaximum(9999.0)
        self.pos_step_dsbox.setObjectName("pos_step_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_step_dsbox)
        self.label_5 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.pos_settling_time_dsbox = QtWidgets.QDoubleSpinBox(
            self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_settling_time_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_settling_time_dsbox.setSizePolicy(sizePolicy)
        self.pos_settling_time_dsbox.setDecimals(3)
        self.pos_settling_time_dsbox.setSingleStep(0.01)
        self.pos_settling_time_dsbox.setObjectName("pos_settling_time_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_settling_time_dsbox)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 6, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_2.setSpacing(13)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.slit_width_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_width_lineEdit.sizePolicy().hasHeightForWidth())
        self.slit_width_lineEdit.setSizePolicy(sizePolicy)
        self.slit_width_lineEdit.setReadOnly(True)
        self.slit_width_lineEdit.setObjectName("slit_width_lineEdit")
        self.horizontalLayout_2.addWidget(self.slit_width_lineEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_7.setSpacing(13)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.gap_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gap_lineEdit.sizePolicy().hasHeightForWidth())
        self.gap_lineEdit.setSizePolicy(sizePolicy)
        self.gap_lineEdit.setReadOnly(True)
        self.gap_lineEdit.setObjectName("gap_lineEdit")
        self.horizontalLayout_7.addWidget(self.gap_lineEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter_3)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/as_schematic.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.gridLayout_3.addWidget(self.splitter_3, 3, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.groupBox_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_3.addWidget(self.line_3, 3, 1, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.groupBox_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_3.addWidget(self.line_4, 0, 1, 1, 1)
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
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.matplotlibimageWidget = MatplotlibImageWidget(self.groupBox)
        self.matplotlibimageWidget.setProperty("reseverColorMap", False)
        self.matplotlibimageWidget.setColorBarToggle(False)
        self.matplotlibimageWidget.setAutoColorLimit(True)
        self.matplotlibimageWidget.setObjectName("matplotlibimageWidget")
        self.gridLayout.addWidget(self.matplotlibimageWidget, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuConfiguration = QtWidgets.QMenu(self.menubar)
        self.menuConfiguration.setObjectName("menuConfiguration")
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
        self.actionReload = QtWidgets.QAction(MainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad_From = QtWidgets.QAction(MainWindow)
        self.actionLoad_From.setObjectName("actionLoad_From")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionLocate = QtWidgets.QAction(MainWindow)
        self.actionLocate.setObjectName("actionLocate")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuConfiguration.addAction(self.actionReload)
        self.menuConfiguration.addAction(self.actionSave)
        self.menuConfiguration.addAction(self.actionLoad_From)
        self.menuConfiguration.addAction(self.actionSave_As)
        self.menuConfiguration.addSeparator()
        self.menuConfiguration.addAction(self.actionLocate)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.run_btn.clicked.connect(MainWindow.on_run)
        self.actionReload.triggered.connect(MainWindow.on_reload_config)
        self.actionLoad_From.triggered.connect(MainWindow.on_loadfrom_config)
        self.actionSave.triggered.connect(MainWindow.on_save_config)
        self.actionSave_As.triggered.connect(MainWindow.on_saveas_config)
        self.actionLocate.triggered.connect(MainWindow.on_locate_config)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Device"))
        self.info_lbl.setText(_translate("MainWindow", "info"))
        self.ems_detail_btn.setText(_translate("MainWindow", "..."))
        self.label_14.setText(_translate("MainWindow", "Orientation"))
        self.ems_orientation_cbb.setItemText(0, _translate("MainWindow", "X"))
        self.ems_orientation_cbb.setItemText(1, _translate("MainWindow", "Y"))
        self.run_btn.setText(_translate("MainWindow", "Run"))
        self.label.setText(_translate("MainWindow", "Select Device"))
        self.label_3.setText(_translate("MainWindow", "Configuration"))
        self.label_16.setText(_translate("MainWindow", "Voltage [V]"))
        self.label_7.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">L</span></p></body></html>"
            ))
        self.label_13.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">L</span><span style=\" vertical-align:sub;\">1</span></p></body></html>"
            ))
        self.label_12.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">L</span><span style=\" vertical-align:sub;\">2</span></p></body></html>"
            ))
        self.label_8.setText(_translate("MainWindow", "Gap [mm]"))
        self.label_20.setText(_translate("MainWindow", "Begin"))
        self.label_21.setText(_translate("MainWindow", "End"))
        self.label_22.setText(_translate("MainWindow", "Step"))
        self.label_23.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">T</span><span style=\" vertical-align:sub;\">settling</span></p></body></html>"
            ))
        self.volt_settling_time_dsbox.setSuffix(
            _translate("MainWindow", " sec"))
        self.label_11.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Thickness (<span style=\" font-style:italic;\">d</span>)</p></body></html>"
            ))
        self.label_15.setText(_translate("MainWindow", "Position [mm]"))
        self.label_6.setText(_translate("MainWindow", "Lengths [mm]"))
        self.label_17.setText(_translate("MainWindow", "Begin"))
        self.label_18.setText(_translate("MainWindow", "End"))
        self.label_19.setText(_translate("MainWindow", "Step"))
        self.label_5.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">T</span><span style=\" vertical-align:sub;\">settling</span></p></body></html>"
            ))
        self.pos_settling_time_dsbox.setSuffix(
            _translate("MainWindow", " sec"))
        self.label_9.setText(_translate("MainWindow", "Slit [mm]"))
        self.label_10.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Width (<span style=\" font-style:italic;\">s</span>)</p></body></html>"
            ))
        self.label_4.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">g</span></p></body></html>"
            ))
        self.groupBox.setTitle(_translate("MainWindow", "Data Visualization"))
        self.matplotlibimageWidget.setFigureAspectRatio(
            _translate("MainWindow", "auto"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Data Analysis"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuConfiguration.setTitle(
            _translate("MainWindow", "&Configuration"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionLoad_From.setText(_translate("MainWindow", "Load From"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionLocate.setText(_translate("MainWindow", "Locate"))


from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
