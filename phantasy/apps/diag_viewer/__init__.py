# -*- coding: utf8 -*-

import matplotlib.style as mplstyle

import sys
from phantasy_ui import QApp as QApplication

from .app import DeviceViewerWindow

DEFALT_MSTYLE = 'fivethirtyeight'


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '1.1'


def run(cli=False):
    arg = sys.argv
    mstyle = DEFALT_MSTYLE
    if '--mpl-style' in arg:
        mstyle = arg[arg.index('--mpl-style') + 1]
        if mstyle not in mplstyle.available:
            mstyle = DEFALT_MSTYLE
    mplstyle.use(mstyle)
    app = QApplication(sys.argv)
    w = DeviceViewerWindow(version=__version__)
    w.show()
    w.setWindowTitle("Device Viewer: Visualize Device Readings and Settings")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
