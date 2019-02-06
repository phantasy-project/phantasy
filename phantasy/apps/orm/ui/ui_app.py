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
        MainWindow.resize(1440, 1200)
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
            "}\n"
            "\n"
            "QProgressBar {\n"
            "    border: 1px solid gray;\n"
            "    border-radius: 10px;\n"
            "    text-align: center;\n"
            "}\n"
            "\n"
            "QProgressBar::chunk {\n"
            "    background-color: #05B8CC;\n"
            "    width: 20px;\n"
            "    margin: 0.5px;\n"
            "}")
        MainWindow.setIconSize(QtCore.QSize(36, 36))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.hsplitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.hsplitter.sizePolicy().hasHeightForWidth())
        self.hsplitter.setSizePolicy(sizePolicy)
        self.hsplitter.setOrientation(QtCore.Qt.Horizontal)
        self.hsplitter.setObjectName("hsplitter")
        self.elem_models = QtWidgets.QWidget(self.hsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.elem_models.sizePolicy().hasHeightForWidth())
        self.elem_models.setSizePolicy(sizePolicy)
        self.elem_models.setMinimumSize(QtCore.QSize(450, 0))
        self.elem_models.setObjectName("elem_models")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.elem_models)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.elem_models)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.refresh_models_btn = QtWidgets.QPushButton(self.elem_models)
        self.refresh_models_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/refresh.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.refresh_models_btn.setIcon(icon1)
        self.refresh_models_btn.setIconSize(QtCore.QSize(24, 24))
        self.refresh_models_btn.setObjectName("refresh_models_btn")
        self.horizontalLayout_11.addWidget(self.refresh_models_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        self.line = QtWidgets.QFrame(self.elem_models)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.splitter = QtWidgets.QSplitter(self.elem_models)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.select_all_cors_btn = QtWidgets.QToolButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_all_cors_btn.sizePolicy().hasHeightForWidth())
        self.select_all_cors_btn.setSizePolicy(sizePolicy)
        self.select_all_cors_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/select-all.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.select_all_cors_btn.setIcon(icon2)
        self.select_all_cors_btn.setObjectName("select_all_cors_btn")
        self.horizontalLayout_10.addWidget(self.select_all_cors_btn)
        self.inverse_cor_selection_btn = QtWidgets.QToolButton(
            self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inverse_cor_selection_btn.sizePolicy().hasHeightForWidth())
        self.inverse_cor_selection_btn.setSizePolicy(sizePolicy)
        self.inverse_cor_selection_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/invert-selection.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.inverse_cor_selection_btn.setIcon(icon3)
        self.inverse_cor_selection_btn.setObjectName(
            "inverse_cor_selection_btn")
        self.horizontalLayout_10.addWidget(self.inverse_cor_selection_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.nelem_selected_cors_lineEdit = QtWidgets.QLineEdit(
            self.layoutWidget)
        self.nelem_selected_cors_lineEdit.setReadOnly(True)
        self.nelem_selected_cors_lineEdit.setObjectName(
            "nelem_selected_cors_lineEdit")
        self.horizontalLayout_10.addWidget(self.nelem_selected_cors_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.cors_gbox = QtWidgets.QGroupBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cors_gbox.sizePolicy().hasHeightForWidth())
        self.cors_gbox.setSizePolicy(sizePolicy)
        self.cors_gbox.setObjectName("cors_gbox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.cors_gbox)
        self.horizontalLayout_4.setContentsMargins(-1, 9, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cors_treeView = QtWidgets.QTreeView(self.cors_gbox)
        self.cors_treeView.setObjectName("cors_treeView")
        self.horizontalLayout_4.addWidget(self.cors_treeView)
        self.verticalLayout_3.addWidget(self.cors_gbox)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.select_all_bpms_btn = QtWidgets.QToolButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_all_bpms_btn.sizePolicy().hasHeightForWidth())
        self.select_all_bpms_btn.setSizePolicy(sizePolicy)
        self.select_all_bpms_btn.setText("")
        self.select_all_bpms_btn.setIcon(icon2)
        self.select_all_bpms_btn.setObjectName("select_all_bpms_btn")
        self.horizontalLayout_9.addWidget(self.select_all_bpms_btn)
        self.inverse_bpm_selection_btn = QtWidgets.QToolButton(
            self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inverse_bpm_selection_btn.sizePolicy().hasHeightForWidth())
        self.inverse_bpm_selection_btn.setSizePolicy(sizePolicy)
        self.inverse_bpm_selection_btn.setText("")
        self.inverse_bpm_selection_btn.setIcon(icon3)
        self.inverse_bpm_selection_btn.setObjectName(
            "inverse_bpm_selection_btn")
        self.horizontalLayout_9.addWidget(self.inverse_bpm_selection_btn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.nelem_selected_bpms_lineEdit = QtWidgets.QLineEdit(
            self.layoutWidget1)
        self.nelem_selected_bpms_lineEdit.setReadOnly(True)
        self.nelem_selected_bpms_lineEdit.setObjectName(
            "nelem_selected_bpms_lineEdit")
        self.horizontalLayout_9.addWidget(self.nelem_selected_bpms_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.monitors_gbox = QtWidgets.QGroupBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.monitors_gbox.sizePolicy().hasHeightForWidth())
        self.monitors_gbox.setSizePolicy(sizePolicy)
        self.monitors_gbox.setObjectName("monitors_gbox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.monitors_gbox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.bpms_treeView = QtWidgets.QTreeView(self.monitors_gbox)
        self.bpms_treeView.setObjectName("bpms_treeView")
        self.horizontalLayout_6.addWidget(self.bpms_treeView)
        self.verticalLayout.addWidget(self.monitors_gbox)
        self.verticalLayout_4.addWidget(self.splitter)
        self.operations_toolBox = QtWidgets.QToolBox(self.hsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.operations_toolBox.sizePolicy().hasHeightForWidth())
        self.operations_toolBox.setSizePolicy(sizePolicy)
        self.operations_toolBox.setStyleSheet(
            "QToolBox{\n"
            "     icon-size: 30px;\n"
            "}\n"
            "\n"
            "QToolBox QScrollArea > QWidget > QWidget\n"
            "{\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "\n"
            "QToolBox::tab {\n"
            "\n"
            "    background-color: #BABDB6;\n"
            "    /*border: 2px solid gray;*/\n"
            "    border-radius: 5px;\n"
            "    color: black;\n"
            "}\n"
            "\n"
            "QToolBox::tab:selected { \n"
            "    font: italic;\n"
            "    color: blue;\n"
            "}")
        self.operations_toolBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.operations_toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.operations_toolBox.setObjectName("operations_toolBox")
        self.orm_measurement = QtWidgets.QWidget()
        self.orm_measurement.setGeometry(QtCore.QRect(0, 0, 960, 804))
        self.orm_measurement.setObjectName("orm_measurement")
        self.gridLayout = QtWidgets.QGridLayout(self.orm_measurement)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.wait_time_dspinbox = QtWidgets.QDoubleSpinBox(
            self.orm_measurement)
        self.wait_time_dspinbox.setDecimals(1)
        self.wait_time_dspinbox.setMaximum(10.0)
        self.wait_time_dspinbox.setSingleStep(0.5)
        self.wait_time_dspinbox.setProperty("value", 1.0)
        self.wait_time_dspinbox.setObjectName("wait_time_dspinbox")
        self.horizontalLayout_3.addWidget(self.wait_time_dspinbox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.orm_measurement)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.alter_start_lineEdit = QtWidgets.QLineEdit(self.orm_measurement)
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
        self.label_4 = QtWidgets.QLabel(self.orm_measurement)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.alter_stop_lineEdit = QtWidgets.QLineEdit(self.orm_measurement)
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
        self.label_5 = QtWidgets.QLabel(self.orm_measurement)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.alter_steps_lineEdit = QtWidgets.QLineEdit(self.orm_measurement)
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
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.orm_measurement)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.operation_mode_cbb = QtWidgets.QComboBox(self.orm_measurement)
        self.operation_mode_cbb.setObjectName("operation_mode_cbb")
        self.operation_mode_cbb.addItem("")
        self.operation_mode_cbb.addItem("")
        self.horizontalLayout.addWidget(self.operation_mode_cbb)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.monitor_fields_cbb = QtWidgets.QComboBox(self.orm_measurement)
        self.monitor_fields_cbb.setObjectName("monitor_fields_cbb")
        self.monitor_fields_cbb.addItem("")
        self.monitor_fields_cbb.addItem("")
        self.monitor_fields_cbb.addItem("")
        self.horizontalLayout_5.addWidget(self.monitor_fields_cbb)
        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.measure_pb = QtWidgets.QProgressBar(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.measure_pb.sizePolicy().hasHeightForWidth())
        self.measure_pb.setSizePolicy(sizePolicy)
        self.measure_pb.setProperty("value", 24)
        self.measure_pb.setObjectName("measure_pb")
        self.horizontalLayout_7.addWidget(self.measure_pb)
        spacerItem7 = QtWidgets.QSpacerItem(10, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.run_btn = QtWidgets.QPushButton(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.run_btn.sizePolicy().hasHeightForWidth())
        self.run_btn.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.run_btn.setIcon(icon4)
        self.run_btn.setIconSize(QtCore.QSize(24, 24))
        self.run_btn.setObjectName("run_btn")
        self.horizontalLayout_7.addWidget(self.run_btn)
        self.gridLayout.addLayout(self.horizontalLayout_7, 6, 0, 1, 1)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/measure.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.operations_toolBox.addItem(self.orm_measurement, icon5, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 960, 804))
        self.page.setObjectName("page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtWidgets.QLabel(self.page)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.cor_damping_fac_dspinbox = QtWidgets.QDoubleSpinBox(self.page)
        self.cor_damping_fac_dspinbox.setMaximum(1.0)
        self.cor_damping_fac_dspinbox.setSingleStep(0.05)
        self.cor_damping_fac_dspinbox.setProperty("value", 0.5)
        self.cor_damping_fac_dspinbox.setObjectName("cor_damping_fac_dspinbox")
        self.gridLayout_2.addWidget(self.cor_damping_fac_dspinbox, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.page)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.cor_niter_spinbox = QtWidgets.QSpinBox(self.page)
        self.cor_niter_spinbox.setMinimum(1)
        self.cor_niter_spinbox.setMaximum(20)
        self.cor_niter_spinbox.setObjectName("cor_niter_spinbox")
        self.gridLayout_2.addWidget(self.cor_niter_spinbox, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.cor_wait_time_dspinbox = QtWidgets.QDoubleSpinBox(self.page)
        self.cor_wait_time_dspinbox.setDecimals(1)
        self.cor_wait_time_dspinbox.setMaximum(10.0)
        self.cor_wait_time_dspinbox.setSingleStep(0.5)
        self.cor_wait_time_dspinbox.setProperty("value", 1.0)
        self.cor_wait_time_dspinbox.setObjectName("cor_wait_time_dspinbox")
        self.gridLayout_2.addWidget(self.cor_wait_time_dspinbox, 2, 1, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cor_apply_pb = QtWidgets.QProgressBar(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cor_apply_pb.sizePolicy().hasHeightForWidth())
        self.cor_apply_pb.setSizePolicy(sizePolicy)
        self.cor_apply_pb.setProperty("value", 24)
        self.cor_apply_pb.setObjectName("cor_apply_pb")
        self.horizontalLayout_8.addWidget(self.cor_apply_pb)
        spacerItem8 = QtWidgets.QSpacerItem(10, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem8)
        self.cor_apply_btn = QtWidgets.QPushButton(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cor_apply_btn.sizePolicy().hasHeightForWidth())
        self.cor_apply_btn.setSizePolicy(sizePolicy)
        self.cor_apply_btn.setIcon(icon4)
        self.cor_apply_btn.setIconSize(QtCore.QSize(24, 24))
        self.cor_apply_btn.setObjectName("cor_apply_btn")
        self.horizontalLayout_8.addWidget(self.cor_apply_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 4, 0, 1, 2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 547,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem9, 3, 1, 1, 1)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/work.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.operations_toolBox.addItem(self.page, icon6, "")
        self.verticalLayout_2.addWidget(self.hsplitter)
        self.log_gbox = QtWidgets.QGroupBox(self.centralwidget)
        self.log_gbox.setMinimumSize(QtCore.QSize(0, 100))
        self.log_gbox.setObjectName("log_gbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.log_gbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.log_textEdit = QtWidgets.QTextEdit(self.log_gbox)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.log_textEdit.setFont(font)
        self.log_textEdit.setReadOnly(True)
        self.log_textEdit.setObjectName("log_textEdit")
        self.gridLayout_3.addWidget(self.log_textEdit, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.log_gbox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 32))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        MainWindow.setMenuBar(self.menubar)
        self.load_lattice_tool = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/load_lattice.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.load_lattice_tool.setIcon(icon7)
        self.load_lattice_tool.setObjectName("load_lattice_tool")
        self.measure_tool = QtWidgets.QAction(MainWindow)
        self.measure_tool.setIcon(icon5)
        self.measure_tool.setObjectName("measure_tool")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon8)
        self.actionAbout.setObjectName("actionAbout")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon9)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionContents.setIcon(icon10)
        self.actionContents.setObjectName("actionContents")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon11)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(
            QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionSave.setIcon(icon12)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(
            QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon13)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
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

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.run_btn.clicked.connect(MainWindow.on_measure_orm)
        self.cor_apply_btn.clicked.connect(MainWindow.on_apply_orm)
        self.actionOpen.triggered.connect(MainWindow.on_open_orm)
        self.actionSave.triggered.connect(MainWindow.on_save_orm)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_10.setText(_translate("MainWindow", "Refresh"))
        self.refresh_models_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Refresh the elements</p></body></html>")
        )
        self.select_all_cors_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.inverse_cor_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.nelem_selected_cors_lineEdit.setText(
            _translate("MainWindow", "0"))
        self.cors_gbox.setTitle(_translate("MainWindow", "Correctors"))
        self.select_all_bpms_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.inverse_bpm_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.nelem_selected_bpms_lineEdit.setText(
            _translate("MainWindow", "0"))
        self.monitors_gbox.setTitle(_translate("MainWindow", "Monitors"))
        self.label_2.setText(_translate("MainWindow", "Additional Wait Time"))
        self.label_3.setText(_translate("MainWindow", "Alter Range"))
        self.alter_start_lineEdit.setText(_translate("MainWindow", "-0.003"))
        self.label_4.setText(_translate("MainWindow", "To"))
        self.alter_stop_lineEdit.setText(_translate("MainWindow", "0.003"))
        self.label_5.setText(_translate("MainWindow", "N"))
        self.alter_steps_lineEdit.setText(_translate("MainWindow", "5"))
        self.label.setText(_translate("MainWindow", "Operation Mode"))
        self.operation_mode_cbb.setItemText(0, _translate(
            "MainWindow", "Live"))
        self.operation_mode_cbb.setItemText(1, _translate(
            "MainWindow", "Model"))
        self.label_6.setText(_translate("MainWindow", "Fields to Monitor"))
        self.monitor_fields_cbb.setItemText(0, _translate("MainWindow", "X&Y"))
        self.monitor_fields_cbb.setItemText(1, _translate("MainWindow", "X"))
        self.monitor_fields_cbb.setItemText(2, _translate("MainWindow", "Y"))
        self.run_btn.setText(_translate("MainWindow", "Measure"))
        self.operations_toolBox.setItemText(
            self.operations_toolBox.indexOf(self.orm_measurement),
            _translate("MainWindow", "ORM Measurement"))
        self.label_7.setText(_translate("MainWindow", "Damping Factor"))
        self.label_8.setText(_translate("MainWindow", "Iteration"))
        self.label_9.setText(_translate("MainWindow", "Additional Wait Time"))
        self.cor_apply_btn.setText(_translate("MainWindow", "Apply"))
        self.operations_toolBox.setItemText(
            self.operations_toolBox.indexOf(self.page),
            _translate("MainWindow", "Orbit Correction with ORM"))
        self.log_gbox.setTitle(_translate("MainWindow", "Log"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
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
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
