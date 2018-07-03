# -*- coding: utf-8 -*-
"""Layout Elements

The accelerator layout is composed of elements. These elements
represent the various types of accelerator devices or components.
"""

from __future__ import print_function

import sys

from phantasy.library.misc import SpecialDict

try:
    basestring
except NameError:
    basestring = str


# Base Elements
class Fields(object):
    """Fields is a simple container for element field names.

    All keyword arguments become object attributes.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __iter__(self):
        return iter(dir(self))

    def __repr__(self):
        return str(self.__dict__)


class Element(object):
    """Element is the base for the layout element class heirarchy.

    Parameters
    ----------
    z : float
        Position of this accelerator element.
    length : float
        Length of this accelerator element.
    aperture : float
        Minimum size of this accelerator element.
    name : str
        Name of this accelerator element.

    Keyword Arguments
    -----------------
    meta : dict
        Key-value pairs describing this element.
    """

    def __init__(self, z, length, aperture, name, **meta):
        self._z = z
        self._length = length
        self.aperture = aperture
        self._name = name
        self.meta = SpecialDict(meta, self)
        self.fields = Fields()

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
        if isinstance(aperture, (tuple, list)):
            if isinstance(aperture[0], (int, float)):
                self._apertureX = float(aperture[0])
            else:
                raise TypeError(
                    "Element: 'apertureX' property must be a number")
            if isinstance(aperture[1], (int, float)):
                self._apertureY = float(aperture[1])
            else:
                raise TypeError(
                    "Element: 'apertureY' property must be a number")

        elif isinstance(aperture, (int, float)):
            self._apertureX = aperture
            self._apertureY = aperture

        else:
            raise TypeError(
                "Element: 'aperture' property must be a number")

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

    def __repr__(self):
        s = "{{ name:'{elem.name}', z:{elem.z}, length:{elem.length}, " \
            "aperture:{elem.aperture}, meta={elem.meta}, " \
            "fields={elem.fields} }}"
        return type(self).__name__ + s.format(elem=self)


class SeqElement(Element):
    """SeqElement is a composite accelerator element containing a sequence
    of elements.

    Parameters
    ----------
    name : str
        Name of this accelerator element.
    desc : str
        Description of this accelerator element.
    elements : list
        List of elements contained by this sequence.
    """

    def __init__(self, name, elements=None, desc="sequence", **meta):
        super(SeqElement, self).__init__(None, None, None, name, desc=desc,
                                         **meta)
        if elements is None:
            self._elements = []
        else:
            self._elements = elements

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = list(elements)

    @property
    def z(self):
        if len(self.elements) == 0:
            raise Exception(
                "SeqElement: Z-Position undefined for empty sequence")
        return self._elements[0].z

    @z.setter
    def z(self, z):
        if z is not None:
            raise NotImplementedError("SeqElement: Setting z not implemented")

    @property
    def length(self):
        length = 0.0
        for elem in self._elements:
            length += elem.length
        return length

    @length.setter
    def length(self, length):
        if length is not None:
            raise NotImplementedError(
                "SeqElement: Setting length not implemented")

    @property
    def aperture(self):
        return min(self.apertureX, self.apertureY)

    @aperture.setter
    def aperture(self, aperture):
        if aperture is not None:
            raise NotImplementedError(
                "SeqElement: Setting aperture not implemented")

    @property
    def apertureX(self):
        apertureX = float('inf')
        for elem in self._elements:
            apertureX = min(apertureX, elem.apertureX)
        return apertureX

    @apertureX.setter
    def apertureX(self, apertureX):
        if apertureX is not None:
            raise NotImplementedError(
                "SeqElement: Setting apertureX not implemented")

    @property
    def apertureY(self):
        apertureY = float('inf')
        for elem in self._elements:
            apertureY = min(apertureY, elem.apertureY)
        return apertureY

    @apertureY.setter
    def apertureY(self, apertureY):
        if apertureY is not None:
            raise NotImplementedError(
                "SeqElement: Setting apertureY not implemented")

    def append(self, elem):
        self._elements.append(elem)

    def write(self, indent=2, stream=sys.stdout):
        level = 0
        iterators = [iter(self.elements)]

        while len(iterators) > 0:
            it = iterators[-1]
            try:
                elem = next(it)
            except StopIteration:
                del iterators[-1]
                level -= 1
                continue

            stream.write(" " * (indent * level) + str(elem) + "\n")

            if isinstance(elem, SeqElement):
                iterators.append(iter(elem.elements))
                level += 1
                continue

    def __iter__(self):
        return _SeqElementIterator(self)

    def iter(self, start=None, end=None):
        return _SeqElementIterator(self, start, end)

    def __repr__(self):
        s = "{{ name:'{elem.name}', desc:'{elem.desc}', " \
            "nelements:{nelements} }}"
        return type(self).__name__ + s.format(elem=self,
                                              nelements=len(self.elements))


class _SeqElementIterator(object):
    """Deep iterator for SeqElements.
    """

    def __init__(self, seq, start=None, end=None):
        self._iterators = [iter(seq.elements)]
        self._start = start
        self._end = end

    def __iter__(self):
        return self

    def next(self):
        while len(self._iterators) > 0:
            it = self._iterators[-1]
            try:
                elem = next(it)
            except StopIteration:
                del self._iterators[-1]
                continue

            if self._start is not None and isinstance(elem, Element):
                if self._start == elem.name:
                    self._start = None

            if self._end is not None and isinstance(elem, Element):
                if self._end == elem.name:
                    self._iterators = []
                    self._end = None

            if isinstance(elem, SeqElement):
                self._iterators.append(iter(elem))
                continue

            if self._start is None:
                return elem

        raise StopIteration()

    __next__ = next



# Passive Elements

class DriftElement(Element):
    """DriftElement represents a drift tube, drift space, bellows or other
    passive element.
    """
    ETYPE = "DRIFT"

    def __init__(self, z, length, aperture, name="DRIFT", desc="drift", **meta):
        super(DriftElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)


class ValveElement(Element):
    """ValveElement represents a vaccuum valve or other similar valve.
    """
    ETYPE = "VALVE"

    def __init__(self, z, length, aperture, name, desc="valve", **meta):
        super(ValveElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)


class PortElement(Element):
    """PortElement represents a attachment point for pump or other device.
    """
    ETYPE = "PORT"

    def __init__(self, z, length, aperture, name, desc="port", **meta):
        super(PortElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)


# Diagnostic Elements

class BLMElement(Element):
    """BLMElement represents Beam Loss Monitor diagnostic device.
    """
    ETYPE = "BLM"

    def __init__(self, z, length, aperture, name, desc="beam loss monitor",
                 **meta):
        super(BLMElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)


class BPMElement(Element):
    """BPMElement represents Beam Position Monitor diagnostic device.
    """
    ETYPE = "BPM"

    def __init__(self, z, length, aperture, name, desc="beam positon monitor",
                 **meta):
        super(BPMElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        self.fields.x = "X"
        self.fields.x_phy = "XPOS"
        self.fields.y = "Y"
        self.fields.y_phy = "YPOS"
        self.fields.phase = "PHA"
        self.fields.phase_phy = "PHASE"
        self.fields.energy = "ENG"
        self.fields.energy_phy = "ENERGY"
        self.fields.magnitude = "MAG"
        self.fields.magnitude_phy = "MAGNITUDE"


class BCMElement(Element):
    """BCMElement represents Beam Current Monitor diagnostic device.
    """
    ETYPE = "BCM"

    def __init__(self, z, length, aperture, name, desc="beam current monitor",
                 **meta):
        super(BCMElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        self.fields.current = "I"


class BLElement(Element):
    """BLElement represents Bunch Length Monitor diagnostic device.
    """

    ETYPE = "BL"

    def __init__(self, z, length, aperture, name, desc="bunch length monitor",
                 **meta):
        super(BLElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)


class PMElement(Element):
    """PMElement represents Beam Profile Monitor diagnostic device.
    """
    # 'sign' to indicate -45 or 45 position for 'XY' and 'XYRMS' field.

    ETYPE = "PM"

    def __init__(self, z, length, aperture, name, desc="beam profile monitor",
                 **meta):
        super(PMElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)
        self.fields.x = "XCEN"
        self.fields.y = "YCEN"
        self.fields.xy = "XY"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"
        self.fields.xyrms = "XYRMS"
        self.fields.cxy = "CXY"


class EMSElement(Element):
    """EMSElement represents an Emittance Scanner device.
    """

    ETYPE = "EMS"

    def __init__(self, z, length, aperture, name, desc="emittance scanner",
                 **meta):
        super(EMSElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)


class FCElement(Element):
    """FCElement represents an Faraday Cup device.
    """

    ETYPE = "FC"

    def __init__(self, z, length, aperture, name, desc="faraday cup", **meta):
        super(FCElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)


class VDElement(Element):
    """VDElement represents a Viewer Detector device.
    """

    ETYPE = "VD"

    def __init__(self, z, length, aperture, name, desc="viewer detector",
                 **meta):
        super(VDElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)


# Magnetic Elements

class SolElement(Element):
    """SolenoidElement represents a solenoid magnet.
    """

    ETYPE = "SOL"

    def __init__(self, z, length, aperture, name, desc="solenoid", **meta):
        super(SolElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        self.fields.field = "I"
        self.fields.field_phy = "B"


class SolCorElement(Element):
    """SolenoidElement represents a solenoid magnet with correctors
    """

    ETYPE = "SOLCOR"

    def __init__(self, z, length, aperture, name, desc="solenoid w correctors",
                 **meta):
        super(SolCorElement, self).__init__(z, length, aperture, name,
                                            desc=desc, **meta)
        self.fields.field = "I"
        self.fields.field_phy = "B"
        self.h = None
        self.v = None


class BendElement(Element):
    """BendElement represents a bending (dipole) magnet.
    """

    ETYPE = "BEND"

    def __init__(self, z, length, aperture, name, desc="bend magnet", **meta):
        super(BendElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        self.fields.field = "I"
        self.fields.field_phy = "B"
        self.fields.angle = "ANG"
        self.fields.exitAngle = "EXTANG"
        self.fields.entrAngle = "ENTANG"


class HCorElement(Element):
    """HCorElement represents a horizontal corrector magnet or coil.
    """

    ETYPE = "HCOR"

    def __init__(self, z, length, aperture, name,
                 desc="horiz. corrector magnet", **meta):
        super(HCorElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        self.fields.angle = "I"
        self.fields.angle_phy = "ANG"


class VCorElement(Element):
    """VCorElement represents a vertical corrector magnet or coil.
    """

    ETYPE = "VCOR"

    def __init__(self, z, length, aperture, name, desc="vert. corrector magnet",
                 **meta):
        super(VCorElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        self.fields.angle = "I"
        self.fields.angle_phy = "ANG"


class CorElement(Element):
    """CorElement represents an element with horizontal and vertical corrector
    elements.
    """

    ETYPE = "COR"

    def __init__(self, z, length, aperture, name, desc="corrector magnet",
                 **meta):
        super(CorElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        self.h = None
        self.v = None


class QuadElement(Element):
    """QuadElement represents a quadrupole magnet.
    """

    ETYPE = "QUAD"

    def __init__(self, z, length, aperture, name, desc="quadrupole magnet",
                 **meta):
        super(QuadElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        self.fields.gradient = "I"
        self.fields.gradient_phy = "GRAD"


class SextElement(Element):
    """SectElement represents a sextapole magnet.
    """

    ETYPE = "SEXT"

    def __init__(self, z, length, aperture, name, desc="hexapole magnet",
                 **meta):
        super(SextElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        self.fields.field = "I"
        self.fields.field_phy = "B3"


# Electrostatic Elements

class EBendElement(Element):
    """EBendElement represents an electrostatic bending element.
    """

    ETYPE = "EBEND"

    def __init__(self, z, length, aperture, name, desc="ebend", **meta):
        super(EBendElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)
        self.fields.field = "V"
        self.fields.field_phy = "V"


class EQuadElement(Element):
    """EQuadElement represents and electrostatic quadrupole element.
    """

    ETYPE = "EQUAD"

    def __init__(self, z, length, aperture, name, desc="equad", **meta):
        super(EQuadElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)
        self.fields.gradient = "V"
        self.fields.gradient_phy = "V"


# Accelerating Elements

class CavityElement(Element):
    """CavityElement represents a RF cavity.
    """

    ETYPE = "CAV"

    def __init__(self, z, length, aperture, name, desc="cavity", **meta):
        super(CavityElement, self).__init__(z, length, aperture, name,
                                            desc=desc, **meta)
        self.fields.phase = "PHA"
        self.fields.phase_phy = "PHASE"
        self.fields.amplitude = "AMP"
        self.fields.amplitude_phy = "AMPLITUDE"
        self.fields.frequency = "FREQ"


class ColumnElement(Element):
    """ColumnElement represents an DC column.
    """

    ETYPE = "COL"

    def __init__(self, z, length, aperture, name, desc="column", **meta):
        super(ColumnElement, self).__init__(z, length, aperture, name,
                                            desc=desc, **meta)


# Charge Stripper Elements

class StripElement(Element):
    """StripElement represents a charge stripper.
    """

    ETYPE = "STRIP"

    def __init__(self, z, length, aperture, name, desc="charge stripper",
                 **meta):
        super(StripElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)


# Slit Elements

class SlitElement(Element):
    """SlitElement represents a slit/collimator.
    """

    ETYPE = "SLT"

    def __init__(self, z, length, aperture, name, desc="slit",
                 **meta):
        super(SlitElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)


# Chopper Elements

class ChopperElement(Element):
    """ChopperElement represents a chopper.
    """

    ETYPE = "CHP"

    def __init__(self, z, length, aperture, name, desc="chopper",
                 **meta):
        super(ChopperElement, self).__init__(z, length, aperture, name,
                                             desc=desc,
                                             **meta)


# Attenuator Elements

class AttenuatorElement(Element):
    """AttenuatorElement represents an attenuator.
    """

    ETYPE = "ATT"

    def __init__(self, z, length, aperture, name, desc="attenuator",
                 **meta):
        super(AttenuatorElement, self).__init__(z, length, aperture, name,
                                                desc=desc,
                                                **meta)


# Dump Elements

class DumpElement(Element):
    """DumpElement represents a dump.
    """

    ETYPE = "DUMP"

    def __init__(self, z, length, aperture, name, desc="dump",
                 **meta):
        super(DumpElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)


# Aperture Elements

class ApertureElement(Element):
    """ApertureElement represents an aperture.
    """

    ETYPE = "AP"

    def __init__(self, z, length, aperture, name, desc="aperture",
                 **meta):
        super(ApertureElement, self).__init__(z, length, aperture, name,
                                              desc=desc,
                                              **meta)


# Source Elements

class ElectrodeElement(Element):
    """ElectrodeElement represents an source electrode.
    """

    ETYPE = "ELCD"

    def __init__(self, z, length, aperture, name, desc="electrode", **meta):
        super(ElectrodeElement, self).__init__(z, length, aperture, name,
                                               desc=desc, **meta)


# Accelerator Element

class Accelerator(SeqElement):
    """Accelerator represents a complete particle accelerator.
    """

    def __init__(self, name, desc="accelerator", elements=None):
        super(Accelerator, self).__init__(name, desc=desc, elements=elements)
