# encoding: UTF-8

from __future__ import print_function

import sys, os.path, tempfile, random, shutil, numpy

import subprocess, cothread, threading

from cothread import catools

from collections import OrderedDict

from machine.frib.layout.accel import *

from machine.frib.lattice.impact import LatticeFactory


_VIRTUAL_ACCELERATOR = None


def start(accel, config=None, settings=None, data_dir=None):
    global _VIRTUAL_ACCELERATOR
    if _VIRTUAL_ACCELERATOR == None:
        _VIRTUAL_ACCELERATOR = build(accel, config=config, settings=settings, data_dir=data_dir)

    if _VIRTUAL_ACCELERATOR.is_started():
        raise RuntimeError("Virtual Accelerator already started")

    _VIRTUAL_ACCELERATOR.start()
    


def stop():
    global _VIRTUAL_ACCELERATOR
    if _VIRTUAL_ACCELERATOR == None or not _VIRTUAL_ACCELERATOR.is_started():
        raise RuntimeError("Virtual Accelerator not started")

    _VIRTUAL_ACCELERATOR.stop()


def build(accel, config=None, settings=None, data_dir=None):

    va_factory = VirtualAcceleratorFactory(accel, config=config, settings=settings)
    
    return va_factory.build(data_dir)



class VirtualAcceleratorFactory(object):
    
    def __init__(self, accel, config=None, settings=None):
        self.accel = accel
        self.config = config
        self.settings = settings
        self.start= "LS1"
        
    
    def build(self, data_dir):
        if data_dir is None:
            raise RuntimeError("IMPACT data files are not available for virtual accelerator.")
    
        va = VirtualAccelerator(data_dir)
        
        va.settings = self.settings
    
        for elem in self.accel.iter(start=self.start):
            
            if isinstance(elem, CavityElement): 
               chans = elem.channels
               va.append_rw(chans.phase_cset, chans.phase_rset, chans.phase_read, name="Cavity Phase", egu="degree")
               va.append_rw(chans.amplitude_cset, chans.amplitude_rset, chans.amplitude_read, name="Cavity Amplitude", egu="%")
               va.append_elem(elem)
            
            elif isinstance(elem, SolCorrElement):
                chans = elem.channels
                va.append_rw(chans.field_cset, chans.field_rset, chans.field_read, name="Solenoid Field", egu="T")
                va.append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, name="Horizontal Corrector", egu="radian")
                va.append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, name="Vertical Corrector", egu="radian")
                va.append_elem(elem)
            
            elif isinstance(elem, CorrElement):
                chans = elem.channels
                va.append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, name="Horizontal Corrector", egu="radian")
                va.append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, name="Vertical Corrector", egu="radian")
                va.append_elem(elem)
            
            elif isinstance(elem, QuadElement):
                chans = elem.channels
                va.append_rw(chans.gradient_cset, chans.gradient_rset, chans.gradient_read, name="Quadrupole Gradient", egu="T/m")             
                va.append_elem(elem)
            
            elif isinstance(elem, BPMElement):
                chans = elem.channels
                va.append_ro(chans.hposition_read, name="Horizontal Position", egu="m")
                va.append_ro(chans.vposition_read, name="Vertical Position", egu="m")
                va.append_elem(elem)
            
            elif isinstance(elem, (BLMElement, BLElement, PMElement)):
                # ignore these diagnostic elements for now
                pass
        
            elif isinstance(elem, (ValveElement, PortElement)):
                # ignore these elements with no relevant channels
                pass
        
            elif isinstance(elem, DriftElement):
                # drift elements have no channels
                pass
        
            else:
                raise RuntimeError("Unsupported element type: {}".format(type(elem).__name__))
    
        va.lattice = LatticeFactory(self.accel, self.config)
        
        va.lattice.start = self.start
        
        va.lattice.nprocessors = 4
    
        return va



