#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import epics
from numpy import ndarray
import time
from functools import partial
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import DataAcquisitionThread as DAQT

from .ui.ui_app import Ui_MainWindow


class ImageViewerWindow(BaseAppForm, Ui_MainWindow):

    image_data_changed = pyqtSignal(ndarray)

    viz_cnt_max_reached = pyqtSignal()

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
        self.daq_start_btn.clicked.connect(self.on_daq_started)
        self.daq_stop_btn.clicked.connect(self.on_daq_stopped)
        self.xdim_sbox.valueChanged.connect(partial(self.on_update_value, '_xdim'))
        self.ydim_sbox.valueChanged.connect(partial(self.on_update_value, '_ydim'))
        self.daq_rate_dsbox.valueChanged.connect(partial(self.on_update_value, '_daq_rate'))
        self.viz_cnt_max_sbox.valueChanged.connect(partial(self.on_update_value, '_viz_cnt_max'))
        self.image_data_changed.connect(self.matplotlibimageWidget.update_image)
        self.viz_cnt_max_reached.connect(self.on_daq_stopped)

        #
        self._post_init()

    def _post_init(self):
        for o in (self.xdim_sbox, self.ydim_sbox,
                  self.daq_rate_dsbox, self.viz_cnt_max_sbox):
            o.valueChanged.emit(o.value())

        self._daq_stop = False
        self._viz_active_px = QPixmap(":/icons/active.png")
        self._viz_inactive_px = QPixmap(":/icons/inactive.png")
        self._viz_cnt = 0

    @pyqtSlot()
    def on_update_pv(self):
        try:
            self._pv = epics.PV(self.sender().text())
        except:
            QMessageBox.warning(self, "PV Warning",
                    "CA connection cannot be established.",
                    QMessageBox.Ok)
        else:
            self.on_update_image()


    def on_update_value(self, attr_str, v):
        setattr(self, attr_str, v)

    def on_update_image(self):
        data = self._pv.get()
        self.update_image(data)

    def update_image(self, data):
        try:
            m = data.reshape(self._ydim, self._xdim)
            import numpy as np
            m = np.flipud(m)
        except (ValueError, AttributeError) as e:
            QMessageBox.critical(self, "Data Reshaping Error", str(e),
                              QMessageBox.Ok)
            return
        else:
            self.image_data_changed.emit(m)

    @pyqtSlot()
    def on_daq_started(self):
        if self._daq_stop:
            self.set_widgets_status("STOP")
            return

        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(1))
        self.daq_th.started.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.finished.connect(self.on_daq_started)
        self.daq_th.start()

    def on_daq_results_ready(self, r):
        data = r[0]
        self.update_image(data)

    def daq_single(self, iiter):
        t0 = time.time()
        data = self._pv.get()
        dt = time.time() - t0
        print("Execution Time: {} ms".format(dt * 1000))
        time.sleep(1.0 / self._daq_rate - dt)
        return data

    def on_update_daq_status(self, f, s):
        # beat DAQ viz status
        if f == 1.0:
            px = self._viz_active_px
            self._viz_cnt += 1
            self.viz_cnt_lbl.setText(str(self._viz_cnt))
        else:
            px = self._viz_inactive_px
        self.daq_status_lbl.setPixmap(px)
        QTimer.singleShot(200,
                lambda:self.daq_status_lbl.setPixmap(self._viz_inactive_px))
#        if self._daq_nshot > 1:
#            self.daq_pb.setValue(f * 100)
        if self._viz_cnt_max != 0 and self._viz_cnt == self._viz_cnt_max:
            self.viz_cnt_max_reached.emit()

    def set_widgets_status(self, status):
        olist1 = (self.daq_start_btn,)
        olist2 = (self.daq_stop_btn, )
        if status != "START":
            [o.setEnabled(True) for o in olist1]
            [o.setEnabled(False) for o in olist2]
        else:
            [o.setEnabled(False) for o in olist1]
            [o.setEnabled(True) for o in olist2]

    @pyqtSlot()
    def on_daq_stopped(self):
        self._daq_stop = True
        QTimer.singleShot(2000, self.reset)

    def reset(self):
        self._daq_stop = False
        self._viz_cnt = 0

