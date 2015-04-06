# encoding: UTF-8

"""Library for generating IMPACT lattice file (test.in) from Accelerator Design Description."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import sys, os.path, json

from datetime import datetime

from collections import OrderedDict

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

CONFIG_IMPACT_FIELD3D_INPUT_ID = "impact_t7data_input_id"


INTEGRATOR_LINEAR = 1

INTEGRATOR_LORENTZ = 2

_DEFAULT_NPARTICLES = 1000

_DEFAULT_NPROCESSORS = 1

_DEFAULT_STEPS = 4

_DEFAULT_MAPSTEPS = 20

_DEFAULT_INTEGRATOR = INTEGRATOR_LORENTZ


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
                lattice.append([elem.length, steps, mapsteps, 0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, []))

            elif isinstance(elem, ValveElement):
                lattice.append([elem.length, steps, mapsteps, 0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, []))

            elif isinstance(elem, PortElement):
                lattice.append([elem.length, steps, mapsteps, 0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, []))

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

                channels = [ elem.channels.phase_cset, elem.channels.phase_rset, elem.channels.phase_read,
                            elem.channels.amplitude_cset, elem.channels.amplitude_rset, elem.channels.amplitude_read]

                itype = self._get_config_type(elem.dtype, 103)
                if itype == 103:
                    input_id = self._get_config_integrator_input_id(elem.dtype, integrator)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                    lattice.append([elem.length, steps, mapsteps, 103, amplitude, elem.frequency, phase, input_id, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, channels))

                elif itype == 110:
                    input_id = self._get_config_t7data_input_id(elem.dtype)
                    if input_id == None:
                        raise RuntimeError("LatticeFactory: IMPACT input id for '{}' not found".format(elem.name))

                    lattice.append([elem.length, steps, mapsteps, 110, amplitude, elem.frequency, phase, input_id, elem.apertureX/2.0, elem.apertureX/2.0, 0, 0, 0, 0, 0, 1, 2 ])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, channels))

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

                sol_channels = [ elem.channels.field_cset, elem.channels.field_rset, elem.channels.field_read ]
                cor_channels = [ elem.channels.hkick_cset, elem.channels.hkick_rset, elem.channels.hkick_read,
                                  elem.channels.vkick_cset, elem.channels.vkick_rset, elem.channels.vkick_read ]


                lattice.append([elem.length/2.0, steps/2, mapsteps, 3, field, 0.0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, elem.length/2.0, sol_channels))

                lattice.append([0.0, 0, 0, -21, elem.apertureX/2.0, 0.0, hkick, 0.0, vkick, 0.0, 0.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, 0.0, cor_channels))

                lattice.append([elem.length/2.0, steps/2, mapsteps, 3, field, 0.0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length/2.0, sol_channels))

            elif isinstance(elem, QuadElement):
                gradient = 0.0
                if settings != None:
                    if elem.channels.gradient_cset in settings:
                        gradient = settings[elem.channels.gradient_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' not found for element: {}".format(elem.channels.gradient_cset, elem.name))

                channels = [ elem.channels.gradient_cset, elem.channels.gradient_rset, elem.channels.gradient_read ]

                lattice.append([elem.length, steps, mapsteps, 1, gradient, 0.0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, channels))

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

                channels = [ elem.channels.hkick_cset, elem.channels.hkick_rset, elem.channels.hkick_read,
                              elem.channels.vkick_cset, elem.channels.vkick_rset, elem.channels.vkick_read ]

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, elem.length/2.0, []))

                lattice.append([0.0, 0, 0, -21, elem.apertureX/2.0, 0.0, hkick, 0.0, vkick, 0.0, 0.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, 0.0, channels))

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length/2.0, []))

            elif isinstance(elem, HexElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                #channels = [ elem.channels.field_cset, elem.channels.field_rset, elem.channels.field_read ]
                #
                ## IMPACT element 5 is not currently document. Below is provided for reference.
                ## L, ss, ms, 5, Gq(T/m), Gs(T/m^2),Go(T/m^3),Gd(T/m^4),Gdd(T/m^5),G14,G16,R
                #lattice.append([elem.length, steps, mapsteps, 5, 0.0, field, 0.0, 0.0, 0.0, 0.0, 0.0, elem.apertureX/2.0])
                #lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, channels))

                if field != 0.0:
                    _LOGGER.warning("LatticeFactory: Hexapole magnet element support not implemented. Ignoring field: %s T/m^2", field)
                lattice.append([elem.length, steps, mapsteps, 0, elem.apertureX/2.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, []))

            elif isinstance(elem, BendElement):
                field = 0.0
                if settings != None:
                    if elem.channels.field_cset in settings:
                        field = settings[elem.channels.field_cset]["VAL"]
                    else:
                        raise RuntimeError("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                channels = [ elem.channels.field_cset, elem.channels.field_rset, elem.channels.field_read ]

                if steps < 3:
                    raise RuntimeError("LatticeFactory: '{}' number of steps must be greater than 2.".format(elem.name))

                lattice.append([elem.length/steps, 1, mapsteps, 4, elem.angle/steps, field, 400, elem.apertureX/2.0, elem.entrAngle, elem.exitAngle, 0.0, 0.0, 0.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-(elem.length/2.0)+(elem.length/steps)-poffset, elem.length/steps, channels))

                for i in xrange(2, steps):
                    lattice.append([elem.length/steps, 1, mapsteps, 4, elem.angle/steps, field, 500, elem.apertureX/2.0, 0.0, 0.0, 0.0, 0.0, 0.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-(elem.length/2.0)+i*(elem.length/steps)-poffset, elem.length/steps, channels))

                lattice.append([elem.length/steps, 1, mapsteps, 4, elem.angle/steps, field, 600, elem.apertureX/2.0, elem.entrAngle, elem.exitAngle, 0.0, 0.0, 0.0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length/steps, channels))

            elif isinstance(elem, (ChgStripElement)):
                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, elem.length/2.0, []))

                # Charge stripper for multi charge state: 885
                # Charge stripper for single charge state: 781
                lattice.append([0, 0, 885, -11, 0, 0])
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, 0, []))

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length/2.0, []))

            elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append([elem.length, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length, []))

            elif isinstance(elem, (BPMElement, PMElement)):
                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, elem.length/2.0, []))

                if isinstance(elem, BPMElement):
                    channels = [ elem.channels.hposition_read, elem.channels.vposition_read,
                                  elem.channels.phase_read ]
                else:
                    channels = [ elem.channels.hposition_read, elem.channels.vposition_read,
                                  elem.channels.hsize_read, elem.channels.vsize_read ]

                lattice.append([0.0, 0, 0, -28], output_elem=elem.name)
                lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z-poffset, 0.0, channels))

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.apertureX/2.0])
                    lattice.chanmap.append((len(lattice._elements)-1, 1, elem.z+(elem.length/2.0)-poffset, elem.length/2.0, []))

            else:
                raise Exception("Unsupport ADD element: {}".format(elem))

        return lattice



class Lattice(object):

    def __init__(self, integrator):
        if integrator not in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
            raise TypeError("Lattice: 'integrator' property must be Enum or None")
        self._integrator = integrator

        self.comment = None
        self.nparticles = _DEFAULT_NPARTICLES
        self.nprocessors = _DEFAULT_NPROCESSORS
        self.chanmap = []
        self._output_map = []
        self._elements = []



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


    def append(self, record, output_elem=None):
        if output_elem != None:
            self._output_map.append(output_elem)
        self._elements.append(record)
        return (len(self._elements) + 11)


    def write(self, file=sys.stdout):
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

    #     # compact lattice by merging drifts
    #     clattice = []
    #     for line in lattice:
    #         if (line[3] == 0) and (len(clattice) > 0) and (clattice[-1][3] == 0):
    #             clattice[-1][0] += line[0]
    #         else:
    #             clattice.append(line)

        for line in self._elements:
            for rec in line:
                if isinstance(rec, int):
                    file.write("{:d} ".format(rec))
                elif isinstance(rec, float):
                    file.write("{:g} ".format(rec))
                else:
                    raise RuntimeError(str(rec))
            file.write("/\r\n")


