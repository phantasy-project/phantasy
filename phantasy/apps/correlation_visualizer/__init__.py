# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import CorrelationVisualizerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '3.4'


def run(cli=False):
    app = QApplication(sys.argv)
    w = CorrelationVisualizerWindow(version=__version__)
    w.show()
    #w.setWindowTitle("Parameters Correlation Analysis and Visualization")
    w.setWindowTitle(
        "Correlation Visualizer: Generic Parameters Scan and Correlation Analysis")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
