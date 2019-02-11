# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import AppLauncherWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '2.0'


def run(cli=False):
    app = QApplication(sys.argv)
    w = AppLauncherWindow(version=__version__)
    w.show()
    w.setWindowTitle("FRIB Physics Applications Launcher")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
