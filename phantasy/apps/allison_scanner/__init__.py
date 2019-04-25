# -*- coding: utf8 -*-

import sys

import cothread
from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .app import AllisonScannerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Allison Scanner: Beam Twiss Parameters Measurement"
__version__ = '0.1'


def run():
    set_mplstyle(sys.argv)
    QApplication(sys.argv)()
    w = AllisonScannerWindow(version=__version__)
    w.show()
    w.setWindowTitle(__title__)
    cothread.WaitForQuit()
