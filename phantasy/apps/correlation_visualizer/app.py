#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import epics
import numpy as np
import time
from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QThread

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction

from phantasy.library.misc import epoch2human
from phantasy.apps.utils import get_save_filename

from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.elementwidget import ElementWidget
from phantasy_ui.widgets.latticewidget import LatticeWidget

from .utils import PVElement
from .utils import PVElementReadonly
from .utils import random_string
from .utils import COLOR_DANGER, COLOR_INFO, COLOR_WARNING, COLOR_PRIMARY
from .utils import delayed_exec

from .app_help import HelpDialog
from .app_elem_select import ElementSelectDialog
from .app_array_set import ArraySetDialog
from .app_points_view import PointsViewWidget
from .app_monitors_view import MonitorsViewWidget
from .app_mps_config import MpsConfigWidget
from .data import ScanDataModel
from .scan import ScanTask
from .scan import ScanWorker
from .ui.ui_app import Ui_MainWindow

TS_FMT = "%Y-%m-%d %H:%M:%S"
BOTTOM_TBTN_ICON_SIZE = 32
SMALL_TBTN_ICON_SIZE = 20

BOTTOM_TBTN_ICON_QSIZE = QSize(BOTTOM_TBTN_ICON_SIZE, BOTTOM_TBTN_ICON_SIZE)
SMALL_TBTN_ICON_QSIZE = QSize(SMALL_TBTN_ICON_SIZE, SMALL_TBTN_ICON_SIZE)

# MPS status
MPS_STATUS = ["Fault", "Disable", "Monitor", "Enable"]
MPS_ENABLE_STATUS = "Enable"

# default MPS pv name
MPS_PV_DEFAULT = 'MPS_FPS:MSTR_N0001:MpsStatus' # FRIB MPS
#MPS_PV_DEFAULT = 'VA:SVR:MpsStatus' # VA MPS

