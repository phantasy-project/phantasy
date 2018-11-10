# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_array_set.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(874, 594)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.vfrom_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.vfrom_lineEdit.setObjectName("vfrom_lineEdit")
        self.horizontalLayout.addWidget(self.vfrom_lineEdit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.vto_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.vto_lineEdit.setObjectName("vto_lineEdit")
        self.horizontalLayout.addWidget(self.vto_lineEdit)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.vstep_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.vstep_lineEdit.setObjectName("vstep_lineEdit")
        self.horizontalLayout.addWidget(self.vstep_lineEdit)
        self.generate_btn = QtWidgets.QPushButton(Dialog)
        self.generate_btn.setObjectName("generate_btn")
        self.horizontalLayout.addWidget(self.generate_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.sort_asc_tbtn = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sort_asc_tbtn.sizePolicy().hasHeightForWidth())
        self.sort_asc_tbtn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/sort-asc.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.sort_asc_tbtn.setIcon(icon)
        self.sort_asc_tbtn.setObjectName("sort_asc_tbtn")
        self.horizontalLayout_3.addWidget(self.sort_asc_tbtn)
        self.sort_desc_tbtn = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sort_desc_tbtn.sizePolicy().hasHeightForWidth())
        self.sort_desc_tbtn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/sort-desc.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.sort_desc_tbtn.setIcon(icon1)
        self.sort_desc_tbtn.setObjectName("sort_desc_tbtn")
        self.horizontalLayout_3.addWidget(self.sort_desc_tbtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.data_textEdit = QtWidgets.QTextEdit(Dialog)
        self.data_textEdit.setReadOnly(False)
        self.data_textEdit.setObjectName("data_textEdit")
        self.verticalLayout.addWidget(self.data_textEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.import_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.import_btn.sizePolicy().hasHeightForWidth())
        self.import_btn.setSizePolicy(sizePolicy)
        self.import_btn.setObjectName("import_btn")
        self.horizontalLayout_2.addWidget(self.import_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_btn.sizePolicy().hasHeightForWidth())
        self.cancel_btn.setSizePolicy(sizePolicy)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ok_btn.sizePolicy().hasHeightForWidth())
        self.ok_btn.setSizePolicy(sizePolicy)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.data_textEdit.textChanged.connect(Dialog.on_text_changed)
        self.sort_asc_tbtn.clicked.connect(Dialog.on_sort_array)
        self.sort_desc_tbtn.clicked.connect(Dialog.on_sort_array)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.vfrom_lineEdit, self.vto_lineEdit)
        Dialog.setTabOrder(self.vto_lineEdit, self.vstep_lineEdit)
        Dialog.setTabOrder(self.vstep_lineEdit, self.generate_btn)
        Dialog.setTabOrder(self.generate_btn, self.sort_asc_tbtn)
        Dialog.setTabOrder(self.sort_asc_tbtn, self.sort_desc_tbtn)
        Dialog.setTabOrder(self.sort_desc_tbtn, self.data_textEdit)
        Dialog.setTabOrder(self.data_textEdit, self.import_btn)
        Dialog.setTabOrder(self.import_btn, self.cancel_btn)
        Dialog.setTabOrder(self.cancel_btn, self.ok_btn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "From"))
        self.label_2.setText(_translate("Dialog", "To"))
        self.label_3.setText(_translate("Dialog", "of Step"))
        self.generate_btn.setText(_translate("Dialog", "Generate"))
        self.sort_asc_tbtn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p> Sort array ascendingly</p></body></html>"
            ))
        self.sort_asc_tbtn.setText(_translate("Dialog", "Sort"))
        self.sort_desc_tbtn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Sort array descendingly</p></body></html>"
            ))
        self.sort_desc_tbtn.setText(_translate("Dialog", "Sort"))
        self.data_textEdit.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Manual changes on the text also updates the alter array</p></body></html>"
            ))
        self.import_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Import from external data file, single column of data</p></body></html>"
            ))
        self.import_btn.setText(_translate("Dialog", "Import"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
        self.ok_btn.setText(_translate("Dialog", "OK"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
