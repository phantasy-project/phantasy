# encoding: UTF-8

from __future__ import print_function

import sys, StringIO

from collections import OrderedDict

from .. import lattice

from ..layout.accel import *



def start(accel, config=None, settings=None):

    cfp = open("_config.py", "w")

    lat = lattice.impact.build_lattice(accel, config=config, settings=settings, start="LS1")

    _write_mapping(lat.sp_mapping, "sp_mapping", file=cfp)
    
    _write_mapping(lat.rb_mapping, "rb_mapping", file=cfp)

    
    channeldb_factory = ChannelDBFactory(accel, config, settings)
    
    channeldb_factory.start = "LS1"
    
    channeldb = channeldb_factory.build()
    
    channeldb.write(file=cfp)
    
    cfp.close()
    
    dbfp = open("impact_va.db", "w")
    
    epicsdb_factory = EpicsDBFactory(accel, config, settings)
    
    epicsdb_factory.start = "LS1"
    
    epicsdb = epicsdb_factory.build()
    
    epicsdb.write(file=dbfp)

    dbfp.close()
    
    testfp = open("test.in", "w")
    
    lat.write(testfp)


    
    
    # Temp Directory

def _write_mapping(mapping, variable, file=sys.stdout):
      
    def write(k, v, file):
        if isinstance(v, int):
            file.write("'{}': {:d}".format(k,v))
        elif isinstance(v, float):
            file.write("'{}': {}".format(k,v))
        else:
            file.write("'{}': '{}'".format(k,v))
        
    file.write("{} = OrderedDict([".format(variable))
    first_sp = True
    for sp in mapping:
        if first_sp:
            first_sp = False
            file.write("('{}', {{".format(sp[0]))
        else:
            file.write(",\r\n    ('{}', {{".format(sp[0]))
        first_item = True
        for k, v in sp[1].iteritems():
            if first_item:
                first_item = False
            else:
                file.write(",")
            if isinstance(v, (str, int, float)):
                write(k, v, file)
            elif isinstance(v, dict):
                file.write("'{}':{{".format(k))
                first_prop = True
                for kk, vv in v.iteritems():
                    if first_prop:
                        first_prop = False
                    else:
                        file.write(", ")
                    write(kk,vv,file)
                file.write("}")
        file.write("})")
    file.write("])\r\n")



