# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_save.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 370)
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
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.browse_rdatapath_btn = QtWidgets.QPushButton(Dialog)
        self.browse_rdatapath_btn.setObjectName("browse_rdatapath_btn")
        self.gridLayout.addWidget(self.browse_rdatapath_btn, 1, 3, 1, 1)
        self.browse_mdatapath_btn = QtWidgets.QPushButton(Dialog)
        self.browse_mdatapath_btn.setObjectName("browse_mdatapath_btn")
        self.gridLayout.addWidget(self.browse_mdatapath_btn, 0, 3, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.save_all_combined_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.save_all_combined_rbtn.setObjectName("save_all_combined_rbtn")
        self.gridLayout_2.addWidget(self.save_all_combined_rbtn, 2, 0, 1, 1)
        self.save_all_separated_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.save_all_separated_rbtn.setObjectName("save_all_separated_rbtn")
        self.gridLayout_2.addWidget(self.save_all_separated_rbtn, 3, 0, 1, 1)
        self.save_rdata_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.save_rdata_rbtn.setObjectName("save_rdata_rbtn")
        self.gridLayout_2.addWidget(self.save_rdata_rbtn, 1, 0, 1, 1)
        self.save_mdata_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.save_mdata_rbtn.setObjectName("save_mdata_rbtn")
        self.gridLayout_2.addWidget(self.save_mdata_rbtn, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 4)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 3, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.mdatapath_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mdatapath_lineEdit.sizePolicy().hasHeightForWidth())
        self.mdatapath_lineEdit.setSizePolicy(sizePolicy)
        self.mdatapath_lineEdit.setObjectName("mdatapath_lineEdit")
        self.gridLayout.addWidget(self.mdatapath_lineEdit, 0, 1, 1, 2)
        self.rdatapath_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rdatapath_lineEdit.sizePolicy().hasHeightForWidth())
        self.rdatapath_lineEdit.setSizePolicy(sizePolicy)
        self.rdatapath_lineEdit.setObjectName("rdatapath_lineEdit")
        self.gridLayout.addWidget(self.rdatapath_lineEdit, 1, 1, 1, 2)

        self.retranslateUi(Dialog)
        self.pushButton_3.clicked.connect(Dialog.reject)
        self.pushButton_2.clicked.connect(Dialog.on_save_data)
        self.browse_mdatapath_btn.clicked.connect(Dialog.on_get_mdata_savepath)
        self.browse_rdatapath_btn.clicked.connect(Dialog.on_get_rdata_savepath)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Save Results To"))
        self.label.setText(_translate("Dialog", "Save Data To"))
        self.browse_rdatapath_btn.setText(_translate("Dialog", "Browse"))
        self.browse_mdatapath_btn.setText(_translate("Dialog", "Browse"))
        self.groupBox.setTitle(_translate("Dialog", "Options"))
        self.label_3.setText(
            _translate(
                "Dialog",
                "<html><head/><body><p><span style=\" vertical-align:super;\">*</span> The combined data will be saving to results filepath.</p></body></html>"
            ))
        self.save_all_combined_rbtn.setText(
            _translate("Dialog",
                       "Save data and results into a single file (*)"))
        self.save_all_separated_rbtn.setText(
            _translate("Dialog", "Save data and results into separated files"))
        self.save_rdata_rbtn.setText(
            _translate("Dialog", "Save analyzed results into a file"))
        self.save_mdata_rbtn.setText(
            _translate("Dialog", "Save measured data into a file"))
        self.pushButton_2.setText(_translate("Dialog", "Save"))
        self.pushButton_3.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
