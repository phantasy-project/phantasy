# encoding: UTF-8

"""Library for running an EPICS-based virtual accelertor using IMPACT particle tracker."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

import os.path, tempfile, random, shutil, numpy
import subprocess, cothread, threading, logging, json, time

from cothread import catools

from collections import OrderedDict

from ....phylib import cfg

from ....phylib.layout.accel import SeqElement, CONFIG_MACHINE 
from ....phylib.layout.accel import CavityElement, SolCorrElement, CorrElement
from ....phylib.layout.accel import QuadElement, BendElement, HexElement, ChgStripElement
from ....phylib.layout.accel import BPMElement, PMElement, BLElement, BCMElement, BLMElement 
from ....phylib.layout.accel import ValveElement, PortElement, DriftElement

from ..lattice.impact import LatticeFactory


# configuration options

CONFIG_IMPACT_EXE_FILE = "impact_exe_file"

CONFIG_IMPACT_DATA_DIR = "impact_data_dir"

# default values

_DEFAULT_IMPACT_EXE = "impact"

_TEMP_DIRECTORY_SUFFIX = "_va_impact"

_DEFAULT_ERROR_VALUE = 0.0

# global logger instance

_LOGGER = logging.getLogger(__name__)

# global virtual accelerator

_VIRTUAL_ACCELERATOR = None



def start(accel, settings=None, machine=None, start=None, end=None, data_dir=None, work_dir=None):
    """Start the global virtual accelerator.

       :param settings: dictionary of machine settings
       :param machine: identifier for this machine instance (ie V_1)
       :param start: name of accelerator element to start simulation
       :param end: name of accelerator element to end simulation
       :param data_dir: path of directory containing IMPACT data files
       :param work_dir: path of directory for execution of IMPACT
    """


    global _VIRTUAL_ACCELERATOR
    if _VIRTUAL_ACCELERATOR == None:
        _VIRTUAL_ACCELERATOR = build(accel, settings, machine, start, end, data_dir, work_dir)

    if _VIRTUAL_ACCELERATOR.is_started():
        raise RuntimeError("Virtual Accelerator already started")

    _VIRTUAL_ACCELERATOR.start()


def stop():
    """Stop the global virtual accelerator.
    """
    global _VIRTUAL_ACCELERATOR
    if _VIRTUAL_ACCELERATOR == None or not _VIRTUAL_ACCELERATOR.is_started():
        raise RuntimeError("Virtual Accelerator not started")

    _VIRTUAL_ACCELERATOR.stop()


def build(accel, settings=None, machine=None, start=None, end=None, data_dir=None, work_dir=None):
    """Convenience method to build a virtual accelerator.

       :param settings: dictionary of machine settings
       :param machine: identifier for this machine instance (ie V_1)
       :param start: name of accelerator element to start simulation
       :param end: name of accelerator element to end simulation
       :param data_dir: path of directory containing IMPACT data files
       :param work_dir: path of directory for execution of IMPACT
       :return: VirtualAccelerator instance
    """
    va_factory = VirtualAcceleratorFactory(accel)

    if settings != None:
        va_factory.settings = settings

    if machine != None:
        va_factory.machine = machine

    if start != None:
        va_factory.start = start

    if end != None:
        va_factory.end = end

    if data_dir != None:
        va_factory.data_dir = data_dir

    if work_dir != None:
        va_factory.work_dir = work_dir

    return va_factory.build()


class VirtualAcceleratorFactory(object):
    """Prepare a VirtualAccelerator for execution.

       The main purpose of this class is to process the accelerator
       description and configure the VirtualAccelerator for proper
       exection.
    """

    def __init__(self, accel):
        self.accel = accel
        self.settings = None
        self.machine = None
        self.start = None
        self.end = None
        self.data_dir = None
        self.work_dir = None


    @property
    def accel(self):
        return self._accel

    @accel.setter
    def accel(self, accel):
        if not isinstance(accel, SeqElement):
            raise TypeError("VirtAccelFactory: 'accel' property much be type SeqElement")
        self._accel = accel


    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if (start != None) and not isinstance(start, basestring):
            raise TypeError("VirtAccelFactory: 'start' property much be type string or None")
        self._start = start


    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end != None) and not isinstance(end, basestring):
            raise TypeError("VirtAccelFactory: 'end' property much be type string or None")
        self._end = end


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if (settings != None) and not isinstance(settings, (dict)):
            raise TypeError("VirtAccelFactory: 'settings' property much be type string or None")
        self._settings = settings


    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, machine):
        if (machine != None) and not isinstance(machine, basestring):
            raise TypeError("VirtAccelFactory: 'machine' property much be type string or None")
        self._machine = machine


    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        if (data_dir != None) and not isinstance(data_dir, basestring):
            raise TypeError("VirtAccelFactory: 'data_dir' property much be type string or None")
        self._data_dir = data_dir


    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        if (work_dir != None) and not isinstance(work_dir, basestring):
            raise TypeError("VirtAccelFactory: 'work_dir' property much be type string or None")
        self._work_dir = work_dir


    def _get_config_settings(self):
        if cfg.config.has_default("settings_file"):
            stgpath = cfg.config.get_default("settings_file")
            if not os.path.isabs(stgpath) and (cfg.config_path != None):
                stgpath = os.path.abspath(os.path.join(os.path.dirname(cfg.config_path), stgpath))
            with open(stgpath, "r") as stgfile:
                return json.load(stgfile)

        return None


    def _get_config_impact_exe(self):
        if cfg.config.has_default(CONFIG_IMPACT_EXE_FILE):
            impact_exe = cfg.config.get_default(CONFIG_IMPACT_EXE_FILE)
            if not os.path.isabs(impact_exe) and impact_exe.startswith(".") and (cfg.config_path != None):
                impact_exe = os.path.abspath(os.path.join(os.path.dirname(cfg.config_path), impact_exe))
            return impact_exe

        return _DEFAULT_IMPACT_EXE


    def build(self):
        """Process the accelerator description and configure the Virtual Accelerator.
        """
        settings = self.settings
        if settings == None:
            settings = self._get_config_settings()

        if settings == None:
            raise RuntimeError("VirtAccelFactory: No settings have been provided, check the configuration.")

        machine = self.machine
        if (machine == None) and cfg.config.has_default(CONFIG_MACHINE):
            machine = cfg.config.get_default(CONFIG_MACHINE)

        data_dir = self.data_dir
        if (data_dir == None) and cfg.config.has_default(CONFIG_IMPACT_DATA_DIR):
            data_dir = cfg.config.get_default(CONFIG_IMPACT_DATA_DIR)

        if data_dir == None:
            raise RuntimeError("VirtAccelFactory: No data directory provided, check the configuration")

        work_dir = self.work_dir

        impact_exe = self._get_config_impact_exe()

        latfactory = LatticeFactory(self.accel)
        latfactory.start = self.start
        latfactory.end = self.end

        va = VirtualAccelerator(latfactory, settings, machine, impact_exe, data_dir, work_dir)

        for elem in self.accel.iter(start=self.start, end=self.end):

            if isinstance(elem, CavityElement):
                chans = elem.channels
                va.append_rw(chans.phase_cset, chans.phase_rset, chans.phase_read, 
                             name="Cavity Phase", egu="degree")
                va.append_rw(chans.amplitude_cset, chans.amplitude_rset, chans.amplitude_read, 
                             name="Cavity Amplitude", egu="%")
                va.append_elem(elem)

            elif isinstance(elem, SolCorrElement):
                chans = elem.channels
                va.append_rw(chans.field_cset, chans.field_rset, chans.field_read, 
                             name="Solenoid Field", egu="T", drvratio=0.10)
                va.append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, 
                             name="Horizontal Corrector", egu="radian", drvabs=0.001)
                va.append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, 
                             name="Vertical Corrector", egu="radian", drvabs=0.001)
                va.append_elem(elem)

            elif isinstance(elem, CorrElement):
                chans = elem.channels
                va.append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, 
                             name="Horizontal Corrector", egu="radian", drvabs=0.001)
                va.append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, 
                             name="Vertical Corrector", egu="radian", drvabs=0.001)
                va.append_elem(elem)

            elif isinstance(elem, BendElement):
                chans = elem.channels
                va.append_rw(chans.field_cset, chans.field_rset, chans.field_read, 
                             name="Bend Relative Field", egu="none", drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, QuadElement):
                chans = elem.channels
                va.append_rw(chans.gradient_cset, chans.gradient_rset, chans.gradient_read, 
                             name="Quadrupole Gradient", egu="T/m", drvratio=0.10)
                va.append_elem(elem)

            elif isinstance(elem, HexElement):
                _LOGGER.warning("VirtAccelFactory: Hexapole magnet element support not implemented. Ignoring channels.")
                #chans = elem.channels
                #va.append_rw(chans.field_cset, chans.field_rset, chans.field_read, name="Hexapole Field", egu="T/m^2", drvrel=0.05)
                #va.append_elem(elem)

            elif isinstance(elem, BPMElement):
                chans = elem.channels
                va.append_ro(chans.hposition_read, name="Horizontal Position", egu="m")
                va.append_ro(chans.vposition_read, name="Vertical Position", egu="m")
                va.append_ro(chans.phase_read, name="Beam Phase", egu="degree")
                va.append_elem(elem)

            elif isinstance(elem, PMElement):
                chans = elem.channels
                va.append_ro(chans.hposition_read, name="Horizontal Position", egu="m")
                va.append_ro(chans.vposition_read, name="Vertical Position", egu="m")
                va.append_ro(chans.hsize_read, name="Horizontal Size", egu="m")
                va.append_ro(chans.vsize_read, name="Vertical Size", egu="m")
                va.append_elem(elem)

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                # ignore these diagnostic elements for now
                pass

            elif isinstance(elem, (ValveElement, PortElement, ChgStripElement)):
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
    def __init__(self, latfactory, settings, machine, impact_exe, data_dir, work_dir=None):
        if not isinstance(latfactory, LatticeFactory):
            raise TypeError("VirtualAccelerator: Invalid type for LatticeFactory")
        self._latfactory = latfactory

        if not isinstance(settings, dict):
            raise TypeError("VirtualAccelerator: Invalid type for accelerator Settings")
        self._settings = settings

        if not isinstance(machine, basestring):
            raise TypeError("VirtualAccelerator: Invalid type for machine value")
        self._machine = machine

        self.impact_exe = impact_exe
        self.data_dir = data_dir
        self.work_dir = work_dir
        
        # status to identify va simulation results
        self.va_good = "OK"
        self.va_bad = "ERR"

        self._epicsdb = []
        self._csetmap = OrderedDict()
        self._elemmap = OrderedDict()

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
        if not isinstance(impact_exe, basestring):
            raise TypeError("VirtualAccelerator: 'impact_exe' property much be type string")
        self._impact_exe = impact_exe


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
        if (work_dir != None) and not isinstance(work_dir, basestring):
            raise TypeError("VirtualAccelerator: 'work_dir' property much be type string or None")
        self._work_dir = work_dir


    def append_rw(self, cset, rset, read, name="Element", egu="", prec=5, drvabs=None, drvrel=None, drvratio=None):
        """Append a set of read/write channels to this virtual accelerator.
        The algorithm to set EPICS DRVH/DRVK is as:
            - if absolute limit (drvabs) is given, use absolute
            - or if relative limit (drvres) is given, use relative
            - or if a ratio (drvratio) is given, use ratio
            - otherwise, no limit.
        
        :param cset:        pv name of set point
        :param rset:        pv name of read back for set point
        :param read:        pv name of read back
        :param name:        element description
        :param egu:         EPICS record engineering unit
        :param prec:        EPICS display precision
        :param drvabs:      absolute driven limit with +-abs(drvabs)
        :param drvrel:      relative driven limit, value +- abs(drvabs)
        :param drvratio:    driven ratio of setting point value * (1 +- ratio) 
        """
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append RW channel when started")

        val = self._settings[cset]["VAL"]
        drvh = None
        drvl = None
        if drvabs is not None:
            drvh = abs(drvabs)
            drvl = - abs(drvabs)
        elif drvrel is not None:
            drvh = val + abs(drvabs)
            drvl = val - abs(drvabs)            
        elif drvratio != None:
            drvh = val + abs(val*drvratio)
            drvl = val - abs(val*drvratio)

        self._epicsdb.append(("ao", cset, OrderedDict([
                ("DESC", "{} Set Point".format(name)),
                ("VAL", val),
                ("DRVH", drvh),
                ("DRVL", drvl),
                ("PREC", prec),
                ("EGU", egu)
            ])))

        self._epicsdb.append(("ai", rset, OrderedDict([
                ("DESC", "{} Set Point Read Back".format(name)),
                ("VAL", self._settings[rset]["VAL"]),
                ("PREC", prec),
                ("EGU", egu)
            ])))

        self._epicsdb.append(("ai", read, OrderedDict([
                ("DESC", "{} Read Back"),
                ("VAL", self._settings[read]["VAL"]),
                ("PREC", prec),
                ("EGU", egu)
            ])))

        self._csetmap[cset] = (rset, read)


    def append_ro(self, read, name="Element", egu="", prec=5):
        """Append a read-only channel to this virtual accelerator.
        """
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append RO channel when started")

        self._epicsdb.append(("ai", read, OrderedDict([
                ("DESC", "{} Read Back".format(name)),
                ("VAL", "0.0"),
                ("PREC", prec),
                ("EGU", egu)
            ])))


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

        if self.work_dir != None and os.path.exists(self.work_dir):
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
            #self._executer.Wait()


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
            if self._subscriptions != None:
                _LOGGER.debug("VirtualAccelerator: Cleanup: close connections")
                for sub in self._subscriptions:
                    sub.close()
                self._subscriptions = None

            if self._ioc_process != None:
                _LOGGER.debug("VirtualAccelerator: Cleanup: terminate IOC process")
                self._ioc_process.terminate()
                self._ioc_process.wait()
                self._ioc_process = None

            if self._ioc_logfile != None:
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
        chanprefix = ""
        if (self._machine != None) and (len(self._machine.strip()) > 0):
            chanprefix = self._machine.strip()+":"

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

        if self.work_dir != None:
            os.makedirs(self.work_dir)
            self._rm_work_dir = False
        else:
            self.work_dir = tempfile.mkdtemp(_TEMP_DIRECTORY_SUFFIX)
            self._rm_work_dir = True

        _LOGGER.info("VirtualAccelerator: Working directory: %s", self._work_dir)

        # input file paths
        epicsdbpath = os.path.join(self.work_dir, "va.db")
        latticepath = os.path.join(self.work_dir, "test.in")

        #output file paths
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
            settings = self._copy_settings_with_noise()
            self._latfactory.settings = settings
            lattice = self._latfactory.build()

            with open(latticepath, "w") as outfile:
                lattice.write(outfile)

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

            _LOGGER.info("VirtualAccelerator: IMPACT execution time: %f s", time.time()-start)

            if status == 0:
                catools.caput(chanstat, self.va_good)
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT exited with non-zero status code: %s\r\n%s", status, stdout)
                catools.caput(chanstat, self.va_bad)

            if os.path.isfile(fort18path):
                fort18 = numpy.loadtxt(fort18path, usecols=(0, 1))
                fort18length = fort18.shape[0]
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT output not found: %s", fort18path)
                catools.caput(chanstat, self.va_bad)
                fort18length = 0

            if os.path.isfile(fort24path):
                fort24 = numpy.loadtxt(fort24path, usecols=(1, 2))
                fort24length = fort24.shape[0]
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT output not found: %s", fort24path)
                catools.caput(chanstat, self.va_bad)
                fort24length = 0

            if os.path.isfile(fort25path):
                fort25 = numpy.loadtxt(fort25path, usecols=(1, 2))
                fort25length = fort25.shape[0]
            else:
                _LOGGER.warning("VirtualAccelerator: IMPACT output not found: %s", fort25path)
                catools.caput(chanstat, self.va_bad)
                fort25length = 0

            output_map = []
            for elem in lattice.elements:
                if elem.itype in [ -28 ]:
                    output_map.append(elem.name)

            output_length = len(output_map)

            if(fort18length < output_length):
                _LOGGER.warning("VirtualAccelerator: IMPACT fort.18 length %s, expecting %s",
                                 fort18length, output_length)
                catools.caput(chanstat, self.va_bad)

            if(fort24length < output_length):
                _LOGGER.warning("VirtualAccelerator: IMPACT fort.24 length %s, expecting %s",
                                 fort24length, output_length)
                catools.caput(chanstat, self.va_bad)

            if(fort25length < output_length):
                _LOGGER.warning("VirtualAccelerator: IMPACT fort.25 length %s, expecting %s", 
                                fort25length, output_length)
                catools.caput(chanstat, self.va_bad)

            for idx in xrange(min(fort18length, fort24length, fort25length)):

                elem = self._elemmap[output_map[idx]]

                if isinstance(elem, BPMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.hposition_read, 
                                  fort24[idx,0])
                    catools.caput(elem.channels.hposition_read, fort24[idx,0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.vposition_read, 
                                  fort25[idx,0])
                    catools.caput(elem.channels.vposition_read, fort25[idx,0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.phase_read, 
                                  fort18[idx,1])
                    catools.caput(elem.channels.phase_read, fort18[idx,1])
                elif isinstance(elem, PMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.hposition_read, 
                                  fort24[idx,0])
                    catools.caput(elem.channels.hposition_read, fort24[idx,0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.vposition_read, 
                                  fort25[idx,0])
                    catools.caput(elem.channels.vposition_read, fort25[idx,0])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.hsize_read, 
                                  fort24[idx,1])
                    catools.caput(elem.channels.hsize_read, fort24[idx,1])
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.vsize_read, 
                                  fort25[idx,1])
                    catools.caput(elem.channels.vsize_read, fort25[idx,1])
                else:
                    _LOGGER.warning("VirtualAccelerator: Output from element type not supported: %s", 
                                    type(elem).__name__)

            # Write the default error value to the remaing output PVs.
            for idx in xrange(min(fort18length, fort24length, fort25length), output_length):

                elem = self._elemmap[output_map[idx]]

                if isinstance(elem, BPMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.hposition_read,
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.hposition_read, _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.vposition_read,
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.vposition_read, _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.phase_read, 
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.phase_read, _DEFAULT_ERROR_VALUE)
                elif isinstance(elem, PMElement):
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.hposition_read, 
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.hposition_read, _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.vposition_read, 
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.vposition_read, _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.hsize_read, 
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.hsize_read, _DEFAULT_ERROR_VALUE)
                    _LOGGER.debug("VirtualAccelerator: Update read: %s to %s", elem.channels.vsize_read, 
                                  _DEFAULT_ERROR_VALUE)
                    catools.caput(elem.channels.vsize_read, _DEFAULT_ERROR_VALUE)
                else:
                    _LOGGER.warning("VirtualAccelerator: Output from element type not supported: %s", 
                                    type(elem).__name__)

            for name, value in self._csetmap.iteritems():
                _LOGGER.debug("VirtualAccelerator: Update rset: %s to %s", value[1], settings[name]["VAL"])
                catools.caput(value[1], settings[name]["VAL"])

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
        catools.caput(cset[1][0], value)
        self._settings[cset[0]]["VAL"] = float(value)



    def _handle_noise_monitor(self, value):
        """Handle updates of the NOISE channel.
        """
        _LOGGER.debug("VirtualAccelerator: Update noise: %s", value)
        self._noise = float(value)


    def _copy_settings_with_noise(self):
        s = OrderedDict()
        for name, value in self._settings.iteritems():
            s[name] = OrderedDict(value)
            s[name]["VAL"] = s[name]["VAL"] + s[name]["VAL"] * self._noise * 2.0*(random.random()-0.5)
        return s


    def _write_epicsdb(self, buf):
        for record in self._epicsdb:
            buf.write("record({}, \"{}\") {{\r\n".format(record[0], record[1]))
            for name, value in record[2].iteritems():
                if value == None:
                    pass # ignore fields with value None
                elif isinstance(value, int):
                    buf.write("    field(\"{}\", {})\r\n".format(name, value))
                elif isinstance(value, float):
                    buf.write("    field(\"{}\", {})\r\n".format(name, value))
                else:
                    buf.write("    field(\"{}\", \"{}\")\r\n".format(name, value))
            buf.write("}\r\n\r\n")



class _Cothread_Popen(object):
    """A helpful wrapper class that integrates the python
       standard popen() method with the Cothread library.
    """

    def __init__(self, *args, **kwargs):
        self._process = subprocess.Popen(*args, **kwargs)
        self._output = None
        self._event = None


    def communicate(self, input=None): # @ReservedAssignment
        """Start a real OS thread to wait for process communication.
        """
        if self._event == None:
            self._event = cothread.Event()
            threading.Thread(target=self._communicate_thread, args=(input,)).start()
        elif input != None:
            raise RuntimeError("_Cothread_Popen: Communicate method already called")

        self._event.Wait()
        return (self._output[0], self._output[1], self._process.poll())


    def _communicate_thread(self, input): # @ReservedAssignment
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

