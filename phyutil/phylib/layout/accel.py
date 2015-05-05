# encoding: UTF-8

"""
Accelerator Design Description
==============================

The Accelerator Design Description (ADD) is a data model developed to capture
the accelerator design independent of file format and/or simulation tool.
It is used as intermediate data structure when converting between formats
or generating lattice files for use with various simulation tools.
"""

from __future__ import print_function

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


from collections import OrderedDict

# configuration options

CONFIG_MACHINE = "machine"

CONFIG_LENGTH = "length"

CONFIG_APERTURE = "aperture"

CONFIG_APERTURE_X = "aperture_x"

CONFIG_APERTURE_Y = "aperture_y"

CONFIG_CAV_BETA = "cav_beta"

CONFIG_CAV_VOLTAGE = "cav_voltage"

CONFIG_CAV_FREQUENCY = "cav_frequency"

CONFIG_BEND_ANGLE = "bend_angle"

CONFIG_BEND_ENTR_ANGLE = "bend_entr_angle"

CONFIG_BEND_EXIT_ANGLE = "bend_exit_angle"


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



class BaseElement(object):
    """
    BaseElement is the base for the accelerator class heirarchy.

    :param float z: Position of this accelerator element
    :param float length: Length of this accelerator element
    :param float aperture: Minimum size of this accelerator element
    :param str desc: Description of this accelerator element
    """
    def __init__(self, z, length, aperture, desc=""):
        self.z = z
        self.length = length
        if isinstance(aperture, (tuple,list)):
            self.apertureX = aperture[0]
            self.apertureY = aperture[1]
        else:
            self.aperture = aperture
        self.desc = desc
        self.channels = Channels()
        self.chanstore = OrderedDict()

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if not isinstance(z, (int, float)):
            raise TypeError("BaseElement: 'z' property must be type a number")
        self._z = z

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if not isinstance(length, (int, float)):
            raise TypeError("BaseElement: 'length' property must be type a number")
        self._length = length


    @property
    def aperture(self):
        return min(self.apertureX, self.apertureY)

    @aperture.setter
    def aperture(self, aperture):
        self.apertureX = aperture
        self.apertureY = aperture


    @property
    def apertureX(self):
        return self._apertureX

    @apertureX.setter
    def apertureX(self, apertureX):
        if not isinstance(apertureX, (int, float)):
            raise TypeError("BaseElement: 'apertureX' property must be a number")
        self._apertureX = apertureX


    @property
    def apertureY(self):
        return self._apertureY

    @apertureY.setter
    def apertureY(self, apertureY):
        if not isinstance(apertureY, (int, float)):
            raise TypeError("BaseElement: 'apertureY' property must be a number")
        self._apertureY = apertureY


    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        if not isinstance(desc, basestring):
            raise TypeError("BaseElement: 'desc' property must be a string")
        self._desc = desc


    def __str__(self):
        s = "{{ desc:'{elem.desc}', z:{elem.z}, length:{elem.length}, aperture:{elem.aperture}, channels:{elem.channels} }}"
        return type(self).__name__ + s.format(elem=self)



class NamedElement(BaseElement):
    """
    NamedElement is an accelerator element with unique name.

    :param float z: Position of this accelerator element
    :param float length: Length of accelerator element
    :param float aperture: Minimum size of accelerator element
    :param str name: Name of accelerator element
    :param str desc: Description of accelerator element
    """
    def __init__(self, z, length, aperture, name, desc=""):
        super(NamedElement, self).__init__(z, length, aperture, desc=desc)
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, basestring):
            raise TypeError("NamedElement: 'name' property must be a string")
        if len(name) == 0:
            raise ValueError("NamedElement: 'name' property must not be empty")
        self._name = name


    def __str__(self):
        s = "{{ name:'{elem.name}', desc:'{elem.desc}', z:{elem.z}, length:{elem.length}, aperture:{elem.aperture}, channels:{elem.channels} }}"
        return type(self).__name__ + s.format(elem=self)



