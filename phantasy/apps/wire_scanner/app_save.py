#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
from collections import OrderedDict
import time

from phantasy import epoch2human

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy.apps.utils import get_save_filename

from .ui.ui_save import Ui_Dialog

TS_FMT = "%Y-%m-%d %H:%M:%S"


class SaveDataDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(SaveDataDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Save Data To File(s)")

        # initial filepathes
        mdatapath = self.get_default_filepath(data_type='mdata')
        rdatapath = self.get_default_filepath(data_type='rdata')
        self.mdatapath_lineEdit.setText(mdatapath)
        self.rdatapath_lineEdit.setText(rdatapath)

        # default save option
        # self.save_all_combined_rbtn.setChecked(True)
        self.save_all_separated_rbtn.setChecked(True)

    @pyqtSlot()
    def on_save_data(self):
        """Save data.
        """
        print("SaveDataDialog: save data")

        if self.save_mdata_rbtn.isChecked():
            # only save mdata
            self.__save_mdata()
        elif self.save_rdata_rbtn.isChecked():
            # only save rdata
            self.__save_rdata()
        elif self.save_all_combined_rbtn.isChecked():
            # save all into one file
            self.__save_all_combined()
        elif self.save_all_separated_rbtn.isChecked():
            # save all into two files
            self.__save_mdata()
            self.__save_rdata()

    def __save_all_combined(self):
        filepath = self.rdatapath_lineEdit.text()
        mdata = self.parent._detailed_mdata
        rdata = self.parent._detailed_rdata
        mdata.update(rdata)
        self.__detail_more(mdata)
        self.__save_data_to_file(mdata, filepath)

    def __save_rdata(self):
        filepath = self.rdatapath_lineEdit.text()
        data = self.parent._detailed_rdata
        self.__detail_more(data)
        self.__save_data_to_file(data, filepath)

    def __save_mdata(self):
        filepath = self.mdatapath_lineEdit.text()
        data = self.parent._detailed_mdata
        self.__detail_more(data)
        self.__save_data_to_file(data, filepath)

    def __detail_more(self, data):
        # add other info to data
        ctime = epoch2human(time.time(), fmt=TS_FMT)
        info_dict = OrderedDict()
        info_dict['created'] = ctime
        data.update({'info': info_dict})

    def __save_data_to_file(self, data, filepath):
        # save data to filepath as .json format.
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)
        except:
            QMessageBox.critical(self, "Save Data",
                    "Failed to save data to {}.".format(filepath),
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Data",
                    "Successfully saved data to {}.".format(filepath),
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_get_mdata_savepath(self):
        """Select filepath for measured data.
        """
        print("SaveDataDialog: get mdatapath")
        cdir = os.path.dirname(self.mdatapath_lineEdit.text())
        filepath, ext = get_save_filename(self,
                cdir=cdir,
                filter="JSON Files (*.json)")
        if filepath is None:
            return
        self.mdatapath_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_get_rdata_savepath(self):
        """Select filepath for analyzed results data.
        """
        print("SaveDataDialog: get rdatapath")
        cdir = os.path.dirname(self.rdatapath_lineEdit.text())
        filepath, ext = get_save_filename(self,
                cdir=cdir,
                filter="JSON Files (*.json)")
        if filepath is None:
            return
        self.rdatapath_lineEdit.setText(filepath)

    def get_default_filepath(self, data_type="mdata"):
        """Return default filepath for saving, including two cases:
        1. device_mode (or operation mode) is "simulation":
            ts inherits from loaded file path
        2. device mode (or operation mode) is "live":
            ts is generated from current timestamp
        """
        try:
            cts = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            mode = self.parent._device_mode
            # loaded data filepath, simulation mode
            datafilename = os.path.basename(
                    self.parent.data_filepath_lineEdit.text())
            ename = self.parent._ws_data.device.elem.name.replace(':', '_')
            if mode == 'live':
                ts = cts
            else:
                m = re.match(r'.*([0-9]{8}_[0-9]{6}).*', datafilename)
                if m is not None:
                    ts = m.group(1)
                else:
                    ts = cts
            if data_type == 'mdata':
                filepath = '{}_{}_mdata.json'.format(ename, ts)
            elif data_type == 'rdata':
                filepath = '{}_{}_rdata.json'.format(ename, ts)
        except:
            filepath = ''
        return os.path.abspath(
                os.path.expanduser(os.path.join('~', filepath)))


