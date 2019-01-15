#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy.apps.utils import get_open_filename
from phantasy import generate_settings

from .ui.ui_loadfrom import Ui_Dialog


class LoadSettingsDialog(QDialog, Ui_Dialog):

    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)
    # signal: lattice changed, emit mp.
    latticeChanged = pyqtSignal(QVariant)

    def __init__(self, parent=None):
        super(LoadSettingsDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Load Settings From File")

        # mp
        self.__mp = None

        # events
        self.latticeWidget.latticeChanged.connect(self.on_lattice_changed)

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, o):
        """Lattice loaded.
        """
        self.__mp = o
        self.latticeChanged.emit(o)

    @pyqtSlot()
    def on_open_snpfile(self):
        """open .snp file.
        """
        filepath, ext = get_open_filename(self,
                filter="SNP Files (*.snp);;CSV Files (*.csv)")
        if filepath is None:
            return
        self.filepath_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_load(self):
        """Click OK to load settings.
        """
        if self.__mp is None:
            QMessageBox.warning(self, "Load Settings",
                    "Please load lattice first.",
                    QMessageBox.Ok)
        else:
            snpfile = self.filepath_lineEdit.text()
            settings = generate_settings(snpfile=snpfile,
                    lattice=self.__mp.work_lattice_conf,
                    only_physics=False)
            flat_settings = convert_settings(settings, self.__mp)
            self.settingsLoaded.emit(flat_settings, settings)

            self.accept()


def convert_settings(settings_read, mp):
    """Convert settings to flat.
    """
    flat_settings = []
    for ename, econf in settings_read.items():
        elem = mp.get_elements(name=ename)[0]
        for fname, fval0 in econf.items():
            confline = (elem, fname, fval0)
            flat_settings.append(confline)
    return flat_settings
