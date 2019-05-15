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
    xdata_changed = pyqtSignal(ndarray)
    ydata_changed = pyqtSignal(ndarray)
    xlabel_changed = pyqtSignal('QString')
    ylabel_changed = pyqtSignal('QString')
    def __init__(self, version, mode="Live"):
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
        self.xdata_changed.connect(self.matplotlibimageWidget.setXData)
        self.ydata_changed.connect(self.matplotlibimageWidget.setYData)
        self.xlabel_changed.connect(self.matplotlibimageWidget.setFigureXlabel)
        self.ylabel_changed.connect(self.matplotlibimageWidget.setFigureYlabel)

        self._device_mode = mode.capitalize()
        self._post_init()

    def _post_init(self):
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
        ve = self.voltage_lineEdit
        ve.setValidator(QDoubleValidator())
        ve.textChanged.connect(self.on_v2d)
        ve.returnPressed.connect(partial(self.on_v2d, ve.text()))

        # data
        self._data = None
        # bkgd noise
        for o in (self.bkgd_noise_nelem_sbox, self.bkgd_noise_threshold_sbox):
            o.valueChanged.emit(o.value())

        # pos,volt,dt...
        self._attr_names = [
                '{}_{}'.format(u, v)
                for u in ('pos', 'volt')
                      for v in ('begin', 'end', 'step', 'settling_time')
        ]

        for s in self._attr_names:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.connect(partial(self.on_update_config, s))

        #
        is_sim = self._device_mode=="Simulation"
        self.actionSimulation_Mode.setChecked(is_sim)
        self.actionSimulation_Mode.toggled.emit(is_sim)

        for o in self.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

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
        self.sync_config()
        # update result keys
        self._update_result_keys(s)

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
        for s in self._attr_names:
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
        for s in self._attr_names:
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

    @pyqtSlot()
    def on_run(self):
        self._run()

    def _run(self):
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
        # initial data
        self.on_initial_data(mode=self._device_mode)
        self.on_plot_raw_data()

    def closeEvent(self, e):
        BaseAppForm.closeEvent(self, e)

    @pyqtSlot(bool)
    def on_enable_simulation_mode(self, f):
        if f:
            self._device_mode = "Simulation"
        else:
            self._device_mode = "Live"
        self._initial_devices(self._device_mode)

    @pyqtSlot()
    def on_update_results(self):
        """Calculate Twiss parameters and update UI.
        """
        if self._data is None:
            return
        inten = self.matplotlibimageWidget.get_data()
        res = self._data.calculate_beam_parameters(inten)
        self.update_results_ui(res)

    def on_initial_data(self, mode="Live"):
        self._data = Data(model=self._model, array=self._current_array)
        print(self._current_array.shape)
        if mode == "Simulation":
            pass

    def on_plot_raw_data(self):
        # plot raw data, before processing.
        self.xdata_changed.emit(self._data.x_grid)
        self.xlabel_changed.emit("$x\,\mathrm{[mm]}$")
        self.image_data_changed.emit(self._data.intensity)
        self.raw_view_chkbox.toggled.emit(self.raw_view_chkbox.isChecked())

    @pyqtSlot()
    def on_update_model(self):
        ionc = float(self.ion_charge_lineEdit.text())
        ionm = float(self.ion_mass_lineEdit.text())
        ione = float(self.ion_energy_lineEdit.text())
        self._model.ion_charge = ionc
        self._model.ion_mass = ionm
        self._model.ion_energy = ione
        self.on_v2d(self.voltage_lineEdit.text())
        # update data
        if self._data is not None:
            self._data.model = self._model

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

    @pyqtSlot()
    def on_open_data(self,):
        # open data.
        filepath, ext = get_open_filename(self, filter="JSON Files (*.json)")
        if filepath is None:
            return

        try:
            data = self._data = Data(self._model, file=filepath)
        except KeyError:
            QMessageBox.warning(self, "Open Data", "Failed to open data.",
                    QMessageBox.Ok)
            return
        else:
            # show raw_data
            #
            self.on_plot_raw_data()
            #
            #inten1 = self._update_bkgd_noise()
            # r1 = data.calculate_beam_parameters(inten1)
            # print(r1)

    def _update_bkgd_noise(self):
        if self._data is None:
            return
        try:
            inten1, bkgd_noise = self._data.filter_initial_background_noise(
                               n_elements=self._bkgd_noise_nelem,
                               threshold=self._bkgd_noise_nsigma)
        except (IndexError, ValueError):
            pass
        else:
            self.plot_bkgd_noise(self.bkgd_noise_plot, bkgd_noise,
                                 self._bkgd_noise_nsigma)
            self.image_data_changed.emit(inten1)
            return inten1

    @pyqtSlot(int)
    def on_update_nsampling(self, i):
        # bkgd noise nelem.
        self._bkgd_noise_nelem = i
        self._update_bkgd_noise()

    @pyqtSlot(int)
    def on_update_threshold0(self, i):
        self._bkgd_noise_nsigma = i
        self._update_bkgd_noise()

    def plot_bkgd_noise(self, o, m, n):
        ax = o.axes
        ax.clear()
        m = m.flatten()
        avg = m.mean()
        std = m.std()
        ax.plot(m, color='b')
        ax.axhline(avg, ls='--', color='r')
        ax.axhline(avg + n * std, ls='--', color='m')
        t = r'$\mathrm{{Average}}: {0:.3g}, \sigma: {1:.3g}, \mathrm{{threshold}}: {2:.3g}$'.format(
                avg, std, avg + n * std)
        ax.set_title(t)
        ax.xaxis.set_visible(False)
        o.update_figure()

    @pyqtSlot(bool)
    def on_enable_raw_view(self, f):
        if f: # show pos, volt, intensity
            self.ydata_changed.emit(self._data.volt_grid)
            self.ylabel_changed.emit("$\mathrm{Voltage}\,\mathrm{[V]}$")
        else: # show pos, angle, intensity
            self.ydata_changed.emit(self._data.xp_grid)
            self.ylabel_changed.emit("$x'\,\mathrm{[mrad]}$")

    def update_results_ui(self, res):
        ks = ('x_cen', 'xp_cen', 'x_rms', 'xp_rms',
              'alpha_x', 'beta_x', 'gamma_x', 'emit_x', 'emitn_x', )
        u = self._ems_device.xoy.lower()
        for k in ks:
            o = getattr(self, k + '_lineEdit')
            v = res.get(k.replace('x', u))
            o.setText("{0:.6f}".format(v))

    def _update_result_keys(self, s):
        u = s.lower()
        o = (self.x_cen_lbl, self.xp_cen_lbl,
             self.x_rms_lbl, self.xp_rms_lbl,
             self.alpha_x_lbl, self.beta_x_lbl, self.gamma_x_lbl,
             self.emit_x_lbl, self.emitn_x_lbl)
        v = ["<html>{}<sub>{}</sub></html>".format(i, j) for (i, j) in
                zip((u, u + "'", '&sigma;', '&sigma;', '&alpha;',
                    '&beta;', '&gamma;', '&epsilon;', '&epsilon;'),
                    (0, 0, u, u + "'", u, u, u, u, u + '<sup>n</sup>',))]
        for (i, j) in zip(o, v):
            i.setText(j)

    def _initial_devices(self, mode="Live"):
        if mode == "Live":
            all_devices_dict = get_all_devices()
        else:
            all_devices_dict = get_all_devices("DEVICES", "DEVICES", "EMS")
        self._all_devices_dict = all_devices_dict
        self.ems_names_cbb.addItems(all_devices_dict)
        self.ems_names_cbb.currentTextChanged.connect(self.on_device_changed)
        #
        self.ems_names_cbb.currentTextChanged.emit(
                self.ems_names_cbb.currentText())
        #
        self.ems_orientation_cbb.currentTextChanged.emit(
                self.ems_orientation_cbb.currentText())
