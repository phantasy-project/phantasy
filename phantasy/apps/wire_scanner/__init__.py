# -*- coding: utf8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from .app import WireScannerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '2.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = WireScannerWindow(version=__version__)
    w.show()
    w.setWindowTitle("Wire Scanner (Profile Monitor) Application")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
