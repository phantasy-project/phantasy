# encoding: UTF-8

"""Library for reading device settings from IMPACT input file (test.in)."""

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


import os, logging

from collections import OrderedDict

from ....phylib.layout.accel import *


_LOGGER = logging.getLogger(__name__)


def build_settings(accel, latpath, start=None, end=None):
    """Convenience method for initialize SettingsFactory and generate settings.

       :param accel: accelerator design description element
       :param latpath: path to lattice file (test.in)
       :param start: name of accelerator element to start processing
       :param end: name of accelerator element to end processing
    """
    settings_factory = SettingsFactory(accel, latpath)

    if start != None:
        settings_factory.start = start

    if end != None:
        settings_factory.end = end

    return settings_factory.build()


class SettingsFactory(object):
    """SettingsFactory is a factory class to build a settings dictionary from
       and IMPACT lattice file (test.in) based on an Accelerator Design Description

       :param accel: accelerator design description element
       :param latpath: path to lattice file (test.in)
    """

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
        """Generate the settings dictionary from the IMPACT lattice file.
        """
        if not os.path.isfile(self._latpath):
            raise RuntimeError("SettingsFactory: IMPACT lattice file not found: {}".format(self._latpath))

        with open(self._latpath, "r") as fp:
            lattice_element = _LatticeIterator(fp.readlines(), skip=11)

        settings = OrderedDict()

        for elem in self._accel.iter(self.start, self.end):

            if isinstance(elem, CavityElement):
                (latidx, latelm) = next(lattice_element)

                if latelm[3] not in [ "103", "110" ]:
                    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))

                if not self._isclose(float(latelm[0]), elem.length):
                    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))

                _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)

                settings[elem.channels.phase_cset] = OrderedDict([ ("VAL", float(latelm[6])) ])
                settings[elem.channels.phase_rset] = OrderedDict(settings[elem.channels.phase_cset])
                settings[elem.channels.phase_read] = OrderedDict(settings[elem.channels.phase_cset])

                settings[elem.channels.amplitude_cset] = OrderedDict([ ("VAL", float(latelm[4])) ])
                settings[elem.channels.amplitude_rset] = OrderedDict(settings[elem.channels.amplitude_cset])
                settings[elem.channels.amplitude_read] = OrderedDict(settings[elem.channels.amplitude_cset])


            elif isinstance(elem, SolCorrElement):
                # Solenoid elements are normally split into a number of steps, add these steps to get the total length.
                hkick = None
                vkick = None
                length = 0.0
                while length < elem.length:
                    (latidx, latelm) = next(lattice_element)

                    if latelm[3] == "3":
                         length += float(latelm[0])

                    elif latelm[3] == "-21":
                        hkick = float(latelm[6])
                        vkick = float(latelm[8])

                    else:
                        raise RuntimeError("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))

                    _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)

                if not self._isclose(length, elem.length):
                    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))

                settings[elem.channels.field_cset] = OrderedDict([ ("VAL", float(latelm[4])) ])
                settings[elem.channels.field_rset] = OrderedDict(settings[elem.channels.field_cset])
                settings[elem.channels.field_read] = OrderedDict(settings[elem.channels.field_cset])

                if hkick != None:
                    settings[elem.channels.hkick_cset] = OrderedDict([ ("VAL", hkick ) ])
                else:     
                    _LOGGER.warning("SettingsFactory: %s: Missing horizontal kick setting, assuming 0.0", elem.name)
                    settings[elem.channels.hkick_cset] = OrderedDict([ ("VAL", 0.0 ) ])
                settings[elem.channels.hkick_rset] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.hkick_read] = OrderedDict(settings[elem.channels.hkick_cset])

                if vkick != None:
                    settings[elem.channels.vkick_cset] = OrderedDict([ ("VAL", vkick) ])
                else:
                    _LOGGER.warning("SettingsFactory: %s: Missing vertical kick setting, assuming 0.0", elem.name)
                    settings[elem.channels.vkick_cset] = OrderedDict([ ("VAL", 0.0) ])
                settings[elem.channels.vkick_rset] = OrderedDict(settings[elem.channels.vkick_cset])
                settings[elem.channels.vkick_read] = OrderedDict(settings[elem.channels.vkick_cset])


            elif isinstance(elem, CorrElement):
                (latidx, latelm) = next(lattice_element)

                if latelm[3] not in [ "-21" ]:
                    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))

                _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)

                # Do not check the element length. Element -21 typically has length 0.0 with drift before and after the element.
                #if not self._isclose(float(latelm[0]), elem.length):
                #    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))

                settings[elem.channels.hkick_cset] = OrderedDict([ ("VAL", float(latelm[6])) ])
                settings[elem.channels.hkick_rset] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.hkick_read] = OrderedDict(settings[elem.channels.hkick_cset])
                settings[elem.channels.vkick_cset] = OrderedDict([ ("VAL", float(latelm[8])) ])
                settings[elem.channels.vkick_rset] = OrderedDict(settings[elem.channels.vkick_cset])
                settings[elem.channels.vkick_read] = OrderedDict(settings[elem.channels.vkick_cset])


            elif isinstance(elem, BendElement):
                angle = 0.0
                length = 0.0
                while length < elem.length:
                    (latidx, latelm) = next(lattice_element)
                    
                    if latelm[3] in [ "4" ]:
                        angle += float(latelm[4])
                        length += float(latelm[0])
                    else:
                        raise RuntimeError("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))

                    _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)
                   
                if not self._isclose(length, elem.length):
                    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, length, elem.length))

                settings[elem.channels.angle_cset] = OrderedDict([ ("VAL", angle) ])
                settings[elem.channels.angle_rset] = OrderedDict(settings[elem.channels.angle_cset])
                settings[elem.channels.angle_read] = OrderedDict(settings[elem.channels.angle_cset])


            elif isinstance(elem, QuadElement):
                (latidx, latelm) = next(lattice_element)

                if latelm[3] not in [ "1", "5" ]:
                    raise Exception("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))

                _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)
        
                if not self._isclose(float(latelm[0]), elem.length):
                    raise Exception("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))

                # Both element type 1 and 5 have the quad field strength at index 4. No special logic required!
                settings[elem.channels.gradient_cset] = OrderedDict([ ("VAL", float(latelm[4])) ])
                settings[elem.channels.gradient_rset] = OrderedDict(settings[elem.channels.gradient_cset])
                settings[elem.channels.gradient_read] = OrderedDict(settings[elem.channels.gradient_cset])


            elif isinstance(elem, HexElement):
                #(latidx, latelm) = next(lattice_element)
                #
                #if latelm[3] not in [ "5" ]:
                #    raise Exception("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))
                #
                #_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)
                #
                #if not self._isclose(float(latelm[0]), elem.length):
                #    raise Exception("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))
                #
                _LOGGER.warning("SettingsFactory: Hexapole magnet element support not implemented. Assume field setting 0.0 T/m^2.")

                settings[elem.channels.field_cset] = OrderedDict([ ("VAL", 0.0) ])
                settings[elem.channels.field_rset] = OrderedDict(settings[elem.channels.field_cset])
                settings[elem.channels.field_read] = OrderedDict(settings[elem.channels.field_cset])


            elif isinstance(elem, ChgStripElement):
                (latidx, latelm) = next(lattice_element)

                if latelm[3] != "-11":
                    raise Exception("SettingsFactory: {} at line {}: unexpecting element found: {}".format(elem.name, latidx+1, latelm))

                _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)
        
                # Do not check element length. Element -11 typically has length 0.0, with drift before and after element.
                #if not self._isclose(float(latelm[0]), elem.length):
                #    raise Exception("SettingsFactory: {} at line {}: unexpecting element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))


            elif isinstance(elem, (BLMElement, BCMElement, BPMElement, BLElement, PMElement)):
                pass # ignore diagnostic elements


            elif isinstance(elem, (DriftElement, ValveElement, PortElement)):
                pass # ignore passive elements

            
            else:
                raise Exception("SettingsFactory: unsupported accel element: {}".format(elem))

        return settings


    @staticmethod
    def _isclose(a, b, rtol=1e-5, atol=1e-8):
        # Implementation adopted from NumPy 'isclose()'
        # including the default values for rtol and atol.
        return (abs(a - b) <= (atol + rtol*abs(b)))


class _LatticeIterator():

    def __init__(self, seq, skip=0):
        self._idx = -1
        self._iter = iter(seq)
        self._skip = skip


    def __iter__(self):
        return self


    def next(self):
        while self._skip > 0:
            line = self._iter.next()
            self._idx += 1
            if line.startswith("!"):
                continue
            self._skip -= 1

        while True:
            line = self._iter.next()
            self._idx += 1
            if line.startswith("!"):
                continue
            elm = line.strip().split()
            if float(elm[3]) in [ 0, -13, -28 ]:
                _LOGGER.debug("SettingsFactory: Skipping line %s: %s", self._idx+1, elm)
                continue
            return (self._idx, elm)

