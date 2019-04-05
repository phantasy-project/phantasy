#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import time
from collections import OrderedDict
from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_ui.widgets import LatticeWidget
from phantasy.apps.trajectory_viewer.app_elem_selection import ElementSelectionWidget

from .ui.ui_app import Ui_MainWindow
from .app_save import SaveDataDialog
from .utils import ElementListModelDV as ElementListModel

DTYPE_LIST = ("BCM", "ND", "HMR", )


class DeviceViewerWindow(BaseAppForm, Ui_MainWindow):

    # update
    data_updated = pyqtSignal(QVariant, QVariant, QVariant)
    # init
    data_initialized = pyqtSignal(QVariant, QVariant, QVariant)
    ## selected devices and fields, k: ename, v: list of fields
    #devicesChanged = pyqtSignal(dict)

    # segments updated, list of loaded segments
    segments_updated = pyqtSignal(list)

    xtklbls_changed = pyqtSignal(list)
    xtks_changed = pyqtSignal(list)

    def __init__(self, version):
        super(DeviceViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Devices Viewer")

        # set app properties
        self.setAppTitle("Devices Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Devices Viewer</h4>
            <p>This app is created to visualize the device readings of FRIB
            accelerator, including the diagnostic devices and optics settings,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self._post_init()

    def _post_init(self,):
        # lattice load window
        self._lattice_load_window = None
        # elem selection widget
        self._elem_sel_widget = None
        #
        # list of field names of selected elements
        self.__mp = None
        self._field_list = []
        # list of selected elems
        self._elems_list = []
        # data save
        self._data_save_dlg = None
        #
        self.data_updated.connect(self.matplotlibbarWidget.update_curve)
        self.data_initialized.connect(self.matplotlibbarWidget.reset_data)
        self.set_widgets_status("WAIT")

        # DAQ freq
        self._daq_stop = False
        self._daq_nshot = 1
        self._daqfreq = 1.0
        self.daqfreq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)
        self.daq_nshot_sbox.valueChanged[int].connect(self.update_daq_nshot)
        self._viz_active_px = QPixmap(":/icons/active.png")
        self._viz_inactive_px = QPixmap(":/icons/inactive.png")
        self.daq_pb.setVisible(False)

        # xdata opt
        self.id_as_x_rbtn.setChecked(False)
        self.pos_as_x_rbtn.setChecked(True)
        self._xdata_gauge = 'pos'

        # show with D#### or device name
        self._xtklbls_dnum = []   # init by reset
        self._xtklbls_dname = []  # init by reset

        self.xtks_changed.connect(self.matplotlibbarWidget.set_xticks)
        self.xtklbls_changed.connect(self.matplotlibbarWidget.set_xticklabels)

        # annote
        self._show_annote = False

        # device selection
        self.choose_elems_btn.clicked.connect(self.on_list_devices)
        self.select_all_elems_btn.clicked.connect(self.on_select_all_elems)
        self.inverse_selection_btn.clicked.connect(self.on_inverse_current_elem_selection)

        # field cbb
        self.field_cbb.currentTextChanged.connect(self.on_elem_field_changed)

        # reset figure
        # does not work with matlotlib 2.0.0
        # self.on_init_dataviz()

    @pyqtSlot()
    def on_select_all_elems(self):
        try:
            model = self.devices_treeView.model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self):
        try:
            model = self.devices_treeView.model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    @pyqtSlot(int)
    def update_daq_nshot(self, i):
        self._daq_nshot = i

    @pyqtSlot()
    def on_daq_start(self):
        """Start DAQ.
        """
        if self._elems_list == [] :
            QMessageBox.warning(self, "DAQ Warning",
                    "Cannot find loaded devices.", QMessageBox.Ok)
            return

        if self._daq_stop:
            self.set_widgets_status("STOP")
            return

        self._delt = 1.0 / self._daqfreq
        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(self._daq_nshot))
        self.daq_th.started.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.finished.connect(self.on_daq_start)

        self.daq_th.start()

    @pyqtSlot()
    def on_daq_stop(self):
        """Stop DAQ.
        """
        self._daq_stop = True

    def __refresh_data(self):
        h = [getattr(e, f) for e, f in zip(self._elems_list, self._field_list)]
        if self._xdata_gauge == 'pos':
            s = [e.sb for e in self._elems_list]
        else: # ID as x
            s = list(range(len(h)))
        herr = [0] * len(h)
        self._xtks = s
        # only work with D####
        self._xtklbls_dnum = [e.name[-5:] for e in self._elems_list]
        self._xtklbls_dname = [e.name for e in self._elems_list]
        return s, h, herr

    @pyqtSlot()
    def on_init_dataviz(self):
        # initial plot (reset figure btn)
        s, h, herr = self.__refresh_data()
        self.data_initialized.emit(s, h, herr)
        # reset daq bit
        self._daq_stop = False
        # reset xtklbl
        self.reset_xtklbls()
        # viz cnt
        self._viz_cnt = 0
        self.viz_cnt_lbl.setText('0')
        if self._daq_nshot > 1:
            # daq pb
            self.daq_pb.setValue(0)
            self.daq_pb.setVisible(True)
        else:
            self.daq_pb.setVisible(False)

        # tmp solution
        from mpl4qt.widgets.mplconfig import MatplotlibConfigBarPanel
        MatplotlibConfigBarPanel(self.matplotlibbarWidget)
        #

    @pyqtSlot(bool)
    def on_apply_id_as_xdata(self, f):
        if f:
            print("Apply ID as xdata")
            self._xdata_gauge = 'id'

    @pyqtSlot(bool)
    def on_apply_pos_as_xdata(self, f):
        if f:
            print("Apply Pos as xdata")
            self._xdata_gauge = 'pos'

    def set_widgets_status(self, status):
        olist1 = (self.reset_figure_btn, self.start_btn,
                  self.id_as_x_rbtn, self.pos_as_x_rbtn,
                  self.devices_treeView, self.capture_btn, )
        olist2 = (self.stop_btn, )
        if status != "START":
            [o.setEnabled(True) for o in olist1]
            [o.setEnabled(False) for o in olist2]
        else:
            [o.setEnabled(False) for o in olist1]
            [o.setEnabled(True) for o in olist2]

    @pyqtSlot(bool)
    def on_annote_height(self, f):
        o = self.matplotlibbarWidget
        self._show_annote = f
        if f:
            # annote height on top/bottom of bar
            o.annotate_bar()
        else:
            if o._all_annotes is None:
                return
            # hide annotes
            [i.set_visible(False) for i in o._all_annotes]
        o.update_figure()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
        self._lattice_load_window.show()
        self._lattice_load_window.latticeChanged.connect(self.update_lattice)
        # reset element selection widgets
        self._elem_sel_widget = None

    @pyqtSlot(QVariant)
    def update_lattice(self, o):
        self.__mp = o
        self.segments_updated.emit(self.__mp.lattice_names)

    @pyqtSlot()
    def on_list_devices(self):
        if self.__mp is None:
            QMessageBox.warning(self, "Device Selection",
                    "Cannot find loaded lattice, try to load first, either by clicking Tools > Load Lattice or Ctrl+Shift+L.",
                    QMessageBox.Ok)
            return
        w = self._elem_sel_widget = ElementSelectionWidget(self,
                self.__mp, dtypes=DTYPE_LIST)
        w.elementsSelected.connect(self.on_update_elems)
        w.show()

    @pyqtSlot(list)
    def on_update_elems(self, enames):
        """Selected element names list updated.
        """
        tv = self.devices_treeView
        model = ElementListModel(tv, self.__mp, enames)
        # list of fields of selected element type
        model.fieldsSelected.connect(self.on_selected_fields_updated)
        model.set_model()

        m = tv.model()
        m.elementSelected.connect(self.on_elem_selection_updated)
        model.select_all_items()

    @pyqtSlot(OrderedDict)
    def on_elem_selection_updated(self, d):
        print("selected elems:", d)
        self._field_list = [f[0] for _, f in d.items()]
        self._elems_list = self.devices_treeView.model().get_elements("selected")
        #model = self.devices_treeView.model()
        #self.devicesChanged.emit(model._selected_elements)

    @pyqtSlot(list)
    def on_selected_fields_updated(self, fields):
        o = self.field_cbb
        o.clear()
        o.addItems(fields)
        if 'X' in fields:
            # BPM
            o.setCurrentText('X')
        elif 'TYP' in fields:
            # BCM
            o.setCurrentText('TYP')

    @pyqtSlot('QString')
    def on_elem_field_changed(self, s):
        try:
            model = self.devices_treeView.model()
            model.change_field(s)
        except AttributeError:
            QMessageBox.warning(self, "Change Field",
                    "Failed to change field.", QMessageBox.Ok)

    @pyqtSlot(QVariant)
    def on_daq_results_ready(self, res):
        #print("DAQ Results: ", res)
        self.data = data = np.array(res)
        h, herr = data.mean(axis=0), data.std(axis=0)

        if self._xdata_gauge == 'pos': # s-pos as x
            s = [e.sb for e in self._elems_list]
        else: # ID as x
            s = list(range(len(h)))

        self.data_updated.emit(s, h, herr)

        self.matplotlibbarWidget.clear_annote()
        self.annote_height_chkbox.toggled.emit(self._show_annote)

    def daq_single(self, iiter):
        # fetch data from all devices
        # daq_seq is range(shot number)
        x = np.zeros(len(self._elems_list))
        for i, (e, f) in enumerate(zip(self._elems_list, self._field_list)):
            x[i] = getattr(e, f)
        time.sleep(self._delt)
        return x

    def on_update_daq_status(self, f, s):
        # beat DAQ viz status
        if f == 1.0:
            px = self._viz_active_px
            self._viz_cnt += 1
            self.viz_cnt_lbl.setText(str(self._viz_cnt))
        else:
            px = self._viz_inactive_px
        self.daq_status_lbl.setPixmap(px)
        QTimer.singleShot(200,
                lambda:self.daq_status_lbl.setPixmap(self._viz_inactive_px))
        if self._daq_nshot > 1:
            self.daq_pb.setValue(f * 100)

    @pyqtSlot()
    def on_single_viz_update(self):
        # single viz update.
        if self._elems_list == [] :
            QMessageBox.warning(self, "DAQ Warning",
                    "Cannot find loaded devices.", QMessageBox.Ok)
            return

        self._delt = 1.0 / self._daqfreq
        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(self._daq_nshot))
        self.daq_th.started.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.finished.connect(partial(self.set_widgets_status, "STOP"))
        self.daq_th.start()

    @pyqtSlot()
    def on_save_data(self):
        # save current vized data into file.
        if self._data_save_dlg is None:
            self._data_save_dlg = SaveDataDialog(self)
        self.segments_updated.connect(self._data_save_dlg.on_segments_updated)
        self._data_save_dlg.show()

    def get_mp(self):
        # get MachinePortal instance
        return self.__mp

    @pyqtSlot(bool)
    def toggle_dnum(self, f):
        if f:
            xtklbls = [i.name[-5:] for i in self._elems_list]
            if self._xdata_gauge == 'pos':
                xtks = [i.sb for i in self._elems_list]
            else:
                xtks = list(range(len(xtklbls)))
        else:
            pass

    @pyqtSlot(bool)
    def on_show_dnum(self, f):
        if not f:
            return
        self.xtklbls_changed.emit(self._xtklbls_dnum)
        self.xtks_changed.emit(self._xtks)

    @pyqtSlot(bool)
    def on_show_dname(self, f):
        if not f:
            return
        self.xtklbls_changed.emit(self._xtklbls_dname)
        self.xtks_changed.emit(self._xtks)

    def reset_xtklbls(self):
        [o.toggled.emit(o.isChecked()) for o in
                (self.show_dnum_rbtn, self.show_dname_rbtn)]
