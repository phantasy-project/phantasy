# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elem_select.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_btn.sizePolicy().hasHeightForWidth())
        self.cancel_btn.setSizePolicy(sizePolicy)
        self.cancel_btn.setAutoDefault(True)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.validate_btn = QtWidgets.QPushButton(Dialog)
        self.validate_btn.setObjectName("validate_btn")
        self.horizontalLayout.addWidget(self.validate_btn)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ok_btn.sizePolicy().hasHeightForWidth())
        self.ok_btn.setSizePolicy(sizePolicy)
        self.ok_btn.setAutoDefault(True)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout.addWidget(self.ok_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.elem_mode_radiobtn = QtWidgets.QRadioButton(Dialog)
        self.elem_mode_radiobtn.setObjectName("elem_mode_radiobtn")
        self.gridLayout_2.addWidget(self.elem_mode_radiobtn, 2, 0, 1, 1)
        self.pv_mode_radiobtn = QtWidgets.QRadioButton(Dialog)
        self.pv_mode_radiobtn.setChecked(True)
        self.pv_mode_radiobtn.setObjectName("pv_mode_radiobtn")
        self.gridLayout_2.addWidget(self.pv_mode_radiobtn, 0, 0, 1, 1)
        self.pv_groupBox = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pv_groupBox.sizePolicy().hasHeightForWidth())
        self.pv_groupBox.setSizePolicy(sizePolicy)
        self.pv_groupBox.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
            "    */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1ex; /* leave space at the top for the title */\n"
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
        self.pv_groupBox.setObjectName("pv_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.pv_groupBox)
        self.gridLayout.setContentsMargins(-1, 20, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.copy_set_to_read_btn = QtWidgets.QPushButton(self.pv_groupBox)
        self.copy_set_to_read_btn.setAutoDefault(True)
        self.copy_set_to_read_btn.setObjectName("copy_set_to_read_btn")
        self.gridLayout.addWidget(self.copy_set_to_read_btn, 1, 2, 1, 1)
        self.pv_read_lineEdit = QtWidgets.QLineEdit(self.pv_groupBox)
        self.pv_read_lineEdit.setObjectName("pv_read_lineEdit")
        self.gridLayout.addWidget(self.pv_read_lineEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.pv_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pv_set_lbl = QtWidgets.QLabel(self.pv_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pv_set_lbl.sizePolicy().hasHeightForWidth())
        self.pv_set_lbl.setSizePolicy(sizePolicy)
        self.pv_set_lbl.setAlignment(QtCore.Qt.AlignRight
                                     | QtCore.Qt.AlignTrailing
                                     | QtCore.Qt.AlignVCenter)
        self.pv_set_lbl.setObjectName("pv_set_lbl")
        self.gridLayout.addWidget(self.pv_set_lbl, 0, 0, 1, 1)
        self.pv_set_lineEdit = QtWidgets.QLineEdit(self.pv_groupBox)
        self.pv_set_lineEdit.setText("")
        self.pv_set_lineEdit.setObjectName("pv_set_lineEdit")
        self.gridLayout.addWidget(self.pv_set_lineEdit, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.pv_groupBox, 1, 0, 1, 1)
        self.elem_treeView = QtWidgets.QTreeView(Dialog)
        self.elem_treeView.setStyleSheet("QTreeView {\n"
                                         "    font-family: monospace;\n"
                                         "}")
        self.elem_treeView.setObjectName("elem_treeView")
        self.gridLayout_2.addWidget(self.elem_treeView, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.elem_treeView.doubleClicked['QModelIndex'].connect(
            Dialog.on_select_element)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pv_mode_radiobtn, self.pv_set_lineEdit)
        Dialog.setTabOrder(self.pv_set_lineEdit, self.pv_read_lineEdit)
        Dialog.setTabOrder(self.pv_read_lineEdit, self.copy_set_to_read_btn)
        Dialog.setTabOrder(self.copy_set_to_read_btn, self.elem_mode_radiobtn)
        Dialog.setTabOrder(self.elem_mode_radiobtn, self.elem_treeView)
        Dialog.setTabOrder(self.elem_treeView, self.cancel_btn)
        Dialog.setTabOrder(self.cancel_btn, self.validate_btn)
        Dialog.setTabOrder(self.validate_btn, self.ok_btn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
        self.validate_btn.setText(_translate("Dialog", "Validate"))
        self.ok_btn.setText(_translate("Dialog", "OK"))
        self.elem_mode_radiobtn.setText(_translate("Dialog", "Element"))
        self.pv_mode_radiobtn.setText(_translate("Dialog", "PV"))
        self.pv_groupBox.setTitle(_translate("Dialog", "Input PVs"))
        self.copy_set_to_read_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Smart copy Setpoint PV to Readback PV</p></body></html>"
            ))
        self.copy_set_to_read_btn.setText(_translate("Dialog", "Copy"))
        self.pv_read_lineEdit.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Press Enter after input</p></body></html>"
            ))
        self.label_2.setText(_translate("Dialog", "Readback PV"))
        self.pv_set_lbl.setText(_translate("Dialog", "Setpoint PV"))
        self.pv_set_lineEdit.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Press Enter after input</p></body></html>"
            ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
