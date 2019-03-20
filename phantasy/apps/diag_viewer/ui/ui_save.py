# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_save.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(782, 447)
        Dialog.setStyleSheet(
            "QLineEdit {\n"
            "    border: 0.5px solid gray;\n"
            "    padding: 1 5px;\n"
            "    border-radius: 3px;\n"
            "}\n"
            "\n"
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
            "    subcontrol-position: top left; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.browse_filepath_btn = QtWidgets.QPushButton(Dialog)
        self.browse_filepath_btn.setAutoDefault(False)
        self.browse_filepath_btn.setObjectName("browse_filepath_btn")
        self.gridLayout.addWidget(self.browse_filepath_btn, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.save_figure_chkbox = QtWidgets.QCheckBox(self.groupBox)
        self.save_figure_chkbox.setObjectName("save_figure_chkbox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                  self.save_figure_chkbox)
        self.save_settings_chkbox = QtWidgets.QCheckBox(self.groupBox)
        self.save_settings_chkbox.setObjectName("save_settings_chkbox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole,
                                  self.save_settings_chkbox)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.figure_format_cbb = QtWidgets.QComboBox(self.groupBox)
        self.figure_format_cbb.setObjectName("figure_format_cbb")
        self.figure_format_cbb.addItem("")
        self.figure_format_cbb.addItem("")
        self.figure_format_cbb.addItem("")
        self.gridLayout_2.addWidget(self.figure_format_cbb, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.figure_filepath_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.figure_filepath_lineEdit.setObjectName("figure_filepath_lineEdit")
        self.gridLayout_2.addWidget(self.figure_filepath_lineEdit, 1, 2, 1, 2)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.SpanningRole,
                                  self.gridLayout_2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.mebt2fs1b_chkbox = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt2fs1b_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt2fs1b_chkbox.setSizePolicy(sizePolicy)
        self.mebt2fs1b_chkbox.setObjectName("mebt2fs1b_chkbox")
        self.gridLayout_4.addWidget(self.mebt2fs1b_chkbox, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.mebt2fs1a_chkbox = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt2fs1a_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt2fs1a_chkbox.setSizePolicy(sizePolicy)
        self.mebt2fs1a_chkbox.setObjectName("mebt2fs1a_chkbox")
        self.gridLayout_4.addWidget(self.mebt2fs1a_chkbox, 0, 3, 1, 1)
        self.lebt_chkbox = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lebt_chkbox.sizePolicy().hasHeightForWidth())
        self.lebt_chkbox.setSizePolicy(sizePolicy)
        self.lebt_chkbox.setObjectName("lebt_chkbox")
        self.gridLayout_4.addWidget(self.lebt_chkbox, 0, 1, 1, 1)
        self.mebt_chkbox = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mebt_chkbox.sizePolicy().hasHeightForWidth())
        self.mebt_chkbox.setSizePolicy(sizePolicy)
        self.mebt_chkbox.setObjectName("mebt_chkbox")
        self.gridLayout_4.addWidget(self.mebt_chkbox, 0, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 5, 1, 1)
        self.settings_filepath_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.settings_filepath_lineEdit.setObjectName(
            "settings_filepath_lineEdit")
        self.gridLayout_4.addWidget(self.settings_filepath_lineEdit, 1, 1, 1,
                                    5)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.SpanningRole,
                                  self.gridLayout_4)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 4)
        self.filepath_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filepath_lineEdit.sizePolicy().hasHeightForWidth())
        self.filepath_lineEdit.setSizePolicy(sizePolicy)
        self.filepath_lineEdit.setObjectName("filepath_lineEdit")
        self.gridLayout.addWidget(self.filepath_lineEdit, 0, 1, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 3, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButton_3.clicked.connect(Dialog.reject)
        self.pushButton_2.clicked.connect(Dialog.on_save_data)
        self.browse_filepath_btn.clicked.connect(Dialog.on_get_filepath)
        self.save_figure_chkbox.toggled['bool'].connect(
            self.label_3.setEnabled)
        self.save_figure_chkbox.toggled['bool'].connect(
            self.figure_format_cbb.setEnabled)
        self.save_figure_chkbox.toggled['bool'].connect(
            self.label_4.setEnabled)
        self.save_figure_chkbox.toggled['bool'].connect(
            self.figure_filepath_lineEdit.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.label_2.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.lebt_chkbox.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.mebt_chkbox.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.mebt2fs1a_chkbox.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.mebt2fs1b_chkbox.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.label_5.setEnabled)
        self.save_settings_chkbox.toggled['bool'].connect(
            self.settings_filepath_lineEdit.setEnabled)
        self.filepath_lineEdit.textChanged['QString'].connect(
            Dialog.on_update_filepaths)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.filepath_lineEdit, self.browse_filepath_btn)
        Dialog.setTabOrder(self.browse_filepath_btn, self.save_figure_chkbox)
        Dialog.setTabOrder(self.save_figure_chkbox, self.figure_format_cbb)
        Dialog.setTabOrder(self.figure_format_cbb,
                           self.figure_filepath_lineEdit)
        Dialog.setTabOrder(self.figure_filepath_lineEdit,
                           self.save_settings_chkbox)
        Dialog.setTabOrder(self.save_settings_chkbox, self.lebt_chkbox)
        Dialog.setTabOrder(self.lebt_chkbox, self.mebt_chkbox)
        Dialog.setTabOrder(self.mebt_chkbox, self.mebt2fs1a_chkbox)
        Dialog.setTabOrder(self.mebt2fs1a_chkbox, self.mebt2fs1b_chkbox)
        Dialog.setTabOrder(self.mebt2fs1b_chkbox,
                           self.settings_filepath_lineEdit)
        Dialog.setTabOrder(self.settings_filepath_lineEdit, self.pushButton_3)
        Dialog.setTabOrder(self.pushButton_3, self.pushButton_2)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.browse_filepath_btn.setText(_translate("Dialog", "Browse"))
        self.groupBox.setTitle(_translate("Dialog", "Options"))
        self.save_figure_chkbox.setText(_translate("Dialog", "Save Figure"))
        self.save_settings_chkbox.setText(
            _translate("Dialog", "Save Settings"))
        self.figure_format_cbb.setItemText(0, _translate("Dialog", "png"))
        self.figure_format_cbb.setItemText(1, _translate("Dialog", "jpg"))
        self.figure_format_cbb.setItemText(2, _translate("Dialog", "eps"))
        self.label_3.setText(_translate("Dialog", "Format"))
        self.label_4.setText(_translate("Dialog", "File Path"))
        self.label_5.setText(_translate("Dialog", "File Path"))
        self.mebt2fs1b_chkbox.setText(_translate("Dialog", "MEBT2FS1B"))
        self.label_2.setText(_translate("Dialog", "Segments"))
        self.mebt2fs1a_chkbox.setText(_translate("Dialog", "MEBT2FS1A"))
        self.lebt_chkbox.setText(_translate("Dialog", "LEBT"))
        self.mebt_chkbox.setText(_translate("Dialog", "MEBT"))
        self.pushButton_3.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "File Path"))
        self.pushButton_2.setText(_translate("Dialog", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
