# encoding: UTF-8

"""Library for running an EPICS-based virtual accelertor using IMPACT particle tracker."""

import cothread
import logging
import math
import numpy
import os.path
import random
import re
import shutil
import subprocess
import tempfile
import threading
import time
from collections import OrderedDict
from copy import deepcopy

from cothread import catools
from phantasy.library.lattice.impact import LatticeFactory, OUTPUT_MODE_DIAG
from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SeqElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import ValveElement
from phantasy.library.parser import Configuration

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

# configuration options

CONFIG_MACHINE = "machine"
CONFIG_IMPACT_EXE_FILE = "impact_exe_file"
CONFIG_IMPACT_DATA_DIR = "impact_data_dir"

# default values

_DEFAULT_IMPACT_EXE = "impact"
_TEMP_DIRECTORY_SUFFIX = "_va_impact"
_DEFAULT_ERROR_VALUE = 0.0
_VA_STATUS_GOOD = "OK"
_VA_STATUS_BAD = "ERR"

# global logger instance

_LOGGER = logging.getLogger(__name__)

# global virtual accelerator

_VIRTUAL_ACCELERATOR = None


def start(layout, **kwargs):
    """Start the global virtual accelerator.

    Parameters
    ----------
    layout :
        Accelerator layout object.

    Keyword Arguments
    -----------------
    settings :
        Dictionary of machine settings.
    channels :
        List of channel tuples with (name, properties, tags).
    start :
        Name of accelerator element to start simulation.
    end :
        Name of accelerator element to end simulation.
    data_dir :
        Path of directory containing IMPACT data files.
    work_dir :
        Path of directory for execution of IMPACT.
    """

    global _VIRTUAL_ACCELERATOR
    if _VIRTUAL_ACCELERATOR is None:
        _VIRTUAL_ACCELERATOR = build_virtaccel(layout, **kwargs)

    if _VIRTUAL_ACCELERATOR.is_started():
        raise RuntimeError("Virtual Accelerator already started")

    _VIRTUAL_ACCELERATOR.start()


def stop():
    """Stop the global virtual accelerator.
    """
    global _VIRTUAL_ACCELERATOR
    if _VIRTUAL_ACCELERATOR is None or not _VIRTUAL_ACCELERATOR.is_started():
        raise RuntimeError("Virtual Accelerator not started")

    _VIRTUAL_ACCELERATOR.stop()


def build_virtaccel(layout, **kwargs):
    """Convenience method to build a virtual accelerator.

    Parameters
    ----------
    layout :
        Accelerator layout object

    Keyword Arguments
    -----------------
    settings :
        Dictionary of machine settings
    channels :
        List of channel tuples with (name, properties, tags)
    start :
        Name of accelerator element to start simulation
    end :
        Name of accelerator element to end simulation
    data_dir :
        Path of directory containing IMPACT data files
    work_dir :
        Path of directory for execution of IMPACT

    Returns
    -------
    ret :
        VirtualAccelerator instance
    """
    va_factory = VirtualAcceleratorFactory(layout, **kwargs)

    return va_factory.build()


