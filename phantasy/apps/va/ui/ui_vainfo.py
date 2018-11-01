# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vainfo.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(533, 184)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pid_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pid_label.sizePolicy().hasHeightForWidth())
        self.pid_label.setSizePolicy(sizePolicy)
        self.pid_label.setStyleSheet("QLabel {\n"
                                     "    background-color: white;\n"
                                     "    padding: 3px 3px;\n"
                                     "    border: 1px solid gray;\n"
                                     "    border-radius: 4px;\n"
                                     "}")
        self.pid_label.setText("")
        self.pid_label.setObjectName("pid_label")
        self.gridLayout.addWidget(self.pid_label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cpu_label = QtWidgets.QLabel(Form)
        self.cpu_label.setStyleSheet("QLabel {\n"
                                     "    background-color: white;\n"
                                     "    padding: 3px 3px;\n"
                                     "    border: 1px solid gray;\n"
                                     "    border-radius: 4px;\n"
                                     "}")
        self.cpu_label.setText("")
        self.cpu_label.setObjectName("cpu_label")
        self.gridLayout.addWidget(self.cpu_label, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.mem_label = QtWidgets.QLabel(Form)
        self.mem_label.setStyleSheet("QLabel {\n"
                                     "    background-color: white;\n"
                                     "    padding: 3px 3px;\n"
                                     "    border: 1px solid gray;\n"
                                     "    border-radius: 4px;\n"
                                     "}")
        self.mem_label.setText("")
        self.mem_label.setObjectName("mem_label")
        self.gridLayout.addWidget(self.mem_label, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.cmdline_label = QtWidgets.QLabel(Form)
        self.cmdline_label.setStyleSheet("QLabel {\n"
                                         "    background-color: white;\n"
                                         "    padding: 3px 3px;\n"
                                         "    border: 1px solid gray;\n"
                                         "    border-radius: 4px;\n"
                                         "}")
        self.cmdline_label.setText("")
        self.cmdline_label.setObjectName("cmdline_label")
        self.gridLayout.addWidget(self.cmdline_label, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "PID"))
        self.label_2.setText(_translate("Form", "CPU"))
        self.label_3.setText(_translate("Form", "Memory"))
        self.label_4.setText(_translate("Form", "Command"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
