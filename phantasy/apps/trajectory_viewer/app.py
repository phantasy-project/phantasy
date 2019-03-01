#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMessageBox

from collections import OrderedDict
from collections import deque
from functools import partial
import numpy as np

from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.latticewidget import LatticeWidget
from phantasy.apps.utils import get_save_filename
from phantasy.apps.utils import get_open_filename

from .app_elem_selection import ElementSelectionWidget
from .app_help import HelpDialog
from .ui.ui_app import Ui_MainWindow
from .utils import apply_mplcurve_settings
from .utils import ElementListModel
from .utils import MonitorReadingsDataSheet
from .utils import load_readings_sheet

BPM_UNIT_FAC = {"mm": 1.0, "m": 1e3}


class TrajectoryViewerWindow(BaseAppForm, Ui_MainWindow):

    # curves
    lineChanged = pyqtSignal(int)
    xdataChanged = pyqtSignal(QVariant)
    ydataChanged = pyqtSignal(QVariant)

    # lattice is loaded
    latticeChanged = pyqtSignal(QVariant)

    # selected monitors and fields, k: ename, v: list of fields
    monitorsChanged = pyqtSignal(dict)
    # selected correctors and fields
    correctorsChanged = pyqtSignal(dict)

    def __init__(self, version):
        super(TrajectoryViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Trajectory Viewer")

        # set app properties
        self.setAppTitle("Trajectory Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Trajectory Viewer</h4>
            <p>This app is created to visualize the beam central
            trajectory of FRIB accelerator, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # events
        self.start_btn.clicked.connect(self.start_daq)
        self.stop_btn.clicked.connect(self.stop_daq)

        # select element btn: BPMs
        self.select_bpms_btn.clicked.connect(
                partial(self.on_select_elements, 'bpm', ["BPM"]))

        # select element btn:CORs
        self.select_cors_btn.clicked.connect(
                partial(self.on_select_elements, 'cor', ["HCOR", "VCOR"]))

        # DAQ freq
        self.freq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)

        # curve
        self.lineChanged.connect(self.matplotlibcurveWidget.setLineID)
        self.xdataChanged.connect(self.matplotlibcurveWidget.setXData)
        self.ydataChanged.connect(self.matplotlibcurveWidget.setYData)

        # xy limits
        self.__xylimits_lineEdits = (self.xmin_lineEdit,
                                     self.xmax_lineEdit,
                                     self.ymin_lineEdit,
                                     self.ymax_lineEdit)
        for o in self.__xylimits_lineEdits:
            o.setValidator(QDoubleValidator())
        self.xmin_lineEdit.textChanged.connect(
                partial(self.update_xylimit, 'setXLimitMin'))
        self.xmax_lineEdit.textChanged.connect(
                partial(self.update_xylimit, 'setXLimitMax'))
        self.ymin_lineEdit.textChanged.connect(
                partial(self.update_xylimit, 'setYLimitMin'))
        self.ymax_lineEdit.textChanged.connect(
                partial(self.update_xylimit, 'setYLimitMax'))

        # bpm unit
        self.bpm_unit_millimeter_rbtn.toggled.connect(
                partial(self.on_update_unit, "mm"))
        self.bpm_unit_meter_rbtn.toggled.connect(
                partial(self.on_update_unit, "m"))

        # bpm selection for monitoring
        self.use_all_bpms_rbtn.toggled.connect(
                partial(self.on_update_monitors, "all"))
        self.use_selected_bpms_rbtn.toggled.connect(
                partial(self.on_update_monitors, "selected"))

        # element selection for BPMs/CORs treeview
        self.select_all_bpms_btn.clicked.connect(
                partial(self.on_select_all_elems, "bpm"))
        self.inverse_bpm_selection_btn.clicked.connect(
                partial(self.on_inverse_current_elem_selection, "bpm"))
        self.select_all_cors_btn.clicked.connect(
                partial(self.on_select_all_elems, "cor"))
        self.inverse_cor_selection_btn.clicked.connect(
                partial(self.on_inverse_current_elem_selection, "cor"))

        # DAQ
        self.daq_timer = QTimer()
        self.daq_timer.timeout.connect(self.on_daq_update)

        # post init
        self.post_init()

    @pyqtSlot(bool)
    def on_update_monitors(self, strategy, f):
        """Use 'all' or 'selected' BPMs as monitors.
        """
        if not f:
            return
        model = self.bpms_treeView.model()
        if model is None:
            self._bpms = []
            return
        if strategy == "all":
            self._bpms = self.bpms_treeView.model().get_elements("all")
        else:
            self._bpms = self.bpms_treeView.model().get_elements("selected")

    def update_correctors(self):
        """Update correctors selection (of cors_treeView).
        """
        model = self.cors_treeView.model()
        self._cors = model.get_elements("selected")

    @pyqtSlot(bool)
    def on_update_unit(self, unit, f):
        """Update BPM monitorings unit.
        """
        if f:
            self._bpm_unit = unit
            #print("BPM unit: {}".format(self._bpm_unit))

    @pyqtSlot()
    def on_select_elements(self, mode, dtype_list):
        """Select devices.
        """
        if self.__mp is None:
            QMessageBox.warning(self, "Select Element",
                    "Cannot find loaded lattice, try to load first, either by clicking Tools > Load Lattice or Ctrl+Shift+L.",
                    QMessageBox.Ok)
            return
        w = self._elem_sel_widgets.setdefault(mode,
                ElementSelectionWidget(self, self.__mp, dtypes=dtype_list))
        w.elementsSelected.connect(partial(self.on_update_elems, mode))
        w.show()

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    def post_init(self):
        #
        self.__mp = None
        self._bpm_unit = None
        self._bpms = []  # list of CaElements (e.g. BPM)
        self._cors = []  # list of CaElements (HCOR/VCOR)
        # cache
        self.last_one_rbtn.toggled.connect(partial(self.on_init_cached_traj, 1))
        self.last_five_rbtn.toggled.connect(partial(self.on_init_cached_traj, 5))
        # check last one cache
        self.last_one_rbtn.setChecked(True)

        # lattice load window
        self._lattice_load_window = None
        # elem selection widget, key: 'bpm' and 'cor'
        self._elem_sel_widgets = {}

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        # add another curve to matplotlibcurveWidget
        self.matplotlibcurveWidget.add_curve()

        # bpm monitorings unit
        self.bpm_unit_millimeter_rbtn.setChecked(True)
        assert self._bpm_unit == "mm"

        # selection of bpms for monitoring
        self.use_selected_bpms_rbtn.setChecked(True)
        assert self._bpms == []

        # magplot
        self.show_bpm_mag_btn.toggled.emit(self.show_bpm_mag_btn.isChecked())

        # DAQ
        self._daqfreq = 1.0

        # load default figure config
        p = self.matplotlibcurveWidget
        o = self.bpms_magplot
        apply_mplcurve_settings(p)
        apply_mplcurve_settings(o, filename='mpl_settings_mag.json')

        # init data viz
        self.__init_data_viz()

        # sync fig controls
        xmin, xmax = p.get_xlim()
        ymin, ymax = p.get_ylim()
        self.xmin_lineEdit.setText("{0:.3g}".format(xmin))
        self.xmax_lineEdit.setText("{0:.3g}".format(xmax))
        self.ymin_lineEdit.setText("{0:.3g}".format(ymin))
        self.ymax_lineEdit.setText("{0:.3g}".format(ymax))

        # orm window
        self._orm_window = None
        # Add another curve as reference, data could be selected from
        # cached data
        self._ref_line = self.matplotlibcurveWidget.add_curve(
                            label="Reference",
                            color='g', marker='D', mfc='w')
        # tuple of array of (s, b) for x and y
        self.__cached_traj = ()

        # ref_line for intensity
        self._ref_line_mag = self.bpms_magplot.add_curve(
                            label="Reference", ls='--', lw=1,
                            color='m', marker='D', mfc='w')

    @pyqtSlot(OrderedDict)
    def on_elem_selection_updated(self, mode, d):
        # mode 'bpm':
        #   BPMs selection (bpms_treeView) is updated
        #   * trigger the update of self._bpms (trigger data viz update (timeout))
        # mode 'cor':
        #   CORs selection (cors_treeView) is updated
        #   * trigger the update of self._cors
        model = getattr(self, '{}s_treeView'.format(mode)).model()
        if mode == 'bpm':
            #
            print("[TV] Monitors (BPMs) selction is changed...")
            #
            for o in (self.use_selected_bpms_rbtn, self.use_all_bpms_rbtn):
                o.toggled.emit(o.isChecked())
            # emit selected monitors
            self.monitorsChanged.emit(model._selected_elements)
        else:
            # 'cor' mode
            print("[TV] Correctors selection is changed...")
            self.update_correctors()
            # emit selected correctors
            self.correctorsChanged.emit(model._selected_elements)

        #print("[TV] Selection is updated: ", model._selected_elements)

    @pyqtSlot()
    def on_select_all_elems(self, mode):
        """Select all BPMs/CORs in *mode*s_treeView.
        """
        try:
            print("Select All {}s".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self, mode):
        """Inverse current BPM/COR selection in *mode*s_treeView.
        """
        try:
            print("Inverse {} selection".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot(list)
    def on_update_elems(self, mode, enames):
        """Selected element names list updated, mode: 'bpm'/'cor'
        """
        tv = getattr(self, "{}s_treeView".format(mode))
        model = ElementListModel(tv, self.__mp, enames)
        # list of fields of selected element type
        model.fieldsSelected.connect(partial(self.on_selected_fields_updated, mode))
        model.set_model()

        # bpm/cor selection is changed (elementlistmodel)
        m = tv.model()
        m.elementSelected.connect(partial(self.on_elem_selection_updated, mode))

    @pyqtSlot(QVariant)
    def update_lattice(self, o):
        self.__mp = o
        self.latticeChanged.emit(o)

    @pyqtSlot()
    def start_daq(self):
        # check if BPMs are selected from lattice.
        if self.not_selected_bpms():
            QMessageBox.warning(self, "DAQ Warning",
                    "BPMs are not found, Choose Monitors first.", QMessageBox.Ok)
            return
        # start DAQ
        self.daq_timer.start(1000.0/self._daqfreq)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        # not neat but good for testing
        if 'VA' in self.__mp.last_machine_name:
            self.__mag_field = 'PHA'
        else:
            self.__mag_field = 'MAG'

    @pyqtSlot()
    def stop_daq(self):
        self.daq_timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    @pyqtSlot()
    def on_daq_update(self):
        """Update DAQ and show data.
        """
        if self._bpms == []:
            return
        self.__update_line(0)
        self.__update_line(1)
        if self.show_bpm_mag_btn.isChecked():
            self.__update_intensity()

    @pyqtSlot()
    def onHelp(self):
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    @pyqtSlot()
    def on_launch_orm(self):
        """Launch ORM app.
        """
        if self.__mp is None:
            QMessageBox.warning(self, "ORM (Trajectory Viewer)",
                "Cannot find loaded lattice, try to load first, either by clicking Tools > Load Lattice or Ctrl+Shift+L.", QMessageBox.Ok)
            return

        try:
            m1 = self.bpms_treeView.model()
            m2 = self.cors_treeView.model()
            name_elem_map = m1.name_elem_map
            name_elem_map.update(m2.name_elem_map)
        except:
            name_elem_map = {}
            bpms_dict = {}
            cors_dict = {}
        else:
            bpms_dict = m1._selected_elements
            cors_dict = m2._selected_elements

        if self._orm_window is None:
            from phantasy.apps.orm import OrbitResponseMatrixWindow
            from phantasy.apps.orm import __version__
            self._orm_window = OrbitResponseMatrixWindow(self, __version__,
                    name_map=name_elem_map, mp=self.__mp,
                    bpms=bpms_dict, cors=cors_dict)
            self._orm_window.setWindowTitle(
                    "Orbit Response Matrix (Trajectory Viewer)")
            self.monitorsChanged.connect(
                    partial(self._orm_window.on_update_elements, 'bpm'))
            self.correctorsChanged.connect(
                    partial(self._orm_window.on_update_elements, 'cor'))
        #
        self._orm_window.show()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
        self._lattice_load_window.show()
        self._lattice_load_window.latticeChanged.connect(self.update_lattice)
        # reset element selection widgets
        self._elem_sel_widgets = {}

    def not_selected_bpms(self):
        """Test if BPMs are selected or not.
        """
        return self.bpms_treeView.model() is None

    @pyqtSlot(bool)
    def on_auto_xyscale(self, f):
        """Set auto xyscale or not
        """
        if f: # auto scale
            p = self.matplotlibcurveWidget
            xmin, xmax = p.get_xlim()
            ymin, ymax = p.get_ylim()
            self.xmin_lineEdit.setText("{0:.3g}".format(xmin))
            self.xmax_lineEdit.setText("{0:.3g}".format(xmax))
            self.ymin_lineEdit.setText("{0:.3g}".format(ymin))
            self.ymax_lineEdit.setText("{0:.3g}".format(ymax))
            for o in self.__xylimits_lineEdits:
                o.setEnabled(False)
        else:
            for o in self.__xylimits_lineEdits:
                o.setEnabled(True)

    @pyqtSlot(list)
    def on_selected_fields_updated(self, mode, fields):
        """List of fields for selected element type, only applied when mode
        is 'bpm'.
        """
        if mode != 'bpm':
            return
        # 1 set up field 1 and 2 cbb for data viz (two curves)
        # 2 try to set field-1 X/XCEN, and field-2 Y/YCEN
        fields_cbb = [self.field1_cbb, self.field2_cbb]
        cbs_cbb = [self.on_field1_updated, self.on_field2_updated]
        for o, cb in zip(fields_cbb, cbs_cbb):
            o.currentTextChanged.disconnect(cb)
            o.clear()
            o.addItems(fields)
            o.currentTextChanged.connect(cb)

        if 'X' in fields: # BPM
            self.field1_cbb.setCurrentText("X")
            self.field2_cbb.setCurrentText("Y")
        else: # PM, or others
            self.field1_cbb.setCurrentText("XCEN")
            self.field2_cbb.setCurrentText("YCEN")

        for o in fields_cbb:
            o.currentTextChanged.emit(o.currentText())

    @pyqtSlot('QString')
    def on_field1_updated(self, s):
        """Field-1 is changed, shown as 1st line.
        """
        # update 1st line
        print("Field-1 now is: ", s)
        self._field1 = s
        self.__update_line(0)

    @pyqtSlot('QString')
    def on_field2_updated(self, s):
        """Field-2 is changed, shown as 2nd line.
        """
        print("Field-2 now is: ", s)
        self._field2 = s
        self.__update_line(1)

    def __update_line(self, line_id):
        # refresh line *line_id*.
        # field: str, name of field
        ufac = BPM_UNIT_FAC[self._bpm_unit]
        self.lineChanged.emit(line_id)
        field = getattr(self, '_field{}'.format(line_id + 1))
        xdata = [elem.sb for elem in self._bpms]
        ydata = [getattr(elem, field) * ufac for elem in self._bpms]
        self.xdataChanged.emit(xdata)
        self.ydataChanged.emit(ydata)
        self.matplotlibcurveWidget.setLineLabel(field)
        if self.update_refline_chkbox.isChecked():
            # add to cache
            if line_id == 0:
                self._x_dq.append((xdata, ydata))
            elif line_id == 1:
                self._y_dq.append((xdata, ydata))
            #
            try:
                self.update_reflines()
            except:
                pass

    def update_reflines(self):
        # update cbb for reflines data
        xoy = self.refxoy_cbb.currentText()
        if xoy == 'X':
            dq = self._x_dq
        else:
            dq = self._y_dq
        self.__update_reflines(dq)
        self.__cached_traj = (np.asarray(self._x_dq),
                            np.asarray(self._y_dq))

    def __update_reflines(self, dq):
        x, y = np.asarray(dq).mean(axis=0)
        self.lineChanged.emit(2)
        self.xdataChanged.emit(x)
        self.ydataChanged.emit(y)

    @pyqtSlot('QString')
    def on_show_refcurve(self, s):
        if s == 'X':
            dq = self._x_dq
        else:
            dq = self._y_dq
        self.__update_reflines(dq)

    def __init_data_viz(self):
        # init data viz
        self.lineChanged.emit(0)
        self.xdataChanged.emit([])
        self.ydataChanged.emit([])
        self.lineChanged.emit(1)
        self.xdataChanged.emit([])
        self.ydataChanged.emit([])
        #
        p = self.bpms_magplot
        o = self.matplotlibcurveWidget
        p.setXData([])
        p.setYData([])

    def update_xylimit(self, fs, s):
        if 'YLimit' in fs:
            p = (self.matplotlibcurveWidget,)
        else:
            p = (self.matplotlibcurveWidget, self.bpms_magplot,)
        try:
            x = float(s)
            [getattr(o, fs)(x) for o in p]
        except:
            pass

    @pyqtSlot()
    def on_save_trajectory(self):
        print("Save reference trajectory (both X and Y) to file")
        filepath, ext = get_save_filename(self,
                cdir='.',
                filter="JSON Files (*.json)")
        if filepath is None:
            return

        machine, segment = self.__mp.last_machine_name, self.__mp.last_lattice_name
        print("machine:", machine)
        print("segment:", segment)
        ds = MonitorReadingsDataSheet()
        ds['machine'] = machine
        ds['segment'] = segment
        readings = []
        try:
            traj_x, traj_y = self.__cached_traj
            _, traj_x = traj_x.mean(axis=0)
            _, traj_y = traj_y.mean(axis=0)
        except:
            pass
        else:
            field1 = self.field1_cbb.currentText()
            field2 = self.field2_cbb.currentText()
            for (e, x, y) in zip(self._bpms, traj_x, traj_y):
                readings.append(
                        (e.name, {'field1': {'name': field1, 'value': x},
                                  'field2': {'name': field2, 'value': y},
                                  'phase': {'name': 'PHA', 'value': e.PHA},
                                  'intensity': {
                                      'name': self.__mag_field,
                                      'value': getattr(e, self.__mag_field)}}))
            ds['readings'] = readings
            ds.write(filepath)

    @pyqtSlot()
    def on_load_trajectory(self):
        print("Load reference trajectory (both X and Y) from file")
        filepath, ext = get_open_filename(self,
                filter="JSON Files (*.json)")
        if filepath is None:
            return

        readings = load_readings_sheet(filepath)
        s, x, y, mag = [], [], [], []
        for i, c in readings:
            s.append(i.sb)
            x.append(c['field1']['value'])
            y.append(c['field2']['value'])
            mag.append(c['intensity']['value'])
        self._x_dq.append((s, x))
        self._y_dq.append((s, y))
        self.update_reflines()
        self.__plot_loaded_intensity(s, mag)

    @pyqtSlot(bool)
    def on_init_cached_traj(self, n, f):
        if f:
            self._x_dq = deque([], n)
            self._y_dq = deque([], n)

    @pyqtSlot(bool)
    def on_show_hide_refline(self, f):
        # show/hide ref trajectory/intensity
        self._ref_line.set_visible(f)
        self._ref_line_mag.set_visible(f)
        self.matplotlibcurveWidget.update_figure()

    def __update_intensity(self):
        # update BPM intensities.
        o = self.bpms_magplot
        x = [elem.sb for elem in self._bpms]
        y = [getattr(elem, self.__mag_field) for elem in self._bpms]
        o.setLineID(0)
        o.setXData(x)
        o.setYData(y)

    def __plot_loaded_intensity(self, s, mag):
        # show loaded intensity as reference.
        self._ref_line_mag.set_xdata(s)
        self._ref_line_mag.set_ydata(mag)
        self.bpms_magplot.update_figure()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = TrajectoryViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
