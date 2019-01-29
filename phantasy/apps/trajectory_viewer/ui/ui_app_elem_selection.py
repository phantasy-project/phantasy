# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_elem_selection.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setStyleSheet(
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
            "}")
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.listed_nelem_lineEdit = QtWidgets.QLineEdit(Form)
        self.listed_nelem_lineEdit.setReadOnly(True)
        self.listed_nelem_lineEdit.setObjectName("listed_nelem_lineEdit")
        self.horizontalLayout.addWidget(self.listed_nelem_lineEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.selected_nelem_lineEdit = QtWidgets.QLineEdit(Form)
        self.selected_nelem_lineEdit.setReadOnly(True)
        self.selected_nelem_lineEdit.setObjectName("selected_nelem_lineEdit")
        self.horizontalLayout.addWidget(self.selected_nelem_lineEdit)
        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.dtypes_groupBox = QtWidgets.QGroupBox(Form)
        self.dtypes_groupBox.setCheckable(False)
        self.dtypes_groupBox.setChecked(False)
        self.dtypes_groupBox.setObjectName("dtypes_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.dtypes_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.dtypes_gridLayout = QtWidgets.QGridLayout()
        self.dtypes_gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.dtypes_gridLayout.setObjectName("dtypes_gridLayout")
        self.toggle_all_dtypes_chkbox = QtWidgets.QCheckBox(
            self.dtypes_groupBox)
        self.toggle_all_dtypes_chkbox.setObjectName("toggle_all_dtypes_chkbox")
        self.dtypes_gridLayout.addWidget(self.toggle_all_dtypes_chkbox, 0, 0,
                                         1, 1)
        self.gridLayout.addLayout(self.dtypes_gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.dtypes_groupBox, 0, 0, 1, 1)
        self.treeView = QtWidgets.QTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.gridLayout_3.addWidget(self.treeView, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.toggle_all_dtypes_chkbox.toggled['bool'].connect(
            Form.on_toggle_all_dtypes)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Total Listed Elements"))
        self.label_2.setText(_translate("Form", "Selected Elements"))
        self.dtypes_groupBox.setTitle(
            _translate("Form", "Filter by Device Types"))
        self.toggle_all_dtypes_chkbox.setText(_translate("Form", "All"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
