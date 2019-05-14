#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

import numpy as np
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from numpy import ndarray
from phantasy_ui.templates import BaseAppForm

from phantasy import Configuration
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import get_save_filename
from .device import Device
from ._sim import SimDevice
from .ui.ui_app import Ui_MainWindow
from .utils import find_dconf
from .utils import get_all_devices
from .model import Model
from .data import Data


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
            <p>This app is created for the operation of allison-scanner
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
        self._device_mode = "Live"
        #
        self.installed_px = QPixmap(":/icons/installed.png")
        self.not_installed_px = QPixmap(":/icons/not-installed.png")
        # conf
        self._dconf = self.get_device_config()

        # orientation
        self._ems_orientation = "X"
        self.ems_orientation_cbb.currentTextChanged.connect(self.on_update_orientation)

        # model
        for o in (self.ion_charge_lineEdit, self.ion_mass_lineEdit,
                  self.ion_energy_lineEdit, ):
            o.setValidator(QDoubleValidator(0, 99999999, 6))
            o.returnPressed.connect(self.on_update_model)
        self.voltage_lineEdit.setValidator(QDoubleValidator())
        self.voltage_lineEdit.textChanged.connect(self.on_v2d)

        # init EMS devices
        all_devices_dict = get_all_devices()
        self._all_devices_dict = all_devices_dict
        self.ems_names_cbb.addItems(all_devices_dict)
        self.ems_names_cbb.currentTextChanged.connect(self.on_device_changed)

        for o in self.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

        # pos,volt,dt...
        self.__attr_names = [
                '{}_{}'.format(u, v)
                for u in ('pos', 'volt')
                      for v in ('begin', 'end', 'step', 'settling_time')
        ]
        for s in self.__attr_names:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.connect(partial(self.on_update_config, s))

        #
        self.actionSimulation_Mode.setChecked(True)
        #
        self.ems_names_cbb.currentTextChanged.emit(
                self.ems_names_cbb.currentText())
        #
        self.ems_orientation_cbb.currentTextChanged.emit(
                self.ems_orientation_cbb.currentText())

    @pyqtSlot(float)
    def on_update_config(self, attr, x):
        # update attr of ems (1), live config (2) and _dconf (3)
        setattr(self._ems_device, attr, x)
        getattr(self._ems_device, 'set_{}'.format(attr))()
        self._dconf = self._ems_device.dconf

    @pyqtSlot('QString')
    def on_update_orientation(self, s):
        self._ems_orientation = s
        self._ems_device.xoy = s
        self._oid = oid = self._ems_device._id
        self._pos_begin_fname = "START_POS{}".format(oid)
        self._pos_end_fname = "STOP_POS{}".format(oid)
        self._pos_step_fname = "STEP_POS{}".format(oid)
        self._volt_begin_fname = "START_VOLT{}".format(oid)
        self._volt_end_fname = "STOP_VOLT{}".format(oid)
        self._volt_step_fname = "STEP_VOLT{}".format(oid)
        self._data_pv = self._ems_device.elem.pv("DATA{}".format(oid))[0]
        if self._device_mode == "Live":
            self.sync_config()

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

        self.show_device_config()

        # initial/update model
        ionc = float(self.ion_charge_lineEdit.text())
        ionm = float(self.ion_mass_lineEdit.text())
        ione = float(self.ion_energy_lineEdit.text())
        self._model = Model(device=ems,
                            ion_charge=ionc, ion_mass=ionm, ion_energy=ione)

    def show_device_config(self):
        """Show current device config, use device.sync_params() to refresh
        config with the live data.
        """
        ems = self._ems_device
        self.__show_device_config_static(ems)
        self.__show_device_config_dynamic(ems)

    def __show_device_config_static(self, ems):
        # static
        self.length_lineEdit.setText(str(ems.length))
        self.length1_lineEdit.setText(str(ems.length1))
        self.length2_lineEdit.setText(str(ems.length2))
        self.gap_lineEdit.setText(str(ems.gap))
        self.slit_width_lineEdit.setText(str(ems.slit_width))
        self.slit_thickness_lineEdit.setText(str(ems.slit_thickness))

    def __show_device_config_dynamic(self, ems):
        # dynamic
        for s in self.__attr_names:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.disconnect()
        self.pos_begin_dsbox.setValue(ems.pos_begin)
        self.pos_end_dsbox.setValue(ems.pos_end)
        self.pos_step_dsbox.setValue(ems.pos_step)
        self.pos_settling_time_dsbox.setValue(ems.pos_settling_time)
        self.volt_begin_dsbox.setValue(ems.volt_begin)
        self.volt_end_dsbox.setValue(ems.volt_end)
        self.volt_step_dsbox.setValue(ems.volt_step)
        self.volt_settling_time_dsbox.setValue(ems.volt_settling_time)
        for s in self.__attr_names:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.connect(partial(self.on_update_config, s))

    def sync_config(self):
        """Pull current device configuration from controls network, update
        on the UI.
        """
        ems = self._ems_device
        ems.sync_params()
        self.__show_device_config_dynamic(ems)

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

    def _run_simulation(self):
        # simulation
        from epics import caget

        print("Simulation mode...")
        data_pv = "EMS:Det1Data"
        status_pv = "EMS:SCAN_STATUS"
        trigger_pv = "EMS:START_SCAN"
        #
        x1, x2, dx = [caget(i) for i in
                ("EMS:POS_BEGIN", "EMS:POS_END", "EMS:POS_STEP")]
        y1, y2, dy = [caget(i) for i in
                ("EMS:VOLT_BEGIN", "EMS:VOLT_END", "EMS:VOLT_STEP")]
        #
        xdim = self._xdim = int((x2 - x1) / dx) + 1
        ydim = self._ydim = int((y2 - y1) / dy) + 1
        #
        x = np.linspace(x1, x2, xdim)
        y = np.linspace(y1, y2, ydim)
        xx, yy = np.meshgrid(x, y)
        self.matplotlibimageWidget.setXData(xx)
        self.matplotlibimageWidget.setYData(yy)
        #
        device = self._device = SimDevice(data_pv, status_pv, trigger_pv)
        device.data_changed.connect(self.on_update)
        device.finished.connect(self.on_finished)
        device.start()

    @pyqtSlot()
    def on_run(self):
        if self._device_mode == 'Simulation':
            self._run_simulation()
        else:  # Live
            self._run_live()

    def _run_live(self):
        # live
        print("Live mode...")
        #
        elem = self._ems_device.elem
        x1 = getattr(elem, self._pos_begin_fname)
        x2 = getattr(elem, self._pos_end_fname)
        dx = getattr(elem, self._pos_step_fname)

        try:
            assert (x2 - x1) % dx == 0
        except AssertionError:
            QMessageBox.warning(self, "Scan Range Warning",
                "Input scan range for position indicates non-integer points.",
                QMessageBox.Ok)
            return

        y1 = getattr(elem, self._volt_begin_fname)
        y2 = getattr(elem, self._volt_end_fname)
        dy = getattr(elem, self._volt_step_fname)

        #
        xdim = self._xdim = int((x2 - x1) / dx) + 1
        ydim = self._ydim = int((y2 - y1) / dy) + 1

        _id = self._ems_device._id
        data_pv = elem.pv('DATA{}'.format(_id))[0]
        status_pv = elem.pv('SCAN_STATUS{}'.format(_id))[0]
        trigger_pv = elem.pv('START_SCAN{}'.format(_id))[0]

        device = self._device = SimDevice(data_pv, status_pv, trigger_pv)
        device.data_changed.connect(self.on_update)
        device.finished.connect(self.on_finished)

        # start moving
        if not self.is_valid_to_move():
            QMessageBox.warning(self, "Starting Device",
                    "Device is busy.",
                    QMessageBox.Ok)
            return
        device.start()

    def is_valid_to_move(self):
        # if ok to move or not.
        return self._ems_device.check_status() == 0

    def on_update(self, data):
        m = data.reshape(self._ydim, self._xdim)
        m = np.flipud(m)
        m = np.nan_to_num(m)
        self._current_array = m
        self.image_data_changed.emit(m)

    @pyqtSlot()
    def on_finished(self):
        QMessageBox.information(self, "EMS DAQ",
                                "Data readiness is approaching...",
                                QMessageBox.Ok)
        self.on_update(self._device._data_pv.value)
        # show raw data
        self.on_plot_raw_data()

    def closeEvent(self, e):
        BaseAppForm.closeEvent(self, e)

    @pyqtSlot(bool)
    def on_enable_simulation_mode(self, f):
        if f:
            self._device_mode = "Simulation"
        else:
            self._device_mode = "Live"

    @pyqtSlot()
    def on_update_results(self):
        """Calculate Twiss parameters and update UI.
        """
        print("Update Twiss params")

    def on_plot_raw_data(self):
        # plot raw data.
        data = Data(model=self._model, array=self._current_array)
        inten1 = data.filter_initial_background_noise()
        r1 = data.calculate_beam_parameters(inten1)
        print(r1)

    @pyqtSlot()
    def on_update_model(self):
        ionc = float(self.ion_charge_lineEdit.text())
        ionm = float(self.ion_mass_lineEdit.text())
        ione = float(self.ion_energy_lineEdit.text())
        self._model.ion_charge = ionc
        self._model.ion_mass = ionm
        self._model.ion_energy = ione
        self.on_v2d(self.voltage_lineEdit.text())

    @pyqtSlot('QString')
    def on_v2d(self, s):
        try:
            v = float(s)
        except ValueError:
            out = ''
        else:
            d = self._model.voltage_to_divergence(v)[1] * 1000
            out = "{0:.3f}".format(d)
        finally:
            self.divergence_lineEdit.setText(out)
