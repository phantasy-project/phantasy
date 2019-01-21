#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from phantasy_ui.templates import BaseAppForm


from .ui.ui_app import Ui_MainWindow


class AllisonScannerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(AllisonScannerWindow, self).__init__()

        # app version
        self._version = version

        # window title/version
        self.setWindowTitle("Allison Scanner App")

        # set app properties
        self.setAppTitle("Allison Scanner App")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Allison Scanner App</h4>
            <p>This app is created to ease the usage of allison-scanner
            devices, including the DAQ and post data analysis,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
