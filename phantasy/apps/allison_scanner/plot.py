#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from numpy import ndarray
from .data import draw_beam_ellipse_with_params

from .ui.ui_plot_region import Ui_Form


class PlotWidget(QWidget, Ui_Form):

    data_changed = pyqtSignal(ndarray)
    boundary_changed = pyqtSignal(ndarray)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__()
        self.setupUi(self)
        self._o1 = self.intensity_plot
        self._o2 = self.classification_plot
        self._ax1 = self._o1.axes
        self._ax2 = self._o2.axes
        self._parent = parent
        self._data = parent._data
        self._sf = self._parent._ellipse_sf
        self.plot()
        self.data_changed.connect(self._o1.update_image)
        self.boundary_changed.connect(self._o2.update_image)

    def plot(self):
        for o in (self._o1, self._o2):
            o.setXData(self._data.x_grid)
            o.setYData(self._data.xp_grid)

    @pyqtSlot(dict)
    def on_ellipse_updated(self, r):
        # updadte ellipse
        self._r = r
        self._update_plot()

    @pyqtSlot(float)
    def on_ellipse_size_updated(self, sf):
        # update ellipse size.
        self._sf = sf
        self._update_plot()

    def _update_plot(self):
        self._ax1.patches = []
        ellipse, _, _ = draw_beam_ellipse_with_params(
                            self._r, color='w', factor=self._sf,
                            ax=self._ax1)
        self._o1.update_figure()

        # update classification
        noise_signal_arr = self._data.tag_noise_signal(
                                ellipse=ellipse,
                                factor=1.0)
        self.boundary_changed.emit(noise_signal_arr)
        self._parent._noise_signal_arr = noise_signal_arr