class Element(NamedElement):
    """
    Element is an accelerator element with classified by system, subsystem, device and instance.

    :param float z: Position of this accelerator element
    :param float length: Length of this accelerator element
    :param float aperture: Minimum size of this accelerator element
    :param str name: Name of this accelerator element
    :param str desc: Description of this accelerator element
    :param str system: System of this accelerator element
    :param str subsystem: Subsystem of this accelerator element
    :param str device: Device of this accelerator element
    :param str inst: Instance of this accelerator element
    """
    def __init__(self, z, length, aperture, name, desc="", system="", subsystem="", device="", dtype="", inst=""):
        super(Element, self).__init__(z, length, aperture, name, desc=desc)
        self.system = system
        self.subsystem = subsystem
        self.device = device
        self.dtype = dtype
        self.inst = inst

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        if not isinstance(system, basestring):
            raise TypeError("Element: 'system' property must be a string")
        self._system = system


    @property
    def subsystem(self):
        return self._subsystem

    @subsystem.setter
    def subsystem(self, subsystem):
        if not isinstance(subsystem, basestring):
            raise TypeError("Element: 'subsystem' property must be a string")
        self._subsystem = subsystem


    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device):
        if not isinstance(device, basestring):
            raise TypeError("Element: 'device' property must be a string")
        self._device = device


    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        if not isinstance(dtype, basestring):
            raise TypeError("Element: 'dtype' property must be a string")
        self._dtype = dtype


    def __str__(self):
        s = "{{ name:'{elem.name}', desc:'{elem.desc}', z:{elem.z}, length:{elem.length}, aperture:{elem.aperture}, system:'{elem.system}', " + \
                "subsystem:'{elem.subsystem}', device:'{elem.device}', dtype:'{elem.dtype}', channels:{elem.channels} }}"
        return type(self).__name__ + s.format(elem=self)



class SeqElement(NamedElement):
    """
    SeqElement is a composite accelerator element containing a sequence of elements.

    :param str name: Name of this accelerator element
    :param str desc: Description of this accelerator element
    :param list elements: List of elements contained by this sequence.
    """
    def __init__(self, name="", desc="", elements=None):
        super(SeqElement, self).__init__(None, None, None, name, desc)
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


    def write(self, indent=2):
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

            # print(" "*(indent*level) + str(elem), file=file)

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

            if self._start != None and isinstance(elem, NamedElement):
                if self._start == elem.name:
                    self._start = None

            if self._end != None and isinstance(elem, NamedElement):
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

class DriftElement(BaseElement):
    """
    DriftElement represents a drift tube, drift space, bellows or other passive element.
    """
    def __init__(self, z, length, aperture, desc="drift"):
        super(DriftElement, self).__init__(z, length, aperture, desc=desc)


class ValveElement(Element):
    """
    ValveElement represents a vaccuum valve or other similar valve.
    """
    def __init__(self, z, length, aperture, name, desc="valve", system="", subsystem="", device="", dtype="", inst=""):
        super(ValveElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype, inst=inst)


class PortElement(Element):
    """
    PortElement represents a attachment point for pump or other device.
    """
    def __init__(self, z, length, aperture, name, desc="port", system="", subsystem="", device="", dtype="", inst=""):
        super(PortElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype, inst=inst)



# Diagnostic Elements

class BLMElement(Element):
    """
    BLMElement represents Beam Loss Monitor diagnostic device.
    """
    def __init__(self, z, length, aperture, name, desc="beam loss monitor", system="", subsystem="", device="", dtype="", inst=""):
        super(BLMElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype, inst=inst)


