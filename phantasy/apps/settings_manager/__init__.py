# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '0.2'


def run(cli=False):
    app = QApplication(sys.argv)
    w = SettingsManagerWindow(version=__version__)
    w.show()
    w.setWindowTitle("Settings Manager for Accelerator System")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
