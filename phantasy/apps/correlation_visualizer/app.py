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
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QThread

from .utils import PVElement
from .utils import PVElementReadonly
from .utils import random_string
from .utils import COLOR_DANGER, COLOR_INFO, COLOR_WARNING
from phantasy.apps.utils import get_save_filename

from .utils import milli_sleep

from .data import ScanDataModel

from .scan import ScanTask
from .scan import ScanWorker

from phantasy import epoch2human

TS_FMT = "%Y-%m-%d %H:%M:%S %Z"


class CorrelationVisualizerWindow(BaseAppForm, Ui_MainWindow):

    # scan log
    scanlogUpdated = pyqtSignal('QString')
    scanlogTextColor = pyqtSignal(QColor)

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
        self.scanlogUpdated.connect(self.on_update_log)
        self.scanlogTextColor.connect(self.scan_log_textEdit.setTextColor)
        self.curveUpdated.connect(self.scan_plot_widget.update_curve)

        # (new) unified button for setting alter element
        self.select_alter_elem_btn.clicked.connect(
                lambda: self.on_select_elem(mode='alter'))
        self._sel_elem_dialogs = {} # keys: 'alter', 'monitor'

        # (new) main monitor
        self.select_monitor_elem_btn.clicked.connect(
                lambda: self.on_select_elem(mode='monitor'))

        # alter range
        self.lower_limit_lineEdit.textChanged.connect(self.set_alter_range)
        self.upper_limit_lineEdit.textChanged.connect(self.set_alter_range)
        # range by percentage
        self.scan_percentage_dSpinbox.valueChanged.connect(self.set_alter_range_by_percentage)

        # (new) inventory for selected elements, key: element name.
        self.elem_widgets_dict = {}

        # UI post_init
        self._post_init_ui()

        # init scan config
        self.init_scan_config()

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
                self.scan_task.alter_element = sel_elem

                # initialize scan range
                x0 = self.scan_task.get_initial_setting()
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
                self.scan_task.monitor_element = sel_elem

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
        if self.scan_worker.is_running():
            return

        filename = get_save_filename(self, caption="Save data to file",
                    filter="JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)")

        if filename is not None:
            self.__save_scan_data(filename)

    def __save_scan_data(self, filename):
        """Save scan data.
        """
        data_sheet = self.scan_task.to_datasheet()

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

        # btn's status
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.retake_btn.setEnabled(False)

    @pyqtSlot(float)
    def set_alter_range_by_percentage(self, x):
        """Set scan range by percentage.
        """
        try:
            a = float(self.lower_limit_lineEdit.text())
            b = float(self.upper_limit_lineEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Warning",
                    "Invalid scan range input",
                    QMessageBox.Ok)
        else:
            x0 = (a + b) / 2
            val1, val2 = x0 * (1 - x / 100), x0 * (1 + x / 100)
            self.lower_limit_lineEdit.setText('{0:.2f}'.format(val1))
            self.upper_limit_lineEdit.setText('{0:.2f}'.format(val2))
            self.set_alter_range()

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
            self.scanlogUpdated.emit("Empty input of scan range is invalid...")
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

        # reset scan event log
        self.scan_log_textEdit.clear()
        #
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Starting scan task: {}".format(self.scan_task.name))

        # set alter element to start point
        x_start = self.scan_task.alter_start
        self.scanlogUpdated.emit(
            "Setting alter element to start value ({})...".format(x_start))
        self.scan_task.alter_element.value = x_start
        self.scanlogUpdated.emit(
            "Alter element reaches start value ({})".format(x_start))

        # reset scan_plot_widget

        # scan worker thread
        self.thread = QThread()
        self.scan_worker = ScanWorker(self.scan_task)
        self.scan_worker.moveToThread(self.thread)
        self.scan_worker.scanOneIterFinished.connect(self.on_one_iter_finished)
        self.scan_worker.scanAllDataReady.connect(self.on_scan_data_ready)
        self.scan_worker.scanAllFinished.connect(self.thread.quit)
        self.scan_worker.scanAllFinished.connect(self.scan_worker.deleteLater)
        self.scan_worker.scanAllFinished.connect(self.reset_alter_element)
        self.scan_worker.scanAllFinished.connect(lambda:self.set_btn_status(mode='stop'))
        self.scan_worker.scanAllFinished.connect(lambda:self.set_timestamp(type='stop'))
        self.scan_worker.scanAllFinished.connect(self.on_auto_title)
        # test
        self.scan_worker.scanAllFinished.connect(self.test_scan_finished)

        self.thread.finished.connect(self.thread.deleteLater)

        # test
        self.thread.started.connect(self.test_scan_started)

        self.thread.started.connect(lambda:self.set_btn_status(mode='start'))
        self.thread.started.connect(self.on_auto_labels)
        self.thread.started.connect(lambda:self.set_timestamp(type='start'))

        self.thread.started.connect(self.scan_worker.run)
        self.thread.start()

#        # start scan
#        self.scantimer.start(self.scantimer_deltmsec)
#        # task start timestamp
#        self.ts_start = time.time()
#        # stop timestamp
#        self.ts_stop = None
#
        # update UI
        #self.start_btn.setEnabled(False)
        #self.stop_btn.setEnabled(True)
        #self.pause_btn.setEnabled(True)
        #self.retake_btn.setEnabled(True)

        # auto xylabels
        #self.on_auto_labels()

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
        self.scan_worker.stop()
        self.scanlogTextColor.emit(COLOR_WARNING)
        self.scanlogUpdated.emit("Scan routine stopped.")

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

    @pyqtSlot()
    def set_scan_daq(self):
        """Set scan DAQ parameters, and timeout for DAQ and SCAN timers.
        """
        # total number of scan points
        self.scan_task.alter_number = self.niter_spinBox.value()

        # time wait after every scan data setup, in msec
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
        xlabel = get_auto_label(self.scan_task.alter_element)
        ylabel = get_auto_label(self.scan_task.monitor_element)
        self.scan_plot_widget.setFigureXlabel(xlabel)
        self.scan_plot_widget.setFigureYlabel(ylabel)

    @pyqtSlot()
    def on_auto_title(self):
        """Auto fill out the title of figure.
        """
        if self.scan_worker.is_running():
            QMessageBox.warning(self, "",
                    "Scan routine is not finished.",
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

        if self.scan_worker.is_running():
            # scan is not completed, do nothing
            return

        sm = ScanDataModel(self.scan_task.scan_out_data)
        y = sm.get_yavg()
        y_min, y_max = y.min(), y.max()

        alter_array = self.scan_task.get_alter_array()
        if pos == 'peak': # peak
            xm = alter_array[np.where(y==y_max)]
        elif pos == 'valley': # valley
            xm = alter_array[np.where(y==y_min)]

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
            self.scanlogTextColor.emit(COLOR_INFO)
            self.scanlogUpdated.emit("Set alter element value to {}...".format(x0))
            self.scan_task.alter_element.value = x0
            self.scanlogUpdated.emit("Alter element reaches {}.".format(x0))
            QMessageBox.information(self, "",
                "Set alter element to {0:.3f}".format(x0),
                QMessageBox.Ok)

    def reset_alter_element(self):
        x0 = self.scan_task.get_initial_setting()
        # restore alter elem
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Set back alter element value to {}...".format(x0))
        self.scan_task.alter_element.value = x0
        self.scanlogUpdated.emit(
            "Alter element reaches {}".format(x0))

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

