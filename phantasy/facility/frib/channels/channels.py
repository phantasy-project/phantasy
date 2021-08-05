#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build channels names based on FRIB naming convention.
"""

from collections import OrderedDict

from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import EBendElement
from phantasy.library.layout import EMSElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import FCElement
from phantasy.library.layout import ICElement
from phantasy.library.layout import NDElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import VDElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import ApertureElement
from phantasy.library.layout import AttenuatorElement
from phantasy.library.layout import SlitElement
from phantasy.library.layout import DumpElement
from phantasy.library.layout import ChopperElement
from phantasy.library.layout import HMRElement
from phantasy.library.layout import CollimatorElement


_INDEX_PROPERTY = "elemIndex"
_POSITION_PROPERTY = "elemPosition"
_LENGTH_PROPERTY = "elemLength"
_MACHINE_PROPERTY = "machine"
_NAME_PROPERTY = "elemName"
_HANDLE_PROPERTY = "elemHandle"
_FIELD_PHY_PROPERTY = "elemField_phy"
_FIELD_ENG_PROPERTY = "elemField_eng"
_TYPE_PROPERTY = "elemType"

_PHYTYPE_PROPERTY = "physicsType"
_PHYNAME_PROPERTY = "physicsName"
_MISC_PROPERTY = "misc"


def build_channels(layout, machine=None, **kws):
    """Build channels using FRIB naming convention from accelerator layout.

    Parameters
    ----------
    layout :
        Accelerator layout object
    machine : str
        Machine identifier and optional channel prefix.

    Keyword Arguments
    -----------------
    start : str
        Start element.
    end : str
        End element.
    offset : float
        Longitudinal offset applied on the first element, unit: [m].

    Returns
    -------
    ret : list(tuple)
        List of tuples of (channel, properties, tags)

    See Also
    --------
    :class:`~phantasy.library.layout.Layout`
    :func:`~phantasy.library.misc.complicate_data`
    """

    if machine is None:
        machine = "LIVE"
        prefix = ""
    else:
        prefix = machine + ":"

    data = []
    index = 0
    offset = kws.get('offset', None)

    _start = kws.get('start', None)
    _end = kws.get('end', None)
    for elem in layout.iter(_start, _end):
        index += 1

        if offset is None:
            offset = elem.z - (elem.length / 2.0)

        def buildChannel(element):
            channel = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}".format(prefix, elem=element)
            props = OrderedDict()
            props[_INDEX_PROPERTY] = index
            props[_POSITION_PROPERTY] = str(element.z + (element.length / 2.0) - offset)
            props[_LENGTH_PROPERTY] = str(element.length)
            props[_MACHINE_PROPERTY] = machine
            props[_NAME_PROPERTY] = element.name
            props[_HANDLE_PROPERTY] = ""
            props[_FIELD_PHY_PROPERTY] = ""
            props[_FIELD_ENG_PROPERTY] = ""
            props[_TYPE_PROPERTY] = ""
            props[_PHYTYPE_PROPERTY] = element.dtype
            props[_PHYNAME_PROPERTY] = element.desc
            tags = []
            tags.append("phantasy.sys." + element.system)
            tags.append("phantasy.sub." + element.subsystem)
            return channel, props, tags

        channel, props, tags = buildChannel(elem)

        if isinstance(elem, CavityElement):
            props[_TYPE_PROPERTY] = "CAV"
            props[_FIELD_ENG_PROPERTY] = elem.fields.phase
            props[_FIELD_PHY_PROPERTY] = elem.fields.phase_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":PHA_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":PHA_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":PHA_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.amplitude
            props[_FIELD_PHY_PROPERTY] = elem.fields.amplitude_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":AMPL_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":AMPL_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AMPL_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, SolCorElement):
            props[_TYPE_PROPERTY] = "SOL"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            channel, props, tags = buildChannel(elem.h)
            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_ENG_PROPERTY] = elem.h.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.h.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            channel, props, tags = buildChannel(elem.v)
            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_ENG_PROPERTY] = elem.v.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.v.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, SolElement):
            props[_TYPE_PROPERTY] = "SOL"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, CorElement):
            channel, props, tags = buildChannel(elem.h)
            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_ENG_PROPERTY] = elem.h.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.h.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            channel, props, tags = buildChannel(elem.v)
            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_ENG_PROPERTY] = elem.v.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.v.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, QuadElement):
            props[_TYPE_PROPERTY] = "QUAD"
            props[_FIELD_ENG_PROPERTY] = elem.fields.gradient
            props[_FIELD_PHY_PROPERTY] = elem.fields.gradient_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, BendElement):
            props[_TYPE_PROPERTY] = "BEND"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, SextElement):
            props[_TYPE_PROPERTY] = "SEXT"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":B3_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":B3_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":B3_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, BPMElement):
            props[_TYPE_PROPERTY] = "BPM"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":X_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":Y_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.phase
            props[_FIELD_PHY_PROPERTY] = elem.fields.phase_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":PHA_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.energy
            props[_FIELD_PHY_PROPERTY] = elem.fields.energy_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ENG_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, PMElement):
            props[_TYPE_PROPERTY] = "PM"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xy
            props[_FIELD_PHY_PROPERTY] = elem.fields.xy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XY_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.cxy
            props[_FIELD_PHY_PROPERTY] = elem.fields.cxy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":CXY_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.yrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xyrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xyrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XYRMS_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, EBendElement):
            props[_TYPE_PROPERTY] = "EBEND"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":V_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":V_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":V_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, EQuadElement):
            props[_TYPE_PROPERTY] = "EQUAD"
            props[_FIELD_ENG_PROPERTY] = elem.fields.gradient
            props[_FIELD_PHY_PROPERTY] = elem.fields.gradient_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":V_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":V_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":V_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, StripElement):
            # Charge Stripper has no channels
            pass

        elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
            # Diagnostic elements do not have defined channels
            pass

        elif isinstance(elem, (DriftElement, ValveElement, PortElement)):
            # Passive elements do not have defined channels
            pass

        elif isinstance(elem, (AttenuatorElement, ApertureElement,
                               ChopperElement, DumpElement, SlitElement,
                               NDElement, ICElement)):
            # for element identification only
            pass

        elif isinstance(elem, EMSElement):
            pass

        elif isinstance(elem, VDElement):
            pass

        elif isinstance(elem, FCElement):
            pass

        elif isinstance(elem, HMRElement):
            pass

        elif isinstance(elem, CollimatorElement):
            pass

        else:
            raise RuntimeError("read_layout: Element type '{}' not supported".format(elem.ETYPE))

    return data
