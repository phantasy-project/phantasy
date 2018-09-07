#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_app import Ui_MainWindow
from phantasy_ui.templates import BaseAppForm


class LatticeViewerWindow(BaseAppForm, Ui_MainWindow):
    def __init__(self, version):
        super(LatticeViewerWindow, self).__init__()
        
        # app version
        self._version = version
        
        # window title
        self.setWindowTitle("Lattice Viewer")

        # set app properties
        self.setAppTitle("Lattice Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Lattice Viewer</h4>
            <p>This app is created to visualize the FRIB accelerator
            hierarchical structure, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = LatticeViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
