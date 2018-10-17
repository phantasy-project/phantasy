# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from .app import UnicornApp

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '1.3'


def run(cli=False):
    app = QApplication(sys.argv)
    w = UnicornApp(version=__version__)
    w.show()
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