class VirtualAccelerator(object):

    def __init__(self, data_dir):
        self.work_dir = None
        self.data_dir = data_dir
        #self.impact_cmd = "impact"
        #self.softioc_cmd = "softIoc"
        self.settings = {}
        self.lattice = None
        self._started = False
        self._epicsdb = []
        self._csetmap = OrderedDict()
        self._elemmap = OrderedDict()
       
    
    def append_rw(self, cset, rset, read, name="Element", egu="", prec=5):
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append RW channel when started")
        
        self._epicsdb.append(("ao", cset, OrderedDict([
                ("DESC", "{} Set Point".format(name)),
                ("VAL", self.settings[cset]["VAL"]),
                ("PREC", prec),
                ("EGU", egu)
                #("FLNK", "_"+cset+":FANOUT")
            ])))

        self._epicsdb.append(("ai", rset, OrderedDict([
                ("DESC", "{} Set Point Read Back".format(name)),
                ("VAL", self.settings[rset]["VAL"]),
                ("PREC", prec),
                ("EGU", egu)
                #("INP", cset)
            ])))

        self._epicsdb.append(("ai", read, OrderedDict([
                ("DESC", "{} Read Back"),
                ("VAL", self.settings[read]["VAL"]),
                ("PREC", prec),
                ("EGU", egu)
            ])))
    
        self._csetmap[cset] = (rset, read)
    
    def append_ro(self, read, name="Element", egu="", prec=5):
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Cannot append RO channel when started")
    
        self._epicsdb.append(("ai", read, OrderedDict([
                ("DESC", "{} Read Back".format(name)),
                ("VAL", "0.0"),
                ("PREC", prec),
                ("EGU", egu)
            ])))

    def append_elem(self, elem):
        self._elemmap[elem.name] = elem

    
    def is_started(self):
        return self._started

      
    def start(self):
        if self.is_started():
            raise RuntimeError("VirtualAccelerator: Already started")
        
        if self.work_dir == None:
            self.work_dir = tempfile.mkdtemp("impact")
        elif not os.path.isdir(self.work_dir):
            raise RuntimeError("VirtualAccelerator: Working directory not found")
        print(self.work_dir)
    
        self._started = True
        cothread.Spawn(self._start)


    def stop(self):
        cth = cothread.Spawn(self._stop)
        cth.Wait()


    def _stop(self):
        self._started = False
        cothread.Sleep(2.0)
        shutil.rmtree(self.work_dir)
        
    
    
    def _start(self):
    
        epicsdbpath = os.path.join(self.work_dir, "va.db")
        
        with open(epicsdbpath, "w") as file:
            self._write_epicsdb(file)
    
        softIocLog = open(os.path.join(self.work_dir, "softIoc.log"), "w")
        self._proc_ioc = _Cothread_Popen(["softIoc", "-d", "va.db"], stdout=softIocLog,
                                         stderr=subprocess.STDOUT, cwd=self.work_dir)
        
        for datafile in os.listdir(self.data_dir):
            if os.path.isfile(os.path.join(self.data_dir, datafile)):
                print("SymLink {} to {}".format(os.path.join(self.data_dir, datafile), os.path.join(self.work_dir, datafile)))
                os.symlink(os.path.join(self.data_dir, datafile), os.path.join(self.work_dir, datafile))

        catools.camonitor(self._csetmap.keys(), self._handle_cset)

        latticepath = os.path.join(self.work_dir, "test.in")
                
        while self.is_started():
        
            settings = self._copy_settings(0.001)
            self.lattice.settings = settings
        
            with open(latticepath, "w") as file:
                lattice = self.lattice.build()
                lattice.write(file)
            
            #cothread.Sleep(2.0)
            #print(self.lattice.nprocessors)
            #break
            proc_s = _Cothread_Popen(["mpirun", "-np", str(self.lattice.nprocessors), "impact"], cwd=self.work_dir)
            (stdout, stderr) = proc_s.communicate()
            #print(stdout)
            #print(stderr)
            
            self._handle_results(lattice)
            
            self._handle_readback(settings)
            
              
    
    def _handle_cset(self, value, idx):
        cset = self._csetmap.items()[idx]        
        #print(cset[0], cset[1][0], value)
        catools.caput(cset[1][0], value)
        self.settings[cset[0]]["VAL"] = float(value)
        
    def _handle_results(self, lattice):
        
        output = lattice._output_map

        fort18path = os.path.join(self.work_dir, "fort.18")
        if not os.path.isfile(fort18path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort18path))

        fort24path = os.path.join(self.work_dir, "fort.24")
        if not os.path.isfile(fort24path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort24path))

        fort25path = os.path.join(self.work_dir, "fort.25")
        if not os.path.isfile(fort25path):
            raise RuntimeError("ResultFactory: IMPACT output not found: {}".format(fort25path))

        fort18 = numpy.loadtxt(fort18path, usecols=(0, 1))
        fort24 = numpy.loadtxt(fort24path, usecols=(1, 2))
        fort25 = numpy.loadtxt(fort25path, usecols=(1, 2))
        
        for idx in xrange(len(output)):
            #print(output[idx])
            elem = self._elemmap[output[idx]]
            
            if isinstance(elem, BPMElement):
                #print(elem.channels.hposition_read, fort24[idx,0])
                catools.caput(elem.channels.hposition_read, fort24[idx,0])
                #print(elem.channels.vposition_read, fort25[idx,0])
                catools.caput(elem.channels.hposition_read, fort25[idx,0])
            else:
                print("Output from element type not supported: {}".format(type(elem).__name__))
    
            
    def _handle_readback(self, settings):
        for name, value in self._csetmap.iteritems():
            #print(name, value[1], settings[name]["VAL"])
            catools.caput(value[1], settings[name]["VAL"])
           
        
    def _copy_settings(self, noise=0.0):
        s = OrderedDict()
        for name, value in self.settings.iteritems():
            s[name] = OrderedDict(value)
            s[name]["VAL"] = s[name]["VAL"] + s[name]["VAL"] * noise * 2.0*(random.random()-0.5)
        return s

        
    def _write_epicsdb(self, buf):
        for record in self._epicsdb:
            buf.write("record({}, \"{}\") {{\r\n".format(record[0], record[1]))
            for name, value in record[2].iteritems():
                if isinstance(value, int):
                    buf.write("    field(\"{}\", {})\r\n".format(name, value))
                elif isinstance(value, float):
                    buf.write("    field(\"{}\", {})\r\n".format(name, value))
                else:
                    buf.write("    field(\"{}\", \"{}\")\r\n".format(name, value))
            buf.write("}\r\n\r\n")
    
    
    
class _Cothread_Popen(object):

    def __init__(self, *args, **kwargs):
        self._process = subprocess.Popen(*args, **kwargs)

    def communicate(self, input=None):
        event = cothread.Event()
        threading.Thread(target=self._communicate_thread, args=(event, self._process, input)).start()
        return event.Wait()

    @staticmethod
    def _communicate_thread(event, process, input):
        (stdout, stderr) = process.communicate(input)
        cothread.Callback(_Cothread_Popen._communicate_callback, event, stdout, stderr)

    @staticmethod
    def _communicate_callback(event, stdout, stderr):
        event.Signal((stdout,stderr))


