#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from phantasy_ui import BaseAppForm

from .ui.ui_app import Ui_MainWindow


class ImageViewerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):

        super(ImageViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Image Viewer")

        # set app properties
        self.setAppTitle("Image Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Image Viewer</h4>
            <p>This app is created for image data visualization,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

