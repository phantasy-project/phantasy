#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_app import Ui_MainWindow
from .app_help import HelpDialog
from .app_elem_select import ElementSelectDialog
from .icons import cv_icon
from .icons import save_icon
from .icons import xylabel_icon
from .icons import title_icon
from .icons import moveto_icon
from .icons import set_icon
from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.elementwidget import ElementWidget
from phantasy_ui.widgets.latticewidget import LatticeWidget

import numpy as np
import time
from collections import OrderedDict

from PyQt5.QtWidgets import qApp

from PyQt5.QtGui import QDoubleValidator

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize

from .utils import PVElement
from .utils import PVElementReadonly
from phantasy.apps.utils import get_save_filename

from .utils import milli_sleep

from .data import ScanDataModel
from .data import JSONDataSheet

from phantasy import epoch2human

TS_FMT = "%Y-%m-%d %H:%M:%S %Z"


class CorrelationVisualizerWindow(BaseAppForm, Ui_MainWindow):

    # scan log
    scanlogUpdated = pyqtSignal('QString')

    # scan plot curve w/ errorbar
    curveUpdated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # loaded lattice elements
    elementsTreeChanged = pyqtSignal(QVariant)

    def __init__(self, version):
        super(CorrelationVisualizerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Correlation Visualizer")
        self.setWindowIcon(QIcon(QPixmap(cv_icon)))

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

        # timers
        self.init_timers()

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

        # signals & slots
        self.scanlogUpdated.connect(self.scan_log_textEdit.append)
        self.curveUpdated.connect(self.scan_plot_widget.update_curve)

        # (new) unified button for setting alter element
        self.select_alter_elem_btn.clicked.connect(
                lambda: self.on_select_elem(mode='alter'))
        self._sel_elem_dialogs = {} # keys: 'alter', 'monitor'

        # (new) main monitor
        self.select_monitor_elem_btn.clicked.connect(
                lambda: self.on_select_elem(mode='monitor'))

        # alter range
        self.lower_limit_lineEdit.returnPressed.connect(self.set_alter_range)
        self.upper_limit_lineEdit.returnPressed.connect(self.set_alter_range)
        # range by percentage
        self.scan_percentage_dSpinbox.valueChanged.connect(self.set_alter_range_by_percentage)

        # (new) inventory for selected elements, key: element name.
        self.elem_widgets_dict = {}

        # UI post_init
        self._post_init_ui()

        # q-scan window
        self.qs_window = None

        # lattice-load window
        self.lattice_load_window = None
        self._mp = None

        # alter/monitor elem default values
        self.alter_elem = None
        self.monitor_elem = None

        # vars
        self.ts_start = None
        self.ts_stop = None
        # vline as ruler
        self.vline = None

        #####
        # test select monitors
        #self.select_more_monitor_elems_btn.clicked.connect(self.on_select_monitors)
        #self.elem_widgets_dict = {}
        #from phantasy import MachinePortal
        #self.mp = MachinePortal("VA_LS1FS1", "LINAC")
        #self.i = 0
        #self.tableWidget.setHorizontalHeaderLabels(['Element', 'Field'])

        #####

    #def _show(self):
    #    s = self.sender().text()
    #    w = self.elem_widgets_dict[s]
    #    w.setWindowTitle(w.ename())
    #    w.show()

    #@pyqtSlot()
    #def on_select_monitors(self):
    #    """Select monitor elements, put into the below tableWidget.
    #    """
    #    from PyQt5.QtWidgets import QWidget
    #    from PyQt5.QtCore import Qt
#
#        elem_obj = self.mp.get_elements(type="QUAD")[self.i]
#        self.elem_widgets_dict.setdefault(elem_obj.name,
#                ElementWidget(elem_obj))
#        btn = QPushButton(elem_obj.name)
#        btn.clicked.connect(self._show)
#
#        w = QWidget()
#        hbox = QHBoxLayout(w)
#        hbox.addWidget(btn)
#        hbox.setAlignment(Qt.AlignCenter)
#        hbox.setContentsMargins(5,5,5,5)
#        w.setLayout(hbox)
#
#        self.tableWidget.setRowCount(self.i + 1)
#        self.tableWidget.setCellWidget(self.i, 0, w)
#        self.tableWidget.resizeColumnsToContents()
#
#        self.i += 1

    @pyqtSlot()
    def on_select_elem(self, mode='alter'):
        """Select element via PV or high-level element for alter-vars and
        monitor-vars.
        """
        dlg = self._sel_elem_dialogs.setdefault(mode, ElementSelectDialog(self, mode))
        r = dlg.exec_()
        self.elementsTreeChanged.connect(dlg.on_update_elem_tree)

        if r == QDialog.Accepted:
            # update element obj
            sel_elem = dlg.sel_elem
            name = sel_elem.name
            # create elem_info widget, add into *elem_widgets_dict*
            self.elem_widgets_dict.setdefault(name, ElementWidget(sel_elem))

            elem_btn = QPushButton(name)
            elem_btn.setAutoDefault(True)
            elem_btn.clicked.connect(lambda: self.on_show_elem_info(name))
            elem_btn.setToolTip("Element to alter, click to see element detail")
            elem_btn.setCursor(Qt.PointingHandCursor)

            if mode == 'alter':
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
                self.alter_elem = sel_elem
                #
                # debug
                #print("Selected element name: ", sel_elem.name)
                #
                # initialize scan range
                x0 = self.alter_elem._putPV.get()
                self.lower_limit_lineEdit.setText('{}'.format(x0))
                self.upper_limit_lineEdit.setText('{}'.format(x0))
            elif mode == 'monitor':
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
                self.monitor_elem = sel_elem

        elif r == QDialog.Rejected:
            # do not update alter element obj
            print("cancel")
            return

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
        if self.ts_stop is None:
            return

        filename = get_save_filename(self, caption="Save data to file",
                    filter="JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)")

        if filename is not None:
            self.__save_scan_data(filename)

    def make_data_sheet(self):
        data_sheet = JSONDataSheet()
        # task
        task_dict = OrderedDict()
        task_dict['start'] = epoch2human(self.ts_start, fmt=TS_FMT)
        task_dict['stop'] = epoch2human(self.ts_stop, fmt=TS_FMT)
        task_dict['duration'] = self.ts_stop - self.ts_start
        task_dict['n_iteration'] = self.scan_iternum_val
        task_dict['n_shot'] = self.scan_shotnum_val
        task_dict['n_dim'] = 2
        task_dict['scan_range'] = self.alter_range_array.tolist()
        task_dict['t_wait'] = self.scan_waitmsec_val/1000.0
        task_dict['daq_rate'] = self.scan_daqrate_val
        data_sheet.update({'task': task_dict})

        # devices
        dev_dict = OrderedDict()
        dev_dict['quad'] = {
                'name': self.alter_elem.name,
                'readback_pv': self.alter_elem.get_pvname,
                'setpoint_pv': self.alter_elem.put_pvname,
        }
        dev_dict['monitors'] = []
        dev_dict['monitors'].append({
                'name': self.monitor_elem.name,
                'readback_pv': self.monitor_elem.get_pvname,
        })
        data_sheet.update({'devices': dev_dict})

        # data
        data_dict = OrderedDict()
        data_dict['created'] = epoch2human(time.time(), fmt=TS_FMT)
        data_dict['shape'] = self.scan_out_all.shape
        data_dict['array'] = self.scan_out_all.tolist()
        data_sheet.update({'data': data_dict})

        return data_sheet

    def __save_scan_data(self, filename):
        """Save scan data.
        """
        data_sheet = self.make_data_sheet()

        data_sheet['data'].update({'filepath': filename})
        # save
        data_sheet.write(filename)
        # return flag to indicate success or fail.

    def _post_init_ui(self):
        """post init ui
        """
        # toolbtns
        # save data
        self.save_data_tbtn.setIcon(QIcon(QPixmap(save_icon)))
        self.save_data_tbtn.setIconSize(QSize(48, 48))
        self.save_data_tbtn.setToolTip("Save data to file")
        # auto labels
        self.auto_labels_tbtn.setIcon(QIcon(QPixmap(xylabel_icon)))
        self.auto_labels_tbtn.setIconSize(QSize(48, 48))
        self.auto_labels_tbtn.setToolTip("Auto set xy labels")
        # auto title
        self.auto_title_tbtn.setIcon(QIcon(QPixmap(title_icon)))
        self.auto_title_tbtn.setIconSize(QSize(48, 48))
        self.auto_title_tbtn.setToolTip("Auto set figure title")
        # move to
        self.moveto_tbtn.setIcon(QIcon(QPixmap(moveto_icon)))
        self.moveto_tbtn.setIconSize(QSize(48, 48))
        self.moveto_tbtn.setToolTip("Move cursor line to...")
        menu = QMenu(self)

        # to peak
        peak_action = QAction('Peak', self)
        peak_action.triggered.connect(lambda: self.on_moveto(pos='peak'))

        # to valley
        valley_action = QAction('Valley', self)
        valley_action.triggered.connect(lambda: self.on_moveto(pos='valley'))

        # hide vline
        hide_action = QAction('Hide', self)
        hide_action.triggered.connect(lambda: self.on_moveto(pos='hide'))

        menu.addAction(peak_action)
        menu.addAction(valley_action)
        menu.addSeparator()
        menu.addAction(hide_action)
        self.moveto_tbtn.setMenu(menu)

        # set btn
        self.set_tbtn.setIcon(QIcon(QPixmap(set_icon)))
        self.set_tbtn.setIconSize(QSize(48, 48))
        self.set_tbtn.setToolTip("Set with value vline pointed")

        # validators
        self.lower_limit_lineEdit.setValidator(QDoubleValidator())
        self.upper_limit_lineEdit.setValidator(QDoubleValidator())

        # init scan config
        self.init_scan_config()

        # btn's status
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.retake_btn.setEnabled(False)

    @pyqtSlot('QString')
    def on_select_monitor_vars_type(self, val):
        """Select type for monitor var type
        """
        if val == 'Element':
            # do not accept input
            self.monitor_main_lineEdit.setEnabled(False)
            self.select_more_monitor_elems_btn.setEnabled(True)
        else:
            self.monitor_main_lineEdit.setEnabled(True)
            self.select_more_monitor_elems_btn.setEnabled(False)

    @pyqtSlot('QString')
    def on_select_alter_vars_type(self, val):
        """Select type for alter var type
        """
        if val == 'Element':
            # put and get boxes do not accept input
            self.alter_elem_lineEdit.setEnabled(False)
            self.select_scan_elems_btn.setEnabled(True)
        else:
            self.alter_elem_lineEdit.setEnabled(True)
            self.select_scan_elems_btn.setEnabled(False)

    @pyqtSlot(float)
    def set_alter_range_by_percentage(self, x):
        """Set scan range by percentage.
        """
        a = float(self.lower_limit_lineEdit.text())
        b = float(self.upper_limit_lineEdit.text())
        x0 = (a + b) / 2
        val1, val2 = x0 * (1 - x / 100), x0 * (1 + x / 100)
        self.lower_limit_lineEdit.setText('{0:.2f}'.format(val1))
        self.upper_limit_lineEdit.setText('{0:.2f}'.format(val2))
        self.set_alter_range()

    @pyqtSlot()
    def set_alter_range(self):
        """Set scan alter vars range.

        *alter_range_array* : array to iterately alter
        """
        srange_val1_str = self.lower_limit_lineEdit.text()
        srange_val2_str = self.upper_limit_lineEdit.text()
        if srange_val1_str == '' or srange_val2_str == '':
            return

        sval1, sval2 = float(srange_val1_str), float(srange_val2_str)
        self.alter_range_array = np.linspace(
            sval1, sval2, self.scan_iternum_val)

    def set_scan_outdata(self):
        """Set storage for the data yield from scan.
        """
        # pre-allocated array for every iteration
        self.scan_out_per_iter = np.zeros((self.scan_shotnum_val, 2))
        # pre-allocated array for all the iteration
        # shape: niter, nshot, ndim (2)
        self.scan_out_all = np.asarray([
            [[np.nan, np.nan]] * self.scan_shotnum_val
            ] * self.scan_iternum_val
        )

        # set current index at altered, i.e. self.alter_range_array
        self.current_alter_index = 0

    def init_scan_config(self):
        """Initialize scan configurations, including:
        1. Scan vars: the vars to be altered and
           the ones used as monitoring purpose.
        2. Scan range
        3. DAQ settings
        4. Scan data out settings
        """
        # vars to be altered:

        # vars to be monitored:
        #self.set_monitor_vars()

        # scan daq params
        self.set_scan_daq()

        # scan range
        self.set_alter_range()

        # scan output data
        self.set_scan_outdata()

    @pyqtSlot()
    def on_click_start_btn(self):
        """Start a new scan routine, initialize everything.
        """
        # initialize configuration for scan routine
        self.init_scan_config()

        # reset scan log
        self.scan_log_textEdit.clear()
        self.scanlogUpdated.emit("Starting scan...")

        # reset scan_plot_widget

        # set alter element to start point
        x0 = self.alter_range_array[0]
        self._x0_set = self.alter_elem._putPV.get()
        print("current setpoint: {}".format(self._x0_set))
        print("starting setpoint: {}".format(x0))
        print("Setting to starting setpoint...")
        self.alter_elem._putPV.put(x0, wait=True)

        # start scan
        self.scantimer.start(self.scantimer_deltmsec)
        # task start timestamp
        self.ts_start = time.time()
        # stop timestamp
        self.ts_stop = None

        # update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)
        self.retake_btn.setEnabled(True)

        # auto xylabels
        self.on_auto_labels()

    @pyqtSlot()
    def on_click_stop_btn(self):
        """Stop scan routine, can only start again.
        """
        self.scantimer.stop()
        self.daqtimer.stop()
        # publish summary info in scan log
        self.scanlogUpdated.emit("Scan routine stopped.")

        # set back alter element
        self._set_back_alter_element()

        # update UI
        self.stop_btn.setEnabled(False)
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.retake_btn.setEnabled(True)

    @pyqtSlot()
    def on_click_pause_btn(self):
        """Pause scan routine.
        """
        if self.sender().text() == 'Pause':
            self.pause_btn.setText('Resume')
            # pause action
        else:
            self.pause_btn.setText('Pause')
            # resume action
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.retake_btn.setEnabled(True)

    @pyqtSlot()
    def on_click_retake_btn(self):
        """Re-scan with selected points.
        """
        self.retake_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)

    def init_timers(self):
        """Initialize timers for DAQ and SCAN control.
        """
        self.daqtimer = QTimer()
        self.scantimer = QTimer()
        self.daqtimer.timeout.connect(self.on_daqtimer_timeout)
        self.scantimer.timeout.connect(self.on_scantimer_timeout)

    @pyqtSlot()
    def on_daqtimer_timeout(self):
        """DAQ within one scan iteration.
        """
        try:
            assert self.daq_cnt < self.scan_shotnum_val
        except AssertionError:
            # stop DAQ timer
            self.daqtimer.stop()

            # update scan log
            idx = self.current_alter_index_in_daq
            log = 'Iter:{0:>3d}/[{1:d}] is done at value: {2:>9.2f}.'.format(
                    idx + 1, self.scan_iternum_val, self.alter_range_array[idx])
            self.scanlogUpdated.emit(log)

            # debug only
            #print("-"*20)
            #print(self.current_alter_index_in_daq)
            #print(self.scan_out_per_iter)
            #print(self.scan_out_all)
            #print("-"*20)

            # push finish message
            if not self.scantimer.isActive():
                self.scanlogUpdated.emit("Scan routine finished.")

            # update figure
            self.update_curve()

        else:
            self.scan_out_per_iter[self.daq_cnt, :] = \
                self.alter_elem.value, \
                self.monitor_elem.value

            # update data: scan_out_all
            self.scan_out_all[self.current_alter_index_in_daq, :, :] = self.scan_out_per_iter

            # next daq event
            self.daq_cnt += 1

    @pyqtSlot()
    def on_scantimer_timeout(self):
        """Update parameters for next scan iteration.
        """
        try:
            assert self.current_alter_index < self.scan_iternum_val
        except AssertionError:
            self.scantimer.stop()
            self.start_btn.setEnabled(True)
            #
            # task stop timestamp
            self.ts_stop = time.time()

            # set back alter element
            self._set_back_alter_element()

            # auto title
            self.on_auto_title()

        else:
            # get the current value to be set
            current_alter_val = self.alter_range_array[self.current_alter_index]
            # make set/put operation
            self.alter_elem.value = current_alter_val

            # wait
            milli_sleep(qApp, self.scan_waitmsec_val)

            # start DAQ
            self.start_daqtimer(self.daqtimer_deltmsec, self.current_alter_index)

            # to next alter value
            self.current_alter_index += 1

    def start_daqtimer(self, deltmsec, idx):
        """Start DAQ timer, current alter data *idx* must be reserved within
        the DAQ routine.

        Parameters
        ----------
        deltmsec : float
            Millisecond timeout interval for DAQ timer.
        idx : int
            Index of the current alter value.
        """
        self.current_alter_index_in_daq = idx
        self.daq_cnt = 0 # max: self.scan_shotnum_val
        self.daqtimer.start(deltmsec)

    @pyqtSlot()
    def set_scan_daq(self):
        """Set scan DAQ parameters, and timeout for DAQ and SCAN timers.
        """
        # total number of scan points
        self.scan_iternum_val = self.niter_spinBox.value()
        # time wait after every scan data setup, in msec
        self.scan_waitmsec_val = self.waitsec_dSpinBox.value() * 1000.0
        # total shot number for each scan iteration
        self.scan_shotnum_val = self.nshot_spinBox.value()
        # scan DAQ rate, in Hz
        self.scan_daqrate_val = self.scanrate_dSpinBox.value()

        # scan DAQ timer timeout interval, in msec
        self.daqtimer_deltmsec = 1000.0 / self.scan_daqrate_val

        # SCAN timer timeout interval (between iteration), in msec
        self.scantimer_deltmsec = self.scan_waitmsec_val + (
                self.scan_shotnum_val + 2) * self.daqtimer_deltmsec

        # debug
        #print("iter:{iter}, shot#:{shot}, wait_t:{wt}, daq:{daq}".format(
        #    iter=self.scan_iternum_val, shot=self.scan_shotnum_val,
        #    wt=self.scan_waitmsec_val, daq=self.scan_daqrate_val))
        #print("DAQ Timer interval: {}ms\nSCAN Timer interval: {} ms".format(
        #    self.daqtimer_deltmsec, self.scantimer_deltmsec))

    def delayed_check_pv_status(self, pvelem, delay=1000):
        """Check PV element connected or not.

        Parameters
        ----------
        pvelem : obj
            Instance of `epics.PV`, `PVElement`, `PVElementReadonly`.
        delay : float
            Delay milliseconds to check PV status.
        """
        def check_status(elem):
            if not elem.connected:
                QMessageBox.warning(self, "Warning",
                        "Cannot connect to the input PV(s).",
                        QMessageBox.Ok)
        QTimer.singleShot(delay, lambda: check_status(pvelem))

    def update_curve(self):
        """Update scan plot with fresh data.
        """
        sm = ScanDataModel(self.scan_out_all)
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
                self.qs_window = QuadScanWindow(__version__, self.make_data_sheet())
            except AttributeError:
                QMessageBox.warning(self, "",
                    "Scan Routine is not complete, please try again later.",
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

    @pyqtSlot()
    def onHelp(self):
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    @pyqtSlot()
    def on_auto_labels(self):
        """Auto fill out the xy labels of figure.
        """
        xlabel = get_auto_label(self.alter_elem)
        ylabel = get_auto_label(self.monitor_elem)
        self.scan_plot_widget.setFigureXlabel(xlabel)
        self.scan_plot_widget.setFigureYlabel(ylabel)

    @pyqtSlot()
    def on_auto_title(self):
        """Auto fill out the title of figure.
        """
        if self.ts_stop is None: # scan routine is not finished
            return
        title = "Completed at {ts}\nSCAN Duration: {t:.2f} s".format(
                    ts=epoch2human(self.ts_stop, fmt=TS_FMT),
                    t=self.ts_stop-self.ts_start)
        self.scan_plot_widget.setFigureTitle(title)

    @pyqtSlot()
    def on_moveto(self, pos='peak'):
        """
        1. Move vline to the `xm` where y reaches max.
        2. Set alter elem value as `xm`.
        Pos: 'peak' (default), 'valley', 'hide'.
        """
        if pos == 'hide':
            # hide vline
            if self.vline is not None:
                self.vline.set_visible(False)
                self.scan_plot_widget.update_figure()
            return

        if self.ts_stop is None:
            # no scan completed, do nothing
            return

        sm = ScanDataModel(self.scan_out_all)
        y = sm.get_yavg()
        y_min, y_max = y.min(), y.max()

        if pos == 'peak': # peak
            xm = self.alter_range_array[np.where(y==y_max)]
        elif pos == 'valley': # valley
            xm = self.alter_range_array[np.where(y==y_min)]

        if self.vline is None:
            self.vline = self.scan_plot_widget.axes.axvline(x=xm,
                    alpha=0.8, color='r', ls='--')
            self.scan_plot_widget.update_figure()
        else:
            self.vline.set_visible(True)
            self.vline.set_xdata([xm, xm])
            self.scan_plot_widget.update_figure()

    @pyqtSlot()
    def on_set(self):
        """Set alter_elem where vline pointing to
        """
        if self.vline is None:
            QMessageBox.warning(self, "",
                "No value to set, click MoveTo first",
                QMessageBox.Ok)
        else:
            x0 = self.vline.get_xdata()[0][0]
            self.alter_elem._putPV.put(x0, wait=True)
            QMessageBox.information(self, "",
                "Set alter element to {0:.3f}".format(x0),
                QMessageBox.Ok)

    def _set_back_alter_element(self):
        # restore alter elem
        self.scanlogUpdated.emit("Set back alter element...")
        self.alter_elem._putPV.put(self._x0_set, wait=True)

def get_auto_label(elem):
    """Return string of element name and field name.
    """
    if elem is None:
        return ''
    if isinstance(elem, (PVElement, PVElementReadonly)):
        # return readback pv name
        label = '{pv}'.format(pv=elem.readback[0])
    else:
        # CaElement
        # return element name and field name.
        pass
    return label

