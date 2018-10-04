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
        MainWindow.resize(1600, 1200)
        MainWindow.setStyleSheet(
            "QGroupBox {\n"
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
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
            "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.data_info_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.data_info_groupBox.sizePolicy().hasHeightForWidth())
        self.data_info_groupBox.setSizePolicy(sizePolicy)
        self.data_info_groupBox.setStyleSheet("QLineEdit {\n"
                                              "    font-family: monospace;\n"
                                              "    color: blue;\n"
                                              "    border: 0.5px solid gray;\n"
                                              "    border-radius: 5px;\n"
                                              "    padding: 0 2px;\n"
                                              "}")
        self.data_info_groupBox.setObjectName("data_info_groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.data_info_groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.data_info_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.data_ts_created_lineEdit = QtWidgets.QLineEdit(
            self.data_info_groupBox)
        self.data_ts_created_lineEdit.setStyleSheet("")
        self.data_ts_created_lineEdit.setReadOnly(True)
        self.data_ts_created_lineEdit.setObjectName("data_ts_created_lineEdit")
        self.gridLayout_2.addWidget(self.data_ts_created_lineEdit, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.data_info_groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.task_duration_lineEdit = QtWidgets.QLineEdit(
            self.data_info_groupBox)
        self.task_duration_lineEdit.setStyleSheet("")
        self.task_duration_lineEdit.setReadOnly(True)
        self.task_duration_lineEdit.setObjectName("task_duration_lineEdit")
        self.gridLayout_2.addWidget(self.task_duration_lineEdit, 0, 3, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.data_info_groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 5, 1, 1)
        self.data_size_lineEdit = QtWidgets.QLineEdit(self.data_info_groupBox)
        self.data_size_lineEdit.setStyleSheet("")
        self.data_size_lineEdit.setReadOnly(True)
        self.data_size_lineEdit.setObjectName("data_size_lineEdit")
        self.gridLayout_2.addWidget(self.data_size_lineEdit, 0, 6, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.data_info_groupBox)
        self.label_34.setObjectName("label_34")
        self.gridLayout_2.addWidget(self.label_34, 0, 7, 1, 1)
        self.scan_range_lineEdit = QtWidgets.QLineEdit(self.data_info_groupBox)
        self.scan_range_lineEdit.setStyleSheet("")
        self.scan_range_lineEdit.setReadOnly(True)
        self.scan_range_lineEdit.setObjectName("scan_range_lineEdit")
        self.gridLayout_2.addWidget(self.scan_range_lineEdit, 0, 8, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.data_info_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.quad_name_lineEdit = QtWidgets.QLineEdit(self.data_info_groupBox)
        self.quad_name_lineEdit.setStyleSheet("")
        self.quad_name_lineEdit.setReadOnly(True)
        self.quad_name_lineEdit.setObjectName("quad_name_lineEdit")
        self.gridLayout_2.addWidget(self.quad_name_lineEdit, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.data_info_groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 2, 1, 1)
        self.monitor_names_lineEdit = QtWidgets.QLineEdit(
            self.data_info_groupBox)
        self.monitor_names_lineEdit.setStyleSheet("")
        self.monitor_names_lineEdit.setReadOnly(True)
        self.monitor_names_lineEdit.setObjectName("monitor_names_lineEdit")
        self.gridLayout_2.addWidget(self.monitor_names_lineEdit, 1, 3, 1, 6)
        self.gridLayout_9.addWidget(self.data_info_groupBox, 0, 0, 1, 1)
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
        self.vsplitter = QtWidgets.QSplitter(self.hsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.vsplitter.sizePolicy().hasHeightForWidth())
        self.vsplitter.setSizePolicy(sizePolicy)
        self.vsplitter.setOrientation(QtCore.Qt.Vertical)
        self.vsplitter.setObjectName("vsplitter")
        self.scan_data_plot_groupBox = QtWidgets.QGroupBox(self.vsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.scan_data_plot_groupBox.sizePolicy().hasHeightForWidth())
        self.scan_data_plot_groupBox.setSizePolicy(sizePolicy)
        self.scan_data_plot_groupBox.setObjectName("scan_data_plot_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.scan_data_plot_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.matplotliberrorbarWidget = MatplotlibErrorbarWidget(
            self.scan_data_plot_groupBox)
        self.matplotliberrorbarWidget.setFigureAutoScale(True)
        self.matplotliberrorbarWidget.setObjectName("matplotliberrorbarWidget")
        self.gridLayout.addWidget(self.matplotliberrorbarWidget, 0, 0, 1, 1)
        self.beam_info_groupBox = QtWidgets.QGroupBox(self.vsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.beam_info_groupBox.sizePolicy().hasHeightForWidth())
        self.beam_info_groupBox.setSizePolicy(sizePolicy)
        self.beam_info_groupBox.setObjectName("beam_info_groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.beam_info_groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_8 = QtWidgets.QLabel(self.beam_info_groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.ref_IonZ_lineEdit = QtWidgets.QLineEdit(self.beam_info_groupBox)
        self.ref_IonZ_lineEdit.setObjectName("ref_IonZ_lineEdit")
        self.gridLayout_3.addWidget(self.ref_IonZ_lineEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.beam_info_groupBox)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.ref_beta_lineEdit = QtWidgets.QLineEdit(self.beam_info_groupBox)
        self.ref_beta_lineEdit.setObjectName("ref_beta_lineEdit")
        self.gridLayout_3.addWidget(self.ref_beta_lineEdit, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.beam_info_groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)
        self.ref_IonW_lineEdit = QtWidgets.QLineEdit(self.beam_info_groupBox)
        self.ref_IonW_lineEdit.setObjectName("ref_IonW_lineEdit")
        self.gridLayout_3.addWidget(self.ref_IonW_lineEdit, 2, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.beam_info_groupBox)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 3, 0, 1, 1)
        self.quad_length_lineEdit = QtWidgets.QLineEdit(
            self.beam_info_groupBox)
        self.quad_length_lineEdit.setObjectName("quad_length_lineEdit")
        self.gridLayout_3.addWidget(self.quad_length_lineEdit, 3, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.beam_info_groupBox)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 4, 0, 1, 1)
        self.distance_lineEdit = QtWidgets.QLineEdit(self.beam_info_groupBox)
        self.distance_lineEdit.setObjectName("distance_lineEdit")
        self.gridLayout_3.addWidget(self.distance_lineEdit, 4, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.autofill_beam_info_pushButton = QtWidgets.QPushButton(
            self.beam_info_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.autofill_beam_info_pushButton.sizePolicy()
            .hasHeightForWidth())
        self.autofill_beam_info_pushButton.setSizePolicy(sizePolicy)
        self.autofill_beam_info_pushButton.setObjectName(
            "autofill_beam_info_pushButton")
        self.horizontalLayout.addWidget(self.autofill_beam_info_pushButton)
        self.label_35 = QtWidgets.QLabel(self.beam_info_groupBox)
        self.label_35.setStyleSheet("QLabel {\n"
                                    "    padding: 0 10px;\n"
                                    "    font-style: italic;\n"
                                    "    color: gray;\n"
                                    "}")
        self.label_35.setObjectName("label_35")
        self.horizontalLayout.addWidget(self.label_35)
        self.gridLayout_3.addLayout(self.horizontalLayout, 5, 1, 1, 1)
        self.data_analysis_groupBox = QtWidgets.QGroupBox(self.hsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.data_analysis_groupBox.sizePolicy().hasHeightForWidth())
        self.data_analysis_groupBox.setSizePolicy(sizePolicy)
        self.data_analysis_groupBox.setObjectName("data_analysis_groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.data_analysis_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.toolbox = QtWidgets.QToolBox(self.data_analysis_groupBox)
        self.toolbox.setObjectName("toolbox")
        self.page_params = QtWidgets.QWidget()
        self.page_params.setGeometry(QtCore.QRect(0, 0, 719, 892))
        self.page_params.setObjectName("page_params")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_params)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fitting_input_groupBox = QtWidgets.QGroupBox(self.page_params)
        self.fitting_input_groupBox.setObjectName("fitting_input_groupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.fitting_input_groupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_19 = QtWidgets.QLabel(self.fitting_input_groupBox)
        self.label_19.setObjectName("label_19")
        self.gridLayout_8.addWidget(self.label_19, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_20 = QtWidgets.QLabel(self.fitting_input_groupBox)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_4.addWidget(self.label_20)
        self.coef_a_init_lineEdit = QtWidgets.QLineEdit(
            self.fitting_input_groupBox)
        self.coef_a_init_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coef_a_init_lineEdit.setObjectName("coef_a_init_lineEdit")
        self.horizontalLayout_4.addWidget(self.coef_a_init_lineEdit)
        self.label_21 = QtWidgets.QLabel(self.fitting_input_groupBox)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_4.addWidget(self.label_21)
        self.coef_b_init_lineEdit = QtWidgets.QLineEdit(
            self.fitting_input_groupBox)
        self.coef_b_init_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coef_b_init_lineEdit.setObjectName("coef_b_init_lineEdit")
        self.horizontalLayout_4.addWidget(self.coef_b_init_lineEdit)
        self.label_22 = QtWidgets.QLabel(self.fitting_input_groupBox)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_4.addWidget(self.label_22)
        self.coef_c_init_lineEdit = QtWidgets.QLineEdit(
            self.fitting_input_groupBox)
        self.coef_c_init_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coef_c_init_lineEdit.setObjectName("coef_c_init_lineEdit")
        self.horizontalLayout_4.addWidget(self.coef_c_init_lineEdit)
        self.gridLayout_8.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_23 = QtWidgets.QLabel(self.fitting_input_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_5.addWidget(self.label_23)
        self.opt_method_comboBox = QtWidgets.QComboBox(
            self.fitting_input_groupBox)
        self.opt_method_comboBox.setObjectName("opt_method_comboBox")
        self.opt_method_comboBox.addItem("")
        self.opt_method_comboBox.addItem("")
        self.opt_method_comboBox.addItem("")
        self.opt_method_comboBox.addItem("")
        self.opt_method_comboBox.addItem("")
        self.opt_method_comboBox.addItem("")
        self.opt_method_comboBox.addItem("")
        self.horizontalLayout_5.addWidget(self.opt_method_comboBox)
        self.fit_pushButton = QtWidgets.QPushButton(
            self.fitting_input_groupBox)
        self.fit_pushButton.setObjectName("fit_pushButton")
        self.horizontalLayout_5.addWidget(self.fit_pushButton)
        self.gridLayout_8.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.fitting_input_groupBox)
        self.fitting_output_groupBox = QtWidgets.QGroupBox(self.page_params)
        self.fitting_output_groupBox.setStyleSheet("QLineEdit {\n"
                                                   "    color: black;\n"
                                                   "}")
        self.fitting_output_groupBox.setObjectName("fitting_output_groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.fitting_output_groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_24 = QtWidgets.QLabel(self.fitting_output_groupBox)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_3.addWidget(self.label_24)
        self.coef_a_final_lineEdit = QtWidgets.QLineEdit(
            self.fitting_output_groupBox)
        self.coef_a_final_lineEdit.setText("")
        self.coef_a_final_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coef_a_final_lineEdit.setReadOnly(True)
        self.coef_a_final_lineEdit.setObjectName("coef_a_final_lineEdit")
        self.horizontalLayout_3.addWidget(self.coef_a_final_lineEdit)
        self.label_26 = QtWidgets.QLabel(self.fitting_output_groupBox)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_3.addWidget(self.label_26)
        self.coef_b_final_lineEdit = QtWidgets.QLineEdit(
            self.fitting_output_groupBox)
        self.coef_b_final_lineEdit.setText("")
        self.coef_b_final_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coef_b_final_lineEdit.setReadOnly(True)
        self.coef_b_final_lineEdit.setObjectName("coef_b_final_lineEdit")
        self.horizontalLayout_3.addWidget(self.coef_b_final_lineEdit)
        self.label_25 = QtWidgets.QLabel(self.fitting_output_groupBox)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_3.addWidget(self.label_25)
        self.coef_c_final_lineEdit = QtWidgets.QLineEdit(
            self.fitting_output_groupBox)
        self.coef_c_final_lineEdit.setText("")
        self.coef_c_final_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.coef_c_final_lineEdit.setReadOnly(True)
        self.coef_c_final_lineEdit.setObjectName("coef_c_final_lineEdit")
        self.horizontalLayout_3.addWidget(self.coef_c_final_lineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 3)
        self.label_27 = QtWidgets.QLabel(self.fitting_output_groupBox)
        self.label_27.setObjectName("label_27")
        self.gridLayout_5.addWidget(self.label_27, 1, 0, 1, 1)
        self.resi_chisqr_lineEdit = QtWidgets.QLineEdit(
            self.fitting_output_groupBox)
        self.resi_chisqr_lineEdit.setReadOnly(True)
        self.resi_chisqr_lineEdit.setObjectName("resi_chisqr_lineEdit")
        self.gridLayout_5.addWidget(self.resi_chisqr_lineEdit, 1, 1, 1, 1)
        self.sync_to_init_pushButton = QtWidgets.QPushButton(
            self.fitting_output_groupBox)
        self.sync_to_init_pushButton.setObjectName("sync_to_init_pushButton")
        self.gridLayout_5.addWidget(self.sync_to_init_pushButton, 1, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.fitting_output_groupBox)
        self.twiss_output_groupBox = QtWidgets.QGroupBox(self.page_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.twiss_output_groupBox.sizePolicy().hasHeightForWidth())
        self.twiss_output_groupBox.setSizePolicy(sizePolicy)
        self.twiss_output_groupBox.setStyleSheet("QLineEdit {\n"
                                                 "    color: black;\n"
                                                 "}")
        self.twiss_output_groupBox.setObjectName("twiss_output_groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.twiss_output_groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_31 = QtWidgets.QLabel(self.twiss_output_groupBox)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_6.addWidget(self.label_31)
        self.emit_lineEdit = QtWidgets.QLineEdit(self.twiss_output_groupBox)
        self.emit_lineEdit.setReadOnly(True)
        self.emit_lineEdit.setObjectName("emit_lineEdit")
        self.horizontalLayout_6.addWidget(self.emit_lineEdit)
        self.label_32 = QtWidgets.QLabel(self.twiss_output_groupBox)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_6.addWidget(self.label_32)
        self.nemit_lineEdit = QtWidgets.QLineEdit(self.twiss_output_groupBox)
        self.nemit_lineEdit.setReadOnly(True)
        self.nemit_lineEdit.setObjectName("nemit_lineEdit")
        self.horizontalLayout_6.addWidget(self.nemit_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_28 = QtWidgets.QLabel(self.twiss_output_groupBox)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_7.addWidget(self.label_28)
        self.twiss_alpha_lineEdit = QtWidgets.QLineEdit(
            self.twiss_output_groupBox)
        self.twiss_alpha_lineEdit.setReadOnly(True)
        self.twiss_alpha_lineEdit.setObjectName("twiss_alpha_lineEdit")
        self.horizontalLayout_7.addWidget(self.twiss_alpha_lineEdit)
        self.label_29 = QtWidgets.QLabel(self.twiss_output_groupBox)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_7.addWidget(self.label_29)
        self.twiss_beta_lineEdit = QtWidgets.QLineEdit(
            self.twiss_output_groupBox)
        self.twiss_beta_lineEdit.setReadOnly(True)
        self.twiss_beta_lineEdit.setObjectName("twiss_beta_lineEdit")
        self.horizontalLayout_7.addWidget(self.twiss_beta_lineEdit)
        self.label_30 = QtWidgets.QLabel(self.twiss_output_groupBox)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_7.addWidget(self.label_30)
        self.twiss_gamma_lineEdit = QtWidgets.QLineEdit(
            self.twiss_output_groupBox)
        self.twiss_gamma_lineEdit.setReadOnly(True)
        self.twiss_gamma_lineEdit.setObjectName("twiss_gamma_lineEdit")
        self.horizontalLayout_7.addWidget(self.twiss_gamma_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.beam_ellipse_plot = MatplotlibCurveWidget(
            self.twiss_output_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.beam_ellipse_plot.sizePolicy().hasHeightForWidth())
        self.beam_ellipse_plot.setSizePolicy(sizePolicy)
        self.beam_ellipse_plot.setProperty("figureTightLayout", False)
        self.beam_ellipse_plot.setFigureWidth(4)
        self.beam_ellipse_plot.setProperty("figureDPI", 100)
        self.beam_ellipse_plot.setProperty("figureBackgroundColor",
                                           QtGui.QColor(237, 236, 235))
        self.beam_ellipse_plot.setObjectName("beam_ellipse_plot")
        self.verticalLayout_3.addWidget(self.beam_ellipse_plot)
        self.verticalLayout_2.addWidget(self.twiss_output_groupBox)
        self.toolbox.addItem(self.page_params, "")
        self.page_formulae = QtWidgets.QWidget()
        self.page_formulae.setGeometry(QtCore.QRect(0, 0, 854, 877))
        self.page_formulae.setStyleSheet("QLabel {\n"
                                         "    padding: 5px 10px;\n"
                                         "}")
        self.page_formulae.setObjectName("page_formulae")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_formulae)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_33 = QtWidgets.QLabel(self.page_formulae)
        self.label_33.setObjectName("label_33")
        self.verticalLayout.addWidget(self.label_33)
        self.label_7 = QtWidgets.QLabel(self.page_formulae)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_10 = QtWidgets.QLabel(self.page_formulae)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.page_formulae)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.page_formulae)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(self.page_formulae)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.label_15 = QtWidgets.QLabel(self.page_formulae)
        self.label_15.setObjectName("label_15")
        self.verticalLayout.addWidget(self.label_15)
        self.label_14 = QtWidgets.QLabel(self.page_formulae)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.label_16 = QtWidgets.QLabel(self.page_formulae)
        self.label_16.setObjectName("label_16")
        self.verticalLayout.addWidget(self.label_16)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.toolbox.addItem(self.page_formulae, "")
        self.gridLayout_4.addWidget(self.toolbox, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.hsplitter, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 32))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionOpen.triggered.connect(MainWindow.onOpen)
        self.fit_pushButton.clicked.connect(MainWindow.on_fit_parabola)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.data_info_groupBox.setTitle(
            _translate("MainWindow", "Quad Scan Emittance Measurement"))
        self.label_2.setText(_translate("MainWindow", "Data Created"))
        self.label_3.setText(_translate("MainWindow", "Task Duration [sec]"))
        self.label_4.setText(_translate("MainWindow", "Data Size"))
        self.label_34.setText(_translate("MainWindow", "Scan Range"))
        self.label_5.setText(_translate("MainWindow", "Quadrupole"))
        self.label_6.setText(_translate("MainWindow", "Beam Size Monitor"))
        self.scan_data_plot_groupBox.setTitle(
            _translate("MainWindow", "Data Visualization"))
        self.beam_info_groupBox.setTitle(
            _translate("MainWindow", "Accelerator Beam Infomation"))
        self.label_8.setText(_translate("MainWindow", "Q/A"))
        self.ref_IonZ_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Charg mass ratio</p></body></html>"))
        self.ref_IonZ_lineEdit.setText(_translate("MainWindow", "0.138655"))
        self.label.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Speed (<span style=\" font-weight:600; font-style:italic;\">β</span>)</p></body></html>"
            ))
        self.ref_beta_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion speed in the unit of light velocity of reference charge state</p></body></html>"
            ))
        self.ref_beta_lineEdit.setText(_translate("MainWindow", "0.18898"))
        self.label_9.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Energy (<span style=\" font-weight:600; font-style:italic;\">W</span>)</p></body></html>"
            ))
        self.ref_IonW_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total energy of reference charge state [eV/u]</p></body></html>"
            ))
        self.ref_IonW_lineEdit.setText(
            _translate("MainWindow", "948587559.7936388"))
        self.label_17.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Quad Length (<span style=\" font-weight:600; font-style:italic;\">l</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">q</span>)</p></body></html>"
            ))
        self.quad_length_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>The length of selected quadrupole [m]</p></body></html>"
            ))
        self.quad_length_lineEdit.setText(_translate("MainWindow", "0.25"))
        self.label_18.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Distance between the profile monitor and quadrupole.</p></body></html>"
            ))
        self.label_18.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Distance (<span style=\" font-weight:600; font-style:italic;\">d</span>)</p></body></html>"
            ))
        self.distance_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Distance between the quad and the profile monitor [m]</p></body></html>"
            ))
        self.distance_lineEdit.setText(_translate("MainWindow", "11.24454"))
        self.autofill_beam_info_pushButton.setText(
            _translate("MainWindow", "Auto"))
        self.label_35.setText(
            _translate("MainWindow", "Auto fill beam info by running model"))
        self.data_analysis_groupBox.setTitle(
            _translate("MainWindow", "Data Analysis"))
        self.fitting_input_groupBox.setTitle(
            _translate("MainWindow", "Fitting (Parabola) Settings"))
        self.label_19.setText(
            _translate("MainWindow", "Initial settings for A,B,C"))
        self.label_20.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">A</span></p></body></html>"
            ))
        self.coef_a_init_lineEdit.setText(_translate("MainWindow", "0"))
        self.label_21.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">B</span></p></body></html>"
            ))
        self.coef_b_init_lineEdit.setText(_translate("MainWindow", "0"))
        self.label_22.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">C</span></p></body></html>"
            ))
        self.coef_c_init_lineEdit.setText(_translate("MainWindow", "0"))
        self.label_23.setText(_translate("MainWindow", "Fitting method"))
        self.opt_method_comboBox.setItemText(0,
                                             _translate(
                                                 "MainWindow", "leastsq"))
        self.opt_method_comboBox.setItemText(1,
                                             _translate(
                                                 "MainWindow", "powell"))
        self.opt_method_comboBox.setItemText(2,
                                             _translate(
                                                 "MainWindow", "nelder"))
        self.opt_method_comboBox.setItemText(3,
                                             _translate(
                                                 "MainWindow", "lbfgsb"))
        self.opt_method_comboBox.setItemText(4,
                                             _translate("MainWindow", "ampgo"))
        self.opt_method_comboBox.setItemText(5,
                                             _translate(
                                                 "MainWindow", "basinhopping"))
        self.opt_method_comboBox.setItemText(6,
                                             _translate("MainWindow", "slsqp"))
        self.fit_pushButton.setText(_translate("MainWindow", "Fit"))
        self.fitting_output_groupBox.setTitle(
            _translate("MainWindow", "Fitting Results"))
        self.label_24.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">A</span></p></body></html>"
            ))
        self.label_26.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">B</span></p></body></html>"
            ))
        self.label_25.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">C</span></p></body></html>"
            ))
        self.label_27.setText(_translate("MainWindow", "Residual"))
        self.sync_to_init_pushButton.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Sync A,B,C to be initial settings for next fitting iteration.</p></body></html>"
            ))
        self.sync_to_init_pushButton.setText(_translate("MainWindow", "Sync"))
        self.twiss_output_groupBox.setTitle(
            _translate("MainWindow", "Emittance and Twiss Parameters"))
        self.label_31.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">ε</span></p></body></html>"
            ))
        self.label_32.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">ε</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">n</span></p></body></html>"
            ))
        self.label_28.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">α</span></p></body></html>"
            ))
        self.label_29.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">&beta;</span></p></body></html>"
            ))
        self.label_30.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">&gamma;</span></p></body></html>"
            ))
        self.toolbox.setItemText(
            self.toolbox.indexOf(self.page_params),
            _translate("MainWindow", "Data Analysis"))
        self.label_33.setText(
            _translate(
                "MainWindow",
                "Scan the quadrupole, between the selected beam profile monitor and quadrupole is pure drift."
            ))
        self.label_7.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2</span><span style=\" font-weight:600; font-style:italic;\">(k) = A k</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2</span><span style=\" font-weight:600; font-style:italic;\"> + B k + C</span></p></body></html>"
            ))
        self.label_10.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">11 </span><span style=\" font-weight:600; font-style:italic;\">= A / (d</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2 </span><span style=\" font-weight:600; font-style:italic;\">l</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">q</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2</span><span style=\" font-weight:600; font-style:italic;\">)</span></p></body></html>"
            ))
        self.label_11.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">12 </span><span style=\" font-weight:600; font-style:italic;\">= -B - 2 d l</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">q</span><span style=\" font-weight:600; font-style:italic;\"> σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">11</span><span style=\" font-weight:600; font-style:italic;\"> / (2 d</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2 </span><span style=\" font-weight:600; font-style:italic;\">l</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">q</span><span style=\" font-weight:600; font-style:italic;\">)</span></p></body></html>"
            ))
        self.label_12.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">22 </span><span style=\" font-weight:600; font-style:italic;\">= C - σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">11 </span><span style=\" font-weight:600; font-style:italic;\">- 2 d </span><span style=\" font-weight:600; font-style:italic;\">σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">12 </span><span style=\" font-weight:600; font-style:italic;\">/ d</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2</span></p></body></html>"
            ))
        self.label_13.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">ε = √ (σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">11</span><span style=\" font-weight:600; font-style:italic;\"> σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">22</span><span style=\" font-weight:600; font-style:italic;\"> - σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">12</span><span style=\" font-weight:600; font-style:italic; vertical-align:super;\">2</span><span style=\" font-weight:600; font-style:italic;\">)</span></p></body></html>"
            ))
        self.label_15.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">&alpha; = -σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">12</span><span style=\" font-weight:600; font-style:italic;\"> / ε</span></p></body></html>"
            ))
        self.label_14.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">β = σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">11</span><span style=\" font-weight:600; font-style:italic;\"> / ε</span></p></body></html>"
            ))
        self.label_16.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">γ = σ</span><span style=\" font-weight:600; font-style:italic; vertical-align:sub;\">22</span><span style=\" font-weight:600; font-style:italic;\"> / ε</span></p></body></html>"
            ))
        self.toolbox.setItemText(
            self.toolbox.indexOf(self.page_formulae),
            _translate("MainWindow", "Signal Quad Note"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))


from mpl4qt.widgets.mplcurvewidget import MatplotlibCurveWidget
from mpl4qt.widgets.mplerrorbarwidget import MatplotlibErrorbarWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
