#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QAbstractScrollArea

from collections import OrderedDict

try:
    basestring
except NameError:
    basestring = str

COLUMN_NAMES1 = ['Device', 'Field', 'Setting']
COLUMN_SFIELD_MAP = OrderedDict((
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
    ('Length [m]', 'length'),
    ('Index', 'index'),
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = COLUMN_NAMES1 + COLUMN_NAMES_ATTR


class SettingsModel(QStandardItemModel):
    """Settings model from Settings instance.

    Parameters
    ----------
    flat_settings : list
        List of setting with the format of ``(elem, fname, fval0)``,
        ``elem`` is CaElement object, ``fname`` is field name, ``fval0`` is
        saved field value.
    """
    def __init__(self, parent, flat_settings):
        super(self.__class__, self).__init__(parent)
        self._settings = flat_settings
        self._tv = parent

        # header
        self.header = self.h_name, self.h_field, self.h_val0, \
                self.h_type, self.h_pos, self.h_len, self.h_index \
                = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_val0, \
                self.i_type, self.i_pos, self.i_len, self.i_index \
                = range(len(self.header))

        # set data (pure)
        self.set_data()

        # set headers
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

    def set_data(self):
        for elem, fname, fval0 in self._settings:
            item0 = QStandardItem(elem.name)
            item1 = QStandardItem(fname)
            item2 = QStandardItem('{:.4f}'.format(fval0))
            row = [item0, item1, item2]
            for i, f in enumerate(COLUMN_NAMES):
                if f in COLUMN_NAMES_ATTR:
                    v = getattr(elem, COLUMN_SFIELD_MAP[f])
                    if i == self.i_index:
                        v = '{0:04d}'.format(v)
                    if not isinstance(v, basestring):
                        v = '{0:.4f}'.format(v)
                    item = QStandardItem(v)
                    row.append(item)
            self.appendRow(row)

    def set_model(self):
        # set model, set field column
        self._tv.setModel(self)
        self.__post_init_ui()

    def __post_init_ui(self):
        # view properties
        tv = self._tv
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        tv.setSortingEnabled(True)
        tv.resizeColumnToContents(self.i_name)
        self.sort(self.i_index, Qt.AscendingOrder)
        tv.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


