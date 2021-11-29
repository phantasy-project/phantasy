# -*- coding: utf-8 -*-
"""Layout Elements

The accelerator layout is composed of elements. These elements
represent the various types of accelerator devices or components.
"""

import sys
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

from phantasy.library.misc import SpecialDict
from .style import get_style
from .field_map import get_field_map


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


# Base Elements
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
    ETYPE = 'DEFAULT'
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')

    def __init__(self, z, length, aperture, name, **meta):
        self._z = z
        self._length = length
        self.aperture = aperture
        self._name = name
        self._alignment_data = None
        self.meta = SpecialDict(meta, self)
        self.fields = Fields()

    @property
    def alignment(self):
        """Alignment Series.
        """
        return self._alignment_data

    @alignment.setter
    def alignment(self, o):
        self._alignment_data = o

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
        if not isinstance(name, str):
            raise TypeError("Element: 'name' property must be a string")
        if len(name) == 0:
            raise ValueError("Element: 'name' property must not be empty")
        self._name = name

    def __repr__(self):
        s = "{{ name:'{elem.name}', z:{elem.z}, length:{elem.length}, " \
            "aperture:{elem.aperture}, meta={elem.meta}, " \
            "fields={elem.fields} }}"
        return type(self).__name__ + s.format(elem=self)

    def __eq__(self, other):
        # except fields
        attr_list = ['z', 'length', 'aperture', 'name'] + list(self.meta.keys())
        for k in attr_list:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        """Define the artist drawing representation.

        Parameters
        ----------
        p0 : tuple
            The starting drawing point at coord (x, y).
        angle : float
            Rotation angle in degree.
        mode : str
            Artist representation mode, 'plain' or 'fancy'.
        """
        # --p0-----p1---

        l = self.length
        s = self.z
        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0
        # plain viz
        x1, y1 = x0 + l, y0 + l * np.tan(angle / 180 * np.pi)
        vs = ((x0, y0), (x1, y1))
        cs = ((Path.MOVETO, Path.LINETO))
        pth = Path(vs, cs)
        patch = patches.PathPatch(pth, lw=self._lw, ls=self._ls,
                                  fc=self._fc, ec=self._ec,
                                  alpha=self._alpha)
        self._next_p0 = x1, y1
        self._next_dtheta = 0
        self._artist = patch
        pc = s, (y0 + y1) * 0.5
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


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

    Examples
    --------
    >>> a = SeqElement(elements)
    >>> a[<element_name>]
    >>> a[0]
    """

    def __init__(self, name, elements=None, desc="sequence", **meta):
        super(SeqElement, self).__init__(None, None, None, name, desc=desc,
                                         **meta)
        self._elements_dict = {}
        if elements is None:
            self._elements = []
        else:
            self._elements = elements
        self._elements_dict.update({o.name: o for o in self._elements})

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
        self._elements_dict.update({elem.name: elem})

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

    def __getitem__(self, i):
        if isinstance(i, str):
            return self._elements_dict.get(i, None)
        else:
            return self._elements[i]

    def __len__(self):
        return len(self._elements)

    def size(self):
        return len(self._elements)


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
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')

    def __init__(self, z, length, aperture, name="DRIFT", desc="drift", **meta):
        super(DriftElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0
        # plain viz
        x1, y1 = x0 + l, y0 + l * np.tan(angle / 180 * np.pi)
        vs = ((x0, y0), (x1, y1))
        cs = ((Path.MOVETO, Path.LINETO))
        pth = Path(vs, cs)
        patch = patches.PathPatch(pth, lw=self._lw, ls=self._ls,
                                  fc=self._fc, ec=self._ec,
                                  alpha=self._alpha)
        self._next_p0 = x1, y1
        self._next_dtheta = 0
        self._artist = patch
        pc = s, (y0 + y1) * 0.5
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}



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
    """BLMElement represents Beam Loss Monitor.
    """
    ETYPE = "BLM"

    def __init__(self, z, length, aperture, name, desc="beam loss monitor",
                 **meta):
        super(BLMElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)


class NDElement(Element):
    """NDElement represents Neutron Detector, one kind of Beam Loss Monitor.
    """
    ETYPE = "ND"

    def __init__(self, z, length, aperture, name, desc="neutron detector",
                 **meta):
        super(NDElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)
        fm_avg = get_field_map(self.ETYPE, 'AVERAGE_INTENSITY')
        self.fields.current = fm_avg['ENG']
        self.fields.current_phy = fm_avg['PHY']

        fm_evt = get_field_map(self.ETYPE, 'EVENT')
        self.fields.event = fm_evt['ENG']
        self.fields.event_phy = fm_evt['PHY']

        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        fm = get_field_map(self.ETYPE, 'BIAS_VOLTAGE')
        self.fields.bias_voltage = fm['ENG']
        self.fields.bias_voltage_phy = fm['PHY']


class ICElement(Element):
    """ICElement represents Ion Chamber, one kind of Beam Loss Monitor.
    """
    ETYPE = "IC"

    def __init__(self, z, length, aperture, name, desc="Ion Chamber",
                 **meta):
        super(ICElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)
        fm_avg = get_field_map(self.ETYPE, 'AVERAGE_INTENSITY')
        self.fields.current = fm_avg['ENG']
        self.fields.current_phy = fm_avg['PHY']

        fm_dose = get_field_map(self.ETYPE, 'DOSE_INTENSITY')
        self.fields.dose = fm_dose['ENG']
        self.fields.dose_phy = fm_dose['PHY']

        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        fm = get_field_map(self.ETYPE, 'BIAS_VOLTAGE')
        self.fields.bias_voltage = fm['ENG']
        self.fields.bias_voltage_phy = fm['PHY']


class BPMElement(Element):
    """BPMElement represents Beam Position Monitor diagnostic device.
    """
    ETYPE = "BPM"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="beam positon monitor",
                 **meta):
        super(BPMElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        fm_x = get_field_map(self.ETYPE, 'X')
        fm_y = get_field_map(self.ETYPE, 'Y')
        fm_phase = get_field_map(self.ETYPE, 'PHASE')
        fm_magnitude = get_field_map(self.ETYPE, 'MAGNITUDE')
        fm_energy = get_field_map(self.ETYPE, 'ENERGY')
        self.fields.x = fm_x['ENG']
        self.fields.x_phy = fm_x['PHY']
        self.fields.y = fm_y['ENG']
        self.fields.y_phy = fm_y['PHY']
        self.fields.phase = fm_phase['ENG']
        self.fields.phase_phy = fm_phase['PHY']
        self.fields.magnitude = fm_magnitude['ENG']
        self.fields.magnitude_phy = fm_magnitude['PHY']
        # only for VA
        self.fields.energy = fm_energy['ENG']
        self.fields.energy_phy = fm_energy['PHY']

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        h = self._h * 0.5
        #
        #     p2
        #     |
        # -p1-p0-p3-
        #     |
        #     p4
        #
        x0, y0 = s, 0
        x1, y1 = s - h * 0.5, y0
        x2, y2 = x0, y0 + h
        x3, y3 = x0 + h * 0.5, y0
        x4, y4 = x0, y0 - h
        vs = ((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1))
        cs = (Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY)
        pth = Path(vs, cs)
        patch = patches.PathPatch(pth, lw=self._lw, ls=self._ls,
                                  fc=self._fc, ec=self._ec,
                                  alpha=self._alpha)
        self._next_p0 = x0, y0
        self._next_dtheta = 0
        self._artist = patch
        pc = x0, y0
        self._anote = {'xypos': pc, 'textpc': pc, 'name': self.name,
                       'type': self.ETYPE}


class MarkerElement(Element):
    """MarkerElement represents generic diagnostic device.
    """
    ETYPE = "MK"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="general diagnostic marker",
                 **meta):
        super(MarkerElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        h = self._h * 0.5
        #
        #     p2
        #     |
        # -p1-p0-p3-
        #     |
        #     p4
        #
        x0, y0 = s, 0
        x1, y1 = s - h * 0.5, y0
        x2, y2 = x0, y0 + h
        x3, y3 = x0 + h * 0.5, y0
        x4, y4 = x0, y0 - h
        vs = ((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1))
        cs = (Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY)
        pth = Path(vs, cs)
        patch = patches.PathPatch(pth, lw=self._lw, ls=self._ls,
                                  fc=self._fc, ec=self._ec,
                                  alpha=self._alpha)
        self._next_p0 = x0, y0
        self._next_dtheta = 0
        self._artist = patch
        pc = x0, y0
        self._anote = {'xypos': pc, 'textpc': pc, 'name': self.name,
                       'type': self.ETYPE}


class BCMElement(Element):
    """BCMElement represents Beam Current Monitor diagnostic device.
    """
    ETYPE = "BCM"

    def __init__(self, z, length, aperture, name, desc="beam current monitor",
                 **meta):
        super(BCMElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)

        fm_avg = get_field_map(self.ETYPE, 'AVERAGE_INTENSITY')
        fm_pkavg = get_field_map(self.ETYPE, 'AVERAGE_PEAK_INTENSITY')
        self.fields.current_avg = fm_avg['ENG']  # 1 Hz avg
        self.fields.current_avg_phy = fm_avg['PHY']
        self.fields.current_peak = fm_pkavg['ENG']   # peak avg
        self.fields.current_peak_phy = fm_pkavg['PHY']

class WedgeElement(Element):
    """WedgeElement represents wedge device.
    """
    ETYPE = "WED"

    def __init__(self, z, length, aperture, name, desc="wedge",
                 **meta):
        super(WedgeElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)

        #fm_avg = get_field_map(self.ETYPE, 'AVERAGE_INTENSITY')
        #fm_pkavg = get_field_map(self.ETYPE, 'AVERAGE_PEAK_INTENSITY')
        #self.fields.current_avg = fm_avg['ENG']  # 1 Hz avg
        #self.fields.current_avg_phy = fm_avg['PHY']
        #self.fields.current_peak = fm_pkavg['ENG']   # peak avg
        #self.fields.current_peak_phy = fm_pkavg['PHY']

        self.fields.x = "XCEN"
        self.fields.y = "YCEN"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"


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
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

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
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        fm = get_field_map(self.ETYPE, 'BIAS_VOLTAGE')
        self.fields.bias_voltage = fm['ENG']
        self.fields.bias_voltage_phy = fm['PHY']

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x4, y4 = x0, y0 - h * 0.5

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


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

        fm_int = get_field_map(self.ETYPE, 'AVERAGE_INTENSITY')
        fm_int_pk = get_field_map(self.ETYPE, 'AVERAGE_PEAK_INTENSITY')
        self.fields.intensity = fm_int['ENG']
        self.fields.intensity_phy = fm_int['PHY']
        self.fields.intensity_pk = fm_int_pk['ENG']
        self.fields.intensity_pk_phy = fm_int_pk['PHY']

        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        fm = get_field_map(self.ETYPE, 'BIAS_VOLTAGE')
        self.fields.bias_voltage = fm['ENG']
        self.fields.bias_voltage_phy = fm['PHY']

        # VA only
        self.fields.x = "XCEN"
        self.fields.y = "YCEN"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"


class HMRElement(Element):
    """HMRElement represents a halo ring device, large aperture diagnostic box.
    """

    ETYPE = "HMR"

    def __init__(self, z, length, aperture, name, desc="halo ring", **meta):
        super(HMRElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        fm_avg = get_field_map(self.ETYPE, 'AVERAGE_INTENSITY')
        self.fields.current = fm_avg['ENG']
        self.fields.current_phy = fm_avg['PHY']

        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        fm = get_field_map(self.ETYPE, 'BIAS_VOLTAGE')
        self.fields.bias_voltage = fm['ENG']
        self.fields.bias_voltage_phy = fm['PHY']


class VDElement(Element):
    """VDElement represents a Viewer Detector device.
    """

    ETYPE = "VD"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="viewer detector",
                 **meta):
        super(VDElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)

        self.fields.x = "XCEN"
        self.fields.y = "YCEN"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x4, y4 = x0, y0 - h * 0.5

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


class SDElement(Element):
    """SDElement represents a Silicon Detector device.
    """

    ETYPE = "SD"

    def __init__(self, z, length, aperture, name, desc="silicon detector",
                 **meta):
        super(SDElement, self).__init__(z, length, aperture, name, desc=desc,
                                        **meta)


# Magnetic Elements

class SolElement(Element):
    """SolenoidElement represents a solenoid magnet.
    """

    ETYPE = "SOL"

    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="solenoid", **meta):
        super(SolElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        fm = get_field_map(self.ETYPE, 'FIELD')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.field = fm['ENG']
        self.fields.field_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h
        if mode == 'plain':
            #   p1---p6---p2
            #   |         |
            # --p0   pc   p3--
            #   |         |
            #   p5---p7---p4
            if p0 is None:
                x0, y0 = s - w / 2.0, 0
            else:
                x0, y0 = p0

            x1, y1 = x0, y0 + h * 0.5
            x6, y6 = x1 + w * 0.5, y1
            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x4, y4 = x3, y0 - h * 0.5
            x7, y7 = x6, y4
            x5, y5 = x0, y4
            pc = x0 + w * 0.5, y0

            vs0 = [
                (x0, y0),
                (x1, y1),
                (x6, y6),
                (x2, y2),
                (x3, y3),
                (x4, y4),
                (x7, y7),
                (x5, y5),
                (x0, y0),
            ]
            # rot? not now
            vs = vs0
            cs = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.CLOSEPOLY,
            ]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                     alpha=self._alpha,
                                     lw=self._lw, ls=self._ls)
            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:
            pass

        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


class SolCorElement(Element):
    """SolenoidElement represents a solenoid magnet with correctors
    """

    ETYPE = "SOLCOR"

    def __init__(self, z, length, aperture, name, desc="solenoid w correctors",
                 **meta):
        super(SolCorElement, self).__init__(z, length, aperture, name,
                                            desc=desc, **meta)
        fm = get_field_map(self.ETYPE, 'FIELD')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.field = fm['ENG']
        self.fields.field_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        self.h = None
        self.v = None


class BendElement(Element):
    """BendElement represents a bending (dipole) magnet.
    """

    ETYPE = "BEND"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="bend magnet", **meta):
        super(BendElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        fm_i = get_field_map(self.ETYPE, 'FIELD')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.field = fm_i['ENG']
        self.fields.field_phy = fm_i['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']
        self.fields.angle = "ANG"
        self.fields.exitAngle = "EXTANG"
        self.fields.entrAngle = "ENTANG"

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x4, y4 = x0, y0 - h * 0.5

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


class RotElement(Element):
    """RotElement represents a rotation action on the phasespace, virtual
    only.
    """

    ETYPE = "ROT"

    def __init__(self, z, length, aperture, name,
                 desc="virtual element for ps rotation", **meta):
        super(RotElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        # self.fields.angle = "I"
        # self.fields.angle_phy = "ANG"


class HCorElement(Element):
    """HCorElement represents a horizontal corrector magnet or coil.
    """

    ETYPE = "HCOR"

    def __init__(self, z, length, aperture, name,
                 desc="horiz. corrector magnet", **meta):
        super(HCorElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        fm = get_field_map(self.ETYPE, 'ANGLE')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.angle = fm['ENG']
        self.fields.angle_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']


class VCorElement(Element):
    """VCorElement represents a vertical corrector magnet or coil.
    """

    ETYPE = "VCOR"

    def __init__(self, z, length, aperture, name, desc="vert. corrector magnet",
                 **meta):
        super(VCorElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        fm = get_field_map(self.ETYPE, 'ANGLE')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.angle = fm['ENG']
        self.fields.angle_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']


class CorElement(Element):
    """CorElement represents an element with horizontal and vertical corrector
    elements.
    """

    ETYPE = "COR"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="corrector magnet",
                 **meta):
        super(CorElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        self.h = None
        self.v = None

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        h = self._h * 0.5
        #
        #   p1
        #   |
        # --p0--
        #   |
        #   p2
        #
        x0, y0 = s, 0
        x1, y1 = x0 + l/2.0, h
        x2, y2 = x0 - l/2.0, -h
        vs = ((x1, y1), (x2, y2))
        cs = ((Path.MOVETO, Path.LINETO))
        pth = Path(vs, cs)
        patch = patches.PathPatch(pth, lw=self._lw, ls=self._ls,
                                fc=self._fc, ec=self._ec,
                                alpha=self._alpha)
        self._next_p0 = x0, y0
        self._next_dtheta = 0
        self._artist = patch
        pc = x0, y0
        self._anote = {'xypos': pc, 'textpc': pc, 'name': self.name,
                       'type': self.ETYPE}


class QuadElement(Element):
    """QuadElement represents a quadrupole magnet.
    """

    ETYPE = "QUAD"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="quadrupole magnet",
                 **meta):
        super(QuadElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        fm = get_field_map(self.ETYPE, 'GRADIENT')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.gradient = fm['ENG']
        self.fields.gradient_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']

        self._hv = 'H'
        if 'V' in self.name:
            self._hv = 'V'

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            # _kval >= 0: 'H' in name
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            # _kval < 0: 'V' in name
            #
            #    p4---p5
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p1---p2

            if self._hv == 'H':
                x1, y1 = x0, y0 + h * 0.5 # 0.9
                x4, y4 = x0, y0 - h * 0.5 # 0.1
            else:
                x1, y1 = x0, y0 - h * 0.5 # 0.9
                x4, y4 = x0, y0 + h * 0.5 # 0.1

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            #cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
            #      Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            cs = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


class SextElement(Element):
    """SextElement represents a sextapole magnet.
    """

    ETYPE = "SEXT"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="hexapole magnet",
                 **meta):
        super(SextElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)
        fm = get_field_map(self.ETYPE, 'FIELD')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.field = fm['ENG']
        self.fields.field_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x4, y4 = x0, y0 - h * 0.5

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


class OctElement(Element):
    """OctElement represents a octopole magnet.
    """

    ETYPE = "OCT"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="octopole magnet",
                 **meta):
        super(OctElement, self).__init__(z, length, aperture, name, desc=desc,
                                         **meta)
        fm = get_field_map(self.ETYPE, 'FIELD')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.field = fm['ENG']
        self.fields.field_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x4, y4 = x0, y0 - h * 0.5

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


# Electrostatic Elements

class EBendElement(Element):
    """EBendElement represents an electrostatic bending element.
    """

    ETYPE = "EBEND"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="ebend", **meta):
        super(EBendElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)
        fm = get_field_map(self.ETYPE, 'FIELD')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.field = fm['ENG']
        self.fields.field_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h
        if mode == 'plain':
            #   p1---p6---p2
            #   |         |
            # --p0   pc   p3--
            #   |         |
            #   p5---p7---p4
            if p0 is None:
                x0, y0 = s - w / 2.0, 0
            else:
                x0, y0 = p0

            x1, y1 = x0, y0 + h * 0.5
            x6, y6 = x1 + w * 0.5, y1
            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x4, y4 = x3, y0 - h * 0.5
            x7, y7 = x6, y4
            x5, y5 = x0, y4
            pc = x0 + w * 0.5, y0

            vs0 = [
                (x0, y0),
                (x1, y1),
                (x6, y6),
                (x2, y2),
                (x3, y3),
                (x4, y4),
                (x7, y7),
                (x5, y5),
                (x0, y0),
            ]
            # rot? not now
            vs = vs0
            cs = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.CLOSEPOLY,
            ]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                     alpha=self._alpha,
                                     lw=self._lw, ls=self._ls)
            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:
            pass

        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


class EQuadElement(Element):
    """EQuadElement represents and electrostatic quadrupole element.
    """

    ETYPE = "EQUAD"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="equad", **meta):
        super(EQuadElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)
        fm = get_field_map(self.ETYPE, 'GRADIENT')
        fm_pwr = get_field_map(self.ETYPE, 'POWER_STATUS')
        self.fields.gradient = fm['ENG']
        self.fields.gradient_phy = fm['PHY']
        self.fields.power_status = fm_pwr['ENG']
        self.fields.power_status_phy = fm_pwr['PHY']

        self._hv = 'H'
        if 'V' in self.name:
            self._hv = 'V'

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5
        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            # _kval >= 0: 'H' in name
            #
            #    p1---p2
            #    |    |
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            # _kval < 0: 'V' in name
            #
            #    p4---p5
            #    |    |
            # ---p0---p3---
            #    |    |
            #    |    |
            #    p1---p2

            if self._hv == 'H':
                x1, y1 = x0, y0 + h * 0.8
                x4, y4 = x0, y0 - h * 0.2
            else:
                x1, y1 = x0, y0 - h * 0.8
                x4, y4 = x0, y0 + h * 0.2

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}



# Accelerating Elements

class CavityElement(Element):
    """CavityElement represents a RF cavity.
    """

    ETYPE = "CAV"

    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="cavity", **meta):
        super(CavityElement, self).__init__(z, length, aperture, name,
                                            desc=desc, **meta)
        fm_phase = get_field_map(self.ETYPE, 'PHASE')
        fm_amplitude = get_field_map(self.ETYPE, 'AMPLITUDE')
        fm_phase_crest = get_field_map(self.ETYPE, 'PHASE_CREST')
        fm_amplitude_coef = get_field_map(self.ETYPE, 'AMPLITUDE_COEF')
        fm_lk = get_field_map(self.ETYPE, 'LOCK_STATUS')
        fm_itlk = get_field_map(self.ETYPE, 'INTERLOCK_STATUS')
        self.fields.phase = fm_phase['ENG']
        self.fields.phase_phy = fm_phase['PHY']
        self.fields.amplitude = fm_amplitude['ENG']
        self.fields.amplitude_phy = fm_amplitude['PHY']
        self.fields.phase_crest = fm_phase_crest['ENG']
        self.fields.phase_crest_phy = fm_phase_crest['PHY']
        self.fields.amplitude_coef = fm_amplitude_coef['ENG']
        self.fields.amplitude_coef_phy = fm_amplitude_coef['PHY']
        self.fields.lock_status = fm_lk['ENG']
        self.fields.lock_status_phy = fm_lk['PHY']
        self.fields.interlock_status = fm_itlk['ENG']
        self.fields.interlock_status_phy = fm_itlk['PHY']
        self.fields.frequency = "FREQ"

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        if l == 0.0:
            return
        s = self.z
        w = l
        h = self._h
        if mode == 'plain':
            #   p1---p6---p2
            #   |         |
            # --p0   pc   p3--
            #   |         |
            #   p5---p7---p4
            if p0 is None:
                x0, y0 = s - w / 2.0, 0
            else:
                x0, y0 = p0

            x1, y1 = x0, y0 + h * 0.5
            x6, y6 = x1 + w * 0.5, y1
            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x4, y4 = x3, y0 - h * 0.5
            x7, y7 = x6, y4
            x5, y5 = x0, y4
            pc = x0 + w * 0.5, y0

            vs0 = [
                (x0, y0),
                (x1, y1),
                (x6, y6),
                (x2, y2),
                (x3, y3),
                (x4, y4),
                (x7, y7),
                (x5, y5),
                (x0, y0),
            ]
            # rot? not now
            vs = vs0
            cs = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.CLOSEPOLY,
            ]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                     alpha=self._alpha,
                                     lw=self._lw, ls=self._ls)
            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:
            pass

        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


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


# Foil element
class FoilElement(Element):
    """FoilElement represents a foil, an emittance spoiler.
    """

    ETYPE = "FOIL"

    def __init__(self, z, length, aperture, name, desc="foil",
                 **meta):
        super(FoilElement, self).__init__(z, length, aperture, name, desc=desc,
                                           **meta)

# Slit Elements

class SlitElement(Element):
    """SlitElement represents a slit.
    """

    ETYPE = "SLT"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="slit",
                 **meta):
        super(SlitElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5
        vgap = h * 0.2


        if p0 is None:
            x0, y0 = s - l / 2.0, vgap
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            #    p0---p3
            #    (vgap)
            # -------------
            #    (vgap)
            #    p7---p4
            #    |    |
            #    p6---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0

            x4, y4 = x3, y3 - 2 * vgap
            x5, y5 = x4, y4 - h * 0.5
            x6, y6 = x0, y5
            x7, y7 = x6, y6 + h * 0.5

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0),
                  (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x4, y4)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY,
                  Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, 0.5 * (y3 + y4)
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0 - vgap
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}



# Collimator Elements

class CollimatorElement(Element):
    """CollimatorElement represents a collimator.
    """

    ETYPE = "CLLM"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="collimator",
                 **meta):
        super(CollimatorElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5
        vgap = h * 0.1


        if p0 is None:
            x0, y0 = s - l / 2.0, vgap
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            #    p0---p3
            #    (vgap)
            # -------------
            #    (vgap)
            #    p7---p4
            #    |    |
            #    p6---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0

            x4, y4 = x3, y3 - 2 * vgap
            x5, y5 = x4, y4 - h * 0.5
            x6, y6 = x0, y5
            x7, y7 = x6, y6 + h * 0.5

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0),
                  (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x4, y4)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY,
                  Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, 0.5 * (y3 + y4)
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0 - vgap
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


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


# Taget

class TargetElement(Element):
    """TargetElement represents a target, where primary beam hit on.
    """

    ETYPE = "PTA"
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="target",
                 **meta):
        super(TargetElement, self).__init__(z, length, aperture, name, desc=desc,
                                            **meta)

        self.fields.x = "XCEN"
        self.fields.y = "YCEN"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5

        if p0 is None:
            x0, y0 = s - l / 2.0, 0
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            # ---p0---p3---
            #    |    |
            #    p4---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x4, y4 = x0, y0 - h * 0.5

            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0
            x5, y5 = x3, y4

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x5, y5), (x4, y4), (x0, y0)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, y3
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}


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
    _ls = get_style(ETYPE, 'ls')
    _lw = get_style(ETYPE, 'lw')
    _alpha = get_style(ETYPE, 'alpha')
    _fc = get_style(ETYPE, 'fc')
    _ec = get_style(ETYPE, 'ec')
    _h = get_style(ETYPE, 'h')

    def __init__(self, z, length, aperture, name, desc="dump",
                 **meta):
        super(DumpElement, self).__init__(z, length, aperture, name, desc=desc,
                                          **meta)

        self.fields.x = "XCEN"
        self.fields.y = "YCEN"
        self.fields.xrms = "XRMS"
        self.fields.yrms = "YRMS"

    def set_drawing(self, p0=None, angle=0, mode='plain'):
        l = self.length
        s = self.z
        w = l
        h = self._h * 0.5
        vgap = h * 0.2


        if p0 is None:
            x0, y0 = s - l / 2.0, vgap
        else:
            x0, y0 = p0

        if mode == 'plain':
            #
            #    p1---p2
            #    |    |
            #    p0---p3
            #   (vgap |
            # --------p8-----
            #   (vgap |
            #    p7---p4
            #    |    |
            #    p6---p5
            #
            x1, y1 = x0, y0 + h * 0.5
            x2, y2 = x0 + w, y1
            x3, y3 = x2, y0

            x4, y4 = x3, y3 - 2 * vgap
            x5, y5 = x4, y4 - h * 0.5
            x6, y6 = x0, y5
            x7, y7 = x6, y6 + h * 0.5
            x8, y8 = x3, 0.5 * (y3 + y4)

            vs = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0),
                  (x3, y3), (x8, y8), (x4, y4), (x7, y7), (x6, y6), (x5, y5), (x4, y4)]
            cs = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY,
                  Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            pth = Path(vs, cs)
            patch = patches.PathPatch(pth, fc=self._fc, ec=self._ec,
                                      alpha=self._alpha, lw=self._lw,
                                      ls=self._ls)

            self._artist = patch
            self._next_p0 = x3, 0.5 * (y3 + y4)
            self._next_dtheta = 0
        else:  # fancy mode
            pass
        pc = x0 + 0.5 * w, y0 - vgap
        self._anote = {'xypos': pc, 'textpos': pc,
                       'name': self.name, 'type': self.ETYPE}




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

class SourceElement(Element):
    """Beam source.
    """

    ETYPE = "SOURCE"

    def __init__(self, z, length, aperture, name, desc="beam source", **meta):
        super(SourceElement, self).__init__(z, length, aperture, name,
                                            desc=desc, **meta)


class ElectrodeElement(Element):
    """ElectrodeElement represents an source electrode.
    """

    ETYPE = "ELCD"

    def __init__(self, z, length, aperture, name, desc="electrode", **meta):
        super(ElectrodeElement, self).__init__(z, length, aperture, name,
                                               desc=desc, **meta)


class ELDElement(Element):
    """ELDElement represents an energy loss detector.
    """

    ETYPE = "ELD"

    def __init__(self, z, length, aperture, name, desc="energy loss detector", **meta):
        super(ELDElement, self).__init__(z, length, aperture, name,
                                         desc=desc, **meta)


# Accelerator Element

class Accelerator(SeqElement):
    """Accelerator represents a complete particle accelerator.
    """

    def __init__(self, name, desc="accelerator", elements=None):
        super(Accelerator, self).__init__(name, desc=desc, elements=elements)
