#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import BaseAppForm

from .utils import SettingsModel
from .app_loadfrom import LoadSettingsDialog

from .ui.ui_app import Ui_MainWindow


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(SettingsManagerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Settings Manager")

        # set app properties
        self.setAppTitle("Settings Manager")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Settings Manager</h4>
            <p>This app is created to manage the device settings for
            the accelerator system, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # post init ui
        self.__post_init_ui()

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, o):
        """Lattice is changed, mp.
        """
        self.__mp = o

    @pyqtSlot(QVariant, QVariant)
    def on_settings_loaded(self, flat_settings, settings):
        """Settings are loaded.
        """
        self.__flat_settings = flat_settings
        self.__settings = settings
        self.__on_show_settings()

    def __on_show_settings(self):
        # visualize settings
        model = SettingsModel(self.treeView, self.__flat_settings)
        model.set_model()

    def __post_init_ui(self):
        # placeholders
        self._load_from_dlg = None
        self.__mp = None
        self.__settings = None
        self.__flat_settings = None

    def on_save(self):
        """Save settings to file.
        """
        print("Save settings to file")

    @pyqtSlot()
    def on_load_from_snp(self):
        """Load settings from .snp file.
        """
        if self._load_from_dlg is None:
            self._load_from_dlg = LoadSettingsDialog()
        self._load_from_dlg.settingsLoaded.connect(self.on_settings_loaded)
        self._load_from_dlg.latticeChanged.connect(self.on_lattice_changed)
        self._load_from_dlg.show()

    @pyqtSlot()
    def on_apply_settings(self):
        """Apply (selected) settings to machine.
        """
        if self.__settings is None:
            return
        try:
            lat = self.__mp.work_lattice_conf
            lat.settings = self.__settings
            lat.sync_settings(data_source='model')
        except:
            QMessageBox.warning(self, "Apply Settings",
                    "Failed to apply settings to accelerator.",
                    QMessageBox.Ok)

        else:
            QMessageBox.information(self, "Apply Settings",
                    "Successfully applied settings to accelerator.",
                    QMessageBox.Ok)