class EpicsDBFactory(object):

    def __init__(self, accel, config=None, settings=None):
        self.accel = accel
        if config != None:
            self.config = config
        else:
            self.config = cfg.Configuration()
        
        if settings != None:
            self.settings = settings
        else:
            self.settings = OrderedDict()
        
        self.start = None
        self.end = None
        
        
    def build(self):
        
        db = EpicsDB()
        
        db.append(EpicsRecord("bi", "D_M:SVR:RSTS", [
                ("ZNAM", "Idle"),
                ("ONAM", "Locked")
            ]))
        
        db.append(EpicsRecord("bi", "D_M:SVR:CMD", [
                ("ZNAM", "Idle"),
                ("ONAM", "Busy")
            ]))
        
        db.append(EpicsRecord("waveform", "D_M:LS1:ORBIT:X_RD", [
                ("DESC", "Horizontal Orbit"),
                ("PREC", 5),
                ("EGU", "m"),
                ("NELM", "59")
            ]))
        
        db.append(EpicsRecord("waveform", "D_M:LS1:ORBIT:Y_RD", [
                ("DESC", "Vertical Orbit"),
                ("PREC", 5),
                ("EGU", "m"),
                ("NELM", "59")
            ]))
        
        db.append(EpicsRecord("waveform", "D_M:LS1:ORBIT:Z_RD", [
                ("DESC", "Z Position"),
                ("PREC", 5),
                ("EGU", "m"),
                ("NELM", "59")
            ]))
        
        def append_rw(cset, rset, read, name="Element", egu="", prec=5):
            
            db.append(EpicsRecord("ao", cset, [
                    ("DESC", "{} Set Point".format(name)),
                    ("VAL", self.settings[cset]["VAL"]),
                    ("PREC", prec),
                    ("EGU", egu),
                    ("FLNK", "_"+cset+":FANOUT")
                ]))

            db.append(EpicsRecord("fanout", "_"+cset+":FANOUT", [
                    ("DESC", "{} CSET Fanout".format(name)),
                    ("LNK1", "_"+cset+":CALC"),
                    ("LNK2", rset)
                ]))

            db.append(EpicsRecord("calc", "_"+cset+":CALC", [
                    ("DESC", "{} CSET Noise".format(name)),
                    ("PREC", prec),
                    ("EGU", egu),
                    ("PINI", 1),
                    ("SCAN", "1 second"),
                    ("INPA", "0.05"),
                    ("INPB", cset),
                    ("CALC", "B+B*A*2.0*(RNDM-0.5)")
                ]))

            db.append(EpicsRecord("ai", rset, [
                    ("DESC", "{} Set Point Read Back".format(name)),
                    ("VAL", self.settings[rset]["VAL"]),
                    ("INP", cset)
                ]))

            db.append(EpicsRecord("ai", read, [
                    ("DESC", "{} Read Back"),
                    ("VAL", self.settings[read]["VAL"]),
                    ("PREC", prec),
                    ("EGU", egu)
                ]))
            
        def append_ro(read, name="", egu="", prec=5):
            db.append(EpicsRecord("ai", read, [
                    ("DESC", "{} Read Back".format(name)),
                    ("VAL", "0.0"),
                    ("PREC", prec),
                    ("EGU", egu)
                ]))
        
        
        for elem in self.accel.iter(start=self.start):
            
            if isinstance(elem, CavityElement): 
               chans = elem.channels
               append_rw(chans.phase_cset, chans.phase_rset, chans.phase_read, name="Cavity Phase", egu="degree")
               append_rw(chans.amplitude_cset, chans.amplitude_rset, chans.amplitude_read, name="Cavity Amplitude", egu="%")
            
            elif isinstance(elem, SolCorrElement):
                chans = elem.channels
                append_rw(chans.field_cset, chans.field_rset, chans.field_read, name="Solenoid Field", egu="T")
                append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, name="Horizontal Corrector", egu="radian")
                append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, name="Vertical Corrector", egu="radian")
            
            elif isinstance(elem, CorrElement):
                chans = elem.channels
                append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, name="Horizontal Corrector", egu="radian")
                append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, name="Vertical Corrector", egu="radian")
            
            elif isinstance(elem, QuadElement):
                chans = elem.channels
                append_rw(chans.gradient_cset, chans.gradient_rset, chans.gradient_read, name="Quadrupole Gradient", egu="T/m")             
            
            elif isinstance(elem, BPMElement):
                chans = elem.channels
                append_ro(chans.hposition_read, name="Horizontal Position", egu="m")
                append_ro(chans.vposition_read, name="Vertical Position", egu="m")
            
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
        
        return db
        

class EpicsDB(object):

    def __init__(self):
        self.records = []
    
    def append(self, record):
        self.records.append(record)

    def write(self, file=sys.stdout):
        for record in self.records:
            record.write(file)


class EpicsRecord(object):

    def __init__(self, rtype, name, fields):
        self.rtype = rtype 
        self.name = name
        self.fields = OrderedDict(fields)

    def write(self, file=sys.stdout):
        file.write(str(self))
        
    def __str__(self):
        buf = StringIO.StringIO()
        buf.write("record({}, \"{}\") {{\r\n".format(self.rtype, self.name))
        for name, value in self.fields.iteritems():
            if isinstance(value, int):
                buf.write("    field(\"{}\", {})\r\n".format(name, value))
            elif isinstance(value, float):
                buf.write("    field(\"{}\", {})\r\n".format(name, value))
            else:
                buf.write("    field(\"{}\", \"{}\")\r\n".format(name, value))
        buf.write("}\r\n\r\n")
        return buf.getvalue()