class VirtualAcceleratorFactory(object):
    """Prepare a VirtualAccelerator for execution.

       The main purpose of this class is to process the accelerator
       description and configure the VirtualAccelerator for proper
       exection.
    """

    def __init__(self, layout, **kwargs):
        self.layout = layout
        self.config = kwargs.get("config", None)
        self.settings = kwargs.get("settings", None)
        self.channels = kwargs.get("channels", None)
        self.start = kwargs.get("start", None)
        self.end = kwargs.get("end", None)
        self.data_dir = kwargs.get("data_dir", None)
        self.work_dir = kwargs.get("work_dir", None)

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        if not isinstance(layout, SeqElement):
            raise TypeError("VirtAccelFactory: 'layout' property much be type SeqElement")
        self._layout = layout

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if (start is not None) and not isinstance(start, str):
            raise TypeError("VirtAccelFactory: 'start' property much be type string or None")
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end is not None) and not isinstance(end, str):
            raise TypeError("VirtAccelFactory: 'end' property much be type string or None")
        self._end = end

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not isinstance(config, Configuration):
            raise TypeError("LatticeFactory: 'config' property must be type Configuration")
        self._config = config

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if not isinstance(settings, dict):
            raise TypeError("VirtAccelFactory: 'settings' property much be type dict")
        self._settings = settings

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, channels):
        if not isinstance(channels, list):
            raise TypeError("VirtAccelFactory: 'channels' property much be type list")
        self._channels = channels

    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, machine):
        if (machine is not None) and not isinstance(machine, str):
            raise TypeError("VirtAccelFactory: 'machine' property much be type string or None")
        self._machine = machine

    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if (data_dir is not None) and not isinstance(data_dir, str):
            raise TypeError("VirtAccelFactory: 'data_dir' property much be type string or None")
        self._data_dir = data_dir

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir is not None) and not isinstance(work_dir, str):
            raise TypeError("VirtAccelFactory: 'work_dir' property much be type string or None")
        self._work_dir = work_dir

    def _get_config_impact_exe(self):
        if self.config.has_default(CONFIG_IMPACT_EXE_FILE):
            return self.config.getabspath_default(CONFIG_IMPACT_EXE_FILE, cmd=True)

        return _DEFAULT_IMPACT_EXE

    def _findChannel(self, name, field, handle):
        for channel, props, _ in self.channels:
            if props["elemName"] != name:
                continue
            if props["elemField"] != field:
                continue
            if props["elemHandle"] != handle:
                continue
            # IMPORTANT: Channel names originating from channel finder
            # may be of type 'unicode' instead of 'str'. The cothread
            # library does not have proper support for unicode strings.
            return str(channel)

        raise RuntimeError("VirtAccelFactory: channel not found: '{}', '{}', '{}'".format(name, field, handle))

    def build(self):
        """Process the accelerator description and configure the Virtual Accelerator.
        """
        settings = self.settings

        data_dir = self.data_dir
        if (data_dir is None) and self.config.has_default(CONFIG_IMPACT_DATA_DIR):
            data_dir = self.config.getabspath_default(CONFIG_IMPACT_DATA_DIR)

        if data_dir is None:
            raise RuntimeError("VirtAccelFactory: No data directory provided, check the configuration")

        work_dir = self.work_dir

        impact_exe = self._get_config_impact_exe()

        latfactory = LatticeFactory(self.layout, config=self.config, settings=self.settings)
        latfactory.outputMode = OUTPUT_MODE_DIAG
        latfactory.start = self.start
        latfactory.end = self.end

        m = re.match("(.*:)?(.*):(.*):(.*)", self.channels[0][0])
        if not m:
            raise RuntimeError("VirtAccelFactory: Error determining channel prefix, check channel names")

        if m.group(1) is None:
            chanprefix = None
        else:
            # IMPORTANT: chanprefix must
            # be converted from unicode
            chanprefix = str(m.group(1))

        va = VirtualAccelerator(latfactory, settings, chanprefix, impact_exe, data_dir, work_dir)

        for elem in self.layout.iter(start=self.start, end=self.end):

            if isinstance(elem, CavityElement):
                # Need to normalize cavity phase settings to 0~360
                settings[elem.name][elem.fields.phase] = _normalize_phase(settings[elem.name][elem.fields.phase])
                va.append_rw(self._findChannel(elem.name, elem.fields.phase, "setpoint"),
                             self._findChannel(elem.name, elem.fields.phase, "readset"),
                             self._findChannel(elem.name, elem.fields.phase, "readback"),
                             (elem.name, elem.fields.phase), desc="Cavity Phase", egu="degree", drvh=360, drvl=0)
                va.append_rw(self._findChannel(elem.name, elem.fields.amplitude, "setpoint"),
                             self._findChannel(elem.name, elem.fields.amplitude, "readset"),
                             self._findChannel(elem.name, elem.fields.amplitude, "readback"),
                             (elem.name, elem.fields.amplitude), desc="Cavity Amplitude", egu="%")
                va.append_elem(elem)

            elif isinstance(elem, SolCorElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field), desc="Solenoid Field", egu="T")  # , drvratio=0.10)
                va.append_rw(self._findChannel(elem.h.name, elem.h.fields.angle, "setpoint"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readset"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readback"),
                             (elem.h.name, elem.h.fields.angle), desc="Horizontal Corrector",
                             egu="radian")  # , drvabs=0.001)
                va.append_rw(self._findChannel(elem.v.name, elem.v.fields.angle, "setpoint"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readset"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readback"),
                             (elem.v.name, elem.v.fields.angle), desc="Vertical Corrector",
                             egu="radian")  # , drvabs=0.001)
                va.append_elem(elem)

            elif isinstance(elem, CorElement):
                va.append_rw(self._findChannel(elem.h.name, elem.h.fields.angle, "setpoint"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readset"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readback"),
                             (elem.h.name, elem.h.fields.angle), desc="Horizontal Corrector",
                             egu="radian")  # , drvabs=0.001)
                va.append_rw(self._findChannel(elem.v.name, elem.v.fields.angle, "setpoint"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readset"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readback"),
                             (elem.v.name, elem.v.fields.angle), desc="Vertical Corrector",
                             egu="radian")  # , drvabs=0.001)
                va.append_elem(elem)

            elif isinstance(elem, BendElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field), desc="Bend Relative Field", egu="none")  # , drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, QuadElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.gradient, "setpoint"),
                             self._findChannel(elem.name, elem.fields.gradient, "readset"),
                             self._findChannel(elem.name, elem.fields.gradient, "readback"),
                             (elem.name, elem.fields.gradient), desc="Quadrupole Gradient",
                             egu="T/m")  # , drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, SextElement):
                _LOGGER.warning("VirtAccelFactory: Hexapole magnet element support not implemented. Ignoring channels.")
                # va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                #             self._findChannel(elem.name, elem.fields.field, "readset"),
                #             self._findChannel(elem.name, elem.fields.field, "readback"),
                #             (elem.name, elem.fields.field), desc="Hexapole Field", egu="T/m^2", drvrel=0.05)
                # va.append_elem(elem)

            elif isinstance(elem, BPMElement):
                va.append_ro(self._findChannel(elem.name, elem.fields.x, "readback"),
                             (elem.name, elem.fields.x), desc="Horizontal Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.y, "readback"),
                             (elem.name, elem.fields.y), desc="Vertical Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.phase, "readback"),
                             (elem.name, elem.fields.phase), desc="Beam Phase", egu="degree")
                va.append_ro(self._findChannel(elem.name, elem.fields.energy, "readback"),
                             (elem.name, elem.fields.energy), desc="Beam Energy", egu="MeV")
                va.append_elem(elem)

            elif isinstance(elem, PMElement):
                va.append_ro(self._findChannel(elem.name, elem.fields.x, "readback"),
                             (elem.name, elem.fields.x), desc="Horizontal Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.y, "readback"),
                             (elem.name, elem.fields.y), desc="Vertical Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.xrms, "readback"),
                             (elem.name, elem.fields.xrms), desc="Horizontal Size", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.yrms, "readback"),
                             (elem.name, elem.fields.yrms), desc="Vertical Size", egu="m")
                va.append_elem(elem)

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                # ignore these diagnostic elements for now
                pass

            elif isinstance(elem, (ValveElement, PortElement, StripElement)):
                # ignore these elements with no relevant channels
                pass

            elif isinstance(elem, DriftElement):
                # drift elements have no channels
                pass

            else:
                raise RuntimeError("Unsupported element type: {}".format(type(elem).__name__))

        return va


