# -*- coding: utf8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from .app import QuadScanWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '1.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = QuadScanWindow(version=__version__)
    w.show()
    w.setWindowTitle("Quadrupole Scan App")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
