#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUI App for wire-scanner.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit

from functools import partial

from phantasy_ui.templates import BaseAppForm
from phantasy import MachinePortal
from phantasy import Configuration
from phantasy.apps.wire_scanner.utils import find_dconf
from phantasy.apps.wire_scanner.device import Device

from .ui.ui_app import Ui_MainWindow


class WireScannerWindow(BaseAppForm, Ui_MainWindow):

    # ws config is changed
    confChanged = pyqtSignal()

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

        # events
        self.pm_names_cbb.currentTextChanged.connect(self.on_pm_name_changed)
        for o in self.controls_groupBox.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

        #self.confChanged.connect(self.on_update_device)

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


    @pyqtSlot('QString')
    def on_pm_name_changed(self, n):
        """PM name is changed.
        """
        self._current_pm_name = n
        self._current_pm_elem = self._all_pms_dict[n]
        #
#        self.confChanged.emit()
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
