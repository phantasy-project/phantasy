# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import LatticeViewerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Lattice Viewer: Investigate Loaded Lattice"
__version__ = '1.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = LatticeViewerWindow(version=__version__)
    w.setWindowTitle(__title__)
    w.show()
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
