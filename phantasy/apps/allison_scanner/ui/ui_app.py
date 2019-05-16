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
        self.gridLayout_8 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName("gridLayout_8")
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
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 3, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 4)
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
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1,
                                    QtCore.Qt.AlignHCenter)
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
        self.gridLayout_3.addWidget(self.splitter_3, 3, 3, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.groupBox_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_3.addWidget(self.line_3, 3, 2, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.groupBox_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_3.addWidget(self.line_4, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/update.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 3, 0, 1, 1,
                                    QtCore.Qt.AlignTop)
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
        sizePolicy.setHorizontalStretch(7)
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
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.raw_view_chkbox = QtWidgets.QCheckBox(self.groupBox)
        self.raw_view_chkbox.setObjectName("raw_view_chkbox")
        self.horizontalLayout_9.addWidget(self.raw_view_chkbox)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_9.addWidget(self.checkBox)
        self.gridLayout.addLayout(self.horizontalLayout_9, 2, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_4 = QtWidgets.QSplitter(self.groupBox_3)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.param_tbox = QtWidgets.QToolBox(self.splitter_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(
            self.param_tbox.sizePolicy().hasHeightForWidth())
        self.param_tbox.setSizePolicy(sizePolicy)
        self.param_tbox.setObjectName("param_tbox")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 791, 444))
        self.page_3.setObjectName("page_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.voltage_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.voltage_lineEdit.setObjectName("voltage_lineEdit")
        self.horizontalLayout_8.addWidget(self.voltage_lineEdit)
        self.label_36 = QtWidgets.QLabel(self.page_3)
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_8.addWidget(self.label_36)
        self.label_38 = QtWidgets.QLabel(self.page_3)
        self.label_38.setText("")
        self.label_38.setPixmap(QtGui.QPixmap(":/icons/to.png"))
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_8.addWidget(self.label_38)
        self.divergence_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.divergence_lineEdit.setReadOnly(True)
        self.divergence_lineEdit.setObjectName("divergence_lineEdit")
        self.horizontalLayout_8.addWidget(self.divergence_lineEdit)
        self.label_37 = QtWidgets.QLabel(self.page_3)
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_8.addWidget(self.label_37)
        self.gridLayout_6.addLayout(self.horizontalLayout_8, 3, 0, 1, 2)
        self.label_34 = QtWidgets.QLabel(self.page_3)
        self.label_34.setObjectName("label_34")
        self.gridLayout_6.addWidget(self.label_34, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 4, 0, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.page_3)
        self.label_35.setObjectName("label_35")
        self.gridLayout_6.addWidget(self.label_35, 2, 2, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.page_3)
        self.label_32.setObjectName("label_32")
        self.gridLayout_6.addWidget(self.label_32, 0, 0, 1, 1)
        self.ion_energy_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.ion_energy_lineEdit.setObjectName("ion_energy_lineEdit")
        self.gridLayout_6.addWidget(self.ion_energy_lineEdit, 2, 1, 1, 1)
        self.ion_charge_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.ion_charge_lineEdit.setObjectName("ion_charge_lineEdit")
        self.gridLayout_6.addWidget(self.ion_charge_lineEdit, 0, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.page_3)
        self.label_33.setObjectName("label_33")
        self.gridLayout_6.addWidget(self.label_33, 1, 0, 1, 1)
        self.ion_mass_lineEdit = QtWidgets.QLineEdit(self.page_3)
        self.ion_mass_lineEdit.setObjectName("ion_mass_lineEdit")
        self.gridLayout_6.addWidget(self.ion_mass_lineEdit, 1, 1, 1, 1)
        self.param_tbox.addItem(self.page_3, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 791, 444))
        self.page.setObjectName("page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_39 = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy)
        self.label_39.setObjectName("label_39")
        self.gridLayout_2.addWidget(self.label_39, 0, 0, 1, 1)
        self.bkgd_noise_plot = MatplotlibBaseWidget(self.page)
        self.bkgd_noise_plot.setProperty("figureTightLayout", True)
        self.bkgd_noise_plot.setObjectName("bkgd_noise_plot")
        self.gridLayout_2.addWidget(self.bkgd_noise_plot, 3, 0, 1, 3)
        self.bkgd_noise_threshold_sbox = QtWidgets.QSpinBox(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bkgd_noise_threshold_sbox.sizePolicy().hasHeightForWidth())
        self.bkgd_noise_threshold_sbox.setSizePolicy(sizePolicy)
        self.bkgd_noise_threshold_sbox.setProperty("value", 5)
        self.bkgd_noise_threshold_sbox.setObjectName(
            "bkgd_noise_threshold_sbox")
        self.gridLayout_2.addWidget(self.bkgd_noise_threshold_sbox, 1, 1, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy)
        self.label_40.setObjectName("label_40")
        self.gridLayout_2.addWidget(self.label_40, 1, 0, 1, 1)
        self.bkgd_noise_nelem_sbox = QtWidgets.QSpinBox(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bkgd_noise_nelem_sbox.sizePolicy().hasHeightForWidth())
        self.bkgd_noise_nelem_sbox.setSizePolicy(sizePolicy)
        self.bkgd_noise_nelem_sbox.setProperty("value", 2)
        self.bkgd_noise_nelem_sbox.setObjectName("bkgd_noise_nelem_sbox")
        self.gridLayout_2.addWidget(self.bkgd_noise_nelem_sbox, 0, 1, 1, 1)
        self.auto_update_image_chkbox = QtWidgets.QCheckBox(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.auto_update_image_chkbox.sizePolicy().hasHeightForWidth())
        self.auto_update_image_chkbox.setSizePolicy(sizePolicy)
        self.auto_update_image_chkbox.setChecked(False)
        self.auto_update_image_chkbox.setObjectName("auto_update_image_chkbox")
        self.gridLayout_2.addWidget(self.auto_update_image_chkbox, 1, 2, 1, 1)
        self.param_tbox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 791, 444))
        self.page_2.setObjectName("page_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)
        self.factor_dsbox = QtWidgets.QDoubleSpinBox(self.page_2)
        self.factor_dsbox.setDecimals(1)
        self.factor_dsbox.setMaximum(20.0)
        self.factor_dsbox.setProperty("value", 4.0)
        self.factor_dsbox.setObjectName("factor_dsbox")
        self.gridLayout_7.addWidget(self.factor_dsbox, 0, 1, 1, 1)
        self.plot_region_btn = QtWidgets.QToolButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_region_btn.sizePolicy().hasHeightForWidth())
        self.plot_region_btn.setSizePolicy(sizePolicy)
        self.plot_region_btn.setObjectName("plot_region_btn")
        self.gridLayout_7.addWidget(self.plot_region_btn, 0, 2, 1, 1)
        self.label_49 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        self.label_49.setObjectName("label_49")
        self.gridLayout_7.addWidget(self.label_49, 1, 0, 1, 1)
        self.noise_threshold_sbox = QtWidgets.QDoubleSpinBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noise_threshold_sbox.sizePolicy().hasHeightForWidth())
        self.noise_threshold_sbox.setSizePolicy(sizePolicy)
        self.noise_threshold_sbox.setDecimals(1)
        self.noise_threshold_sbox.setProperty("value", 2.0)
        self.noise_threshold_sbox.setObjectName("noise_threshold_sbox")
        self.gridLayout_7.addWidget(self.noise_threshold_sbox, 1, 1, 1, 1)
        self.apply_noise_correction_btn = QtWidgets.QToolButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_noise_correction_btn.sizePolicy().hasHeightForWidth())
        self.apply_noise_correction_btn.setSizePolicy(sizePolicy)
        self.apply_noise_correction_btn.setObjectName(
            "apply_noise_correction_btn")
        self.gridLayout_7.addWidget(self.apply_noise_correction_btn, 1, 2, 1,
                                    1)
        self.noise_plot = MatplotlibBaseWidget(self.page_2)
        self.noise_plot.setProperty("figureTightLayout", True)
        self.noise_plot.setObjectName("noise_plot")
        self.gridLayout_7.addWidget(self.noise_plot, 2, 0, 1, 3)
        self.param_tbox.addItem(self.page_2, "")
        self.twiss_gbox = QtWidgets.QGroupBox(self.splitter_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(
            self.twiss_gbox.sizePolicy().hasHeightForWidth())
        self.twiss_gbox.setSizePolicy(sizePolicy)
        self.twiss_gbox.setFlat(False)
        self.twiss_gbox.setCheckable(False)
        self.twiss_gbox.setObjectName("twiss_gbox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.twiss_gbox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.x_cen_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.x_cen_lbl.setFont(font)
        self.x_cen_lbl.setObjectName("x_cen_lbl")
        self.gridLayout_5.addWidget(self.x_cen_lbl, 0, 0, 1, 1)
        self.x_cen_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.x_cen_lineEdit.setReadOnly(True)
        self.x_cen_lineEdit.setObjectName("x_cen_lineEdit")
        self.gridLayout_5.addWidget(self.x_cen_lineEdit, 0, 1, 1, 1)
        self.x_rms_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.x_rms_lbl.setFont(font)
        self.x_rms_lbl.setObjectName("x_rms_lbl")
        self.gridLayout_5.addWidget(self.x_rms_lbl, 0, 2, 1, 1)
        self.x_rms_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.x_rms_lineEdit.setReadOnly(True)
        self.x_rms_lineEdit.setObjectName("x_rms_lineEdit")
        self.gridLayout_5.addWidget(self.x_rms_lineEdit, 0, 3, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_41.setObjectName("label_41")
        self.gridLayout_5.addWidget(self.label_41, 0, 4, 1, 1)
        self.xp_cen_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.xp_cen_lbl.setFont(font)
        self.xp_cen_lbl.setObjectName("xp_cen_lbl")
        self.gridLayout_5.addWidget(self.xp_cen_lbl, 1, 0, 1, 1)
        self.xp_cen_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.xp_cen_lineEdit.setReadOnly(True)
        self.xp_cen_lineEdit.setObjectName("xp_cen_lineEdit")
        self.gridLayout_5.addWidget(self.xp_cen_lineEdit, 1, 1, 1, 1)
        self.xp_rms_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.xp_rms_lbl.setFont(font)
        self.xp_rms_lbl.setObjectName("xp_rms_lbl")
        self.gridLayout_5.addWidget(self.xp_rms_lbl, 1, 2, 1, 1)
        self.xp_rms_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.xp_rms_lineEdit.setReadOnly(True)
        self.xp_rms_lineEdit.setObjectName("xp_rms_lineEdit")
        self.gridLayout_5.addWidget(self.xp_rms_lineEdit, 1, 3, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_42.setObjectName("label_42")
        self.gridLayout_5.addWidget(self.label_42, 1, 4, 1, 1)
        self.emit_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.emit_x_lbl.setFont(font)
        self.emit_x_lbl.setObjectName("emit_x_lbl")
        self.gridLayout_5.addWidget(self.emit_x_lbl, 2, 0, 1, 1)
        self.emit_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.emit_x_lineEdit.setReadOnly(True)
        self.emit_x_lineEdit.setObjectName("emit_x_lineEdit")
        self.gridLayout_5.addWidget(self.emit_x_lineEdit, 2, 1, 1, 1)
        self.emitn_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.emitn_x_lbl.setFont(font)
        self.emitn_x_lbl.setObjectName("emitn_x_lbl")
        self.gridLayout_5.addWidget(self.emitn_x_lbl, 2, 2, 1, 1)
        self.emitn_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.emitn_x_lineEdit.setReadOnly(True)
        self.emitn_x_lineEdit.setObjectName("emitn_x_lineEdit")
        self.gridLayout_5.addWidget(self.emitn_x_lineEdit, 2, 3, 1, 1)
        self.label_47 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_47.setObjectName("label_47")
        self.gridLayout_5.addWidget(self.label_47, 2, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.alpha_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.alpha_x_lbl.setFont(font)
        self.alpha_x_lbl.setObjectName("alpha_x_lbl")
        self.horizontalLayout_10.addWidget(self.alpha_x_lbl)
        self.alpha_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.alpha_x_lineEdit.setReadOnly(True)
        self.alpha_x_lineEdit.setObjectName("alpha_x_lineEdit")
        self.horizontalLayout_10.addWidget(self.alpha_x_lineEdit)
        self.beta_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.beta_x_lbl.setFont(font)
        self.beta_x_lbl.setObjectName("beta_x_lbl")
        self.horizontalLayout_10.addWidget(self.beta_x_lbl)
        self.beta_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.beta_x_lineEdit.setReadOnly(True)
        self.beta_x_lineEdit.setObjectName("beta_x_lineEdit")
        self.horizontalLayout_10.addWidget(self.beta_x_lineEdit)
        self.label_48 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_10.addWidget(self.label_48)
        self.gamma_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.gamma_x_lbl.setFont(font)
        self.gamma_x_lbl.setObjectName("gamma_x_lbl")
        self.horizontalLayout_10.addWidget(self.gamma_x_lbl)
        self.gamma_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.gamma_x_lineEdit.setReadOnly(True)
        self.gamma_x_lineEdit.setObjectName("gamma_x_lineEdit")
        self.horizontalLayout_10.addWidget(self.gamma_x_lineEdit)
        self.label_46 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_10.addWidget(self.label_46)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.show_results_btn = QtWidgets.QToolButton(self.twiss_gbox)
        self.show_results_btn.setObjectName("show_results_btn")
        self.horizontalLayout_11.addWidget(self.show_results_btn)
        self.update_results_btn = QtWidgets.QToolButton(self.twiss_gbox)
        self.update_results_btn.setObjectName("update_results_btn")
        self.horizontalLayout_11.addWidget(self.update_results_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.verticalLayout.addWidget(self.splitter_4)
        self.gridLayout_8.addWidget(self.splitter_2, 0, 0, 1, 1)
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
        self.menu_Device = QtWidgets.QMenu(self.menubar)
        self.menu_Device.setObjectName("menu_Device")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon3)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon5)
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
        self.actionSimulation_Mode = QtWidgets.QAction(MainWindow)
        self.actionSimulation_Mode.setCheckable(True)
        self.actionSimulation_Mode.setObjectName("actionSimulation_Mode")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon6)
        self.actionOpen.setObjectName("actionOpen")
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuConfiguration.addAction(self.actionReload)
        self.menuConfiguration.addAction(self.actionSave)
        self.menuConfiguration.addAction(self.actionLoad_From)
        self.menuConfiguration.addAction(self.actionSave_As)
        self.menuConfiguration.addSeparator()
        self.menuConfiguration.addAction(self.actionLocate)
        self.menu_Device.addAction(self.actionSimulation_Mode)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menu_Device.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.param_tbox.setCurrentIndex(1)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.run_btn.clicked.connect(MainWindow.on_run)
        self.actionReload.triggered.connect(MainWindow.on_reload_config)
        self.actionLoad_From.triggered.connect(MainWindow.on_loadfrom_config)
        self.actionSave.triggered.connect(MainWindow.on_save_config)
        self.actionSave_As.triggered.connect(MainWindow.on_saveas_config)
        self.actionLocate.triggered.connect(MainWindow.on_locate_config)
        self.pushButton.clicked.connect(MainWindow.sync_config)
        self.actionSimulation_Mode.toggled['bool'].connect(
            MainWindow.on_enable_simulation_mode)
        self.update_results_btn.clicked.connect(MainWindow.on_update_results)
        self.actionOpen.triggered.connect(MainWindow.on_open_data)
        self.bkgd_noise_nelem_sbox.valueChanged['int'].connect(
            MainWindow.on_update_nsampling)
        self.bkgd_noise_threshold_sbox.valueChanged['int'].connect(
            MainWindow.on_update_threshold0)
        self.checkBox.toggled['bool'].connect(
            self.matplotlibimageWidget.setColorBarToggle)
        self.raw_view_chkbox.toggled['bool'].connect(
            MainWindow.on_enable_raw_view)
        self.auto_update_image_chkbox.toggled['bool'].connect(
            MainWindow.on_enable_auto_filter_bkgd_noise)
        self.plot_region_btn.clicked.connect(MainWindow.on_plot_region)
        self.apply_noise_correction_btn.clicked.connect(
            MainWindow.on_apply_noise_correction)
        self.factor_dsbox.valueChanged['double'].connect(
            MainWindow.on_update_ellipse_size_factor)
        self.noise_threshold_sbox.valueChanged['double'].connect(
            MainWindow.on_update_noise_threshold)
        self.show_results_btn.clicked.connect(MainWindow.on_finalize_results)
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
        self.pushButton.setText(_translate("MainWindow", "Configuration"))
        self.groupBox.setTitle(_translate("MainWindow", "Data Visualization"))
        self.matplotlibimageWidget.setFigureAspectRatio(
            _translate("MainWindow", "auto"))
        self.raw_view_chkbox.setText(_translate("MainWindow", "Raw View"))
        self.checkBox.setText(_translate("MainWindow", "Show Colorbar"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Data Analysis"))
        self.voltage_lineEdit.setText(_translate("MainWindow", "100"))
        self.label_36.setText(_translate("MainWindow", "V"))
        self.label_37.setText(_translate("MainWindow", "mrad"))
        self.label_34.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Energy (<span style=\" font-style:italic;\">E</span><span style=\" font-style:italic; vertical-align:sub;\">k</span>)</p></body></html>"
            ))
        self.label_35.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>eV</p></body></html>"))
        self.label_32.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Charge (<span style=\" font-style:italic;\">Q</span>)</p></body></html>"
            ))
        self.ion_energy_lineEdit.setText(_translate("MainWindow", "12000"))
        self.ion_charge_lineEdit.setText(_translate("MainWindow", "9"))
        self.label_33.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Mass (<span style=\" font-style:italic;\">A</span>)</p></body></html>"
            ))
        self.ion_mass_lineEdit.setText(_translate("MainWindow", "39.948"))
        self.param_tbox.setItemText(
            self.param_tbox.indexOf(self.page_3),
            _translate("MainWindow", "Beam"))
        self.label_39.setText(_translate("MainWindow", "# of Sampling Points"))
        self.label_40.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Threshold by <span style=\" font-style:italic;\">σ</span></p></body></html>"
            ))
        self.auto_update_image_chkbox.setText(
            _translate("MainWindow", "Auto Update"))
        self.param_tbox.setItemText(
            self.param_tbox.indexOf(self.page),
            _translate("MainWindow", "Background Noise"))
        self.label_3.setText(_translate("MainWindow", "Ellipse Size Factor"))
        self.plot_region_btn.setText(_translate("MainWindow", "Plot1"))
        self.label_49.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Noise Threshold by <span style=\" font-style:italic;\">σ</span></p></body></html>"
            ))
        self.apply_noise_correction_btn.setText(
            _translate("MainWindow", "Apply"))
        self.param_tbox.setItemText(
            self.param_tbox.indexOf(self.page_2),
            _translate("MainWindow", "Noise Correction"))
        self.twiss_gbox.setTitle(_translate("MainWindow", "Twiss Paramemters"))
        self.x_cen_lbl.setText(_translate("MainWindow", "x_cen"))
        self.x_rms_lbl.setText(_translate("MainWindow", "x_rms"))
        self.label_41.setText(_translate("MainWindow", "mm"))
        self.xp_cen_lbl.setText(_translate("MainWindow", "xp_cen"))
        self.xp_rms_lbl.setText(_translate("MainWindow", "xp_rms"))
        self.label_42.setText(_translate("MainWindow", "mrad"))
        self.emit_x_lbl.setText(_translate("MainWindow", "emit"))
        self.emitn_x_lbl.setText(_translate("MainWindow", "emit_n"))
        self.label_47.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>mm&middot;mrad</p></body></html>"))
        self.alpha_x_lbl.setText(_translate("MainWindow", "alpha"))
        self.beta_x_lbl.setText(_translate("MainWindow", "beta"))
        self.label_48.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>m</p></body></html>"))
        self.gamma_x_lbl.setText(_translate("MainWindow", "gamma"))
        self.label_46.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>m<span style=\" vertical-align:super;\">-1</span></p></body></html>"
            ))
        self.show_results_btn.setText(_translate("MainWindow", "Show"))
        self.update_results_btn.setText(_translate("MainWindow", "Update"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuConfiguration.setTitle(
            _translate("MainWindow", "&Configuration"))
        self.menu_Device.setTitle(_translate("MainWindow", "&Device"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionLoad_From.setText(_translate("MainWindow", "Load From"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionLocate.setText(_translate("MainWindow", "Locate"))
        self.actionSimulation_Mode.setText(
            _translate("MainWindow", "Simulation Mode"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))


from mpl4qt.widgets.mplbasewidget import MatplotlibBaseWidget
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
