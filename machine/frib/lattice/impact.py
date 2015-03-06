# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

import sys, os.path

from datetime import datetime

from collections import OrderedDict

from phylib import cfg

from ..layout.accel import *


INTEGRATOR_LINEAR = 1

INTEGRATOR_LORENTZ = 2



def build_lattice(accel, config=None, settings=None, start=None, end=None):
    """
    """

    # Read config

    lattice_factory = LatticeFactory(accel, config)

    lattice_factory.settings = settings

    lattice_factory.start = start

    lattice_factory.end = end

    return lattice_factory.build()


class LatticeFactory(object):

    def __init__(self, accel, config=None):
        if not isinstance(accel, SeqElement):
            raise TypeError()
        self._accel = accel

        if not isinstance(config, cfg.Configuration):
            raise TypeError()
        self._config = config

        self.nprocessors = 1
        self.integrator = INTEGRATOR_LORENTZ
        self.settings = {}
        self.start = None
        self.end = None


    @property
    def nparticles(self):
        return self._nparticle

    @nparticles.setter
    def nparticles(self, nparticles):
        self._nparticles = int(nparticles)


    @property
    def nprocessors(self):
        return self._nprocessors

    @nprocessors.setter
    def nprocessors(self, nprocessors):
        self._nprocessors = int(nprocessors)


    @property
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, integrator):
        if integrator not in [ INTEGRATOR_LINEAR, INTEGRATOR_LORENTZ ]:
            raise ValueError("")
        self._integrator = integrator


    def build(self):

        steps = 4
        mapsteps = 20

        lattice = Lattice(self.integrator)

        lattice.nprocessors = self.nprocessors

        for elem in self._accel.iter(self.start, self.end):

            if isinstance(elem, DriftElement):
                lattice.append([elem.length, steps, mapsteps, 0, elem.aperture/2.0])

            elif isinstance(elem, ValveElement):
                lattice.append([elem.length, steps, mapsteps, 0, elem.aperture/2.0])

            elif isinstance(elem, PortElement):
                lattice.append([elem.length, steps, mapsteps, 0, elem.aperture/2.0])

            elif isinstance(elem, CavityElement):

                if elem.channels.phase_cset in self.settings:
                    phase = self.settings[elem.channels.phase_cset]["VAL"]
                else:
                    phase = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.phase_cset, elem.name))


                if elem.channels.amplitude_cset in self.settings:
                    amplitude = self.settings[elem.channels.amplitude_cset]["VAL"]
                else:
                    amplitude = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.amplitude_cset, elem.name))
                
                #radius = elem.diameter / 2.0
                #if cavity_field_3d:
                #    lattice.append([elem.length, 48, 20, 110, amplitude, elem.frequency, phase, _file_id(elem.beta), radius, radius, 0, 0, 0, 0, 0, 1, 2 ])
                #else:
                idx = lattice.append([elem.length, 60, 20, 103, amplitude, elem.frequency, phase, _file_id(elem.beta, self.integrator), elem.aperture/2.0])
                lattice.sp_mapping.append((elem.name, {"z":elem.z+elem.length/2.0, "idx":idx}))

            elif isinstance(elem, SolCorrElement):
                if elem.channels.field_cset in self.settings:
                    field = self.settings[elem.channels.field_cset]["VAL"]
                else:
                    field = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.field_cset, elem.name))

                if elem.channels.hkick_cset in self.settings:
                    hkick = self.settings[elem.channels.hkick_cset]["VAL"]
                else:
                    hkick = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.hkick_cset, elem.name))

                if elem.channels.vkick_cset in self.settings:
                    vkick = self.settings[elem.channels.vkick_cset]["VAL"]
                else:
                    vkick = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.vkick_cset, elem.name))

                idx = lattice.append([elem.length/2.0, 1, 20, 3, field, 0.0, elem.aperture/2.0])
                lattice.sp_mapping.append((elem.name, { "1":{"z":elem.z, "idx":idx} }))
                idx = lattice.append([0.0, 0, 0, -21, elem.aperture/2.0, 0.0, hkick, 0.0, vkick, 0.0, 0.0])
                lattice.sp_mapping.append(("{elem.system}_{elem.subsystem}:COR1_{elem.inst}".format(elem=elem), {"z":elem.z, "idx":idx}))
                idx = lattice.append([elem.length/2.0, 1, 20, 3, field, 0.0, elem.aperture/2.0])
                lattice.sp_mapping[-2][1]["2"] = {"z":elem.z+elem.length/2.0, "idx":idx}

            elif isinstance(elem, QuadElement):
                if elem.channels.gradient_cset in self.settings:
                    gradient = self.settings[elem.channels.gradient_cset]["VAL"]
                else:
                    gradient = 0.0
                    print("LatticeFactory: '{}' not found for element: {}".format(elem.channels.gradient_cset, elem.name))

                idx = lattice.append([elem.length, 50, 20, 1, gradient, 0.0, elem.aperture/2.0])
                lattice.sp_mapping.append((elem.name, {"z":elem.z+elem.length/2.0, "idx":idx}))

            elif isinstance(elem, CorrElement):

                if elem.channels.hkick_cset in self.settings:
                    hkick = self.settings[elem.channels.hkick_cset]["VAL"]
                else:
                    hkick = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.hkick_cset, elem.name))

                if elem.channels.vkick_cset in self.settings:
                    vkick = self.settings[elem.channels.vkick_cset]["VAL"]
                else:
                    vkick = 0.0
                    print("LatticeFactory: '{}' channel not found for element: {}".format(elem.channels.vkick_cset, elem.name))

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.aperture/2.0])

                idx = lattice.append([0.0, 0, 0, -21, elem.aperture/2.0, 0.0, hkick, 0.0, vkick, 0.0, 0.0])
                lattice.sp_mapping.append((elem.name, { "1":{"z":elem.z+elem.length/2.0, "idx":idx} }))

                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.aperture/2.0])

            elif isinstance(elem, HexElement):
                # Need to add settings for this element
                lattice.append([elem.length, steps, mapsteps, 5, elem.aperture/2.0])

            elif isinstance(elem, BendElement):
                # Need to add settings for this element
                lattice.append([elem.length, steps, mapsteps, 4, 0.0, 0.0, 0, elem.aperture/2.0])

            elif isinstance(elem, (ChgStripElement)):
                if elem.length != 0.0:
                    lattice.append([elem.length, steps, mapsteps, 0, elem.aperture/2.0])

            elif isinstance(elem, (BLMElement, PMElement, BLElement, BCMElement)):
                if elem.length != 0.0:
                    lattice.append([elem.length, steps, mapsteps, 0, elem.aperture/2.0])

            elif isinstance(elem, BPMElement):
                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.aperture/2.0])

                idx = lattice.append([0.0, 0, 0, -23], output_elem=elem.name)
                lattice.rb_mapping.append((elem.name, {"z":elem.z+elem.length/2.0, "idx":idx}))
                
                if elem.length != 0.0:
                    lattice.append([elem.length/2.0, steps, mapsteps, 0, elem.aperture/2.0])
                
            else:
                raise Exception("Unsupport ADD element: {}".format(elem))
                
        return lattice


        
