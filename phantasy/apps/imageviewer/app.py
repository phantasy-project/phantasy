#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import epics
from numpy import ndarray
from functools import partial
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from phantasy_ui import BaseAppForm

from .ui.ui_app import Ui_MainWindow


class ImageViewerWindow(BaseAppForm, Ui_MainWindow):

    image_data_changed = pyqtSignal(ndarray)

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

        #
        self.wf_pvname_lineEdit.returnPressed.connect(self.on_update_pv)
        self.xdim_lineEdit.returnPressed.connect(partial(self.on_update_dim, '_xdim'))
        self.ydim_lineEdit.returnPressed.connect(partial(self.on_update_dim, '_ydim'))
        self.image_data_changed.connect(self.matplotlibimageWidget.update_image)

    @pyqtSlot()
    def on_update_pv(self):
        self._pv = epics.PV(self.sender().text())
        #
        self.on_update_image()

    @pyqtSlot()
    def on_update_dim(self, attr_str):
        setattr(self, attr_str, int(self.sender().text()))

    def on_update_image(self):
        data = self._pv.get()
        xdim, ydim = self._xdim, self._ydim
        self.image_data_changed.emit(data.reshape(xdim, ydim))

