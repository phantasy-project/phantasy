# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot_results.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 900)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.matplotlibimageWidget = MatplotlibImageWidget(Form)
        font = QtGui.QFont()
        font.setFamily("aakar")
        font.setPointSize(14)
        self.matplotlibimageWidget.setFigureXYlabelFont(font)
        self.matplotlibimageWidget.setProperty("figureToolbarToggle", False)
        self.matplotlibimageWidget.setAutoColorLimit(True)
        self.matplotlibimageWidget.setObjectName("matplotlibimageWidget")
        self.verticalLayout.addWidget(self.matplotlibimageWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.matplotlibimageWidget.setFigureAspectRatio(
            _translate("Form", "auto"))
        self.matplotlibimageWidget.setFigureXlabel(
            _translate("Form", "$x\\,\\mathrm{[mm]}$"))
        self.matplotlibimageWidget.setFigureYlabel(
            _translate("Form", "$x\'\\,\\mathrm{[mrad]}$"))


from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
