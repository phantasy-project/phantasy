# encoding: UTF-8

"""Library for running an EPICS-based virtual accelertor using FLAME evelope tracker."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import math
import os.path
import random
import re
import shutil
import subprocess
import tempfile
import time
from collections import OrderedDict
from copy import deepcopy

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import cothread
from flame import Machine

from phantasy.library.pv import Popen
from phantasy.library.pv import catools
from phantasy.library.parser import Configuration
from phantasy.library.layout import SeqElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import EBendElement
from phantasy.library.layout import EMSElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import VDElement
from phantasy.library.layout import FCElement
from phantasy.library.layout import ElectrodeElement
from phantasy.library.layout import SlitElement
from phantasy.library.layout import ChopperElement
from phantasy.library.layout import AttenuatorElement
from phantasy.library.layout import DumpElement
from phantasy.library.layout import ApertureElement
from phantasy.library.lattice import FlameLatticeFactory


try:
    basestring  # Python 2.X
except NameError:
    basestring = str  # Python 3.X


# configuration options

CONFIG_MACHINE = "machine"
CONFIG_FLAME_DATA_DIR = "flame_data_dir"

# drift mask: bool
CONFIG_DRIFT_MASK = "drift_mask"

# default values

_TEMP_DIRECTORY_SUFFIX = "_va_flame"

# _DEFAULT_ERROR_VALUE = 0.0

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
        Path of directory containing FLAME data files.
    work_dir :
        Path of directory for execution of FLAME.
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
        Path of directory containing FLAME data files.
    work_dir :
        Path of directory for execution of FLAME.

    Returns
    -------
    ret :
        VirtualAccelerator instance.
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
        if (start is not None) and not isinstance(start, basestring):
            raise TypeError("VirtAccelFactory: 'start' property much be type string or None")
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end is not None) and not isinstance(end, basestring):
            raise TypeError("VirtAccelFactory: 'end' property much be type string or None")
        self._end = end

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not isinstance(config, Configuration):
            raise TypeError("VirtAccelFactory: 'config' property must be type Configuration")
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
        if (machine is not None) and not isinstance(machine, basestring):
            raise TypeError("VirtAccelFactory: 'machine' property much be type string or None")
        self._machine = machine

    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if (data_dir is not None) and not isinstance(data_dir, basestring):
            raise TypeError("VirtAccelFactory: 'data_dir' property much be type string or None")
        self._data_dir = data_dir

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir is not None) and not isinstance(work_dir, basestring):
            raise TypeError("VirtAccelFactory: 'work_dir' property much be type string or None")
        self._work_dir = work_dir

    def _findChannel(self, name, field, handle):
        for channel, props, _ in self.channels:
            if props["elemName"] != name:
                continue
            if props["elemField_eng"] != field:
                continue
            if props["elemHandle"] != handle:
                continue
            # IMPORTANT: Channel names originating from channel finder
            # may be of type 'unicode' instead of 'str'. The cothread
            # library does not have proper support for unicode strings.
            return str(channel)

        raise RuntimeError("VirtAccelFactory: channel not found: '{}', '{}', '{}'".format(name, field, handle))

    def _get_config(self, section, option, defvalue):
        if self.config.has_option(section, option):
            value = self.config.get(section, option)
            _LOGGER.debug("VirtAccelFactory: [{}] '{}' found in configuration: {}".format(section, option, value))
            return value
        return defvalue

    def build(self):
        """Process the accelerator description and configure the Virtual Accelerator.
        """
        settings = self.settings

        data_dir = self.data_dir
        if (data_dir is None) and self.config.has_default(CONFIG_FLAME_DATA_DIR):
            data_dir = self.config.getabspath_default(CONFIG_FLAME_DATA_DIR)

        if data_dir is None:
            raise RuntimeError("VirtAccelFactory: No data directory provided, check the configuration")

        work_dir = self.work_dir

        latfactory = FlameLatticeFactory(self.layout, config=self.config, settings=self.settings)
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

        va = VirtualAccelerator(latfactory, settings, chanprefix, data_dir, work_dir)

        for elem in self.layout.iter(start=self.start, end=self.end):
            # check drift mask first
            if self._get_config(elem.dtype, CONFIG_DRIFT_MASK, 'False').lower() == 'true':
                elem = DriftElement(elem.z, elem.length, elem.aperture, elem.name)
            #

            if isinstance(elem, CavityElement):
                # Need to normalize cavity phase settings to 0~360
                settings[elem.name][elem.fields.phase_phy] = _normalize_phase(settings[elem.name][elem.fields.phase_phy])
                va.append_rw(self._findChannel(elem.name, elem.fields.phase, "setpoint"),
                             self._findChannel(elem.name, elem.fields.phase, "readset"),
                             self._findChannel(elem.name, elem.fields.phase, "readback"),
                             (elem.name, elem.fields.phase_phy), desc="Cavity Phase", egu="degree", drvh=360, drvl=0)
                va.append_rw(self._findChannel(elem.name, elem.fields.amplitude, "setpoint"),
                             self._findChannel(elem.name, elem.fields.amplitude, "readset"),
                             self._findChannel(elem.name, elem.fields.amplitude, "readback"),
                             (elem.name, elem.fields.amplitude_phy), desc="Cavity Amplitude", egu="%")
                va.append_elem(elem)

            elif isinstance(elem, SolCorElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field_phy), desc="Solenoid Field", egu="T") #, drvratio=0.10)
                va.append_rw(self._findChannel(elem.h.name, elem.h.fields.angle, "setpoint"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readset"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readback"),
                             (elem.h.name, elem.h.fields.angle_phy), desc="Horizontal Corrector", egu="radian") #, drvabs=0.001)
                va.append_rw(self._findChannel(elem.v.name, elem.v.fields.angle, "setpoint"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readset"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readback"),
                             (elem.v.name, elem.v.fields.angle_phy), desc="Vertical Corrector", egu="radian") #, drvabs=0.001)
                va.append_elem(elem)

            elif isinstance(elem, SolElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field_phy), desc="Solenoid Field", egu="T") #, drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, CorElement):
                va.append_rw(self._findChannel(elem.h.name, elem.h.fields.angle, "setpoint"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readset"),
                             self._findChannel(elem.h.name, elem.h.fields.angle, "readback"),
                             (elem.h.name, elem.h.fields.angle_phy), desc="Horizontal Corrector", egu="radian") #, drvabs=0.001)
                va.append_rw(self._findChannel(elem.v.name, elem.v.fields.angle, "setpoint"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readset"),
                             self._findChannel(elem.v.name, elem.v.fields.angle, "readback"),
                             (elem.v.name, elem.v.fields.angle_phy), desc="Vertical Corrector", egu="radian") #, drvabs=0.001)
                va.append_elem(elem)

            elif isinstance(elem, BendElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field_phy), desc="Bend Relative Field", egu="none") #, drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, EBendElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field_phy), desc="EBend Field", egu="V") #, drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, QuadElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.gradient, "setpoint"),
                             self._findChannel(elem.name, elem.fields.gradient, "readset"),
                             self._findChannel(elem.name, elem.fields.gradient, "readback"),
                             (elem.name, elem.fields.gradient_phy), desc="Quadrupole Gradient", egu="T/m") #, drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, EQuadElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.gradient, "setpoint"),
                             self._findChannel(elem.name, elem.fields.gradient, "readset"),
                             self._findChannel(elem.name, elem.fields.gradient, "readback"),
                             (elem.name, elem.fields.gradient_phy), desc="EQuad Field", egu="V")
                va.append_elem(elem)

            elif isinstance(elem, SextElement):
                va.append_rw(self._findChannel(elem.name, elem.fields.field, "setpoint"),
                             self._findChannel(elem.name, elem.fields.field, "readset"),
                             self._findChannel(elem.name, elem.fields.field, "readback"),
                             (elem.name, elem.fields.field_phy), desc="Sextupole Gradient", egu="T/m^2")
                va.append_elem(elem)

            elif isinstance(elem, BPMElement):
                va.append_ro(self._findChannel(elem.name, elem.fields.x, "readback"),
                             (elem.name, elem.fields.x_phy), desc="Horizontal Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.y, "readback"),
                             (elem.name, elem.fields.y_phy), desc="Vertical Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.phase, "readback"),
                             (elem.name, elem.fields.phase_phy), desc="Beam Phase", egu="degree")
                va.append_ro(self._findChannel(elem.name, elem.fields.energy, "readback"),
                             (elem.name, elem.fields.energy_phy), desc="Beam Energy", egu="MeV")
                va.append_elem(elem)

            elif isinstance(elem, PMElement):
                va.append_ro(self._findChannel(elem.name, elem.fields.x, "readback"),
                             (elem.name, elem.fields.x), desc="Horizontal Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.y, "readback"),
                             (elem.name, elem.fields.y), desc="Vertical Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.xy, "readback"),
                             (elem.name, elem.fields.xy), desc="Diagonal Position", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.xrms, "readback"),
                             (elem.name, elem.fields.xrms), desc="Horizontal Size", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.yrms, "readback"),
                             (elem.name, elem.fields.yrms), desc="Vertical Size", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.xyrms, "readback"),
                             (elem.name, elem.fields.xyrms), desc="Diagonal Size", egu="m")
                va.append_ro(self._findChannel(elem.name, elem.fields.cxy, "readback"),
                             (elem.name, elem.fields.cxy), desc="X-Y Correlation", egu="m")
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

            elif isinstance(elem, (AttenuatorElement, ApertureElement,
                                   ChopperElement, DumpElement, SlitElement)):
                # no channels for now
                pass

            elif isinstance(elem, (EMSElement, VDElement, FCElement)):
                pass

            elif isinstance(elem, ElectrodeElement):
                pass

            else:
                raise RuntimeError("Unsupported element type: {}".format(type(elem).__name__))

        return va


class VirtualAccelerator(object):
    """VirtualAccelerator executes and manages the EPICS IOC process and
    FLAME simulation thread.
    """
    def __init__(self, latfactory, settings, chanprefix, data_dir, work_dir=None):
        if not isinstance(latfactory, FlameLatticeFactory):
            raise TypeError("VirtualAccelerator: Invalid type for FlameLatticeFactory")
        self._latfactory = latfactory

        if not isinstance(settings, dict):
            raise TypeError("VirtualAccelerator: Invalid type for accelerator Settings")
        self._settings = settings

        self._chanprefix = chanprefix
        self._data_dir = data_dir
        self._work_dir = work_dir

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
        self._wait_event = cothread.Event(False)

    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if not isinstance(data_dir, basestring):
            raise TypeError("VirtualAccelerator: 'data_dir' property much be type string")
        self._data_dir = data_dir

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir is not None) and not isinstance(work_dir, basestring):
            raise TypeError("VirtualAccelerator: 'work_dir' property much be type string or None")
        self._work_dir = work_dir

    def append_rw(self, cset, rset, read, field, desc="Element", egu="", prec=5, drvh=None, drvl=None, drvabs=None, drvrel=None, drvratio=None):
        """Append a set of read/write channels to this virtual accelerator.
        The algorithm to set EPICS DRVH/DRVL is as:
            - if absolute limit (drvabs) is given, use absolute
            - or if relative limit (drvres) is given, use relative
            - or if a ratio (drvratio) is given, use ratio
            - otherwise, no limit.

        Parameters
        ----------
        cset : str
            PV name of set point, handle is 'setpoint'.
        rset : str
            PV name of read back for set point, handle is 'readset'.
        read : str
            PV name of read back, handle is 'readback'.
        field : tuple
            Tuple with element name and field.
        desc : str
            Element description.
        egu :
            EPICS record engineering unit.
        prec : int
            EPICS display precision.
        drvabs :
            Absolute driven limit with +-abs(drvabs).
        drvrel :
            Relative driven limit, value +- abs(drvabs).
        drvratio :
            Driven ratio of setting point value * (1 +- ratio).
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
            drvh = val + abs(val*drvratio)
            drvl = val - abs(val*drvratio)

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
                ("DESC", "{} Read Back".format(desc)),
                ("VAL", val),
                ("PREC", prec),
                ("EGU", egu)
            ])))

        self._csetmap[cset] = (rset, read)
        self._fieldmap[cset] = field

    def append_ro(self, read, field, desc="Element", egu="", prec=5):
        """Append a read-only channel to this virtual accelerator.

        Parameters
        ----------
        read : str
            PV name of read back, handle is
        field : tuple
            Tuple with element name and field.
        desc : str
            Element description.
        egu :
            EPICS record engineering unit.
        prec : int
            EPICS display precision.
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
        cothread.Spawn(self._co_start, raise_on_wait, raise_on_wait=True).Wait()

    def _co_start(self, raise_on_wait):
        _LOGGER.debug("VirtualAccelerator: Start (cothread)")
        if self._started:
            raise RuntimeError("VirtualAccelerator: Already started")

        if not os.path.isdir(self.data_dir):
            raise RuntimeError("VirtualAccelerator: Data directory not found: {}".format(self.data_dir))

        if self.work_dir is not None and os.path.exists(self.work_dir):
            raise RuntimeError("VirtualAccelerator: Working directory already exists: {}".format(self.work_dir))

        self._started = True
        self._continue = True
        self._wait_event.Reset()
        cothread.Spawn(self._co_execute_with_cleanup, raise_on_wait, raise_on_wait=False)

    def stop(self):
        """Stop the virtual accelerator.
           Spawn a new cothread to stop gracefully.
        """
        _LOGGER.debug("VirtualAccelerator: Stop")
        cothread.Spawn(self._co_stop, raise_on_wait=True).Wait()

    def _co_stop(self):
        _LOGGER.debug("VirtualAccelerator: Stop (cothread)")
        if self._started:
            _LOGGER.debug("VirtualAccelerator: Initiate shutdown")
            self._continue = False
        else:
            raise RuntimeError("VirtualAccelerator: Not started")

    def wait(self, timeout=None):
        _LOGGER.debug("VirtualAccelerator: Wait")
        """Wait for the virtual accelerator to stop
        """
        cothread.Spawn(self._co_wait, timeout, raise_on_wait=True).Wait()

    def _co_wait(self, timeout):
        _LOGGER.debug("VirtualAccelerator: Wait (cothread)")
        if self._started:
            self._wait_event.Wait(timeout)
        else:
            raise RuntimeError("VirtualAccelerator: Not started")

    def _co_execute_with_cleanup(self, raise_on_wait):
        """Executer method wraps the call to _execute and ensure that
           the proper clean up of connections and processes.
        """
        _LOGGER.debug("VirtualAccelerator: Execute (cothread)")
        execute_error = None
        try:
            cothread.Spawn(self._co_execute, raise_on_wait=raise_on_wait).Wait()
        except Exception as e:
            execute_error = e
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
            else:
                _LOGGER.debug("VirtualAccelerator: Cleanup: IOC log file is NONE")

            if self._rm_work_dir:
                _LOGGER.debug("VirtualAccelerator: Cleanup: remove work directory")
                shutil.rmtree(self.work_dir)
            else:
                _LOGGER.debug("VirtualAccelerator: Cleanup: work directory is NONE")

            self._started = False
            self._continue = False

            if execute_error is None:
                self._wait_event.Signal()
            else:
                self._wait_event.SignalException(execute_error)

    def _co_execute(self):
        """Execute the virtual accelerator. This includes the following:

        1. Creating a temporary working directory for execution of FLAME.
        2. Setup the working directory by symlinking from the data directory.
        3. Writing the EPICS DB to the working directory (va.db).
        4. Starting the softIoc and channel initializing monitors.
        5. Add noise to the settings for all input (CSET) channels.
        6. Create or update the FLAME machine configuration.
        7. Propagate the FLAME simulation and read the results.
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
        channoise = chanprefix+"SVR:NOISE"

        self._epicsdb.append(("ao", channoise, OrderedDict([
                ("DESC", "Noise level of Virtual Accelerator"),
                ("VAL", 0.001),
                ("PREC", 5)
            ])))

        chanstat = chanprefix+"SVR:STATUS"

        self._epicsdb.append(("bi", chanstat, OrderedDict([
                ("DESC", "Status of Virtual Accelerator"),
                ("VAL", 1),
                ("ZNAM", "ERR"),
                ("ONAM", "OK"),
                ("PINI", "1")
            ])))

        chancharge = chanprefix+"SVR:CHARGE"

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
        latticepath = os.path.join(self.work_dir, "test.lat")

        #output file paths
        epicslogpath = os.path.join(self.work_dir, "softioc.log")

        if os.path.isabs(self.data_dir):
            abs_data_dir = self.data_dir
            self._latfactory.dataDir = self.data_dir
        else:
            abs_data_dir = os.path.abspath(self.data_dir)
            self._latfactory.dataDir = os.path.abspath(self.data_dir)
        print(self._latfactory.dataDir)

        with open(epicsdbpath, "w") as outfile:
            self._write_epicsdb(outfile)
        _LOGGER.info("VirtualAccelerator: Write EPICS database to %s", epicsdbpath)
        #_LOGGER.debug("VirtualAccelerator: Write EPICS database to %s", epicsdbpath)

        self._ioc_logfile = open(epicslogpath, "w")
        self._ioc_process = Popen(["softIoc", "-d", "va.db"], cwd=self.work_dir,
                                  stdout=self._ioc_logfile, stderr=subprocess.STDOUT)
        _LOGGER.debug("VirtualAccelerator: Start EPICS soft IOC with log %s", epicslogpath)

        _LOGGER.debug("VirtualAccelerator: Connecting to channels: {}".format(len(self._csetmap.keys())))

        self._subscriptions = []

        self._subscriptions.append(catools.camonitor(channoise, self._handle_noise_monitor))

        self._subscriptions.extend(catools.camonitor(self._csetmap.keys(), self._handle_cset_monitor))

        _LOGGER.debug("VirtualAccelerator: Connecting to channels: Done")

        machine = None

        while self._continue:
            # update the RSET channels with new settings
            batch = catools.CABatch()
            for cset in self._csetmap.items():
                name, field = self._fieldmap[cset[0]]
                batch[cset[1][0]] = self._settings[name][field]
            batch.caput()

            settings = self._copy_settings_with_noise()
            self._latfactory.settings = settings
            lattice = self._latfactory.build()

            with open(latticepath, "w") as outfile:
                lattice.write(outfile)

            start = time.time()

            if machine is None:
                _LOGGER.debug("VirtualAccelerator: Create FLAME machine from configuration")
                machine = Machine(lattice.conf())
            else:
                _LOGGER.debug("VirtualAccelerator: Reconfigure FLAME machine from configuration")
                for idx, elem in enumerate(lattice.elements):
                    machine.reconfigure(idx, elem[2])

            _LOGGER.debug("VirtualAccelerator: Allocate FLAME state from configuration")
            S = machine.allocState({})

            output_map = []
            for elem in lattice.elements:
                if 'name' in elem[3]:
                    output_map.append(elem[3]['name'])
                else:
                    output_map.append(None)

            batch = catools.CABatch()
            for i in range(0, len(machine)):
                machine.propagate(S, i, 1)

                if output_map[i] in self._elemmap:
                    elem = self._elemmap[output_map[i]]
                    if isinstance(elem, BPMElement):
                        x_centroid = S.moment0_env[0]/1.0e3 # convert mm to m
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.x_phy], x_centroid)
                        batch[self._readfieldmap[elem.name][elem.fields.x_phy]] = x_centroid
                        y_centroid = S.moment0_env[2]/1.0e3 # convert mm to m
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.y_phy], y_centroid)
                        batch[self._readfieldmap[elem.name][elem.fields.y_phy]] = y_centroid
                         # convert rad to deg and adjust for 161MHz sampling frequency
                        phase = _normalize_phase(2.0 * S.ref_phis * (180.0 / math.pi))
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.phase_phy], phase)
                        batch[self._readfieldmap[elem.name][elem.fields.phase_phy]] = phase
                        energy = S.ref_IonEk/1.0e6 # convert eV to MeV
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.energy_phy], energy)
                        batch[self._readfieldmap[elem.name][elem.fields.energy_phy]] = energy
                    elif isinstance(elem, PMElement):
                        x_centroid = S.moment0_env[0]/1.0e3 # convert mm to m
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.x], x_centroid)
                        batch[self._readfieldmap[elem.name][elem.fields.x]] = x_centroid
                        y_centroid = S.moment0_env[2]/1.0e3 # convert mm to m
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.y], y_centroid)
                        batch[self._readfieldmap[elem.name][elem.fields.y]] = y_centroid
                        x_rms = S.moment0_rms[0]/1.0e3 # convert mm to m
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.xrms], x_rms)
                        batch[self._readfieldmap[elem.name][elem.fields.xrms]] = x_rms
                        y_rms = S.moment0_rms[2]/1.0e3
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.yrms], y_rms)
                        batch[self._readfieldmap[elem.name][elem.fields.yrms]] = y_rms

                        sign = elem.sign
                        xy_centroid = (sign*x_centroid + y_centroid)/math.sqrt(2.0) # convert mm to m
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.xy], xy_centroid)
                        batch[self._readfieldmap[elem.name][elem.fields.xy]] = xy_centroid

                        xy_rms = 1.0e-3*math.sqrt(
                                (S.moment1_env[0, 0] + S.moment1_env[2, 2])*0.5
                                + sign*S.moment1_env[0, 2]
                        )
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.xyrms], xy_rms)
                        batch[self._readfieldmap[elem.name][elem.fields.xyrms]] = xy_rms

                        cxy = sign * S.moment1_env[0, 2] * 1e-6 / x_rms / y_rms
                        _LOGGER.debug("VirtualAccelerator: Update read: %s to %s",
                                      self._readfieldmap[elem.name][elem.fields.cxy], cxy)
                        batch[self._readfieldmap[elem.name][elem.fields.cxy]] = cxy

            batch.caput()

            _LOGGER.info("VirtualAccelerator: FLAME execution time: %f s", time.time()-start)

            # Allow the BPM, PM, etc. readbacks to update
            # before the device setting readbacks PVs.
            cothread.Yield()

            batch = catools.CABatch()
            for name, value in self._csetmap.items():
                name, field = self._fieldmap[name]
                _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", value[1], settings[name][field])
                batch[value[1]] = settings[name][field]
            batch.caput()

            # Sleep for a fraction (10%) of the total execution time
            # when one simulation costs more than 0.50 seconds.
            # Otherwise, sleep for the rest of 1 second.
            # If a scan is being done on this virtual accelerator,
            # then the scan server has a period of time to update
            # setpoints before the next run of IMPACT.
            if (time.time()-start) > 0.50:
                cothread.Sleep((time.time()-start)*0.1)
            else:
                cothread.Sleep(1.0 - (time.time()-start))

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
            s[name][field] = s[name][field] + s[name][field] * self._noise * 2.0*(random.random()-0.5)
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
