# -*- coding: utf8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from .app import CorrelationVisualizerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '3.2'


def run(cli=False):
    app = QApplication(sys.argv)
    w = CorrelationVisualizerWindow(version=__version__)
    w.show()
    #w.setWindowTitle("Parameters Correlation Analysis and Visualization")
    w.setWindowTitle("Generic Parameters Scan Analysis Application")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
