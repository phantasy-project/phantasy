# encoding: UTF-8

"""
Layout Elements
===============

The accelerator layout is composed of  elements. These elements
represent the various types of accelerator devices or components.

:author: Dylan Maxwell
:date: 2015-06-09

:copyright: Copyright (c) 2015, Facility for Rare Isotope Beams

"""

from __future__ import print_function

import sys

from collections import OrderedDict


# Base Elements

class Channels(object):
    """
    Channels is a simple container for channel names.

    :param kwargs: All keyword parameters converted to object attributes
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(key, value)


    def __str__(self):
        return str(self.__dict__)



class Fields(object):
    """
    Fields is a simple container for element field names.

    :param **kwargs: All keyword arguments become object attributes
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(key, value)


    def __iter__(self):
        return iter(dir(self))


    def __str__(self):
        return str(self.__dict__)



class Element(object):
    """
    Element is the base for the layout element class heirarchy.

    :param float z: Position of this accelerator element
    :param float length: Length of this accelerator element
    :param float aperture: Minimum size of this accelerator element
    :param str name: name of this accelerator element
    :param str **meta: Meta data describing this accelerator element
    """
    def __init__(self, z, length, aperture, name, **meta):
        self.z = z
        self.length = length
        self.aperture = aperture
        self.name = name
        self.meta = dict(meta)
        self.fields = Fields()
        self.channels = Channels()
        self.chanstore = OrderedDict()

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if not isinstance(z, (int, float)):
            raise TypeError("Element: 'z' property must be a number")
        self._z = z

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if not isinstance(length, (int, float)):
            raise TypeError("Element: 'length' property must be a number")
        self._length = length


    @property
    def aperture(self):
        return min(self.apertureX, self.apertureY)

    @aperture.setter
    def aperture(self, aperture):
        if isinstance(aperture, (tuple,list)):
            if isinstance(aperture[0], (int, float)):
                self.apertureX = float(aperture[0])
            else:
                raise TypeError("Element: 'apertureX' property must be a number")
            if isinstance(aperture[1], (int, float)):
                self.apertureY = float(aperture[1])
            else:
                raise TypeError("Element: 'apertureY' property must be a number")

        elif isinstance(aperture, (int, float)):
            self.apertureX = aperture
            self.apertureY = aperture

        else:
            raise TypeError("Element: 'aperture' property must be a number")

    @property
    def apertureX(self):
        return self._apertureX

    @apertureX.setter
    def apertureX(self, apertureX):
        if not isinstance(apertureX, (int, float)):
            raise TypeError("Element: 'apertureX' property must be a number")
        self._apertureX = apertureX


    @property
    def apertureY(self):
        return self._apertureY

    @apertureY.setter
    def apertureY(self, apertureY):
        if not isinstance(apertureY, (int, float)):
            raise TypeError("Element: 'apertureY' property must be a number")
        self._apertureY = apertureY


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, basestring):
            raise TypeError("Element: 'name' property must be a string")
        if len(name) == 0:
            raise ValueError("Element: 'name' property must not be empty")
        self._name = name


    def __getattr__(self, name):
        return self.meta.get(name, "")


    def __str__(self):
        s = "{{ name:'{elem.name}', z:{elem.z}, length:{elem.length}, aperture:{elem.aperture}, meta={elem.meta}, fields={elem.fields} }}"
        return type(self).__name__ + s.format(elem=self)



class SeqElement(Element):
    """
    SeqElement is a composite accelerator element containing a sequence of elements.

    :param str name: Name of this accelerator element
    :param str desc: Description of this accelerator element
    :param list elements: List of elements contained by this sequence.
    """
    def __init__(self, name, elements=None, desc="sequence", **meta):
        super(SeqElement, self).__init__(None, None, None, name, desc=desc, **meta)
        if elements == None:
            self.elements = []
        else:
            self.elements = elements


    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = list(elements)


    @property
    def z(self):
        if len(self.elements) == 0:
            raise Exception("SeqElement: Z-Position undefined for empty sequence")
        return self.elements[0].z

    @z.setter
    def z(self, z):
        if z != None:
            raise NotImplementedError("SeqElement: Setting z not implemented")


    @property
    def length(self):
        length = 0.0
        for elem in self.elements:
            length += elem.length
        return length

    @length.setter
    def length(self, length):
        if length != None:
            raise NotImplementedError("SeqElement: Setting length not implemented")


    @property
    def aperture(self):
        return min(self.apertureX, self.apertureY)

    @aperture.setter
    def aperture(self, aperture):
        if aperture != None:
            raise NotImplementedError("SeqElement: Setting aperture not implemented")


    @property
    def apertureX(self):
        apertureX = float('inf')
        for elem in self.elements:
            apertureX = min(apertureX, elem.apertureX)
        return apertureX

    @apertureX.setter
    def apertureX(self, apertureX):
        if apertureX != None:
            raise NotImplementedError("SeqElement: Setting apertureX not implemented")


    @property
    def apertureY(self):
        apertureY = float('inf')
        for elem in self.elements:
            apertureY = min(apertureY, elem.apertureY)
        return apertureY

    @apertureY.setter
    def apertureY(self, apertureY):
        if apertureY != None:
            raise NotImplementedError("SeqElement: Setting apertureY not implemented")


    def append(self, elem):
        self.elements.append(elem)


    def write(self, indent=2, stream=sys.stdout):
        level = 0
        iterators = [ iter(self.elements) ]

        while len(iterators) > 0:
            it = iterators[-1]
            try:
                elem = it.next()
            except StopIteration:
                del iterators[-1]
                level -= 1
                continue

            stream.write(" "*(indent*level) + str(elem) + "\n")

            if isinstance(elem, SeqElement):
                iterators.append(iter(elem.elements))
                level += 1
                continue


    def __iter__(self):
        return _SeqElementIterator(self)


    def iter(self, start=None, end=None):
        return _SeqElementIterator(self, start, end)


    def __str__(self):
        s = "{{ name:'{elem.name}', desc:'{elem.desc}', nelements:{nelements} }}"
        return type(self).__name__ + s.format(elem=self, nelements=len(self.elements))



