# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot_region.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.intensity_plot = MatplotlibImageWidget(Form)
        self.intensity_plot.setProperty("figureToolbarToggle", False)
        self.intensity_plot.setProperty("reseverColorMap", False)
        self.intensity_plot.setAutoColorLimit(True)
        self.intensity_plot.setObjectName("intensity_plot")
        self.gridLayout.addWidget(self.intensity_plot, 0, 0, 1, 1)
        self.classification_plot = MatplotlibImageWidget(Form)
        self.classification_plot.setProperty("figureToolbarToggle", False)
        self.classification_plot.setObjectName("classification_plot")
        self.gridLayout.addWidget(self.classification_plot, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.intensity_plot.setFigureAspectRatio(_translate("Form", "auto"))
        self.intensity_plot.setFigureXlabel(
            _translate("Form", "$x\\,\\mathrm{[mm]}$"))
        self.intensity_plot.setFigureYlabel(
            _translate("Form", "$x\'\\,\\mathrm{[mrad]}$"))
        self.intensity_plot.setFigureTitle(
            _translate("Form", "Intensity Distribution"))
        self.classification_plot.setFigureAspectRatio(
            _translate("Form", "auto"))
        self.classification_plot.setFigureXlabel(
            _translate("Form", "$x\\,\\mathrm{[mm]}$"))
        self.classification_plot.setFigureYlabel(
            _translate("Form", "$x\'\\,\\mathrm{[mrad]}$"))
        self.classification_plot.setFigureTitle(
            _translate("Form", "Signal/Noise Classification"))


from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
