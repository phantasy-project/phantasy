# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dat2json.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(679, 269)
        Dialog.setStyleSheet("QLineEdit {\n"
                             "    border: 0.5px solid gray;\n"
                             "    padding: 1 5px;\n"
                             "    border-radius: 3px;\n"
                             "}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.open_datfile_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.open_datfile_btn.sizePolicy().hasHeightForWidth())
        self.open_datfile_btn.setSizePolicy(sizePolicy)
        self.open_datfile_btn.setObjectName("open_datfile_btn")
        self.gridLayout.addWidget(self.open_datfile_btn, 1, 0, 1, 2)
        self.locate_datfile_btn = QtWidgets.QPushButton(Dialog)
        self.locate_datfile_btn.setObjectName("locate_datfile_btn")
        self.gridLayout.addWidget(self.locate_datfile_btn, 1, 4, 1, 1)
        self.datfilepath_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.datfilepath_lineEdit.setObjectName("datfilepath_lineEdit")
        self.gridLayout.addWidget(self.datfilepath_lineEdit, 2, 0, 1, 5)
        self.locate_jsonfile_btn = QtWidgets.QPushButton(Dialog)
        self.locate_jsonfile_btn.setObjectName("locate_jsonfile_btn")
        self.gridLayout.addWidget(self.locate_jsonfile_btn, 3, 4, 1, 1)
        self.jsonfilepath_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.jsonfilepath_lineEdit.setObjectName("jsonfilepath_lineEdit")
        self.gridLayout.addWidget(self.jsonfilepath_lineEdit, 4, 0, 1, 5)
        spacerItem = QtWidgets.QSpacerItem(466, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 3)
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 5, 3, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 5, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 2)
        self.open_jsonpath_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.open_jsonpath_btn.sizePolicy().hasHeightForWidth())
        self.open_jsonpath_btn.setSizePolicy(sizePolicy)
        self.open_jsonpath_btn.setObjectName("open_jsonpath_btn")
        self.gridLayout.addWidget(self.open_jsonpath_btn, 3, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 5)

        self.retranslateUi(Dialog)
        self.open_datfile_btn.clicked.connect(Dialog.on_open_datfile)
        self.open_jsonpath_btn.clicked.connect(Dialog.on_save_jsonfile)
        self.locate_datfile_btn.clicked.connect(Dialog.on_locate_datfile)
        self.locate_jsonfile_btn.clicked.connect(Dialog.on_locate_jsonfile)
        self.pushButton_3.clicked.connect(Dialog.on_convert_file)
        self.pushButton_6.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_datfile_btn.setText(
            _translate("Dialog", "Select DAT file from"))
        self.locate_datfile_btn.setText(_translate("Dialog", "Locate"))
        self.locate_jsonfile_btn.setText(_translate("Dialog", "Locate"))
        self.pushButton_6.setText(_translate("Dialog", "E&xit"))
        self.pushButton_3.setText(_translate("Dialog", "Convert"))
        self.open_jsonpath_btn.setText(
            _translate("Dialog", "Save JSON file to"))
        self.label.setText(
            _translate(
                "Dialog",
                "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Convert .dat file to .json file </span></p></body></html>"
            ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
