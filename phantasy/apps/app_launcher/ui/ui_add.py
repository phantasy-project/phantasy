# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 320)
        Dialog.setStyleSheet("QLineEdit, QTextEdit {\n"
                             "    border: 0.5px solid gray;\n"
                             "    padding: 1 5px;\n"
                             "    border-radius: 3px;\n"
                             "}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.desc_textEdit = QtWidgets.QTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.desc_textEdit.sizePolicy().hasHeightForWidth())
        self.desc_textEdit.setSizePolicy(sizePolicy)
        self.desc_textEdit.setObjectName("desc_textEdit")
        self.gridLayout.addWidget(self.desc_textEdit, 1, 2, 4, 3)
        self.cmd_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cmd_lineEdit.sizePolicy().hasHeightForWidth())
        self.cmd_lineEdit.setSizePolicy(sizePolicy)
        self.cmd_lineEdit.setObjectName("cmd_lineEdit")
        self.gridLayout.addWidget(self.cmd_lineEdit, 5, 2, 1, 3)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop
                                  | QtCore.Qt.AlignTrailing)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(383, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 3)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 6, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 4, 1, 1)
        self.name_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.name_lineEdit.sizePolicy().hasHeightForWidth())
        self.name_lineEdit.setSizePolicy(sizePolicy)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.gridLayout.addWidget(self.name_lineEdit, 0, 2, 1, 3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.icon_btn = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.icon_btn.sizePolicy().hasHeightForWidth())
        self.icon_btn.setSizePolicy(sizePolicy)
        self.icon_btn.setMinimumSize(QtCore.QSize(64, 64))
        self.icon_btn.setMaximumSize(QtCore.QSize(64, 64))
        self.icon_btn.setBaseSize(QtCore.QSize(64, 64))
        self.icon_btn.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/app3.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.icon_btn.setIcon(icon)
        self.icon_btn.setIconSize(QtCore.QSize(64, 64))
        self.icon_btn.setObjectName("icon_btn")
        self.horizontalLayout.addWidget(self.icon_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 3, 1)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.on_click_ok)
        self.pushButton_2.clicked.connect(Dialog.reject)
        self.icon_btn.clicked.connect(Dialog.on_select_icon)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Name"))
        self.desc_textEdit.setPlaceholderText(
            _translate(
                "Dialog",
                "Description to the app, brief introduction or helpful guideline..."
            ))
        self.cmd_lineEdit.setPlaceholderText(
            _translate("Dialog", "Command to execute to start the app..."))
        self.label_3.setText(_translate("Dialog", "Executable"))
        self.label_2.setText(_translate("Dialog", "Description"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.name_lineEdit.setPlaceholderText(
            _translate("Dialog",
                       "Name of the application or launcher entry..."))
        self.label_4.setText(_translate("Dialog", "Icon"))
        self.icon_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Select a PNG file as the icon.</p></body></html>"
            ))
        self.icon_btn.setText(_translate("Dialog", "..."))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
