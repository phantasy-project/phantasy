#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from phantasy.apps.utils import get_save_filename

from .ui.ui_save import Ui_Dialog


class SaveDataDialog(QDialog, Ui_Dialog):

    def __init__(self, parent):
        super(SaveDataDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Save Data To File(s)")

        #
        self._post_init()

    def _post_init(self):
        # check figure and settings options
        self.save_figure_chkbox.setChecked(True)
        self.save_settings_chkbox.setChecked(True)

        # all segs
        all_segs = ("LEBT", "MEBT", "MEBT2FS1A", "MEBT2FS1B", )
        self._all_segs_chkbox = [
            getattr(self, "{}_chkbox".format(s.lower())) for s in all_segs]
        self._selected_segs = []

        for o in self._all_segs_chkbox:
            o.toggled.connect(self.on_update_segs)
            o.setChecked(True)

        # figure format
        self.figure_format_cbb.currentTextChanged.connect(
                self.on_update_figure_filepath)

    @pyqtSlot('QString')
    def on_update_figure_filepath(self, fmt):
        filepath_name = self.figure_filepath_lineEdit.text().rsplit('.', 1)[0]
        filepath = '{}.{}'.format(filepath_name, fmt)
        self.figure_filepath_lineEdit.setText(filepath)

    @pyqtSlot(bool)
    def on_update_segs(self, checked):
        s = self.sender().text()
        if checked:
            self._selected_segs.append(s)
        else:
            self._selected_segs.remove(s)
        print(self._selected_segs)

    @pyqtSlot()
    def on_save_data(self):
        print("SaveDataDialog: Save Data")

    @pyqtSlot()
    def on_get_filepath(self):
        print("SaveDataDialog: Get filepath")
        cdir = os.path.dirname(self.filepath_lineEdit.text())
        filepath, ext = get_save_filename(self,
                cdir=cdir,
                filter="CSV Files (*.csv)")
        if filepath is None:
            return
        self.filepath_lineEdit.setText(filepath)
        self.on_update_filepaths()

    @pyqtSlot()
    def on_update_filepaths(self):
        # update all filepaths.
        try:
            fname, ext = self.filepath_lineEdit.text().rsplit('.', 1)
        except ValueError:
            return

        # fig
        fig_fmt = self.figure_format_cbb.currentText()
        figure_filepath = '{}.{}'.format(fname, fig_fmt)
        self.figure_filepath_lineEdit.setText(figure_filepath)

        # settings
        settings_filepath = fname + '.json'
        self.settings_filepath_lineEdit.setText(settings_filepath)
