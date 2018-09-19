#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_app import Ui_MainWindow
#from .app_help import HelpDialog
#from .icons import tv_icon
from phantasy_ui.templates import BaseAppForm


class CorrelationVisualizerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(CorrelationVisualizerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Correlation Visualizer")
        # self.setWindowIcon(QIcon(QPixmap(icon)))

        # set app properties
        self.setAppTitle("Correlation Visualizer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Correlation Visualizer</h4>
            <p>This app is created to visualize the correlation between
            selected parameters, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
