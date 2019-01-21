# -*- coding: utf8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from .app import AllisonScannerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '0.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = AllisonScannerWindow(version=__version__)
    w.show()
    w.setWindowTitle("Allison Scanner Application")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