class BPMElement(Element):
    """
    BPMElement represents Beam Position Monitor diagnostic device.
    """
    def __init__(self, z, length, aperture, name, desc="beam positon monitor", system="", subsystem="", device="", dtype="", inst=""):
        super(BPMElement,self).__init__(z, length, aperture, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.hposition_read = None
        self.channels.vposition_read = None
        self.channels.phase_read = None



class BCMElement(Element):
    """
    BCMElement represents Beam Current Monitor diagnostic device.
    """
    def __init__(self, z, length, aperture, name, desc="beam current monitor", system="", subsystem="", device="", dtype="", inst=""):
        super(BCMElement,self).__init__(z, length, aperture, name, desc=desc, system=system,
                                            subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.current = None


class BLElement(Element):
    """
    BLElement represents Bunch Length Monitor diagnostic device.
    """
    def __init__(self, z, length, aperture, name, desc="bunch length monitor", system="", subsystem="", device="", dtype="", inst=""):
        super(BLElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                             subsystem=subsystem, device=device, dtype=dtype, inst="")


class PMElement(Element):
    """
    PMElement represents Beam Profile Monitor diagnostic device.
    """
    def __init__(self, z, length, aperture, name, desc="beam profile monitor", system="", subsystem="", device="", dtype="", inst=""):
        super(PMElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                             subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.hposition_read = None
        self.channels.vposition_read = None
        self.channels.hsize_read = None
        self.channels.vsize_read = None



# Magnetic Elements


class SolElement(Element):
    """
    SolenoidElement represents a solenoid magnet.
    """
    def __init__(self, z, length, aperture, name, desc="solenoid", system="", subsystem="", device="", dtype="", inst=""):
        super(SolElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.field_cset = "FIELD_CSET"
        self.channels.field_rset = "FIELD_RSET"
        self.channels.field_read = "FIELD_READ"



class SolCorrElement(SolElement):
    """
    SolenoidElement represents a solenoid magnet with correctors
    """
    def __init__(self, z, length, aperture, name, desc="solenoid w correctors", system="", subsystem="", device="", dtype="", inst=""):
        super(SolCorrElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.hkick_cset = "HKICK_CSET"
        self.channels.hkick_rset = "HKICK_RSET"
        self.channels.hkick_read = "HKICK_READ"
        self.channels.vkick_cset = "VKICK_CSET"
        self.channels.vkick_rset = "VKICK_RSET"
        self.channels.vkick_read = "VKICK_READ"

class BendElement(Element):
    """
    BendElement represents a bending (dipole) magnet.
    """
    def __init__(self, z, length, aperture, name, desc="bend magnet", system="", subsystem="", device="", dtype="", inst=""):
        super(BendElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.angle = 0.0
        self.entrAngle = 0.0
        self.exitAngle = 0.0
        self.channels.field_cset = "FIELD_CSET"
        self.channels.field_rset = "FIELD_RSET"
        self.channels.field_read = "FIELD_READ"

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError("CavityElement: 'angle' property must be type a number")
        self._angle = angle


    @property
    def entrAngle(self):
        return self._entrAngle

    @entrAngle.setter
    def entrAngle(self, entrAngle):
        if not isinstance(entrAngle, (int, float)):
            raise TypeError("CavityElement: 'entrAngle' property must be type a number")
        self._entrAngle = entrAngle


    @property
    def exitAngle(self):
        return self._exitAngle

    @exitAngle.setter
    def exitAngle(self, exitAngle):
        if not isinstance(exitAngle, (int, float)):
            raise TypeError("CavityElement: 'exitAngle' property must be type a number")
        self._exitAngle = exitAngle


class CorrElement(Element):
    """
    CorrElement represents a corrector (dipole) magnet.
    """
    def __init__(self, z, length, aperture, name, desc="corrector magnet", system="", subsystem="", device="", dtype="", inst=""):
        super(CorrElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.hkick_cset = "HKICK_CSET"
        self.channels.hkick_rset = "HKICK_RSET"
        self.channels.hkick_read = "HKICK_READ"
        self.channels.vkick_cset = "VKICK_CSET"
        self.channels.vkick_rset = "VKICK_RSET"
        self.channels.vkick_read = "VKICK_READ"


class QuadElement(Element):
    """
    QuadElement represents a quadrupole magnet.
    """
    def __init__(self, z, length, aperture, name, desc="quadrupole magnet", system="", subsystem="", device="", dtype="", inst=""):
        super(QuadElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.gradient_cset = "GRADIENT_CSET"
        self.channels.gradient_rset = "GRADIENT_RSET"
        self.channels.gradient_read = "GRADIENT_READ"


class HexElement(Element):
    """
    HexElement represents a hexapole magnet.
    """
    def __init__(self, z, length, aperture, name, desc="hexapole magnet", system="", subsystem="", device="", dtype="", inst=""):
        super(HexElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.channels.field_read = "FIELD_READ"
        self.channels.field_cset = "FIELD_CSET"
        self.channels.field_rset = "FIELD_RSET"

# RF Elements

class CavityElement(Element):
    """
    CavityElement represents a RF cavity.
    """
    def __init__(self, z, length, aperture, name, desc="cavity", system="", subsystem="", device="", dtype="", inst=""):
        super(CavityElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)
        self.beta = 0.0
        self.voltage = 0.0
        self.frequency = 0.0
        self.channels.phase_cset = "PHASE_CSET"
        self.channels.phase_rset = "PHASE_RSET"
        self.channels.phase_read = "PHASE_READ"
        self.channels.amplitude_cset = "AMPLITUDE_CSET"
        self.channels.amplitude_rset = "AMPLITUDE_RSET"
        self.channels.amplitude_read = "AMPLITUDE_READ"


    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, beta):
        if not isinstance(beta, (int, float)):
            raise TypeError("CavityElement: 'beta' property must be type a number")
        self._beta = beta


    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        if not isinstance(voltage, (int, float)):
            raise TypeError("CavityElement: 'voltage' property must be type a number")
        self._voltage = voltage


    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("CavityElement: 'frequency' property must be type a number")
        self._frequency = frequency


# Charge Stripper Elements

class ChgStripElement(Element):
    """
    ChgStripElement represents a charge stripper.
    """
    def __init__(self, z, length, aperture, name, desc="charge stripper", system="", subsystem="", device="", dtype="", inst=""):
        super(ChgStripElement, self).__init__(z, length, aperture, name, desc=desc, system=system,
                                                subsystem=subsystem, device=device, dtype=dtype, inst=inst)


# Accelerator Element

class Accelerator(SeqElement):
    """
    Accelerator represents a complete particle accelerator.
    """
    def __init__(self, name, desc="accelerator", elements=None):
        super(Accelerator, self).__init__(name, desc=desc, elements=elements)