class VirtualAccelerator(object):
    """VirtualAccelerator executes and manages the
       EPICS IOC process and IMPACT simulation process.
    """

    def __init__(self, latfactory, settings, chanprefix, impact_exe, data_dir, work_dir=None):
        if not isinstance(latfactory, LatticeFactory):
            raise TypeError("VirtualAccelerator: Invalid type for LatticeFactory")
        self._latfactory = latfactory

        if not isinstance(settings, dict):
            raise TypeError("VirtualAccelerator: Invalid type for accelerator Settings")
        self._settings = settings

        self._chanprefix = chanprefix
        self.impact_exe = impact_exe
        self.data_dir = data_dir
        self.work_dir = work_dir

        self._epicsdb = []
        self._csetmap = OrderedDict()
        self._elemmap = OrderedDict()
        self._fieldmap = OrderedDict()
        self._readfieldmap = OrderedDict()

        self._noise = 0.001

        self._started = False
        self._continue = False
        self._rm_work_dir = False

        self._ioc_process = None
        self._ioc_logfile = None

        self._subscriptions = None
        self._lock = cothread.Event(False)

    @property
    def impact_exe(self):
        return self._impact_exe

    @impact_exe.setter
    def impact_exe(self, impact_exe):
        if not isinstance(impact_exe, str):
            raise TypeError("VirtualAccelerator: 'impact_exe' property much be type string")
        self._impact_exe = impact_exe

    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if not isinstance(data_dir, str):
            raise TypeError("VirtualAccelerator: 'data_dir' property much be type string")
        self._data_dir = data_dir

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir is not None) and not isinstance(work_dir, str):
            raise TypeError("VirtualAccelerator: 'work_dir' property much be type string or None")
        self._work_dir = work_dir

    def append_rw(self, cset, rset, read, field, desc="Element", egu="", prec=5, drvh=None, drvl=None, drvabs=None,
                  drvrel=None, drvratio=None):
        """Append a set of read/write channels to this virtual accelerator.
        The algorithm to set EPICS DRVH/DRVK is as:
            - if absolute limit (drvabs) is given, use absolute
            - or if relative limit (drvres) is given, use relative
            - or if a ratio (drvratio) is given, use ratio
            - otherwise, no limit.
        
        :param cset:        pv name of set point
        :param rset:        pv name of read back for set point
        :param read:        pv name of read back
        :param field:       tuple with element name and field
        :param desc:        element description
        :param egu:         EPICS record engineering unit
        :param prec:        EPICS display precision
        :param drvabs:      absolute driven limit with +-abs(drvabs)
        :param drvrel:      relative driven limit, value +- abs(drvabs)
        :param drvratio:    driven ratio of setting point value * (1 +- ratio) 
        """
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append RW channel when started")

        val = self._settings[field[0]][field[1]]
        if drvabs is not None:
            drvh = abs(drvabs)
            drvl = - abs(drvabs)
        elif drvrel is not None:
            drvh = val + abs(drvabs)
            drvl = val - abs(drvabs)
        elif drvratio is not None:
            drvh = val + abs(val * drvratio)
            drvl = val - abs(val * drvratio)

        self._epicsdb.append(("ao", cset, OrderedDict([
            ("DESC", "{} Set Point".format(desc)),
            ("VAL", val),
            ("DRVH", drvh),
            ("DRVL", drvl),
            ("PREC", prec),
            ("EGU", egu)
        ])))

        self._epicsdb.append(("ai", rset, OrderedDict([
            ("DESC", "{} Set Point Read Back".format(desc)),
            ("VAL", val),
            ("PREC", prec),
            ("EGU", egu)
        ])))

        self._epicsdb.append(("ai", read, OrderedDict([
            ("DESC", "{} Read Back"),
            ("VAL", val),
            ("PREC", prec),
            ("EGU", egu)
        ])))

        self._csetmap[cset] = (rset, read)
        self._fieldmap[cset] = field

    def append_ro(self, read, field, desc="Element", egu="", prec=5):
        """Append a read-only channel to this virtual accelerator.

           :param read:        pv name of read back
           :param field:       tuple with element name and field
           :param desc:        element description
           :param egu:         EPICS record engineering unit
           :param prec:        EPICS display precision
        """
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append RO channel when started")

        self._epicsdb.append(("ai", read, OrderedDict([
            ("DESC", "{} Read Back".format(desc)),
            ("VAL", "0.0"),
            ("PREC", prec),
            ("EGU", egu)
        ])))

        if field[0] not in self._readfieldmap:
            self._readfieldmap[field[0]] = OrderedDict()
        self._readfieldmap[field[0]][field[1]] = read

    def append_elem(self, elem):
        """Append an accelerator element to this virtual accelerator.
        """
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append element when started")
        self._elemmap[elem.name] = elem

    def is_started(self):
        """Check is virtual accelerator has been started."""
        return self._started

    def start(self, raise_on_wait=False):
        """Start the virtual accelerator. Spawn a new cothread to handle execution.
        """
        _LOGGER.debug("VirtualAccelerator: Start")
        cothread.Spawn(self._starter, raise_on_wait, raise_on_wait=True).Wait()

    def _starter(self, raise_on_wait):
        _LOGGER.debug("VirtualAccelerator: Start (cothread)")
        if self._started:
            raise RuntimeError("VirtualAccelerator: Already started")

        if not os.path.isdir(self.data_dir):
            raise RuntimeError("VirtualAccelerator: Data directory not found: {}".format(self.data_dir))

        if self.work_dir is not None and os.path.exists(self.work_dir):
            raise RuntimeError("VirtualAccelerator: Working directory already exists: {}".format(self.work_dir))

        self._started = True
        self._continue = True
        self._executer = cothread.Spawn(self._executer, raise_on_wait=raise_on_wait)

    def stop(self):
        """Stop the virtual accelerator.
           Spawn a new cothread to stop gracefully.
        """
        _LOGGER.debug("VirtualAccelerator: Stop")
        cothread.Spawn(self._stopper, raise_on_wait=True).Wait()

    def _stopper(self):
        _LOGGER.debug("VirtualAccelerator: Stop (cothread)")
        if self._started:
            _LOGGER.debug("VirtualAccelerator: Initiate shutdown")
            self._continue = False
            # self._executer.Wait()

    def wait(self, timeout=None):
        """Wait for the virtual accelerator to stop
        """
        if self._started:
            self._executer.Wait(timeout)

    def _executer(self):
        """Executer method wraps the call to _execute and ensure that
           the proper clean up of connections and processes.
        """
        _LOGGER.debug("VirtualAccelerator: Execute (cothread)")
        try:
            self._execute()
        finally:
            _LOGGER.info("VirtualAccelerator: Cleanup")
            if self._subscriptions is not None:
                _LOGGER.debug("VirtualAccelerator: Cleanup: close connections")
                for sub in self._subscriptions:
                    sub.close()
                self._subscriptions = None

            if self._ioc_process is not None:
                _LOGGER.debug("VirtualAccelerator: Cleanup: terminate IOC process")
                self._ioc_process.terminate()
                self._ioc_process.wait()
                self._ioc_process = None

            if self._ioc_logfile is not None:
                _LOGGER.debug("VirtualAccelerator: Cleanup: close IOC log file")
                self._ioc_logfile.close()
                self._ioc_logfile = None

            if self._rm_work_dir:
                _LOGGER.debug("VirtualAccelerator: Cleanup: remove work directory")
                shutil.rmtree(self.work_dir)

            self._executer = None
            self._continue = False
            self._started = False

    def _execute(self):
        """Execute the virtual accelerator. This includes the following:
            1. Creating a temporary working directory for execution of IMPACT.
            2. Setup the working directory by symlinking from the data directory.
            3. Writing the EPICS DB to the working directory (va.db).
            4. Starting the softIoc and channel initializing monitors.
            5. Add noise to the settings for all input (CSET) channels.
            6. Generate the IMPACT lattice file in working directory (test.in).
            7. Execute IMPACT simulation and read the output files (fort.??).
            8. Update the READ channels of all devives.
            9. Update the REST channels of input devies.
            10. Repeat from step #5.
        """
        _LOGGER.debug("VirtualAccelerator: Execute virtual accelerator")

        if self._chanprefix is None:
            chanprefix = ""
        else:
            chanprefix = self._chanprefix

        # Add channel for sample counting
        sample_cnt = chanprefix + "SVR:CNT"

        self._epicsdb.append(("ai", sample_cnt, OrderedDict([
            ("DESC", "Sample counter for scan client"),
            ("VAL", 0)
        ])))

        # Add channel for VA configuration and control
        channoise = chanprefix + "SVR:NOISE"

        self._epicsdb.append(("ao", channoise, OrderedDict([
            ("DESC", "Noise level of Virtual Accelerator"),
            ("VAL", 0.001),
            ("PREC", 5)
        ])))

        chanstat = chanprefix + "SVR:STATUS"

        self._epicsdb.append(("bi", chanstat, OrderedDict([
            ("DESC", "Status of Virtual Accelerator"),
            ("VAL", 1),
            ("ZNAM", "ERR"),
            ("ONAM", "OK"),
            ("PINI", "1")
        ])))

        chancharge = chanprefix + "SVR:CHARGE"

        self._epicsdb.append(("ai", chancharge, OrderedDict([
            ("DESC", "Q/M of Virtual Accelerator"),
            ("VAL", 0.0),
            ("PREC", 5)
        ])))

        if self.work_dir is not None:
            os.makedirs(self.work_dir)
            self._rm_work_dir = False
        else:
            self.work_dir = tempfile.mkdtemp(_TEMP_DIRECTORY_SUFFIX)
            self._rm_work_dir = True

        _LOGGER.info("VirtualAccelerator: Working directory: %s", self._work_dir)

        # input file paths
        epicsdbpath = os.path.join(self.work_dir, "va.db")
        latticepath = os.path.join(self.work_dir, "test.in")
        modelmappath = os.path.join(self.work_dir, "model.map")

        # output file paths
        fort18path = os.path.join(self.work_dir, "fort.18")
        fort24path = os.path.join(self.work_dir, "fort.24")
        fort25path = os.path.join(self.work_dir, "fort.25")
        epicslogpath = os.path.join(self.work_dir, "softioc.log")

        if os.path.isabs(self.data_dir):
            abs_data_dir = self.data_dir
        else:
            abs_data_dir = os.path.abspath(self.data_dir)

        for datafile in os.listdir(abs_data_dir):
            srcpath = os.path.join(abs_data_dir, datafile)
            destpath = os.path.join(self.work_dir, datafile)
            if os.path.isfile(os.path.join(abs_data_dir, datafile)):
                os.symlink(srcpath, destpath)
                _LOGGER.debug("VirtualAccelerator: Link data file %s to %s", srcpath, destpath)

        with open(epicsdbpath, "w") as outfile:
            self._write_epicsdb(outfile)

        self._ioc_logfile = open(epicslogpath, "w")
        self._ioc_process = _Cothread_Popen(["softIoc", "-d", "va.db"], cwd=self.work_dir,
                                            stdout=self._ioc_logfile, stderr=subprocess.STDOUT)

        self._subscriptions = []

        self._subscriptions.append(catools.camonitor(channoise, self._handle_noise_monitor))

        self._subscriptions.extend(catools.camonitor(self._csetmap.keys(), self._handle_cset_monitor))

        while self._continue:
            # update the RSET channels with new settings
            for cset in self._csetmap.items():
                name, field = self._fieldmap[cset[0]]
                catools.caput(cset[1][0], self._settings[name][field])

            settings = self._copy_settings_with_noise()
            self._latfactory.settings = settings
            lattice = self._latfactory.build()

            catools.caput(chancharge, lattice.initialCharge)

            with open(latticepath, "w") as outfile:
                with open(modelmappath, "w") as mapfile:
                    lattice.write(outfile, mapstream=mapfile)

            start = time.time()

            if os.path.isfile(fort18path):
                os.remove(fort18path)

            if os.path.isfile(fort24path):
                os.remove(fort24path)

            if os.path.isfile(fort25path):
                os.remove(fort25path)

            impact_process = _Cothread_Popen(["mpirun", "-np", str(lattice.nprocessors),
                                              str(self.impact_exe)], cwd=self.work_dir,
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            (stdout, _, status) = impact_process.communicate()

            # The virtual accelerator shutdown is likely to occur while IMPACT is executing,
            # so check if virtual accelerator has been stopped before proceeding.
            if not self._continue:
                break

            _LOGGER.info("VirtualAccelerator: IMPACT execution time: %f s", time.time() - start)

            if status == 0:
                catools.caput(chanstat, _VA_STATUS_GOOD)
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT exited with non-zero status code: %s\r\n%s", status, stdout)
                catools.caput(chanstat, _VA_STATUS_BAD)

            if os.path.isfile(fort18path):
                fort18 = numpy.loadtxt(fort18path, usecols=(0, 1, 3))
                fort18length = fort18.shape[0]
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT output not found: %s", fort18path)
                catools.caput(chanstat, _VA_STATUS_BAD)
                fort18length = 0

            if os.path.isfile(fort24path):
                fort24 = numpy.loadtxt(fort24path, usecols=(1, 2))
                fort24length = fort24.shape[0]
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT output not found: %s", fort24path)
                catools.caput(chanstat, _VA_STATUS_BAD)
                fort24length = 0

            if os.path.isfile(fort25path):
                fort25 = numpy.loadtxt(fort25path, usecols=(1, 2))
                fort25length = fort25.shape[0]
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT output not found: %s", fort25path)
                catools.caput(chanstat, _VA_STATUS_BAD)
                fort25length = 0

            output_map = []
            for elem in lattice.elements:
                if elem.itype in [-28]:
                    output_map.append(elem.name)

            output_length = len(output_map)

            if fort18length < output_length:
                _LOGGER.warning("VirtualAccelerator: IMPACT fort.18 length %s, expecting %s",
                                fort18length, output_length)
                catools.caput(chanstat, _VA_STATUS_BAD)

            if fort24length < output_length:
                _LOGGER.warning("VirtualAccelerator: IMPACT fort.24 length %s, expecting %s",
                                fort24length, output_length)
                catools.caput(chanstat, _VA_STATUS_BAD)

            if fort25length < output_length:
                _LOGGER.warning("VirtualAccelerator: IMPACT fort.25 length %s, expecting %s",
                                fort25length, output_length)
                catools.caput(chanstat, _VA_STATUS_BAD)

            def get_phase(idx):
                # IMPACT computes the phase in radians,
                # need to convert to degrees for PV.
                return _normalize_phase(2.0 * fort18[idx, 1] * (180.0 / math.pi))

            for idx in range(min(fort18length, fort24length, fort25length)):

                elem = self._elemmap[output_map[idx]]

                if isinstance(elem, BPMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.x], fort24[idx, 0])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.x], fort24[idx, 0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.y], fort25[idx, 0])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.y], fort25[idx, 0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.phase], get_phase(idx))
                    catools.caput(self._readfieldmap[elem.name][elem.fields.phase], get_phase(idx))
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.energy], fort18[idx, 2])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.energy], fort18[idx, 2])
                elif isinstance(elem, PMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.x], fort24[idx, 0])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.x], fort24[idx, 0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.y], fort25[idx, 0])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.y], fort25[idx, 0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.xrms], fort24[idx, 1])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.xrms], fort24[idx, 1])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.yrms], fort25[idx, 1])
                    catools.caput(self._readfieldmap[elem.name][elem.fields.yrms], fort25[idx, 1])
                else:
                    _LOGGER.warning("VirtualAccelerator: Output from element type not supported: %s",
                                    type(elem).__name__)

            # Write the default error value to the remaing output PVs.
            for idx in range(min(fort18length, fort24length, fort25length), output_length):

                elem = self._elemmap[output_map[idx]]

                if isinstance(elem, BPMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.x], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.x], _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.y], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.y], _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.phase], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.phase], _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.energy], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.energy], _DEFAULT_ERROR_VALUE)
                elif isinstance(elem, PMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.x], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.x], _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.y], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.y], _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.xrms], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.xrms], _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                  self._readfieldmap[elem.name][elem.fields.yrms], _DEFAULT_ERROR_VALUE)
                    catools.caput(self._readfieldmap[elem.name][elem.fields.yrms], _DEFAULT_ERROR_VALUE)
                else:
                    _LOGGER.warning("VirtualAccelerator: Output from element type not supported: %s",
                                    type(elem).__name__)

            # Allow the BPM, PM, etc. readbacks to update
            # before the device setting readbacks PVs.
            cothread.Yield()

            for name, value in self._csetmap.items():
                name, field = self._fieldmap[name]
                _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", value[1], settings[name][field])
                catools.caput(value[1], settings[name][field])

            # Sleep for a fraction (10%) of the total execution time 
            # when one simulation costs more than 0.50 seconds.
            # Otherwise, sleep for the rest of 1 second. 
            # If a scan is being done on this virtual accelerator,
            # then the scan server has a period of time to update
            # setpoints before the next run of IMPACT.
            if (time.time() - start) > 0.50:
                cothread.Sleep((time.time() - start) * 0.1)
            else:
                cothread.Sleep(1.0 - (time.time() - start))

    def _handle_cset_monitor(self, value, idx):
        """Handle updates of CSET channels by updating
           the corresponding setting and RSET channel.
        """
        cset = self._csetmap.items()[idx]
        _LOGGER.debug("VirtualAccelerator: Update cset: '%s' to %s", cset[0], value)
        name, field = self._fieldmap[cset[0]]
        self._settings[name][field] = float(value)

    def _handle_noise_monitor(self, value):
        """Handle updates of the NOISE channel.
        """
        _LOGGER.debug("VirtualAccelerator: Update noise: %s", value)
        self._noise = float(value)

    def _copy_settings_with_noise(self):
        s = deepcopy(self._settings)
        for name, field in self._fieldmap.values():
            s[name][field] = s[name][field] + s[name][field] * self._noise * 2.0 * (random.random() - 0.5)
        return s

    def _write_epicsdb(self, buf):
        for record in self._epicsdb:
            buf.write("record({}, \"{}\") {{\r\n".format(record[0], record[1]))
            for name, value in record[2].items():
                if value is None:
                    pass  # ignore fields with value None
                elif isinstance(value, int):
                    buf.write("    field(\"{}\", {})\r\n".format(name, value))
                elif isinstance(value, float):
                    buf.write("    field(\"{}\", {})\r\n".format(name, value))
                else:
                    buf.write("    field(\"{}\", \"{}\")\r\n".format(name, value))
            buf.write("}\r\n\r\n")


