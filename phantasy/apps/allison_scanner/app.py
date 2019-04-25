#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

import numpy as np
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from numpy import ndarray
from phantasy_ui.templates import BaseAppForm

from phantasy import Configuration
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import get_save_filename
from .device import Device
from .ui.ui_app import Ui_MainWindow
from .utils import find_dconf
from .utils import get_all_devices


class AllisonScannerWindow(BaseAppForm, Ui_MainWindow):
    image_data_changed = pyqtSignal(ndarray)

    def __init__(self, version):
        super(AllisonScannerWindow, self).__init__()

        # app version
        self._version = version

        # window title/version
        self.setWindowTitle("Allison Scanner App")

        # set app properties
        self.setAppTitle("Allison Scanner App")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Allison Scanner App</h4>
            <p>This app is created to ease the usage of allison-scanner
            devices, including the DAQ and post data analysis,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        self.image_data_changed.connect(self.matplotlibimageWidget.update_image)

        self._post_init()

    def _post_init(self):
        #
        self.installed_px = QPixmap(":/icons/installed.png")
        self.not_installed_px = QPixmap(":/icons/not-installed.png")
        # conf
        self._dconf = self.get_device_config()

        # orientation
        self._ems_orientation = 'X'
        self.ems_orientation_cbb.currentTextChanged.connect(self.on_update_orientation)

        # init EMS devices
        all_devices_dict = get_all_devices()
        self._all_devices_dict = all_devices_dict
        self.ems_names_cbb.addItems(all_devices_dict)
        self.ems_names_cbb.currentTextChanged.connect(self.on_device_changed)

        # pos
        for s in ['{}_{}'.format(u, v) for u in ('pos', 'volt')
                  for v in ('begin', 'end', 'step', 'settling_time')]:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.connect(partial(self.on_update_config, s))

        #
        self.ems_names_cbb.currentTextChanged.emit(self.ems_names_cbb.currentText())
        #
        for o in self.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

    @pyqtSlot(float)
    def on_update_config(self, attr, x):
        setattr(self._ems_device, attr, x)
        self._dconf = self._ems_device.dconf

    @pyqtSlot('QString')
    def on_update_orientation(self, s):
        self._ems_orientation = s
        try:
            self._ems_device.xoy = s
            self.show_default_config()
        except:
            pass

    def get_device_config(self, path=None):
        """Return device config from *path*.
        """
        path = find_dconf() if path is None else path
        dconf = Configuration(path)
        return dconf

    @pyqtSlot('QString')
    def on_device_changed(self, s):
        """Change device by selecting the name.
        """
        self._currnet_device_name = s
        self._current_device_elem = self._all_devices_dict[s]
        self.on_update_device()
        self.statusInfoChanged.emit("Selected device: {}".format(s))

    def on_update_device(self):
        # update ems device.
        ems = Device(self._current_device_elem, self._ems_orientation,
                     self._dconf)
        self._ems_device = ems

        if ems.info == "Installed":
            px = self.installed_px
            tt = "Device is ready to use"
        else:
            px = self.not_installed_px
            tt = "Device is not ready to use"
        self.info_lbl.setPixmap(px)
        self.info_lbl.setToolTip(tt)

        self.show_default_config()

    def show_default_config(self):
        """Show default loaded device config.
        """
        ems = self._ems_device
        self.length_lineEdit.setText(str(ems.length))
        self.length1_lineEdit.setText(str(ems.length1))
        self.length2_lineEdit.setText(str(ems.length2))
        self.gap_lineEdit.setText(str(ems.gap))
        self.slit_width_lineEdit.setText(str(ems.slit_width))
        self.slit_thickness_lineEdit.setText(str(ems.slit_thickness))
        #
        self.pos_begin_dsbox.setValue(ems.pos_begin)
        self.pos_end_dsbox.setValue(ems.pos_end)
        self.pos_step_dsbox.setValue(ems.pos_step)
        self.pos_settling_time_dsbox.setValue(ems.pos_settling_time)
        self.volt_begin_dsbox.setValue(ems.volt_begin)
        self.volt_end_dsbox.setValue(ems.volt_end)
        self.volt_step_dsbox.setValue(ems.volt_step)
        self.volt_settling_time_dsbox.setValue(ems.volt_settling_time)

    @pyqtSlot()
    def on_loadfrom_config(self):
        """Load configuration from a file.
        """
        filepath, ext = get_open_filename(self, filter="INI Files (*.ini)")
        if filepath is None:
            return

        try:
            dconf_copy = Configuration(self._dconf.config_path)
            self._dconf = Configuration(filepath)
        except:
            self._dconf = dconf_copy
            QMessageBox.warning(self, "Load Configuration",
                                "Failed to load configuration file from {}.".format(filepath),
                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Load Configuration",
                                    "Loaded configuration file from {}.".format(filepath),
                                    QMessageBox.Ok)
        finally:
            self.on_update_device()

        print("Load config from {}".format(filepath))

    @pyqtSlot()
    def on_saveas_config(self):
        """Save configuration to a file.
        """
        filepath, ext = get_save_filename(self, filter="INI Files (*.ini)")
        if filepath is None:
            return
        self.__save_config_to_file(filepath)
        print("Save config as {}".format(filepath))

    @pyqtSlot()
    def on_save_config(self):
        """Save configuration.
        """
        filepath = self._dconf.config_path
        self.__save_config_to_file(filepath)
        print("Save config to {}".format(filepath))

    def __save_config_to_file(self, filepath):
        try:
            self._ems_device.save_dconf(filepath)
        except:
            QMessageBox.warning(self, "Save Configuration",
                                "Failed to save configuration file to {}".format(filepath),
                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Configuration",
                                    "Saved configuration file to {}".format(filepath),
                                    QMessageBox.Ok)

    @pyqtSlot()
    def on_reload_config(self):
        """Reload configuration.
        """
        filepath = self._dconf.config_path

        self._dconf = Configuration(self._dconf.config_path)
        self.on_update_device()
        QMessageBox.information(self, "Reload Configuration",
                                "Reloaded configuration file from {}.".format(filepath),
                                QMessageBox.Ok)

        print("Reload config from {}".format(filepath))

    @pyqtSlot()
    def on_locate_config(self):
        """Locate (find and open) device configuration file path.
        """
        path = self._dconf.config_path
        QDesktopServices.openUrl(QUrl(path))

    @pyqtSlot()
    def on_run(self):
        from cothread.catools import camonitor, caput

        r = camonitor("EMS:ArrayData", self.on_update,
                      notify_disconnect=True)
        print(r)
        caput("EMS:TRIGGER_CMD", 1)
        self.i = 0

    def on_update(self, value):
        self.i += 1
        if self.i == 61:
            print
        m = value.reshape(501, 61)
        m = np.flipud(m)
        self.image_data_changed.emit(m)