class CorrelationVisualizerWindow(BaseAppForm, Ui_MainWindow):

    # scan log
    scanlogUpdated = pyqtSignal('QString')
    scanlogTextColor = pyqtSignal(QColor)

    # scan plot curve w/ errorbar
    curveUpdated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # loaded lattice elements
    elementsTreeChanged = pyqtSignal(QVariant)

    # number of extra monitors
    extraMonitorsNumberChanged = pyqtSignal(int)

    # MPS connection is changed, only when MPS guardian is enabled.
    mpsConnectionChanged = pyqtSignal(bool)

    # MPS status is changed
    mpsStatusChanged = pyqtSignal('QString')

    # signal to trig PAUSE action
    pauseScan = pyqtSignal(bool)

    def __init__(self, version):
        super(CorrelationVisualizerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Correlation Visualizer")

        # set app properties
        self.setAppTitle("Correlation Visualizer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Correlation Visualizer</h4>
            <p>This app is created to visualize the correlation between
            selected parameters, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # daq ctrl btns
        self.start_btn.clicked.connect(self.on_click_start_btn)
        self.stop_btn.clicked.connect(self.on_click_stop_btn)
        self.retake_btn.clicked.connect(self.on_click_retake_btn)
        self.pause_btn.clicked.connect(self.on_click_pause_btn)

        # events
        self.niter_spinBox.valueChanged.connect(self.set_scan_daq)
        self.nshot_spinBox.valueChanged.connect(self.set_scan_daq)

        self.waitsec_dSpinBox.valueChanged.connect(self.set_scan_daq)
        self.scanrate_dSpinBox.valueChanged.connect(self.set_scan_daq)
        # output scan data
        self.save_data_tbtn.clicked.connect(self.save_data)
        # auto xylabels
        self.auto_labels_tbtn.clicked.connect(self.on_auto_labels)
        # auto title
        self.auto_title_tbtn.clicked.connect(self.on_auto_title)
        # move to peak/valley
        self.moveto_tbtn.clicked.connect(self.on_moveto)
        # set btn: set alter_elem with the value vline pointing to
        self.set_tbtn.clicked.connect(self.on_set)
        # clear log btn
        self.clear_log_tbtn.clicked.connect(self.scan_log_textEdit.clear)
        # fs +
        self.inc_fontsize_tbtn.clicked.connect(lambda: self.update_logfontsize(mode="+"))
        # fs -
        self.dec_fontsize_tbtn.clicked.connect(lambda: self.update_logfontsize(mode="-"))

        # view selected points btn
        self.view_selected_pts_tbtn.clicked.connect(self.on_view_selected_points)

        # set alter array btn
        self.alter_array_btn.clicked.connect(self.on_set_alter_array)
        self._set_alter_array_dialogs = {} # keys: alter element name

        # enable arbitary alter array input
        self.enable_arbitary_array_chkbox.toggled.connect(self.on_toggle_array)

        # signals & slots
        self.scanlogUpdated.connect(self.on_update_log)
        self.scanlogTextColor.connect(self.scan_log_textEdit.setTextColor)
        self.curveUpdated.connect(self.scan_plot_widget.update_curve)
        # point selector
        self.scan_plot_widget.selectedIndicesUpdated.connect(self.on_select_points)

        # (new) unified button for setting alter element
        self.select_alter_elem_btn.clicked.connect(
                partial(self.on_select_elem, 'alter'))
        self._sel_elem_dialogs = {} # keys: 'alter', 'monitor'

        # (new) main monitor
        self.select_monitor_elem_btn.clicked.connect(
                partial(self.on_select_elem, 'monitor'))

        # additional monitors
        self.select_more_monitor_elems_btn.clicked.connect(
                self.on_select_extra_elem)
        # list of tuple of 'ename fname, mode',
        # ElementWidget keeps in self.elem_widgets_dict by indexing
        self._extra_monitors = []
        self.show_extra_monitors_btn.clicked.connect(
                self.on_show_extra_monitors)
        # widget for monitors view
        self.monitors_viewer = None

        # alter range
        self.lower_limit_lineEdit.textChanged.connect(self.set_alter_range)
        self.upper_limit_lineEdit.textChanged.connect(self.set_alter_range)

        # extra monitors counter
        self.extraMonitorsNumberChanged[int].connect(self.on_extra_monitors_number_changed)

        # inventory for selected elements
        # key: (ename, fname, mode), value: ElementWidget
        self.elem_widgets_dict = {}

        # UI post_init
        self._post_init_ui()

        # scan worker
        self.scan_worker = None

        # index array for retake
        self._indices_for_retake = []
        # (x, y) coords when seleted
        self._indices_for_retake_points = []

        # init scan config
        self.init_scan_config()

        # q-scan window
        self.qs_window = None

        # lattice-load window
        self.lattice_load_window = None
        self._mp = None

        # moveto flag, set True when moveto some point.
        self._moveto_flag = False

        # points selected viewer
        self.pts_viewer = None

        # mps config widget
        self.mps_config_widget = None
        self._mps_pvname = MPS_PV_DEFAULT
        self.mps_pv = epics.PV(self._mps_pvname)
        # enable MPS guardian by default
        delayed_exec(lambda:self.actionMPS_guardian.setChecked(True), 1.0)
        #self.actionMPS_guardian.setChecked(True)
        #
        self.pauseScan[bool].connect(self.on_pause_scan)

    @pyqtSlot(bool)
    def on_pause_scan(self, f):
        if f and self.pause_btn.isEnabled():
            self.pause_btn.setText('Resume')
            # pause action
            self.scanlogTextColor.emit(COLOR_DANGER)
            self.scanlogUpdated.emit("Scan is paused by MPS")
            self.scanlogTextColor.emit(COLOR_WARNING)
            self.scanlogUpdated.emit("Scan task is paused, click 'Resume' to continue")
            self.scan_worker.pause()
            QMessageBox.warning(self, "MPS Guardian Says",
                    "Scan is paused by MPS, click 'Resume' button to continue.",
                    QMessageBox.Ok)

    @pyqtSlot(bool)
    def on_toggle_array(self, ischecked):
        """If checked,
        1. disconnect textChanged of lower_limit_lineEdit, upper_limit_lineEdit
        2. disconnect valueChanged of niter_spinBox
        3. disable lower_limit_lineEdit, upper_limit_lineEdit, niter_spinBox
        if not checked, connect 1&2 and enable 3.
        """
        if ischecked:
            self.lower_limit_lineEdit.textChanged.disconnect()
            self.upper_limit_lineEdit.textChanged.disconnect()
            self.niter_spinBox.valueChanged.disconnect()
            self.lower_limit_lineEdit.setEnabled(False)
            self.upper_limit_lineEdit.setEnabled(False)
            self.niter_spinBox.setEnabled(False)
        else:
            self.lower_limit_lineEdit.textChanged.connect(self.set_alter_range)
            self.upper_limit_lineEdit.textChanged.connect(self.set_alter_range)
            self.niter_spinBox.valueChanged.connect(self.set_scan_daq)
            self.lower_limit_lineEdit.setEnabled(True)
            self.upper_limit_lineEdit.setEnabled(True)
            self.niter_spinBox.setEnabled(True)

    @pyqtSlot(QVariant, QVariant)
    def on_select_points(self, ind, pts):
        """*ind*: list of index numbers, *pts*: list of (x, y) coords.
        e.g. the orignal xarray is [5 4 3 2 1], selected ind is [1 2 4],
        then pts is [(xi,yi)], xi is x[1], x[2], x[4], i.e. 4, 3, 1, yi is
        the value at xi.
        """
        self.add_retake_indices(ind, pts)
        self.on_view_selected_points()

    def add_retake_indices(self, ind, pts):
        """Make index array for retake, if ind[i] is already selected,
        skip, if not add it into.
        """
        for i, idx in enumerate(ind):
            if idx in self._indices_for_retake:
                continue
            else:
                self._indices_for_retake.append(idx)
                self._indices_for_retake_points.append(pts[i])

    @pyqtSlot(int)
    def update_retake_indices_view(self, idx):
        """Update retake indices array, idx and points, and update points view.
        """
        self.remove_idx_from_retake_indices(idx)
        self.on_view_selected_points()

    def remove_idx_from_retake_indices(self, idx):
        """Remove *idx* from retake index array.
        """
        index_of_idx = self._indices_for_retake.index(idx)
        self._indices_for_retake.pop(index_of_idx)
        self._indices_for_retake_points.pop(index_of_idx)

    def clear_retake_indices(self):
        """Clear selected points for RETAKE to be empty list.
        """
        self._indices_for_retake = []
        self._indices_for_retake_points = []
        self.on_view_selected_points()

    @pyqtSlot()
    def on_select_elem(self, mode='alter'):
        """Select element via PV or high-level element for alter-vars and
        monitor-vars.
        """
        dlg = self._sel_elem_dialogs.setdefault(mode, ElementSelectDialog(self, mode, mp=self._mp))
        r = dlg.exec_()
        self.elementsTreeChanged.connect(dlg.on_update_elem_tree)

        if r == QDialog.Accepted:
            # update element obj (CaField)
            sel_elem = dlg.sel_elem # CaField
            sel_elem_display = dlg.sel_elem_display # CaElement
            if dlg.sel_field is None:
                elem_btn_lbl = sel_elem_display.ename
            else:
                elem_btn_lbl = '{0} [{1}]'.format(sel_elem_display.name, dlg.sel_field)

            new_sel_key = ' '.join((sel_elem_display.ename, sel_elem.name, mode))
            # create elem_info widget, add into *elem_widgets_dict*
            self.elem_widgets_dict.setdefault(
                new_sel_key, ElementWidget(sel_elem_display, fields=dlg.sel_field))

            elem_btn = QPushButton(elem_btn_lbl)
            elem_btn.setAutoDefault(True)
            elem_btn.clicked.connect(partial(self.on_show_elem_info, new_sel_key))
            elem_btn.setCursor(Qt.PointingHandCursor)

            if mode == 'alter':
                tp = "Element to alter, click to see element detail"
                current_hbox = self.alter_elem_lineEdit.findChild(QHBoxLayout)
                if current_hbox is None:
                    hbox = QHBoxLayout()
                    hbox.addWidget(elem_btn)
                    hbox.setContentsMargins(0, 0, 0, 0)
                    self.alter_elem_lineEdit.setLayout(hbox)
                else:
                    current_hbox.itemAt(0).widget().setParent(None)
                    current_hbox.addWidget(elem_btn)
                    current_hbox.update()
                self.scan_task.alter_element = sel_elem

                # initialize scan range
                x0 = self.scan_task.get_initial_setting()
                self.lower_limit_lineEdit.setText('{}'.format(x0))
                self.upper_limit_lineEdit.setText('{}'.format(x0))
            elif mode == 'monitor':
                tp = "Element to monitor, click to see element detail"
                current_hbox = self.monitor_elem_lineEdit.findChild(QHBoxLayout)
                if current_hbox is None:
                    hbox = QHBoxLayout()
                    hbox.addWidget(elem_btn)
                    hbox.setContentsMargins(0, 0, 0, 0)
                    self.monitor_elem_lineEdit.setLayout(hbox)
                else:
                    current_hbox.itemAt(0).widget().setParent(None)
                    current_hbox.addWidget(elem_btn)
                    current_hbox.update()
                self.scan_task.monitor_element = sel_elem

            elem_btn.setToolTip(tp)

        elif r == QDialog.Rejected:
            # do not update alter element obj
            return

    @pyqtSlot()
    def on_select_extra_elem(self):
        """Select element as extra monitor(s).
        """
        dlg = ElementSelectDialog(self, 'monitor', mp=self._mp)
        r = dlg.exec_()
        if r == QDialog.Accepted:
            sel_elem = dlg.sel_elem
            sel_elem_display = dlg.sel_elem_display

            new_sel_key = ' '.join((sel_elem_display.ename, sel_elem.name, 'monitor'))

            # add new monitor
            self.elem_widgets_dict.setdefault(
                new_sel_key, ElementWidget(sel_elem_display, fields=dlg.sel_field))

            if new_sel_key in self._extra_monitors:
                # skip if already selected as an extra monitor
                return
            self._extra_monitors.append(new_sel_key)

            # add to scan task
            self.scan_task.add_extra_monitor(sel_elem)
            # update the counter for the total number of extra monitors
            self.extraMonitorsNumberChanged.emit(len(self._extra_monitors))
            # show afterward by default
            if self.auto_show_extra_chkbox.isChecked():
                self.on_show_extra_monitors()

        elif r == QDialog.Rejected:
            return

    @pyqtSlot(int)
    def on_extra_monitors_number_changed(self, n):
        """Update the counter of total number of extra monitors.
        """
        self.extra_monitors_counter_lbl.setText("Monitors ({})".format(n))

    @pyqtSlot()
    def on_show_extra_monitors(self):
        """Show extra monitors.
        """
        # show all extra monitors of scan task
        data = [(name, self.elem_widgets_dict[name]) for name in self._extra_monitors]
        if self.monitors_viewer is None:
            self.monitors_viewer = MonitorsViewWidget(self, data)
        else:
            self.monitors_viewer.set_data(data)
        self.monitors_viewer.show()
        self.monitors_viewer.adjustSize()

    @pyqtSlot('QString')
    def update_extra_monitors(self, name):
        """Update extra monitors, after deletion.
        1. remove name from _extra_monitors
        2. remove key of name from elem_widgets_dict
        3. remove from scan_task
        4. update view
        """
        idx = self._extra_monitors.index(name)
        self._extra_monitors.remove(name)
        self.scan_task.del_extra_monitor(idx)
        self.extraMonitorsNumberChanged.emit(len(self._extra_monitors))
        self.on_show_extra_monitors()

    @pyqtSlot()
    def on_show_elem_info(self, name):
        """Show element obj info in a popup elementWidget.

        Parameters
        ----------
        name : str
            Element name.
        """
        w = self.elem_widgets_dict[name]
        w.setWindowTitle(name)
        w.show()

    @pyqtSlot()
    def save_data(self):
        """save data.
        """
        if self.scan_worker is None:
            return
        if self.scan_worker.is_running():
            return

        filename, ext = get_save_filename(self, caption="Save data to file",
            filter="JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5);;TXT Files (*.txt *.csv)")

        if filename is None:
            return
        if ext.upper() == 'JSON':
            self.__save_data_as_json(filename)
        elif ext.upper() == 'CSV':
            self.__save_data_as_array(filename)
        elif ext.upper() == 'H5':
            pass
        QMessageBox.information(self, "", "Save data to {}".format(filename))

    def __save_data_as_json(self, filename):
        """Save scan data as json datasheet.
        """
        data_sheet = self.scan_task.to_datasheet()

        data_sheet['data'].update({'filepath': filename})
        # save
        data_sheet.write(filename)
        # return flag to indicate success or fail.

    def __save_data_as_array(self, filename):
        """csv/txt"""
        sm = ScanDataModel(self.scan_task.scan_out_data)
        ynerr = [] # [yi, yi_err, ...], y0:x, y1:y
        for i in range(0, sm.shape[-1]):
            ynerr.append(sm.get_avg()[:, i])
            ynerr.append(sm.get_err()[:, i])

        header = 'App: Correlation Visualizer {}\n'.format(self._version)
        header += 'Data table saved on {}\n'.format(epoch2human(time.time(), fmt=TS_FMT))
        header += 'Scan job is done on {}\n'.format(epoch2human(self.scan_task.ts_stop, fmt=TS_FMT))
        header += 'Columns ({}) definitions: standard error comes after average reading\n'.format(2 * sm.shape[-1])
        header += '<x> x_std <y> y_std <y1> y1_std ...\n'
        header += 'x: {}\ny: {}\n'.format(
                self.scan_task.alter_element.readback[0],
                self.scan_task.monitor_element.readback[0])
        header += 'yi is the i-th extra monitor\n'
        for i,elem in enumerate(self.scan_task.get_extra_monitors()):
            header += 'Extra monitor {}: {}\n'.format(i+1, elem.readback[0])
        np.savetxt(filename, np.vstack(ynerr).T, header=header,
                   delimiter='\t')

    def _post_init_ui(self):
        """post init ui
        """
        # toolbtns
        # save data
        self.save_data_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.save_data_tbtn.setToolTip("Save data to file")
        # auto labels
        self.auto_labels_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.auto_labels_tbtn.setToolTip("Auto set xy labels")
        # auto title
        self.auto_title_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.auto_title_tbtn.setToolTip("Auto set figure title")
        # move to
        self.moveto_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.moveto_tbtn.setToolTip("Move cross-ruler to...")

        menu = QMenu(self)
        # to peak
        peak_action = QAction('Peak', self)
        peak_action.triggered.connect(lambda: self.on_moveto(pos='peak'))

        # to valley
        valley_action = QAction('Valley', self)
        valley_action.triggered.connect(lambda: self.on_moveto(pos='valley'))

        # hide cross-ruler
        hide_action = QAction('Hide', self)
        hide_action.triggered.connect(lambda: self.on_moveto(pos='hide'))

        # set up menu
        menu.addAction(peak_action)
        menu.addAction(valley_action)
        menu.addSeparator()
        menu.addAction(hide_action)
        self.moveto_tbtn.setMenu(menu)

        # scan event log textedit
        # clear log btn
        self.clear_log_tbtn.setIconSize(SMALL_TBTN_ICON_QSIZE)
        self.clear_log_tbtn.setToolTip("Clear scan event log")

        # fontsize + btn
        self.inc_fontsize_tbtn.setIconSize(SMALL_TBTN_ICON_QSIZE)
        self.inc_fontsize_tbtn.setToolTip("Increase Fontsize")
        # fontsize - btn
        self.dec_fontsize_tbtn.setIconSize(SMALL_TBTN_ICON_QSIZE)
        self.dec_fontsize_tbtn.setToolTip("Decrease Fontsize")

        # set btn
        self.set_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.set_tbtn.setToolTip("Set with value cross-ruler pointed")

        # view retake points btn
        self.view_selected_pts_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.view_selected_pts_tbtn.setToolTip("Show selected points to retake")

        menu_pts = QMenu(self)
        # show all selected points
        show_pts_act = QAction('Show', self)
        show_pts_act.triggered.connect(self.on_view_selected_points)
        # clear all points
        clear_pts_act = QAction('Clear', self)
        clear_pts_act.triggered.connect(self.clear_retake_indices)
        # set up menu_pts
        menu_pts.addAction(show_pts_act)
        menu_pts.addAction(clear_pts_act)
        self.view_selected_pts_tbtn.setMenu(menu_pts)

        # validators
        self.lower_limit_lineEdit.setValidator(QDoubleValidator())
        self.upper_limit_lineEdit.setValidator(QDoubleValidator())

        # btn's status
        self.set_btn_status(mode='init')

        # clear init curve data
        empty_arr = np.asarray([])
        self.curveUpdated.emit(empty_arr, empty_arr, empty_arr, empty_arr)

        # MPS guardian status
        mps_skipped_icon = QIcon(QPixmap(":/icons/mps_skipped.png"))
        mps_normal_icon = QIcon(QPixmap(":/icons/mps_normal.png"))
        mps_fault_icon = QIcon(QPixmap(":/icons/mps_fault.png"))
        mps_disconnected_icon = QIcon(QPixmap(":/icons/mps_disconnected.png"))
        mps_connected_icon = QIcon(QPixmap(":/icons/mps_connected.png"))
        self._mps_status_icons = {
            'skipped': mps_skipped_icon,
            'disconnected': mps_disconnected_icon,
            'connected': mps_connected_icon,
            'normal': mps_normal_icon,
            'fault': mps_fault_icon
        }

    @pyqtSlot()
    def set_alter_range(self):
        """Set scan alter vars range.
        """
        srange_val1_str = self.lower_limit_lineEdit.text()
        srange_val2_str = self.upper_limit_lineEdit.text()
        try:
            sval1, sval2 = float(srange_val1_str), float(srange_val2_str)
        except ValueError:
            self.scanlogTextColor.emit(COLOR_DANGER)
            self.scanlogUpdated.emit("Empty input of scan range is invalid")
        else:
            self.scan_task.alter_start = sval1
            self.scan_task.alter_stop = sval2

    def init_scan_config(self):
        """Initialize scan configurations, including:
        1. Scan vars: the vars to be altered and
           the ones used as monitoring purpose.
        2. Scan range
        3. DAQ settings
        4. Scan data out settings
        """
        task_name = random_string(6)
        self.scan_task = ScanTask(task_name)
        # initialize ScanTask
        # daq
        self.set_scan_daq()
        # scan range
        self.set_alter_range()

    @pyqtSlot()
    def on_click_start_btn(self):
        """Start a new scan routine, initialize everything.
        """
        # initialize configuration for scan routine
        # initialize scan out data
        self.scan_task.init_out_data()

        # check scan config
        if not self.scan_task.is_valid():
            QMessageBox.warning(self, "Scan Task Warning",
                    "Scan Task is not valid", QMessageBox.Ok)
            return

        #
        self.scanlogTextColor.emit(COLOR_PRIMARY)
        self.scanlogUpdated.emit("[START] button is pushed")
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Starting scan task: {}".format(self.scan_task.name))

        # set alter element to start point
        x_start = self.scan_task.alter_start
        self.scanlogUpdated.emit(
                "Setting alter element to {0:.3f}...".format(x_start))
        self.scan_task.alter_element.value = x_start
        self.scanlogUpdated.emit(
                "Alter element reaches {0:.3f}".format(x_start))

        # reset scan_plot_widget

        # start scan thread
        self.__start_scan_thread()

    def __retake_scan(self):
        """Retake at selected points.
        """
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit("Retake is activated...")
        self.__start_scan_thread(index_array=self._indices_for_retake)

    def __resume_scan(self):
        """Start scan at where paused.
        """
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Resuming scan task: {}".format(self.scan_task.name))
        self.__start_scan_thread(self.scan_starting_index)

    def __start_scan_thread(self, starting_index=0, index_array=None):
        # scan worker thread
        self.thread = QThread()
        self.scan_worker = ScanWorker(self.scan_task,
                                      starting_index=starting_index,
                                      index_array=index_array)
        self.scan_worker.moveToThread(self.thread)
        self.scan_worker.scanOneIterFinished.connect(self.on_one_iter_finished)
        self.scan_worker.scanAllDataReady.connect(self.on_scan_data_ready)
        self.scan_worker.scanFinished.connect(self.thread.quit)
        self.scan_worker.scanFinished.connect(self.scan_worker.deleteLater)
        self.scan_worker.scanFinished.connect(self.reset_alter_element)
        self.scan_worker.scanFinished.connect(lambda:self.set_btn_status(mode='stop'))
        self.scan_worker.scanFinished.connect(lambda:self.set_timestamp(type='stop'))
        self.scan_worker.scanFinished.connect(self.on_auto_title)

        # scan is stopped by STOP btn
        self.scan_worker.scanStopped.connect(self.scan_worker.scanFinished)

        # scan is paused by PAUSE btn
        self.scan_worker.scanPaused.connect(lambda:self.set_btn_status(mode='pause'))
        self.scan_worker.scanPausedAtIndex.connect(self.on_keep_scan_index)
        #
        self.scan_worker.scanPaused.connect(self.thread.quit)

        # test
        self.scan_worker.scanFinished.connect(self.test_scan_finished)

        self.thread.finished.connect(self.thread.deleteLater)

        # test
        self.thread.started.connect(self.test_scan_started)

        self.thread.started.connect(lambda:self.set_btn_status(mode='start'))
        self.thread.started.connect(self.on_auto_labels)
        self.thread.started.connect(lambda:self.set_timestamp(type='start'))

        self.thread.started.connect(self.scan_worker.run)
        self.thread.start()

    @pyqtSlot(int, float, QVariant)
    def on_one_iter_finished(self, idx, x, arr):
        """Every one iteration finished, push event log
        """
        niter = self.scan_task.alter_number
        self.scanlogTextColor.emit(COLOR_INFO)
        msg = 'Iter:{0:>3d}/[{1:d}] is done at value: {2:>9.2f}'.format(
                idx + 1, niter, x)
        self.scanlogUpdated.emit(msg)
        # update scan plot figure
        self.update_curve(arr)

    @pyqtSlot(QVariant)
    def on_scan_data_ready(self, arr):
        """Scan out data is ready.
        """
        print(arr)

    @pyqtSlot()
    def on_click_stop_btn(self):
        """Stop scan routine, can only start again.
        """
        if self.scan_worker is None:
            return
        if self.scan_worker.is_running():
            self.scanlogTextColor.emit(COLOR_PRIMARY)
            self.scanlogUpdated.emit("[STOP] button is pushed")
            self.scan_worker.stop()
            self.scanlogTextColor.emit(COLOR_WARNING)
            self.scanlogUpdated.emit("Scan task is stopped.")

    @pyqtSlot()
    def set_btn_status(self, mode='start'):
        """Set control btns status for 'start' and 'stop'.
        """
        if mode == 'start': # after push start button to start scan
            print("Thread is started...")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.pause_btn.setEnabled(True)
            self.retake_btn.setEnabled(True)
        elif mode == 'stop': # scan is finished or stopped
            print("Thread is stopped...")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.retake_btn.setEnabled(True)
        elif mode == 'pause': # scan is paused
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.retake_btn.setEnabled(False)
        elif mode == 'init': # when app is started up
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.retake_btn.setEnabled(False)

    @pyqtSlot()
    def on_click_pause_btn(self):
        """Pause scan routine.
        """
        if self.sender().text() == 'Pause':
            self.pause_btn.setText('Resume')
            # pause action
            self.scanlogTextColor.emit(COLOR_PRIMARY)
            self.scanlogUpdated.emit("[PAUSE] button is pushed")
            self.scanlogTextColor.emit(COLOR_WARNING)
            self.scanlogUpdated.emit("Scan task is paused, click 'Resume' to continue")
            self.scan_worker.pause()
        else:
            self.pause_btn.setText('Pause')
            self.scanlogTextColor.emit(COLOR_PRIMARY)
            self.scanlogUpdated.emit("[RESUME] button is pushed")
            # resume action
            self.__resume_scan()

    @pyqtSlot(int)
    def on_keep_scan_index(self, idx):
        """Keep the index at current scan value.
        """
        self.scan_starting_index = idx

    @pyqtSlot()
    def on_click_retake_btn(self):
        """Re-scan with selected points.
        """
        self.scanlogTextColor.emit(COLOR_PRIMARY)
        self.scanlogUpdated.emit("[RETAKE] button is pushed")
        self.__retake_scan()

    @pyqtSlot()
    def set_scan_daq(self):
        """Set scan DAQ parameters, and timeout for DAQ and SCAN timers.
        """
        # total number of scan points
        self.scan_task.alter_number = self.niter_spinBox.value()

        # time wait after every scan data setup, in sec
        self.scan_task.t_wait = self.waitsec_dSpinBox.value()

        # total shot number for each scan iteration
        self.scan_task.shotnum = self.nshot_spinBox.value()

        ## scan DAQ rate, in Hz
        self.scan_task.daq_rate = self.scanrate_dSpinBox.value()

    def update_curve(self, arr):
        """Update scan plot with fresh data.
        """
        sm = ScanDataModel(arr)
        x, y, xerr, yerr = sm.get_xavg(), sm.get_yavg(), sm.get_xerr(), sm.get_yerr()
        self.curveUpdated.emit(x, y, xerr, yerr)

    @pyqtSlot()
    def onQuadScanAction(self):
        """Show Quad scan data analysis app.
        """
        from phantasy.apps.quad_scan import QuadScanWindow
        from phantasy.apps.quad_scan import __version__

        if self.qs_window is None:
            try:
                self.qs_window = QuadScanWindow(__version__,
                        self.scan_task.to_datasheet())
            except (AttributeError, TypeError):
                QMessageBox.warning(self, "",
                    "Scan task is not complete, please try again later.",
                    QMessageBox.Ok)
                return
        self.qs_window.show()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self.lattice_load_window is None:
            self.lattice_load_window = LatticeWidget()
        self.lattice_load_window.show()
        self.lattice_load_window.latticeChanged.connect(self.update_mp)

    @pyqtSlot(QVariant)
    def update_mp(self, o):
        """Update MachinePortal instance, after reload lattice.
        """
        self._mp = o
        self.elementsTreeChanged.emit(o)

    @pyqtSlot(bool)
    def onEnableMPSGuardian(self, f):
        """Enable MPS guardian or not.
        """
        btn = self.mps_status_btn
        def on_mps_connected(pvname=None, conn=None, **kws):
            # MPS connection is changed
            self.mpsConnectionChanged.emit(conn)

        def on_mps_changed(**kws):
            # MPS status is changed
            v = kws.get('char_value')
            self.mpsStatusChanged.emit(v)

        if f:  # enable MPS guardian
            self.mps_pv.connection_callbacks = [on_mps_connected]
            self.mps_pv.add_callback(on_mps_changed)
            self.mpsConnectionChanged.connect(
                    partial(self.on_update_mps_status, reason='conn'))
            self.mpsStatusChanged.connect(
                    partial(self.on_update_mps_status, reason='val'))
            # if connected, set
            if self.mps_pv.connected:
                self.mpsConnectionChanged.emit(True)
                self.mpsStatusChanged.emit(self.mps_pv.get(as_string=True))
            else:
                self.mpsConnectionChanged.emit(False)
        else:  # not enable MPS guardian, MPS may be still running
            self.mpsConnectionChanged.disconnect()
            self.mpsStatusChanged.disconnect()
            btn.setIcon(self._mps_status_icons['skipped'])
            btn.setToolTip("MPS guardian is not enabled")

    @pyqtSlot()
    def on_update_mps_status(self, change, reason='conn'):
        """Update MPS status button icon when MPS guardian is enabled.
        *change* is bool when *reason* is 'conn', while str when
        *reason* is 'val'.
        """
        btn = self.mps_status_btn
        if reason == 'conn':
            if change:  # MPS is connected
                #print("set btn to connected icon")
                btn.setIcon(self._mps_status_icons['connected'])
                btn.setToolTip("MPS guardian is enabled, connection is established")
            else:  # MPS is disconnected
                #print("set btn to disconnected icon")
                btn.setIcon(self._mps_status_icons['disconnected'])
                btn.setToolTip("MPS guardian is enabled, connection is lost")
        else:  # val
            self._set_mps_status_btn(change)

    def _set_mps_status_btn(self, v):
        """Check MPS status readings, and set indicators.
        """
        btn = self.mps_status_btn
        if v != MPS_ENABLE_STATUS:
            #print("set btn to fault icon")
            btn.setIcon(self._mps_status_icons['fault'])
            # pause scan
            self.pauseScan.emit(True)
        else:
            #print("set btn to normal icon")
            btn.setIcon(self._mps_status_icons['normal'])
        btn.setToolTip("MPS guardian is enabled, status is {}".format(v))

    @pyqtSlot()
    def on_config_mps(self):
        """Config MPS: PV for the status.
        """
        if self.mps_config_widget is None:
            self.mps_config_widget = MpsConfigWidget(self)
        r = self.mps_config_widget.exec_()
        if r == QDialog.Accepted:
            self._mps_pvname = self.mps_config_widget.pvname
            self.mps_pv = epics.PV(self._mps_pvname)
            # re-check MPS guardian
            if self.actionMPS_guardian.isChecked():
                self.actionMPS_guardian.setChecked(False)
                delayed_exec(
                    lambda:self.actionMPS_guardian.setChecked(True), 5.0)
#                self.actionMPS_guardian.toggled.emit(True)
        else:
            pass

    @pyqtSlot()
    def onHelp(self):
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    @pyqtSlot()
    def on_auto_labels(self):
        """Auto fill out the xy labels of figure.
        """
        xlabel = get_auto_label(self.scan_task.alter_element)
        ylabel = get_auto_label(self.scan_task.monitor_element)
        self.scan_plot_widget.setFigureXlabel(xlabel)
        self.scan_plot_widget.setFigureYlabel(ylabel)

    @pyqtSlot()
    def on_auto_title(self):
        """Auto fill out the title of figure.
        """
        if self.scan_worker is None:
            return

        if self.scan_worker.is_running():
            QMessageBox.warning(self, "",
                    "Scan task is not finished.",
                    QMessageBox.Ok)
            return

        ts_start = self.scan_task.ts_start
        ts_stop = self.scan_task.ts_stop
        title = "Completed at {ts}\nSCAN Duration: {t:.2f} s".format(
                    ts=epoch2human(ts_stop, fmt=TS_FMT),
                    t=ts_stop-ts_start)
        self.scan_plot_widget.setFigureTitle(title)

    @pyqtSlot()
    def on_moveto(self, pos='peak'):
        """Move cross-ruler to the `xm` where y reaches max.
        *Pos*: 'peak' (default), 'valley', 'hide'.
        """
        if pos == 'hide':  # hide cross-ruler
            self.scan_plot_widget.set_visible_hvlines(False)
            self._moveto_flag = False
            return

        if self.scan_worker is None or self.scan_worker.is_running():
            # scan is not completed, do nothing
            return

        sm = ScanDataModel(self.scan_task.scan_out_data)
        y = sm.get_yavg()
        y_min, y_max = y.min(), y.max()

        alter_array = self.scan_task.get_alter_array()
        if pos == 'peak': # peak
            xm = alter_array[np.where(y==y_max)][0]
            ym = y_max
        elif pos == 'valley': # valley
            xm = alter_array[np.where(y==y_min)][0]
            ym = y_min

        # draw/update cross-ruler
        self.scan_plot_widget.draw_hvlines(xm, ym)
        self.scan_plot_widget.set_visible_hvlines(True)
        # set moveto_flag
        self._moveto_flag = True

    @pyqtSlot()
    def on_set(self):
        """Set alter_elem where cross-ruler pointing to
        """
        if not self._moveto_flag:
            QMessageBox.warning(self, "",
                "No value to set, click 'MoveTo' button or use " +
                "'Cross-ruler' tool to pick the coordinate to moveto",
                QMessageBox.Ok)
        else:
            x0 = self.scan_plot_widget._cpoint.get_xdata()[0]
            self.scanlogTextColor.emit(COLOR_INFO)
            self.scanlogUpdated.emit("Setting alter element to {0:.3f}...".format(x0))
            self.scan_task.alter_element.value = x0
            self.scanlogUpdated.emit("Alter element reaches {0:.3f}.".format(x0))
            QMessageBox.information(self, "",
                "Set alter element to {0:.3f}".format(x0),
                QMessageBox.Ok)

    def reset_alter_element(self):
        x0 = self.scan_task.get_initial_setting()
        # restore alter elem
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
                "Scan task is done, reset alter element...")
        self.scanlogUpdated.emit(
                "Setting alter element to {0:.3f}...".format(x0))
        self.scan_task.alter_element.value = x0
        self.scanlogUpdated.emit(
                "Alter element reaches {0:.3f}".format(x0))
        # in case it is 'resume' while scan is done
        self.pause_btn.setText('Pause')

    @pyqtSlot()
    def set_timestamp(self, type='start'):
        """Update start timestamp of scan task.
        """
        print("---set ts {}...".format(type))
        if type == 'start':
            self.scan_task.ts_start = time.time()
        elif type == 'stop':
            self.scan_task.ts_stop = time.time()

    @pyqtSlot('QString')
    def on_update_log(self, s):
        """Update scan event log.
        """
        msg = '[{0}] {1}'.format(epoch2human(time.time(), fmt=TS_FMT), s)
        self.scan_log_textEdit.append(msg)

    @pyqtSlot()
    def on_set_alter_array(self):
        """Set alter array dialog.
        """
        dlg = self._set_alter_array_dialogs.setdefault(
                self.scan_task.name, ArraySetDialog(self))
        r = dlg.exec_()

        if r == QDialog.Accepted:
            arr = dlg.array
            self.scan_task.set_alter_array(arr)
            self.niter_spinBox.setValue(self.scan_task.alter_number)
            v1, v2 = self.scan_task.alter_start, self.scan_task.alter_stop
            self.lower_limit_lineEdit.setText(str(v1))
            self.upper_limit_lineEdit.setText(str(v2))
        elif r == QDialog.Rejected:
            print("No array set")
            return

    @pyqtSlot()
    def on_view_selected_points(self):
        """Show selected points to retake.
        """
        alter_array = self.scan_task.get_alter_array()
        sm = ScanDataModel(self.scan_task.scan_out_data)
        x_rd, y_rd, sy_rd = sm.get_xavg(), sm.get_yavg(), sm.get_yerr()

        data = []
        for idx, pts in zip(self._indices_for_retake, self._indices_for_retake_points):
            # index, alter_value, selected_point_x_pos, selected_point_y_pos, current_y_pos
            # current_y_pos is updated when clicking this button, if after retaking, this value should be updated)
            data.append((idx, alter_array[idx], pts[0], pts[1], (y_rd[idx], sy_rd[idx])))

        if self.pts_viewer is None:
            self.pts_viewer = PointsViewWidget(self, data)
        else:
            self.pts_viewer.set_data(data)
        self.pts_viewer.show()
        self.pts_viewer.adjustSize()

    @pyqtSlot()
    def update_logfontsize(self, mode="+"):
        """Grow/shrink scan eventlog fontsize.
        """
        font = self.scan_log_textEdit.currentFont()
        ps = font.pointSize()
        new_ps = ps + 1 if mode == '+' else ps - 1
        font.setPointSize(new_ps)
        self.scan_log_textEdit.setCurrentFont(font)

    # test slots
    def test_scan_started(self):
        print(self.scan_task)
        print("-"*20)
        print("alter start : ", self.scan_task.alter_start)
        print("alter stop  : ", self.scan_task.alter_stop)
        print("alter number: ", self.scan_task.alter_number)
        print("shot number : ", self.scan_task.shotnum)
        print("alter array : ", self.scan_task.get_alter_array())
        print("alter elem  : ", self.scan_task.alter_element)
        print("monitor elem: ", self.scan_task.monitor_element)
        print("out data    : ", self.scan_task.scan_out_data)
        print("initial set : ", self.scan_task.get_initial_setting())
        print("ts_start    : ", self.scan_task.ts_start)
        print("ts_stop     : ", self.scan_task.ts_stop)
        print("-"*20)
        print("\n")

    def test_scan_finished(self):
        print(self.scan_task)
        print("-"*20)
        print("alter start : ", self.scan_task.alter_start)
        print("alter stop  : ", self.scan_task.alter_stop)
        print("alter number: ", self.scan_task.alter_number)
        print("shot number : ", self.scan_task.shotnum)
        print("alter array : ", self.scan_task.get_alter_array())
        print("alter elem  : ", self.scan_task.alter_element)
        print("monitor elem: ", self.scan_task.monitor_element)
        print("out data    : ", self.scan_task.scan_out_data)
        print("initial set : ", self.scan_task.get_initial_setting())
        print("ts_start    : ", self.scan_task.ts_start)
        print("ts_stop     : ", self.scan_task.ts_stop)
        print("-"*20)
        print("\n")
        print("thread is running?", self.thread.isRunning())


def get_auto_label(elem):
    """Return string of element name and field name.
    """
    if elem is None:
        return ''
    if isinstance(elem, (PVElement, PVElementReadonly)):
        # return readback pv name
        label = '{pv}'.format(pv=elem.readback[0])
    else:
        # !elem is CaField!
        # CaField
        # return element name and field name.
        label = '{en} [{fn}]'.format(en=elem.ename, fn=elem.name)
    return label