class _SeqElementIterator(object):
    """
    Deep iterator for SeqElements.
    """
    def __init__(self, seq, start=None, end=None):
        self._iterators = [ iter(seq.elements) ]
        self._start = start
        self._end = end


    def __iter__(self):
        return self


    def next(self):
        while len(self._iterators) > 0:
            it = self._iterators[-1]
            try:
                elem = it.next()
            except StopIteration:
                del self._iterators[-1]
                continue

            if self._start != None and isinstance(elem, Element):
                if self._start == elem.name:
                    self._start = None

            if self._end != None and isinstance(elem, Element):
                if self._end == elem.name:
                    self._iterators = []
                    self._end = None

            if isinstance(elem, SeqElement):
                self._iterators.append(iter(elem))
                continue

            if self._start == None:
                return elem

        raise StopIteration()



# Passive Elements

class DriftElement(Element):
    """
    DriftElement represents a drift tube, drift space, bellows or other passive element.
    """

    ETYPE="DRIFT"

    def __init__(self, z, length, aperture, name="DRIFT", desc="drift", **meta):
        super(DriftElement, self).__init__(z, length, aperture, name, desc=desc, **meta)


class ValveElement(Element):
    """
    ValveElement represents a vaccuum valve or other similar valve.
    """

    ETYPE="VALVE"

    def __init__(self, z, length, aperture, name, desc="valve", **meta):
        super(ValveElement, self).__init__(z, length, aperture, name, desc=desc, **meta)


class PortElement(Element):
    """
    PortElement represents a attachment point for pump or other device.
    """

    ETYPE="PORT"

    def __init__(self, z, length, aperture, name, desc="port", **meta):
        super(PortElement, self).__init__(z, length, aperture, name, desc=desc, **meta)



# Diagnostic Elements

class BLMElement(Element):
    """
    BLMElement represents Beam Loss Monitor diagnostic device.
    """

    ETYPE="BLM"

    def __init__(self, z, length, aperture, name, desc="beam loss monitor", **meta):
        super(BLMElement, self).__init__(z, length, aperture, name, desc=desc, **meta)


