#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUI App for wire-scanner.
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QShortcut

from functools import partial
import json
import numpy as np
import os

from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.elementwidget import ElementWidget
from phantasy import MachinePortal
from phantasy import Configuration
from phantasy.apps.wire_scanner.utils import find_dconf
from phantasy.apps.wire_scanner.device import Device
from phantasy.apps.wire_scanner.device import PMData
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import get_save_filename

from .app_utils import DeviceRunner
from .app_utils import DataAnalyzer
from .app_save import SaveDataDialog
from .app_dat2json import Dat2JsonDialog
from .utils import apply_mplcurve_settings
from .ui.ui_app import Ui_MainWindow

FIELD_OF_INTEREST_LIST = ["XCEN", "YCEN", "XRMS", "YRMS", "XYRMS", "CXY"]

FONTSIZE_MIN, FONTSIZE_MAX = 4, 24


class WireScannerWindow(BaseAppForm, Ui_MainWindow):

    lineChanged = pyqtSignal(int)
    xdataChanged = pyqtSignal(QVariant)
    ydataChanged = pyqtSignal(QVariant)

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
            devices, including the DAQ and post data analysis,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # variable initialization
        self._ws_device = None
        self._ws_data = None
        self._device_mode = "live"
        # signals after subnoise
        self._sig1_subnoise = None
        self._sig2_subnoise = None
        self._sig3_subnoise = None
        # dict of results for ioc (device)
        self._results_for_ioc = {}
        # detailed results and measured data
        self._detailed_rdata = {}
        self._detailed_mdata = {}
        # a2ua
        self.__factor_a2ua = 1.0
        self.__signal_unit = "$\mu$A"
        # widgets
        self._data_converter_dlg = None
        self._data_saving_dlg = None
        # pos windows artists
        self._wpos1_art = None
        self._wpos2_art = None
        self._wpos3_art = None
        # default lineEdit fontsize
        self.__default_lineEdit_fontsize = self.w11_sum_lineEdit.font().pointSize()

        # events
        self.pm_names_cbb.currentTextChanged.connect(self.on_pm_name_changed)
        for o in self.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

        self.start_pos1_lineEdit.textChanged.connect(self.startpos1_lineEdit.setText)
        self.start_pos2_lineEdit.textChanged.connect(self.startpos2_lineEdit.setText)
        self.stop_pos1_lineEdit.textChanged.connect(self.stoppos1_lineEdit.setText)
        self.stop_pos2_lineEdit.textChanged.connect(self.stoppos2_lineEdit.setText)

        # fontsize
        self.fontsize_inc_btn.clicked.connect(partial(self.update_fontsize, '+'))
        self.fontsize_dec_btn.clicked.connect(partial(self.update_fontsize, '-'))

        # loaded datafile path
        self.data_filepath_lineEdit.textChanged.connect(self.on_datafilepath_changed)

        # curves
        self.lineChanged.connect(self.matplotlibcurveWidget.setLineID)
        self.xdataChanged.connect(self.matplotlibcurveWidget.setXData)
        self.ydataChanged.connect(self.matplotlibcurveWidget.setYData)

        # hide lines button
        self.hide_curve1_btn.toggled[bool].connect(partial(self.on_hide_curve, 1))
        self.hide_curve2_btn.toggled[bool].connect(partial(self.on_hide_curve, 2))
        self.hide_curve3_btn.toggled[bool].connect(partial(self.on_hide_curve, 3))

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

        # init data plot
        self.init_data_plot()

    def init_data_plot(self):
        """Initial data plot.
        """
        self.matplotlibcurveWidget.setFigureAutoScale(False)
        self.matplotlibcurveWidget.setYTickFormat("Custom", "%g")
        self.xdataChanged.emit([])
        self.ydataChanged.emit([])
        self.matplotlibcurveWidget.add_curve()
        self.matplotlibcurveWidget.add_curve()

        # load default mpl curve config
        apply_mplcurve_settings(self.matplotlibcurveWidget)
        self.matplotlibcurveWidget.setFigureAutoScale(False)

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
        # adv analysis groupbox
        self.adv_analysis_groupBox.setVisible(self.adv_analysis_chkbox.isChecked())

        # hide run status progressbar
        self.run_progressbar.setVisible(False)
        self.emstop_btn.setVisible(False)
        self.analysis_progressbar.setVisible(False)

        # all lineEdit obje for results display
        self.__all_results_lineEdits = \
                self.results_wires_gb.findChildren((QLineEdit, QLabel)) + \
                self.results_beam_gb.findChildren((QLineEdit, QLabel))

        # keyshort
        fs_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        fs_reset.activated.connect(self.reset_fontsize)

    @pyqtSlot('QString')
    def on_pm_name_changed(self, n):
        """PM name is changed.
        """
        self._current_pm_name = n
        self._current_pm_elem = self._all_pms_dict[n]
        #
        self.on_update_device()
        # info
        self.statusInfoChanged.emit("Selected device: {}".format(n))

    def on_update_device(self):
        # update ws device object.

        # ws device
        ws = Device(self._current_pm_elem, self._dconf)
        self._ws_device = ws

        if ws.misc_info == "Installed":
            pixmap = QPixmap(":/icons/installed.png")
            tt = "Device is ready to use"
        else:
            pixmap = QPixmap(":/icons/not-installed.png")
            tt = "Device is not ready to use"
        self.info_lbl.setPixmap(pixmap)
        self.info_lbl.setToolTip(tt)

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

    def run_device(self, what_to_do, evt_sender):
        if self._ws_device is None:
            return
        device = self._ws_device
        oplist = [getattr(device, i) for i in what_to_do]
        self.__run_device(oplist, evt_sender, device)

    @pyqtSlot()
    def on_run_device(self):
        """Run device in the all-in-one style.
        """
        oplist = [
            'init_potentiometer',
            'enable_scan',
            'init_motor_pos',
            'reset_interlock',
            'set_scan_range',
            'set_bias_volt',
            'move',
            'init_motor_pos',
        ]
        self.run_device(oplist, self.sender())

    @pyqtSlot()
    def on_init_potentimeter(self):
        oplist = ['init_potentiometer']
        self.run_device(oplist, self.sender())

    @pyqtSlot()
    def on_enable_scan(self):
        oplist = ['enable_scan']
        self.run_device(oplist, self.sender())

    @pyqtSlot()
    def on_reset_interlock(self):
        oplist = ['reset_interlock']
        self.run_device(oplist, self.sender())

    @pyqtSlot()
    def on_set_bias_volt(self):
        oplist = ['set_bias_volt']
        self.run_device(oplist, self.sender())

    @pyqtSlot()
    def on_move(self):
        oplist = ['move']
        self.run_device(oplist, self.sender())

    @pyqtSlot()
    def on_init_motor_pos(self):
        oplist = ['init_motor_pos']
        self.run_device(oplist, self.sender(), )

    @pyqtSlot()
    def on_set_scan_range(self):
        oplist = ['set_scan_range']
        self.run_device(oplist, self.sender())

    @pyqtSlot(float, 'QString')
    def update_progress_bar(self, x, s):
        self.run_progressbar.setValue(x)
        self.run_progressbar.setFormat("Running: {}... (%p%)".format(s))

    @pyqtSlot()
    def complete(self, sender_obj):
        sender_obj.setEnabled(True)
        self.run_progressbar.setVisible(False)
        self.emstop_btn.setVisible(False)

    @pyqtSlot()
    def on_show_device_details(self):
        """Show selected PM details.
        """
        if self._device_mode == 'live':
            self._current_pm_widget = ElementWidget(self._current_pm_elem, fields=FIELD_OF_INTEREST_LIST)
            self._current_pm_widget.show()
        else:
            QMessageBox.warning(self, "Device Details",
                    "Not supported in 'Simulation' mode.",
                    QMessageBox.Ok)

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
            with open(filepath, 'w') as f:
                self._dconf.write(f)
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

    @pyqtSlot(bool)
    def on_show_advanced_ctrlpanel(self, f):
        """Show/hide advanced control panel.
        """
        self.advctrl_groupBox.setVisible(f)

    @pyqtSlot(bool)
    def on_show_advanced_analysis_panel(self, f):
        """Show/hide advanced data analysis panel.
        """
        self.adv_analysis_groupBox.setVisible(f)

    @pyqtSlot(bool)
    def on_amp_to_micro_amp(self, f):
        """If checked, change FACTOR_A2UA as 1e6.
        """
        if f:
            self.__factor_a2ua = 1.0e6
            self.__signal_unit = "A"
        else:
            self.__factor_a2ua = 1.0
            self.__signal_unit = "$\mu$A"
        # update ylabel
        self.matplotlibcurveWidget.setFigureYlabel("Signal [{}]".format(self.__signal_unit))
        # update results -> sum row
        for o in (self.w11_sum_lineEdit, self.w21_sum_lineEdit, self.w22_sum_lineEdit):
            s = o.text()
            if s != '' and s != 'nan':
                o.setText('{0:.4g}'.format(float(s) * self.__factor_a2ua))

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
        self.thread.terminate()

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
            with open(filepath, 'r') as f:
                d = json.load(f)
            ename = _get_element_name(d)
            # locate device combobox
            self.pm_names_cbb.setCurrentText(ename)
            self._ws_device.sync_data(mode='file', filename=filepath)
        except:
            QMessageBox.critical(self, "Load Data",
                    "Failed to load data from {}.".format(filepath),
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Load Data",
                    "Successfully loaded data from {}.".format(filepath),
                    QMessageBox.Ok)
            # plot data, new PMData instance
            self._ws_data = PMData(self._ws_device)
            self.on_plot_raw_data()
            self.on_reset_xyscale()

            # put filepath in data_filepath_lineEdit
            self.data_filepath_lineEdit.setText(filepath)
            # reset results for ioc dict
            self._results_for_ioc = {}
            # detail measured data
            self._detailed_mdata = self._ws_device.data_sheet
            self._ws_device.detail_data_sheet(self._detailed_mdata)
            # reset save dlg
            self._data_saving_dlg = None

    @pyqtSlot()
    def on_locate_data_file(self):
        """Locate loaded data file.
        """
        path = self.data_filepath_lineEdit.text()
        QDesktopServices.openUrl(QUrl(path))

    @pyqtSlot()
    def on_save_data(self):
        """Save data into file.
        """
        if self._data_saving_dlg is None:
            self._data_saving_dlg = SaveDataDialog(self)
        self._data_saving_dlg.exec_()

    @pyqtSlot()
    def on_sync_data(self):
        """Sync data from controls PV.
        """
        print("Sync data from PVs")
        if self._ws_device is None:
            return
        ename = self._ws_device.elem.name
        if self._device_mode != 'live':
            QMessageBox.warning(self, "Sync Data",
                    "Current operation mode is 'Simulation', sync data is not supported, only support loading data.",
                    QMessageBox.Ok)
            return
        try:
            self._ws_device.sync_data(mode='live')
        except:
            QMessageBox.critical(self, "Sync Data",
                    "Failed to sync data from controls network for {}.".format(ename),
                    QMessageBox.Ok)
            return
        else:
            #QMessageBox.information(self, "Sync Data",
            #        "Successfully synced data for {}.".format(ename),
            #        QMessageBox.Ok)
            self.statusInfoChanged.emit(
                "Successfully synced data for {}.".format(ename))

            # plot data, new PMData instance
            self._ws_data = PMData(self._ws_device)
            self.on_plot_raw_data()
            self.on_reset_xyscale()

            # reset results for ioc dict
            self._results_for_ioc = {}
            # detail measured data
            self._detailed_mdata = self._ws_device.data_sheet
            self._ws_device.detail_data_sheet(self._detailed_mdata)
            # reset data save dlg
            self._data_saving_dlg = None

    @pyqtSlot()
    def on_dat2json(self):
        """Convert data file from old .dat to new .json format.
        """
        if self._data_saving_dlg is None:
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

    @pyqtSlot()
    def on_plot_raw_data(self):
        """Plot raw data.
        """
        if self._ws_data is None:
            QMessageBox.critical(self, "Plot Data",
                    "Data is not ready, sync or load first.",
                    QMessageBox.Ok)
            return
        #try:
        #    self._ws_data = PMData(self._ws_device)
        #except RuntimeError:
        #    QMessageBox.critical(self, "Plot Data",
        #            "Data is not ready, sync or load first.",
        #            QMessageBox.Ok)
        #    return
        ws_data = self._ws_data
        # u
        self.lineChanged.emit(0)
        self.xdataChanged.emit(ws_data.raw_pos1)
        self.ydataChanged.emit(ws_data.signal_u)
        #self.matplotlibcurveWidget.setLineLabel("u")
        # v
        self.lineChanged.emit(1)
        self.xdataChanged.emit(ws_data.raw_pos2)
        self.ydataChanged.emit(ws_data.signal_v)
        #self.matplotlibcurveWidget.setLineLabel("v")

        # w
        self.lineChanged.emit(2)
        if self._ws_data.device.dtype != 'flapper':
            self.xdataChanged.emit(ws_data.raw_pos2)
            self.ydataChanged.emit(ws_data.signal_w)
            #self.matplotlibcurveWidget.setLineLabel("w")
        else:
            self.xdataChanged.emit([])
            self.ydataChanged.emit([])
            self.matplotlibcurveWidget.setLineLabel("")

        #
        self.matplotlibcurveWidget.setFigureXlabel("Pos [mm]")
        self.matplotlibcurveWidget.setFigureYlabel(
                "Signal [{}]".format(self.__signal_unit))

    @pyqtSlot()
    def on_plot_with_adjusted_pos(self):
        """Plot data with s(adjusted to beam frame), signal.
        """
        if self._ws_data is None:
            try:
                self._ws_data = PMData(self._ws_device)
            except RuntimeError:
                QMessageBox.critical(self, "Plot Data",
                        "Data is not ready, sync or load first.",
                        QMessageBox.Ok)
                return
        # u
        self.lineChanged.emit(0)
        s0 = self._ws_data.adjust_position(
                self._ws_data.raw_pos1, 0,
                self._ws_data.offset_u,)
        self.xdataChanged.emit(s0)
        #self.ydataChanged.emit(self._ws_data.signal_u)

        # v
        self.lineChanged.emit(1)
        s1 = self._ws_data.adjust_position(
                self._ws_data.raw_pos2, 1,
                self._ws_data.offset_v,)
        self.xdataChanged.emit(s1)
        #self.ydataChanged.emit(self._ws_data.signal_v)

        if self._ws_data.device.dtype != "flapper":
            # w
            self.lineChanged.emit(2)
            s2 = self._ws_data.adjust_position(
                    self._ws_data.raw_pos2, 2,
                    self._ws_data.offset_w,)
            self.xdataChanged.emit(s2)
            #self.ydataChanged.emit(self._ws_data.signal_w)

    @pyqtSlot()
    def on_plot_after_subnoise(self):
        """Plot data after background noise substraction.
        """
        try:
            sig1 = self._ws_data._sig1_subnoise
            sig2 = self._ws_data._sig2_subnoise
            sig3 = self._ws_data._sig3_subnoise
            if sig1 is None or sig2 is None or sig3 is None:
                raise RuntimeError
        except:
            QMessageBox.critical(self, "Plot Data",
                    "Data is not ready, if synced/loaded, analyze first.",
                    QMessageBox.Ok)
        else:
            self.lineChanged.emit(0)
            self.ydataChanged.emit(sig1)
            self.lineChanged.emit(1)
            self.ydataChanged.emit(sig2)
            if self._ws_data.device.dtype != "flapper":
                self.lineChanged.emit(2)
                self.ydataChanged.emit(sig3)

    @pyqtSlot()
    def on_analyze_data(self):
        """Analyze data in the all-in-one style.
        """
        try:
            self._ws_data = PMData(self._ws_device)
        except:
            QMessageBox.critical(self, "Analyze Data",
                    "Data is not ready, failed to analyze.",
                    QMessageBox.Ok)
            return

        self.analysis_progressbar.setVisible(True)
        self.thread1 = QThread()
        self.data_analyzer = DataAnalyzer(self._ws_data)
        self.data_analyzer.moveToThread(self.thread1)
        self.data_analyzer.resultsReady.connect(self.on_results_ready)
        self.data_analyzer.finished.connect(self.on_analysis_complete)
        self.data_analyzer.finished.connect(self.thread1.quit)
        self.data_analyzer.finished.connect(self.data_analyzer.deleteLater)
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.thread1.started.connect(self.data_analyzer.run)
        self.thread1.start()
        self.analyze_btn.setEnabled(False)

    @pyqtSlot(dict)
    def on_results_ready(self, d):
        """Display results, d: dict of results.
        """
        FMT = "{0:.4g}"
        pixmap = ":/icons/success.png"
        if d == {}:
            # error
            pixmap = ":/icons/fail.png"
            self.analyzed_status_lbl.setPixmap(QPixmap(pixmap))
            self.analyzed_status_lbl.setToolTip("Failed to process data")
            return
        self.analyzed_status_lbl.setPixmap(QPixmap(pixmap))
        self.analyzed_status_lbl.setToolTip("Data processed without error")
        for o,v in zip(
                ['w11_{}_lineEdit'.format(s) for s in ('sum', 'center', 'rms')],
                [d['sum1'] * self.__factor_a2ua, d['cen1'], d['rms1']]):
            getattr(self, o).setText(FMT.format(v))

        for o,v in zip(
                ['w21_{}_lineEdit'.format(s) for s in ('sum', 'center', 'rms')],
                [d['sum2'] * self.__factor_a2ua, d['cen2'], d['rms2']]):
            getattr(self, o).setText(FMT.format(v))

        for o,v in zip(
                ['w22_{}_lineEdit'.format(s) for s in ('sum', 'center', 'rms')],
                [d['sum3'] * self.__factor_a2ua, d['cen3'], d['rms3']]):
            getattr(self, o).setText(FMT.format(v))

        # xyuv
        xc, yc, uc, vc = d['xcen'], d['ycen'], d['ucen'], d['vcen']
        xrms, yrms, urms, vrms = d['xrms'], d['yrms'], d['urms'], d['vrms']
        xrms90, yrms90, urms90, vrms90 = d['x90p'], d['y90p'], d['u90p'], d['v90p']
        xrms99, yrms99, urms99, vrms99 = d['x99p'], d['y99p'], d['u99p'], d['v99p']
        cxy, cxy90, cxy99 = d['cxy'], d['cxy90p'], d['cxy99p']

        for o,v in zip(
                ['{}_lineEdit'.format(s) for s in ('xc', 'yc', 'uc', 'vc')] +
                ['{}_lineEdit'.format(s) for s in ('xrms', 'yrms', 'urms', 'vrms')] +
                ['{}_lineEdit'.format(s) for s in ('xrms90', 'yrms90', 'urms90', 'vrms90')] +
                ['{}_lineEdit'.format(s) for s in ('xrms99', 'yrms99', 'urms99', 'vrms99')] +
                ['{}_lineEdit'.format(s) for s in ('cxy', 'cxy90', 'cxy99')],
                [xc, yc, uc, vc, xrms, yrms, urms, vrms, xrms90, yrms90, urms90, vrms90, xrms99, yrms99, urms99, vrms99, cxy, cxy90, cxy99]):
            getattr(self, o).setText(FMT.format(v))

        # results for ioc (device)
        self._results_for_ioc = {
                'xcen': xc, 'ycen': yc,
                'xrms': xrms, 'yrms': yrms,
                'cxy': cxy}
        # detailed results dict
        rdata = {'results': d}
        self._ws_device.detail_data_sheet(rdata)
        self._detailed_rdata = rdata

    @pyqtSlot()
    def on_analysis_complete(self):
        print("data analysis is completed")
        self.analysis_progressbar.setVisible(False)
        self.analyze_btn.setEnabled(True)

        wpos_list = [self._ws_data._pos_window1, self._ws_data._pos_window2, self._ws_data._pos_window3]
        for i, iwpos in enumerate(wpos_list):
            if iwpos is None:
                sl, sr = np.nan, np.nan
            else:
                sl, sr = iwpos
            getattr(self, 'wpos{}_left_lineEdit'.format(i+1)).setText('{0:.5g}'.format(sl))
            getattr(self, 'wpos{}_right_lineEdit'.format(i+1)).setText('{0:.5g}'.format(sr))

    def __run_device(self, oplist, sender_obj, device):
        self.run_progressbar.setVisible(True)
        self.emstop_btn.setVisible(True)
        self.run_progressbar.setValue(0)
        self.thread = QThread()

        self.device_runner = DeviceRunner(oplist, device, self._device_mode)
        self.device_runner.moveToThread(self.thread)
        self.device_runner.update_progress.connect(self.update_progress_bar)
        self.device_runner.sync_data.connect(self.on_sync_data)
        self.device_runner.finished.connect(partial(self.complete, sender_obj))
        self.device_runner.finished.connect(self.thread.quit)
        self.device_runner.finished.connect(self.device_runner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.device_runner.run)
        self.thread.start()

        sender_obj.setEnabled(False)

    @pyqtSlot()
    def on_sync_results_to_ioc(self):
        """Sync analyzed results back to device (IOC), the dynamic fields are:
        'XCEN', 'YCEN', 'XRMS', 'YRMS', 'CXY'.
        """
        try:
            if self._ws_data._results_for_ioc == {}:
                raise RuntimeError
            self._ws_data.sync_results_to_ioc()
        except:
            QMessageBox.warning(self, "Sync Results To Device",
                    "Results are not ready, Analyze first.",
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Sync Results to Device",
                    "Results are synced to device.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_reset_xyscale(self):
        """Reset xy data scale.
        """
        self.matplotlibcurveWidget.setFigureAutoScale(True)
        self.matplotlibcurveWidget.setFigureAutoScale(False)

    @pyqtSlot(bool)
    def on_plot_wpos1(self, show):
        """Plot position window 1.
        """
        self.__show_wpos(show, 1)

    @pyqtSlot(bool)
    def on_plot_wpos2(self, show):
        """Plot position window 2.
        """
        self.__show_wpos(show, 2)

    @pyqtSlot(bool)
    def on_plot_wpos3(self, show):
        """Plot position window 3.
        """
        self.__show_wpos(show, 3)

    def __show_wpos(self, show, i):
        # i: int: (wid+1) 1,2,3
        art_obj_name = '_wpos{}_art'.format(i)
        if show:
            x1 = float(getattr(self, 'wpos{}_left_lineEdit'.format(i)).text())
            x2 = float(getattr(self, 'wpos{}_right_lineEdit'.format(i)).text())
            print("plot wpos{}: {}, {}".format(i, x1, x2))
            if getattr(self, art_obj_name) is None:
                ax = self.matplotlibcurveWidget.axes
                o = ax.axvspan(x1, x2, alpha=0.3, color='gray', zorder=-10)
                setattr(self, art_obj_name, o)
            art_obj = getattr(self, art_obj_name)
            art_obj.set_xy([(x1, 0), (x1, 1), (x2, 1), (x2, 0), (x1, 0)])
            art_obj.set_visible(True)
        else:
            o = getattr(self, art_obj_name)
            if o is not None:
                o.set_visible(False)
        self.matplotlibcurveWidget.update_figure()

    @pyqtSlot(bool)
    def on_hide_curve(self, line_id, show):
        """Hide curve indicated by *line_id* (1, 2, 3) or not.
        """
        self.lineChanged.emit(line_id - 1)
        self.matplotlibcurveWidget.setLineVisible(not show)

    @pyqtSlot()
    def update_fontsize(self, mode="+", fontsize=None):
        """Grow/shrink fontsize (results display panel)
        """
        for o in self.__all_results_lineEdits:
            font = o.font()
            ps = font.pointSize()
            new_ps = ps + 1 if mode == '+' else ps - 1
            if new_ps > FONTSIZE_MAX  or new_ps < FONTSIZE_MIN: new_ps = self.__default_lineEdit_fontsize
            font.setPointSize(new_ps)
            o.setFont(font)

    @pyqtSlot()
    def reset_fontsize(self):
        for o in self.__all_results_lineEdits:
            font = o.font()
            font.setPointSize(self.__default_lineEdit_fontsize)
            o.setFont(font)

    @pyqtSlot('QString')
    def on_datafilepath_changed(self, filepath):
        """Data filepath is changed.
        """
        filename = os.path.basename(filepath) + "\n"
        self.matplotlibcurveWidget.setFigureTitle(filename)


def _get_element_name(data):
    # get element from loaded data dict.
    try:
        # data file is saved from live mode
        return data['device']['element']
    except:
        # if data file is converted from old dat file
        return data['ename']

