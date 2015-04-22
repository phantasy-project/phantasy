# encoding: UTF-8

"""Library for generating IMPACT lattice file (test.in) from Accelerator Design Description."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import os.path, logging, json

from datetime import datetime

from ....phylib import cfg

from ....phylib.layout.accel import *


CONFIG_IMPACT_NPARTICLES = "impact_nparticles"

CONFIG_IMPACT_NPROCESSORS = "impact_nprocessors"

CONFIG_IMPACT_TYPE = "impact_type"

CONFIG_IMPACT_STEPS = "impact_steps"

CONFIG_IMPACT_MAPSTEPS = "impact_mapsteps"

CONFIG_IMPACT_INTEGRATOR = "impact_integrator"

CONFIG_IMPACT_LINEAR_INPUT_ID = "impact_linear_input_id"

CONFIG_IMPACT_LORENTZ_INPUT_ID = "impact_lorentz_input_id"

CONFIG_IMPACT_T7DATA_INPUT_ID = "impact_t7data_input_id"


INTEGRATOR_LINEAR = 1

INTEGRATOR_LORENTZ = 2

_DEFAULT_NPARTICLES = 1000

_DEFAULT_NPROCESSORS = 1

_DEFAULT_STEPS = 4

_DEFAULT_MAPSTEPS = 20

_DEFAULT_INTEGRATOR = INTEGRATOR_LORENTZ


_LOGGER = logging.getLogger(__name__)


def build_lattice(accel, settings=None, start=None, end=None):
    """Convenience method for building the IMPACT lattice."""

    lattice_factory = LatticeFactory(accel)

    if settings != None:
        lattice_factory.settings = settings

    if start != None:
        lattice_factory.start = start

    if end != None:
        lattice_factory.end = end

    return lattice_factory.build()


class LatticeFactory(object):
    """LatticeFactory class builds an IMPACT lattice
       object from an Accelerator Design Description.
    """

    def __init__(self, accel):
        self.accel = accel
        self.nparticles = None
        self.nprocessors = None
        self.integrator = None
        self.settings = None
        self.start = None
        self.end = None


    @property
    def accel(self):
        return self._accel

    @accel.setter
    def accel(self, accel):
        if not isinstance(accel, SeqElement):
            raise TypeError("LatticeFactory: 'accel' property must be type a SeqElement")
        self._accel = accel


    @property
    def nparticles(self):
        return self._nparticles

    @nparticles.setter
    def nparticles(self, nparticles):
        if (nparticles != None) and not isinstance(nparticles, (int,float)):
            raise TypeError("LatticeFactory: 'nparticles' property must be number or None")
        self._nparticles = nparticles if nparticles == None else int(nparticles)


    @property
    def nprocessors(self):
        return self._nprocessors

    @nprocessors.setter
    def nprocessors(self, nprocessors):
        if (nprocessors != None) and not isinstance(nprocessors, (int,float)):
            raise TypeError("LatticeFactory: 'nprocessors' property must be number or None")
        self._nprocessors = nprocessors if nprocessors == None else int(nprocessors)


    @property
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, integrator):
        if (integrator != None) and integrator not in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
            raise TypeError("LatticeFactory: 'integrator' property must be Enum or None")
        self._integrator = integrator


    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if (start != None) and not isinstance(start, basestring):
            raise TypeError("LatticeFactory: 'start' property much be type string or None")
        self._start = start


    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end != None) and not isinstance(end, basestring):
            raise TypeError("LatticeFactory: 'end' property much be type string or None")
        self._end = end


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if (settings != None) and not isinstance(settings, (dict)):
            raise TypeError("LatticeFactory: 'settings' property much be type string or None")
        self._settings = settings


    def _get_config_type(self, dtype, default):
        if cfg.config.has_option(dtype, CONFIG_IMPACT_TYPE, False):
            return cfg.config.getint(dtype, CONFIG_IMPACT_TYPE, False)

        return default


    def _get_config_integrator_input_id(self, dtype, integrator):
        if (integrator == INTEGRATOR_LINEAR):
            if cfg.config.has_option(dtype, CONFIG_IMPACT_LINEAR_INPUT_ID, False):
                return cfg.config.getint(dtype, CONFIG_IMPACT_LINEAR_INPUT_ID, False)

        if (integrator == INTEGRATOR_LORENTZ):
            if cfg.config.has_option(dtype, CONFIG_IMPACT_LORENTZ_INPUT_ID, False):
                return cfg.config.getint(dtype, CONFIG_IMPACT_LORENTZ_INPUT_ID, False)

        return None


    def _get_config_t7data_input_id(self, dtype):
        if cfg.config.has_option(dtype, CONFIG_IMPACT_T7DATA_INPUT_ID, False):
            return cfg.config.getint(dtype, CONFIG_IMPACT_T7DATA_INPUT_ID, False)

        return None


    def _get_config_nparticles(self):
        if cfg.config.has_default(CONFIG_IMPACT_NPARTICLES):
            return cfg.config.getint_default(CONFIG_IMPACT_NPARTICLES)

        return _DEFAULT_NPARTICLES


    def _get_config_nprocessors(self):
        if cfg.config.has_default(CONFIG_IMPACT_NPROCESSORS):
            return cfg.config.getint_default(CONFIG_IMPACT_NPROCESSORS)

        return _DEFAULT_NPROCESSORS


    def _get_config_integrator(self):
        if cfg.config.has_default(CONFIG_IMPACT_INTEGRATOR):
            integrator = cfg.config.getint_default(CONFIG_IMPACT_INTEGRATOR)
            if integrator in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
                return integrator

        return _DEFAULT_INTEGRATOR


    def _get_config_settings(self):
        if cfg.config.has_default("settings_file"):
            stgpath = cfg.config.get_default("settings_file")
            if not os.path.isabs(stgpath) and (cfg.config_path != None):
                stgpath = os.path.abspath(os.path.join(os.path.dirname(cfg.config_path), stgpath))
            with open(stgpath, "r") as stgfile:
                return json.load(stgfile)

        return None


    def _get_config_steps(self, dtype=None):
        if (dtype == None) and cfg.config.has_default(CONFIG_IMPACT_STEPS):
            return cfg.config.getint_default(CONFIG_IMPACT_STEPS)

        if (dtype != None) and cfg.config.has_option(dtype, CONFIG_IMPACT_STEPS):
            return cfg.config.getint(dtype, CONFIG_IMPACT_STEPS)

        return _DEFAULT_STEPS


    def _get_config_mapsteps(self, dtype=None):
        if (dtype == None) and cfg.config.has_default(CONFIG_IMPACT_MAPSTEPS):
            return cfg.config.getint_default(CONFIG_IMPACT_MAPSTEPS)

        if (dtype != None) and cfg.config.has_option(dtype, CONFIG_IMPACT_MAPSTEPS):
            return cfg.config.getint(dtype, CONFIG_IMPACT_MAPSTEPS)

        return _DEFAULT_MAPSTEPS



    def build(self):

        nparticles = self.nparticles
        if nparticles == None:
            nparticles = self._get_config_nparticles()

        nprocessors = self.nprocessors
        if nprocessors == None:
            nprocessors = self._get_config_nprocessors()

        integrator = self.integrator
        if integrator == None:
            integrator = self._get_config_integrator()

        settings = self.settings
        if settings == None:
            settings = self._get_config_settings()

        lattice = Lattice(integrator)
        lattice.nparticles = nparticles
        lattice.nprocessors = nprocessors
        lattice.comment = "Name: {a.name}, Desc: {a.desc}".format(a=self._accel)

        poffset = None

        for elem in self._accel.iter(self.start, self.end):

            if poffset == None:
                poffset = elem.z - (elem.length/2.0)

            if isinstance(elem, Element):
                steps = self._get_config_steps(elem.dtype)
                mapsteps = self._get_config_mapsteps(elem.dtype)
            else:
                steps = self._get_config_steps()
                mapsteps = self._get_config_mapsteps()

            if isinstance(elem, DriftElement):
                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, ValveElement):
                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="VALVE")

            elif isinstance(elem, PortElement):
                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="PORT")

            elif isinstance(elem, CavityElement):
                phase = 0.0
                if settings != None:
                    if elem.channels.phase_cset in settings:
                        phase = settings[elem.channels.phase_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.phase_cset, elem.name))

                amplitude = 0.0
                if settings != None:
                    if elem.channels.amplitude_cset in settings:
                        amplitude = settings[elem.channels.amplitude_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.amplitude_cset, elem.name))

                itype = self._get_config_type(elem.dtype, 103)
                if itype == 103:
                    input_id = self._get_config_integrator_input_id(elem.dtype, integrator)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                    lattice.addProperty("AMP", "V")
                    lattice.addProperty("PHA", "deg")

                    lattice.append("{length} {steps} {mapsteps} {itype} {properties[AMP]} "+str(elem.frequency)+" {properties[PHA]} "+str(input_id)+" {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=103, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="CAV",
                                    properties={ "AMP":amplitude, "PHA":phase })
                elif itype == 110:
                    input_id = self._get_config_t7data_input_id(elem.dtype)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                    lattice.addProperty("AMP", "V")
                    lattice.addProperty("PHA", "deg")

                    lattice.append("{length} {steps} {mapsteps} {itype} {properties[AMP]} "+str(elem.frequency)+" {properties[PHA]} "+str(input_id)+" {radius} {radius} 0 0 0 0 0 1 2",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=110, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="CAV",
                                    properties={ "AMP":amplitude, "PHA":phase })

                else:
                    raise RuntimeError("LatticeFactory: IMPACT element type for '{}' not supported: {}".format(elem.name, itype))

            elif isinstance(elem, SolCorrElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                hkick = 0.0
                if settings != None:
                    if elem.channels.hkick_cset in settings:
                        hkick = settings[elem.channels.hkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.hkick_cset, elem.name))

                vkick = 0.0
                if settings != None:
                    if elem.channels.vkick_cset in settings:
                        vkick = settings[elem.channels.vkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.vkick_cset, elem.name))


                lattice.addProperty("B", "T")

                lattice.append("{length} {steps} {mapsteps} {itype} {properties[B]} 0 {radius}",
                                    length=elem.length/2.0, steps=steps/2, mapsteps=mapsteps, itype=3, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name=elem.name, etype="SOL", properties={ "B":field })

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 {properties[ANG]} 0.0 0.0 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem), etype="HCOR", properties={ "ANG":hkick })

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 0.0 0.0 {properties[ANG]} 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem), etype="VCOR", properties={ "ANG":vkick })

                lattice.append("{length} {steps} {mapsteps} {itype} {properties[B]} 0 {radius}",
                                    length=elem.length/2.0, steps=steps/2, mapsteps=mapsteps, itype=3, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="SOL", properties={ "B":field })


            elif isinstance(elem, QuadElement):
                gradient = 0.0
                if settings != None:
                    if elem.channels.gradient_cset in settings:
                        gradient = settings[elem.channels.gradient_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' not found for element: {}".format(elem.channels.gradient_cset, elem.name))

                lattice.addProperty("GRAD", "T/m")

                lattice.append("{length} {steps} {mapsteps} {itype} {properties[GRAD]} 0 {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=1, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="QUAD", properties={ "GRAD":gradient })


            elif isinstance(elem, CorrElement):
                hkick = 0.0
                if settings != None:
                    if elem.channels.hkick_cset in settings:
                        hkick = settings[elem.channels.hkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.hkick_cset, elem.name))

                vkick = 0.0
                if settings != None:
                    if elem.channels.vkick_cset in settings:
                        vkick = settings[elem.channels.vkick_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.vkick_cset, elem.name))

                lattice.addProperty("ANG", "rad")

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 {properties[ANG]} 0.0 0.0 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCH_{elem.inst}".format(elem=elem), etype="HCOR", properties={ "ANG":hkick })

                lattice.append("{length} {steps} {mapsteps} {itype} {radius} 0.0 0.0 0.0 {properties[ANG]} 0.0 0.0",
                                    length=0.0, steps=0, mapsteps=0, itype=-21, radius=elem.apertureX/2.0, position=elem.z-poffset,
                                    name="{elem.system}_{elem.subsystem}:DCV_{elem.inst}".format(elem=elem), etype="VCOR", properties={ "ANG":vkick })

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")


            elif isinstance(elem, HexElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                ## IMPACT element 5 is not currently document. Below is provided for reference.
                ## L, ss, ms, 5, Gq(T/m), Gs(T/m^2),Go(T/m^3),Gd(T/m^4),Gdd(T/m^5),G14,G16,R
                #lattice.append("{length} {steps} {mapsteps} {itype} 0.0 {properties[B]} 0.0 0.0 0.0 0.0 0.0 {radius}",
                #                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=5, radius=elem.apertureX/2.0,
                #                    position=elem.z+(elem.length/2.0)-poffset, name=elem.name, etype="SEXT", properties={ "B":field })

                if field != 0.0:
                    _LOGGER.warning("LatticeFactory: Hexapole magnet element support not implemented. Ignoring field: %s T/m^2", field)

                lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, BendElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                if steps < 3:
                    raise RuntimeError("LatticeFactory: '{}' number of steps must be greater than 2.".format(elem.name))

                lattice.addProperty("B", "T")

                lattice.append("{length} {steps} {mapsteps} {itype} "+str(elem.angle/steps)+" {properties[B]} 400 {radius} "+str(elem.entrAngle)+" "+str(elem.exitAngle)+" 0.0 0.0 0.0",
                                    length=elem.length/steps, steps=1, mapsteps=mapsteps, itype=4, radius=elem.apertureX/2.0,
                                    position=elem.z-(elem.length/2.0)+(elem.length/steps)-poffset,
                                    name=elem.name, etype="BEND", properties={ "B":field })

                for i in xrange(2, steps):
                    lattice.append("{length} {steps} {mapsteps} {itype} "+str(elem.angle/steps)+" {properties[B]} 500 {radius} 0.0 0.0 0.0 0.0 0.0",
                                    length=elem.length/steps, steps=1, mapsteps=mapsteps, itype=4, radius=elem.apertureX/2.0,
                                    position=elem.z-(elem.length/2.0)+i*(elem.length/steps)-poffset,
                                    name=elem.name, etype="BEND", properties={ "B":field })

                lattice.append("{length} {steps} {mapsteps} {itype} "+str(elem.angle/steps)+" {properties[B]} 600 {radius} "+str(elem.entrAngle)+" "+str(elem.exitAngle)+" 0.0 0.0 0.0",
                                    length=elem.length/steps, steps=1, mapsteps=mapsteps, itype=4, radius=elem.apertureX/2.0,
                                    position=elem.z-(elem.length/2.0)+(elem.length/steps)-poffset,
                                    name=elem.name, etype="BEND", properties={ "B":field })

            elif isinstance(elem, (ChgStripElement)):
                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                # Charge stripper for multi charge state: 885
                # Charge stripper for single charge state: 781
                lattice.append("{length} 0 885 {itype} 0 0", length=0.0, itype=-11, position=elem.z-poffset, name=elem.name, etype="STRIP")

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            elif isinstance(elem, (BPMElement, PMElement)):
                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name="DRIFT", etype="DRIFT")

                if isinstance(elem, BPMElement):
                    etype = "BPM"
                else:
                    etype = "PM"

                lattice.append("0 0 0 {itype}", length=0.0, itype=-28, radius=elem.apertureX/2.0,
                                    position=elem.z-poffset, name=elem.name, etype=etype)

                if elem.length != 0.0:
                    lattice.append("{length} {steps} {mapsteps} {itype} {radius}",
                                    length=elem.length/2.0, steps=steps, mapsteps=mapsteps, itype=0, radius=elem.apertureX/2.0,
                                    position=elem.z+(elem.length/2.0)-poffset, name="DRIFT", etype="DRIFT")

            else:
                raise Exception("Unsupport ADD element: {}".format(elem))

        return lattice



class Lattice(object):
    """Describes the IMPACT lattice (test.in) including header and elements.

    :params integrator: integrator type (Linear Map or Lorentz)
    """
    def __init__(self, integrator):
        if integrator not in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
            raise TypeError("Lattice: 'integrator' property must be Enum or None")
        self._integrator = integrator

        self.comment = None
        self.nparticles = _DEFAULT_NPARTICLES
        self.nprocessors = _DEFAULT_NPROCESSORS
        self.elements = []
        self.properties = []



    @property
    def nparticles(self):
        return self._nparticles

    @nparticles.setter
    def nparticles(self, nparticles):
        self._nparticles = int(nparticles)


    @property
    def nprocessors(self):
        return self._nprocessors

    @nprocessors.setter
    def nprocessors(self, nprocessors):
        self._nprocessors = int(nprocessors)


    def append(self, elemformat, length=0.0, steps=0, mapsteps=0, itype=0, radius=0.0, position=0.0, name=None, etype=None, properties={}):
        self.elements.append(LatticeElement(elemformat, length, steps, mapsteps, itype, radius, position, name, etype, properties))


    def addProperty(self, name, units):
        for prop in self.properties:
            if prop.name == name:
                if prop.units == units:
                    return # Proprty has already added, and it has the same units so nothing needed to be done.
                else:
                    raise RuntimeError("Lattice: Error adding property: '{}': Units not match: '{}' vs '{}'".format(name, units, prop.units))

        self.properties.append(LatticeProperty(name, units))


    def write(self, file=sys.stdout):
        """Write the IMPACT lattice file (test.in) to the specified file object.

        :param file: file-like object to write lattice (test.in)
        """
        file.write("!! Generated by PhysUtil - {}\r\n".format(datetime.now()))
        if self.comment != None: file.write("!! {}\r\n".format(self.comment))
        file.write("{lat.nprocessors} 1\r\n".format(lat=self))
        file.write("6 {lat.nparticles} {lat._integrator} 0 3\r\n".format(lat=self))
        file.write("65 65 129 4 0.140000 0.140000 0.1025446\r\n")
        file.write("3 0 0 1\r\n")
        file.write("{lat.nparticles}\r\n".format(lat=self))
        file.write("0.0\r\n")
        file.write("1.48852718947e-10\r\n")
        file.write("0.22734189E-02  0.88312578E-04  0.00000000E+00  1.000  1.000  0.000  0.000\r\n")
        file.write("0.22734189E-02  0.88312578E-04  0.00000000E+00  1.000  1.000  0.000  0.000\r\n")
        file.write("0.76704772E-01  0.34741445E-05  0.00000000E+00  1.000  1.000  0.000  0.000\r\n")
        file.write("0.0 0.5e6 931.49432e6 0.1386554621848 80.50e6 0.0 99.9\r\n")

        # TODO: Option to compact lattice by merging drifts, etc.

        for elem in self.elements:
            file.write(str(elem))
            file.write(" /\r\n")



class LatticeElement(object):
    """Describes an IMPACT lattice element (a row in the test.in file).

    :param elemformat: a python format string
    :param length: element length
    :param steps: number of simulation steps
    :param mapsteps: number of sumulation map steps
    :param itype: the IMPACT numeric element type
    :param radius: element radius
    :param position: element position
    :param name: element name
    :param etype: element type
    :param properties: element property values
    """

    def __init__(self, elemformat, length=0.0, steps=4, mapsteps=20, itype=0, radius=0.0, position=0.0, name=None, etype=None, properties={}):
        self.elemformat = elemformat
        self.length = length
        self.steps = steps
        self.mapsteps = mapsteps
        self.itype = itype
        self.position = position
        self.radius = radius
        self.name = name
        self.etype = etype
        self.properties = properties


    def __str__(self):
        return self.elemformat.format(length=self.length, steps=self.steps, mapsteps=self.mapsteps,
                                        itype=self.itype, radius=self.radius, position=self.position, properties=self.properties)




class LatticeProperty(object):
    """Describes a property of a lattice elements such as field or angle.

    :param name: the property name
    :param units: the physical units
    """
    def __init__(self, name, units):
        self.name = name
        self.units = units


    def __str__(self):
        return "{{ name='{prop.name}', units='{prop.units}' }}".format(prop=self)

