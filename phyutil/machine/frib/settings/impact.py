# encoding: UTF-8

"""Library for reading device settings from IMPACT input file (test.in)."""

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import os

from collections import OrderedDict

from ....phylib.layout.accel import *


def build_settings(accel, latpath, start=None, end=None):

    settings_factory = SettingsFactory(accel, latpath)

    if start != None:
        settings_factory.start = start

    if end != None:
        settings_factory.end = end

    return settings_factory.build()


class SettingsFactory(object):

    def __init__(self, accel, latpath):
        self.accel = accel
        self.latpath = latpath
        self.start = None
        self.end = None


    @property
    def accel(self):
        return self._accel

    @accel.setter
    def accel(self, accel):
        if not isinstance(accel, SeqElement):
            raise TypeError("AccelFactory: 'accel' property much be type SeqElement")
        self._accel = accel


    @property
    def latpath(self):
        return self._latpath

    @latpath.setter
    def latpath(self, latpath):
        if not isinstance(latpath, basestring):
            raise TypeError("AccelFactory: 'latpath' property much be type string")
        self._latpath = latpath


    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if (start != None) and not isinstance(start, basestring):
            raise TypeError("AccelFactory: 'start' property much be type string or None")
        self._start = start


    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end != None) and not isinstance(end, basestring):
            raise TypeError("AccelFactory: 'end' property much be type string or None")
        self._end = end



    def build(self):

        if not os.path.isfile(self._latpath):
            raise RuntimeError("SettingsFactory: IMPACT lattice file not found: {}".format(self._latpath))

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