class ChannelDBFactory(object):

    def __init__(self, accel, config=None, settings=None):
        self.accel = accel
        if config != None:
            self.config = config
        else:
            self.config = cfg.Configuration()
        
        if settings != None:
            self.settings = settings
        else:
            self.settings = OrderedDict()
        
        self.start = None
        self.end = None
        
    
    def build(self):
    
        db = ChannelDB()
    
        for elem in self.accel.iter(start=self.start):
            
            if isinstance(elem, CavityElement): 
               chans = elem.channels
               db.append("_"+chans.phase_cset+":CALC", [("name", elem.name),("type","Cavity"),("field","Phase")])
               #append_rw(chans.phase_cset, chans.phase_rset, chans.phase_read, name="Cavity Phase", egu="degree")
               db.append("_"+chans.amplitude_cset+":CALC", [("name", elem.name),("type","Cavity"),("field","Amplitude")])
               #append_rw(chans.amplitude_cset, chans.amplitude_rset, chans.amplitude_read, name="Cavity Amplitude", egu="%")
            
            elif isinstance(elem, SolCorrElement):
                chans = elem.channels
                cor_name = "{elem.system}_{elem.subsystem}:COR1_{elem.inst}".format(elem=elem)
                db.append("_"+chans.field_cset+":CALC", [("name", elem.name),("type","Solenoid"),("field","B")])
                #append_rw(chans.field_cset, chans.field_rset, chans.field_read, name="Solenoid Field", egu="T")
                db.append("_"+chans.hkick_cset+":CALC", [("name", cor_name),("type","DCH"),("field","HKICK")])
                #append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, name="Horizontal Corrector", egu="radian")
                db.append("_"+chans.vkick_cset+":CALC", [("name", cor_name),("type","DCV"),("field","VKICK")])
                #append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, name="Vertical Corrector", egu="radian")
            
            elif isinstance(elem, CorrElement):
                chans = elem.channels
                print(elem.name, chans.hkick_cset, chans.vkick_cset)
                db.append("_"+chans.hkick_cset+":CALC", [("name", elem.name),("type","DCH"),("field","HKICK")])
                #append_rw(chans.hkick_cset, chans.hkick_rset, chans.hkick_read, name="Horizontal Corrector", egu="radian")
                db.append("_"+chans.vkick_cset+":CALC", [("name", elem.name),("type","DCV"),("field","VKICK")])
                #append_rw(chans.vkick_cset, chans.vkick_rset, chans.vkick_read, name="Vertical Corrector", egu="radian")
            
            elif isinstance(elem, QuadElement):
                chans = elem.channels
                db.append("_"+chans.gradient_cset+":CALC", [("name", elem.name),("type","Quadrupole"),("field","B")])
                #append_rw(chans.gradient_cset, chans.gradient_rset, chans.gradient_read, name="Quadrupole Gradient", egu="T/m")             
            
            elif isinstance(elem, BPMElement):
                chans = elem.channels
                #append_ro(chans.hposition_read, name="Horizontal Position", egu="m")
                #append_ro(chans.vposition_read, name="Vertical Position", egu="m")
            
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
        
        return db
        
    
class ChannelDB(object):

    def __init__(self):
        self.channels = OrderedDict()

    def append(self, chan, props):
        self.channels[chan] = OrderedDict(props)

    def write(self, file=sys.stdout):
        file.write("# pv mapping\r\n")
        file.write("pv_mapping = {")
        first_channel = True
        for chan, props in self.channels.iteritems():
            if first_channel:
                first_channel = False
                file.write(" '{}': {{".format(chan))
            else:
                file.write(",\r\n    '{}': {{".format(chan))
            first_prop = True
            for name, value in props.iteritems():
                if first_prop:
                    first_prop = False
                    file.write("'{}':'{}'".format(name, value))
                else:
                    file.write(",'{}':'{}'".format(name, value))
            file.write("}")
        file.write("}")

