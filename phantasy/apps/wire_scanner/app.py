#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUI App for wire-scanner.
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox

from functools import partial

from phantasy_ui.templates import BaseAppForm
from phantasy import MachinePortal
from phantasy import Configuration
from phantasy.apps.wire_scanner.utils import find_dconf
from phantasy.apps.wire_scanner.device import Device
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import get_save_filename

from .app_utils import DeviceRunner
from .ui.ui_app import Ui_MainWindow


class WireScannerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(WireScannerWindow, self).__init__()

        # app version
        self._version = version

        # window title/version
        self.setWindowTitle("Wire Scanner App")
        #self.setWindowIcon()

        # set app properties
        self.setAppTitle("Wire Scanner App")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Wire Scanner App</h4>
            <p>This app is created to ease the usage of wire-scanner
            devices, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # variable initialization
        self._ws_device = None
        self._device_mode = "live"
        # widgets
        self._data_converter_dlg = None

        # events
        self.pm_names_cbb.currentTextChanged.connect(self.on_pm_name_changed)
        for o in self.controls_groupBox.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

        self.start_pos1_lineEdit.textChanged.connect(self.startpos1_lineEdit.setText)
        self.start_pos2_lineEdit.textChanged.connect(self.startpos2_lineEdit.setText)
        self.stop_pos1_lineEdit.textChanged.connect(self.stoppos1_lineEdit.setText)
        self.stop_pos2_lineEdit.textChanged.connect(self.stoppos2_lineEdit.setText)

        # validator
        for o in (self.start_pos1_lineEdit, self.start_pos2_lineEdit,
                  self.stop_pos1_lineEdit, self.stop_pos2_lineEdit,
                  self.offset1_lineEdit, self.offset2_lineEdit,
                  self.offset3_lineEdit, self.outlimit_lineEdit,
                  self.startpos1_lineEdit, self.startpos2_lineEdit,
                  self.stoppos1_lineEdit, self.stoppos2_lineEdit):
            o.setValidator(QDoubleValidator())

        # init ui
        self.post_init_ui()

    def post_init_ui(self):
        # all PMs
        all_pms_dict = self.get_all_pms()
        all_pm_names = sorted(all_pms_dict)
        self._all_pms_dict = all_pms_dict

        # set pm names cbb
        self.pm_names_cbb.currentTextChanged.disconnect(self.on_pm_name_changed)
        self.pm_names_cbb.addItems(all_pm_names)
        self.pm_names_cbb.currentTextChanged.connect(self.on_pm_name_changed)

        # current pm
        self._current_pm_name = self.pm_names_cbb.currentText()
        self._current_pm_elem = self._all_pms_dict[self._current_pm_name]

        # load config from system config file.
        self._dconf = self.get_device_config()
        self.on_update_device()

        # update visibility of advctrl groupbox
        self.advctrl_groupBox.setVisible(self.advctrl_chkbox.isChecked())

        # hide run status progressbar
        self.run_progressbar.setVisible(False)
        self.emstop_btn.setVisible(False)

    @pyqtSlot('QString')
    def on_pm_name_changed(self, n):
        """PM name is changed.
        """
        self._current_pm_name = n
        self._current_pm_elem = self._all_pms_dict[n]
        #
        self.on_update_device()

    def on_update_device(self):
        # update ws device object.

        # ws device
        ws = Device(self._current_pm_elem, self._dconf)
        self._ws_device = ws

        # display configuration
        self.dtype_lineEdit.setText(ws.dtype)
        self.coord_lineEdit.setText(ws.coord)
        self.start_pos1_lineEdit.setText(str(ws.scan_start_pos[0]))
        self.start_pos2_lineEdit.setText(str(ws.scan_start_pos[1]))
        self.stop_pos1_lineEdit.setText(str(ws.scan_stop_pos[0]))
        self.stop_pos2_lineEdit.setText(str(ws.scan_stop_pos[1]))
        self.offset1_lineEdit.setText(str(ws.wire_offset[0]))
        self.offset2_lineEdit.setText(str(ws.wire_offset[1]))
        self.offset3_lineEdit.setText(str(ws.wire_offset[2]))

    @pyqtSlot()
    def on_run_device(self):
        """Run device in the all-in-one style.
        """
        if self._ws_device is None:
            return

        device = self._ws_device

        self.run_progressbar.setVisible(True)
        self.emstop_btn.setVisible(True)
        self.run_progressbar.setValue(0)
        self.thread = QThread()
        oplist = [
            device.init_potentiometer,
            device.enable_scan,
            device.init_motor_pos,
            device.reset_interlock,
            device.set_scan_range,
            device.set_bias_volt,
            device.move,
            device.init_motor_pos,
        ]
        self.device_runner = DeviceRunner(oplist, device, self._device_mode)
        self.device_runner.moveToThread(self.thread)
        self.device_runner.update_progress.connect(self.update_progress_bar)
        #self.device_runner.results.connect(self.display_results)
        self.device_runner.finished.connect(self.complete)
        self.device_runner.finished.connect(self.thread.quit)
        self.device_runner.finished.connect(self.device_runner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.device_runner.run)
        self.thread.start()

        self.run_btn.setEnabled(False)

    @pyqtSlot(float, 'QString')
    def update_progress_bar(self, x, s):
        self.run_progressbar.setValue(x)
        self.run_progressbar.setFormat("Running: {}... (%p%)".format(s))

    @pyqtSlot(dict)
    def display_results(self, results):
        for k, v in results.items():
            self.result_box.append('%s: %s' % (k, v))

    @pyqtSlot()
    def complete(self):
        self.run_btn.setEnabled(True)
        self.run_progressbar.setVisible(False)
        self.emstop_btn.setVisible(False)

    @pyqtSlot()
    def on_show_device_details(self):
        """Show selected PM details.
        """
        from phantasy_ui.widgets.elementwidget import ElementWidget
        self._current_pm_widget = ElementWidget(self._current_pm_elem)
        self._current_pm_widget.show()

    @pyqtSlot()
    def onHelp(self):
        return
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    @pyqtSlot()
    def on_loadfrom_config(self):
        """Load configuration from a file.
        """
        print("Load From")

    @pyqtSlot()
    def on_saveas_config(self):
        """Save configuration to a file.
        """
        print("Save As")

    @pyqtSlot()
    def on_save_config(self):
        """Save configuration.
        """
        print("Save")

    @pyqtSlot()
    def on_reload_config(self):
        """Reload configuration.
        """
        print("Reload")

    @pyqtSlot(bool)
    def on_show_advanced_ctrlpanel(self, f):
        """Show/hide advanced control panel.
        """
        self.advctrl_groupBox.setVisible(f)

    @pyqtSlot(bool)
    def on_enable_simulation_mode(self, f):
        if f:
            self._device_mode = "simulation"
        else:
            self._device_mode = "live"

    @pyqtSlot()
    def on_emstop_device(self):
        """Emergency stop running device.
        """
        self.device_runner.stop()

    @pyqtSlot()
    def on_load_data(self):
        """Open file to load previous saved measured data.
        """
        print("Load data from file")
        filepath, ext = get_open_filename(self,
                filter="JSON Files (*.json)")
        if filepath is None:
            return
        try:
            self._ws_device.sync_data(mode='file', filename=filepath)
        except:
            QMessageBox.critical(self, "Load Data",
                    "Failed to load data from {}".format(filepath),
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Load Data",
                    "Successfully loaded data from {}".format(filepath),
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_save_data(self):
        """Save data into file.
        """
        print("Save data to file")
        filepath, ext = get_save_filename(self,
                filter="JSON Files (*.json)")
        if filepath is None:
            return
        try:
            self._ws_device.save_data(filepath)
        except:
            QMessageBox.critical(self, "Save Data",
                    "Failed to save data to {}".format(filepath),
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Data",
                    "Successfully saved data to {}".format(filepath),
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_sync_data(self):
        """Sync data from controls PV.
        """
        print("Sync data from PVs")
        if self._ws_device is None:
            return
        self._ws_device.sync_data(mode='live')

    @pyqtSlot()
    def on_dat2json(self):
        """Convert data file from old .dat to new .json format.
        """
        from .app_dat2json import Dat2JsonDialog
        self._data_converter_dlg = Dat2JsonDialog()
        self._data_converter_dlg.show()

    @pyqtSlot()
    def on_locate_config(self):
        """Locate (find and open) device configuration file path.
        """
        path = self._dconf.config_path
        QDesktopServices.openUrl(QUrl(path))

    def get_all_pms(self):
        """Return all PM elements.
        """
        mp1 = MachinePortal("FRIB", "LEBT")
        mp2 = MachinePortal("FRIB", "MEBT")
        elems = mp1.get_elements(type="PM") + mp2.get_elements(type="PM")
        names = [i.name for i in elems]
        return dict(zip(names, elems))

    def get_device_config(self, path=None):
        """Get device config from *path*.
        """
        path = find_dconf() if path is None else path
        dconf = Configuration(path)
        return dconf
