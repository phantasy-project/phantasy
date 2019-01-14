#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from phantasy_ui.templates import BaseAppForm

from .utils import SettingsModel

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

        # testing
        self.settings = get_settings()
        self.on_show_settings()

        #
        self.adjustSize()

    def on_show_settings(self):
        model = SettingsModel(self.treeView, self.settings)
        model.set_model()


def get_settings():
    from phantasy import MachinePortal
    from phantasy import generate_settings
    import os

    mp = MachinePortal(machine='FRIB', segment='LEBT')
    lat = mp.work_lattice_conf
    rpath = "/home/tong/Dropbox/FRIB/work/phantasy-project/phantasy-examples/notebooks/work_with_save_restore"
    snpfile = os.path.join(rpath, 'Ar_LEBT_to_MEBT_20180321.snp')
    settings_read = generate_settings(snpfile=snpfile, lattice=lat, only_physics=False)

    flat_settings = []
    for ename, econf in settings_read.items():
        elem = lat.get_elements(name=ename)[0]
        for fname, fval0 in econf.items():
            confline = (elem, fname, fval0)
            flat_settings.append(confline)
    return flat_settings