class BPMElement(Element):
    """
    BPMElement represents Beam Position Monitor diagnostic device.
    """

    ETYPE="BPM"

    def __init__(self, z, length, aperture, name, desc="beam positon monitor", **meta):
        super(BPMElement,self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.hposition_read = None
        self.channels.vposition_read = None
        self.channels.phase_read = None
        self.channels.energy_read = None
        self.fields.x = "X"
        self.fields.y = "Y"
        self.fields.phase = "PHA"
        self.fields.energy = "ENG"


class BCMElement(Element):
    """
    BCMElement represents Beam Current Monitor diagnostic device.
    """

    ETYPE="BCM"

    def __init__(self, z, length, aperture, name, desc="beam current monitor", **meta):
        super(BCMElement,self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.current = None
        self.fields.current = "I"


class BLElement(Element):
    """
    BLElement represents Bunch Length Monitor diagnostic device.
    """

    ETYPE="BL"

    def __init__(self, z, length, aperture, name, desc="bunch length monitor", **meta):
        super(BLElement, self).__init__(z, length, aperture, name, desc=desc, **meta)


class PMElement(Element):
    """
    PMElement represents Beam Profile Monitor diagnostic device.
    """

    ETYPE="PM"

    def __init__(self, z, length, aperture, name, desc="beam profile monitor", **meta):
        super(PMElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.hposition_read = None
        self.channels.vposition_read = None
        self.channels.hsize_read = None
        self.channels.vsize_read = None
        self.fields.x = "X"
        self.fields.y = "Y"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"



# Magnetic Elements


class SolElement(Element):
    """
    SolenoidElement represents a solenoid magnet.
    """

    ETYPE="SOL"

    def __init__(self, z, length, aperture, name, desc="solenoid", **meta):
        super(SolElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.field_cset = "FIELD_CSET"
        self.channels.field_rset = "FIELD_RSET"
        self.channels.field_read = "FIELD_READ"
        self.fields.field = "B"



class SolCorElement(SolElement):
    """
    SolenoidElement represents a solenoid magnet with correctors
    """

    ETYPE="SOLCOR"

    def __init__(self, z, length, aperture, name, desc="solenoid w correctors", **meta):
        super(SolCorElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.hkick_cset = "HKICK_CSET"
        self.channels.hkick_rset = "HKICK_RSET"
        self.channels.hkick_read = "HKICK_READ"
        self.channels.vkick_cset = "VKICK_CSET"
        self.channels.vkick_rset = "VKICK_RSET"
        self.channels.vkick_read = "VKICK_READ"
        self.h = None
        self.v = None


class BendElement(Element):
    """
    BendElement represents a bending (dipole) magnet.
    """

    ETYPE="BEND"

    def __init__(self, z, length, aperture, name, desc="bend magnet", **meta):
        super(BendElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.angle = 0.0
        self.entrAngle = 0.0
        self.exitAngle = 0.0
        self.channels.field_cset = "FIELD_CSET"
        self.channels.field_rset = "FIELD_RSET"
        self.channels.field_read = "FIELD_READ"
        self.fields.field = "B"
        self.fields.angle = "ANG"
        self.fields.exitAngle = "EXTANG"
        self.fields.entrAngle = "ENTANG"


class HCorElement(Element):
    """
    HCorElement represents a horizontal corrector magnet or coil.
    """

    ETYPE="HCOR"

    def __init__(self, z, length, aperture, name, desc="horiz. corrector magnet", **meta):
        super(HCorElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.fields.angle = "ANG"


class VCorElement(Element):
    """
    VCorElement represents a vertical corrector magnet or coil.
    """

    ETYPE="VCOR"

    def __init__(self, z, length, aperture, name, desc="vert. corrector magnet", **meta):
        super(VCorElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.fields.angle = "ANG"


class CorElement(Element):
    """
    CorElement represents an element with horizontal and vertical corrector elements.
    """

    ETYPE="COR"

    def __init__(self, z, length, aperture, name, desc="corrector magnet", **meta):
        super(CorElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.hkick_cset = "HKICK_CSET"
        self.channels.hkick_rset = "HKICK_RSET"
        self.channels.hkick_read = "HKICK_READ"
        self.channels.vkick_cset = "VKICK_CSET"
        self.channels.vkick_rset = "VKICK_RSET"
        self.channels.vkick_read = "VKICK_READ"
        self.h = None
        self.v = None


class QuadElement(Element):
    """
    QuadElement represents a quadrupole magnet.
    """

    ETYPE="QUAD"

    def __init__(self, z, length, aperture, name, desc="quadrupole magnet", **meta):
        super(QuadElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.gradient_cset = "GRADIENT_CSET"
        self.channels.gradient_rset = "GRADIENT_RSET"
        self.channels.gradient_read = "GRADIENT_READ"
        self.fields.gradient = "GRAD"


class SextElement(Element):
    """
    SectElement represents a sextapole magnet.
    """

    ETYPE="SEXT"

    def __init__(self, z, length, aperture, name, desc="hexapole magnet", **meta):
        super(SextElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.channels.field_read = "FIELD_READ"
        self.channels.field_cset = "FIELD_CSET"
        self.channels.field_rset = "FIELD_RSET"
        self.fields.field = "B"


# RF Elements

class CavityElement(Element):
    """
    CavityElement represents a RF cavity.
    """

    ETYPE="CAV"

    def __init__(self, z, length, aperture, name, desc="cavity", **meta):
        super(CavityElement, self).__init__(z, length, aperture, name, desc=desc, **meta)
        self.beta = 0.0
        self.voltage = 0.0
        self.frequency = 0.0
        self.channels.phase_cset = "PHASE_CSET"
        self.channels.phase_rset = "PHASE_RSET"
        self.channels.phase_read = "PHASE_READ"
        self.channels.amplitude_cset = "AMPLITUDE_CSET"
        self.channels.amplitude_rset = "AMPLITUDE_RSET"
        self.channels.amplitude_read = "AMPLITUDE_READ"
        self.fields.phase = "PHA"
        self.fields.amplitude = "AMP"
        self.fields.frequency = "FREQ"



# Charge Stripper Elements

class StripElement(Element):
    """
    StripElement represents a charge stripper.
    """

    ETYPE="STRIP"

    def __init__(self, z, length, aperture, name, desc="charge stripper", **meta):
        super(StripElement, self).__init__(z, length, aperture, name, desc=desc, **meta)


# Accelerator Element

class Accelerator(SeqElement):
    """
    Accelerator represents a complete particle accelerator.
    """
    def __init__(self, name, desc="accelerator", elements=None):
        super(Accelerator, self).__init__(name, desc=desc, elements=elements)