def _normalize_phase(phase):
    while phase >= 360.0:
        phase -= 360.0
    while phase < 0.0:
        phase += 360.0
    return phase


class _Cothread_Popen(object):
    """A helpful wrapper class that integrates the python
       standard popen() method with the Cothread library.
    """

    def __init__(self, *args, **kwargs):
        self._process = subprocess.Popen(*args, **kwargs)
        self._output = None
        self._event = None

    def communicate(self, input=None):  # @ReservedAssignment
        """Start a real OS thread to wait for process communication.
        """
        if self._event is None:
            self._event = cothread.Event()
            threading.Thread(target=self._communicate_thread, args=(input,)).start()
        elif input is not None:
            raise RuntimeError("_Cothread_Popen: Communicate method already called")

        self._event.Wait()
        return (self._output[0], self._output[1], self._process.poll())

    def _communicate_thread(self, input):  # @ReservedAssignment
        """Executes in separate OS thread. Wait for communication
           then return the output to the cothread context.
        """
        output = self._process.communicate(input)
        cothread.Callback(self._communicate_callback, output)

    def _communicate_callback(self, output):
        """Record the output and then signal other cothreads.
        """
        self._output = output
        self._event.Signal()

    def wait(self):
        """Wait for the process to complete and result the exit code.
        """
        self.communicate()
        return self._process.poll()

    def terminate(self):
        """Send the terminate signal. See subprocess.Popen.terminate()
        """
        self._process.terminate()

    def kill(self):
        """Send the kill signal.  See subprocess.Popen.kill()
        """
        self._process.kill()
