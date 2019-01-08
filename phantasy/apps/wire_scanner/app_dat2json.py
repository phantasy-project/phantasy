#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import get_save_filename
from .ui.ui_dat2json import Ui_Dialog
from .converter import read_from_datfile
from .converter import save_to_jsonfile


class Dat2JsonDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dat2JsonDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("PM Data Converter")

    @pyqtSlot()
    def on_open_datfile(self):
        print("open datfile")
        filepath, ext = get_open_filename(self,
                filter="Dat Files (*.dat)")
        if filepath is None:
            return
        self.datfilepath_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_save_jsonfile(self):
        print("save jsonfile")
        filepath, ext = get_save_filename(self,
                filter="JSON Files (*.json)")
        if filepath is None:
            return
        self.jsonfilepath_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_locate_datfile(self):
        print("locate datfile")
        filepath = self.datfilepath_lineEdit.text()
        QDesktopServices.openUrl(QUrl(filepath))

    @pyqtSlot()
    def on_locate_jsonfile(self):
        print("locate jsonfile")
        filepath = self.jsonfilepath_lineEdit.text()
        QDesktopServices.openUrl(QUrl(filepath))

    @pyqtSlot()
    def on_convert_file(self):
        print("convert data file")
        datfilepath = self.datfilepath_lineEdit.text()
        jsonfilepath = self.jsonfilepath_lineEdit.text()
        try:
            data_dict = read_from_datfile(datfilepath)
            if not data_dict: raise RuntimeError
            save_to_jsonfile(jsonfilepath, data_dict)
        except:
            QMessageBox.critical(self, "Data Converter",
                    "Failed to convert dat file.", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Data Converter",
                    "Successfully convert to json.", QMessageBox.Ok)