def _file_id(n, integrator):
    if n > 0.0:
        while n < 1.0:
            n *= 10
        return 100*int(n) + 10*integrator
    else:
        raise Exception("Cannot generate file id from '{}'".format(n))
  

class Lattice(object):

    def __init__(self, integrator, nparticles=1000, nprocessors=10):
        self.nparticles = nparticles
        self.nprocessors = nprocessors
        self._integrator = integrator
    #    self._change_states = []
        self._output_map = []
        self._elements = []
        self.sp_mapping = []
        self.rb_mapping = []


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
        file.write("{lat.nprocessors} 1\r\n".format(lat=self))
        file.write("6 {lat.nparticles} {lat._integrator} 0 4\r\n".format(lat=self))
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



def build_settings(accel, latpath, start=None, end=None):

    settings_factory = SettingsFactory(accel, latpath)

    settings_factory.start = start

    settings_factory.end = end

    return settings_factory.build()



class SettingsFactory(object):

    def __init__(self, accel, latpath):
        self._accel = accel
        self._latpath = latpath
        self.start = None
        self.end = None


    def build(self):

        if not os.path.isfile(self._latpath):
            raise Exception("SettingsFactory: IMPACT lattice file not found: {}".format(self._latpath))

        with open(self._latpath, "r") as fp:
            lattice_element = _LatticeIterator(fp.readlines(), start=11)

        settings = OrderedDict()

        for elem in self._accel.iter(self.start, self.end):

            if isinstance(elem, CavityElement):
                (latidx, latelm) = next(lattice_element)

                if latelm[3] not in [ "103", "110" ]:
                    raise Exception("SettingsFactory: expecting cavity element at line {}, found element: {}".format(latidx+1, latelm))

                if float(latelm[0]) != elem.length:
                    raise Exception("SettingsFactory: expecting cavity element at line {} with length {}: expecting length {}".format(latidx+1, latelm[0], elem.length))

                settings[elem.channels.phase_cset] = OrderedDict([ ("VAL", float(latelm[6])) ])
                settings[elem.channels.phase_rset] = OrderedDict(settings[elem.channels.phase_cset])
                settings[elem.channels.phase_read] = OrderedDict(settings[elem.channels.phase_cset])

                settings[elem.channels.amplitude_cset] = OrderedDict([ ("VAL", float(latelm[4])) ])
                settings[elem.channels.amplitude_rset] = OrderedDict(settings[elem.channels.amplitude_cset])
                settings[elem.channels.amplitude_read] = OrderedDict(settings[elem.channels.amplitude_cset])

            elif isinstance(elem, SolCorrElement):
                # Solenoid elements are normally split into a number of steps, add these steps to get the total length.
                length = 0.0
                while length < elem.length:
                    (latidx, latelm) = next(lattice_element)
                    if latelm[3] != "3":
                        raise Exception("SettingsFactory: expecting solenoid element at line {}, found element: {}".format(latidx+1, latelm))
                    length += float(latelm[0])

                if length > elem.length:
                    raise Exception("SettingsFactory: expecting solenoid element at line {} with length {}: expecting length {}".format(latidx+1, latelm[0], elem.length))

                settings[elem.channels.field_cset] = OrderedDict([ ("VAL", float(latelm[4])) ])
                settings[elem.channels.field_rset] = OrderedDict(settings[elem.channels.field_cset])
                settings[elem.channels.field_read] = OrderedDict(settings[elem.channels.field_cset])
                settings[elem.channels.hkick_cset] = OrderedDict([ ("VAL", 0.0) ])
                settings[elem.channels.hkick_rset] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.hkick_read] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.vkick_cset] = OrderedDict([ ("VAL", 0.0) ])
                settings[elem.channels.vkick_rset] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.vkick_read] = OrderedDict(settings[elem.channels.hkick_cset])

            elif isinstance(elem, QuadElement):
                (latidx, latelm) = next(lattice_element)

                if latelm[3] != "1":
                    raise Exception("SettingsFactory: expecting QuadElement at line {}: found element: {}".format(latidx+1, latelm))
        
                if float(latelm[0]) != elem.length:
                    raise Exception("SettingsFactory: expecting QuadElement at line {} with length {}: expecting length {}".format(latidx+1, latelm[0], elem.length))

                settings[elem.channels.gradient_cset] = OrderedDict([ ("VAL", float(latelm[4])) ])
                settings[elem.channels.gradient_rset] = OrderedDict(settings[elem.channels.gradient_cset])
                settings[elem.channels.gradient_read] = OrderedDict(settings[elem.channels.gradient_cset])

            elif isinstance(elem, CorrElement):
                settings[elem.channels.hkick_cset] = OrderedDict([ ("VAL", 0.0) ])
                settings[elem.channels.hkick_rset] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.hkick_read] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.vkick_cset] = OrderedDict([ ("VAL", 0.0) ])
                settings[elem.channels.vkick_rset] = OrderedDict(settings[elem.channels.vkick_cset])
                settings[elem.channels.vkick_read] = OrderedDict(settings[elem.channels.vkick_cset])

            #elif isinstance(elem, cs.CSElement):
            #    settings[elem.name] = {}

            #elif isinstance(elem, mag.HexElement):
            #    pass

            elif isinstance(elem, (BLMElement, BCMElement, BPMElement, BLElement, PMElement)):
                pass # ignore diagnostic elements

            elif isinstance(elem, (DriftElement, ValveElement, PortElement)):
                pass # ignore passive elements
            
            else:
                raise Exception("SettingsFactory: unsupported accel element: {}".format(elem))

        return settings


class _LatticeIterator():

    def __init__(self, seq, start=0):
        self._idx = -1
        self._iter = iter(seq)
        self._start = start


    def __iter__(self):
        return self


    def next(self):
        while self._idx < (self._start-1):
            self._iter.next()
            self._idx += 1

        while True:
            line = self._iter.next()
            self._idx += 1
            if line.startswith("!"):
                continue
            elm = line.strip().split()
            if (len(elm) <= 3) or (float(elm[3]) <= 0):
                continue
            return (self._idx, elm)
