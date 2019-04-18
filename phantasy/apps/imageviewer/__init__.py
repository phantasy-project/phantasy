# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import ImageViewerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "ImageViewer: Yet Another Viewer for Image"
__version__ = '0.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = ImageViewerWindow(version=__version__)
    w.setWindowTitle(__title__)
    w.show()
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
