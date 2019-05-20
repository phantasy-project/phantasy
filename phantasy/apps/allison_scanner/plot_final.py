#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget

from .data import draw_beam_ellipse_with_params
from .ui.ui_plot_results import Ui_Form


class PlotResults(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(PlotResults, self).__init__()
        self.setupUi(self)
        self._o = self.matplotlibimageWidget
        self._ax = self._o.axes
        self._parent = parent
        self._data = parent._data

    @property
    def results(self):
        return self._r

    @results.setter
    def results(self, r):
        self._r = r

    def plot_data(self):
        m = self._parent.matplotlibimageWidget.get_data()
        self._o.setXData(self._data.x_grid)
        self._o.setYData(self._data.xp_grid)
        self._o.update_image(m)
        self._data.plot(m, results=self._r, ax=self._ax, image_on=False,
                profile_on=True, profile_opt={'lw': 1.5, 'color': 'w'},
                ellipse_on=True, ellipse_opt={'c': 'w', 'color': 'w'})
        # results
        self._show_results(self._r)

    def _show_results(self, r):
        for k in r:
            if k.startswith('alpha'):
                u = k[-1]
                break

        ks = '{u}_cen,{u}p_cen,{u}_rms,{u}p_rms,alpha_{u},beta_{u},gamma_{u},emit_{u},emitn_{u}'.format(u=u).split(',')
        names = ["{}<sub>{}</sub>".format(i, j) for (i, j) in
                 zip((u, u + "'", '&sigma;', '&sigma;', '&alpha;',
                     '&beta;', '&gamma;', '&epsilon;', '&epsilon;'),
                     (0, 0, u, u + "'", u, u, u, u, u + '<sup>n</sup>',))]
        us = ("mm", "mrad", "mm", "mrad", "", "m", "m<sup>-1</sup>", "mm&middot;mrad", "mm&middot;mrad")

        s =['<h5>{0:<3s} = {1:.6f} {2}<h5>'.format(n, r.get(k), ui) for (n, k, ui) in zip(names, ks, us)]
        self.textEdit.setHtml("<html>{}</html>".format(''.join(s)))
