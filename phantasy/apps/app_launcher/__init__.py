# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import AppLauncherWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Global Launcher for FRIB Physics Apps"
__version__ = '3.0'


def run(cli=False):
    app = QApplication(sys.argv)
    arg = sys.argv
    if '--log' in arg:
        logfile = arg[arg.index('--log') + 1]
    else:
        logfile = None

    w = AppLauncherWindow(version=__version__, logfile=logfile)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
