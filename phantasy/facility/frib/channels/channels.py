# encoding: UTF-8

"""Build channels names based on FRIB naming convention.

   :author: Dylan Maxwell <maxwelld@frib.msu.edu>
   :date: 2015-06-16
"""

from collections import OrderedDict

from phantasy.library.layout import DriftElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import PMElement


_INDEX_PROPERTY = "elemIndex"
_POSITION_PROPERTY = "elemPosition"
_LENGTH_PROPERTY = "elemLength"
_MACHINE_PROPERTY = "machine"
_NAME_PROPERTY = "elemName"
_HANDLE_PROPERTY = "elemHandle"
_FIELD_PROPERTY = "elemField"
_TYPE_PROPERTY = "elemType"


def build_channels(layout, machine=None):
    """Build the channels using FRIB naming convention from the accelerator layout.

       :param layout: accelerator layout object
       :param machine: machine identifier and optional channel prefix
       :return: list of tuples of (channel, properties, tags)
    """

    if machine is None:
        machine = "LIVE"
        prefix = ""
    else:
        prefix = machine+":"

    data = []
    index = 0
    offset = None

    for elem in layout:

        index += 1

        if offset is None:
            offset = elem.z - (elem.length/2.0)

        def buildChannel(element):
            channel = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}".format(prefix,elem=element)
            props = OrderedDict()
            props[_INDEX_PROPERTY] = index
            props[_POSITION_PROPERTY] = str(element.z+(element.length/2.0)-offset)
            props[_LENGTH_PROPERTY] = str(element.length)
            props[_MACHINE_PROPERTY] = machine
            props[_NAME_PROPERTY] = element.name
            props[_HANDLE_PROPERTY] = ""
            props[_FIELD_PROPERTY] = ""
            props[_TYPE_PROPERTY] = ""
            tags = []
            tags.append("phyutil.sys."+element.system)
            tags.append("phyutil.sub."+element.subsystem)
            return channel, props, tags

        channel, props, tags = buildChannel(elem)

        if isinstance(elem, CavityElement):
            props[_TYPE_PROPERTY] = "CAV"
            props[_FIELD_PROPERTY] = elem.fields.phase
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":PHA_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":PHA_RSET", OrderedDict(props), list(tags))) 
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":PHA_RD",OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.amplitude
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":AMPL_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":AMPL_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":AMPL_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, SolCorElement):
            props[_TYPE_PROPERTY] = "SOL"
            props[_FIELD_PROPERTY] = elem.fields.field
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":B_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":B_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":B_RD", OrderedDict(props), list(tags)))

            channel, props, tags = buildChannel(elem.h)
            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_PROPERTY] = elem.h.fields.angle
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":ANG_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":ANG_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":ANG_RD", OrderedDict(props), list(tags)))
            
            channel, props, tags = buildChannel(elem.v)
            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_PROPERTY] = elem.v.fields.angle
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":ANG_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":ANG_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":ANG_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, CorElement):
            channel, props, tags = buildChannel(elem.h)
            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_PROPERTY] = elem.h.fields.angle
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":ANG_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":ANG_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":ANG_RD", OrderedDict(props), list(tags)))

            channel, props, tags = buildChannel(elem.v)
            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_PROPERTY] = elem.v.fields.angle
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":ANG_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":ANG_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":ANG_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, QuadElement):
            props[_TYPE_PROPERTY] = "QUAD"
            props[_FIELD_PROPERTY] = elem.fields.gradient
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":GRAD_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":GRAD_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":GRAD_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, BendElement):
            props[_TYPE_PROPERTY] = "BEND"
            props[_FIELD_PROPERTY] = elem.fields.field
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":B_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":B_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":B_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, SextElement):
            props[_TYPE_PROPERTY] = "SEXT"
            props[_FIELD_PROPERTY] = elem.fields.field
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel+":B_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel+":B_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":B_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, BPMElement):
            props[_TYPE_PROPERTY] = "BPM"

            props[_FIELD_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":X_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":Y_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.phase
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":PHA_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.energy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":ENG_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, PMElement):
            props[_TYPE_PROPERTY] = "PM"

            props[_FIELD_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":X_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":Y_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.xy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":XY_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":YRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_PROPERTY] = elem.fields.xyrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel+":XYRMS_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, StripElement):
            # Charge Stripper has no channels
            pass

        elif isinstance(elem, (BLMElement, BLElement, BCMElement)):
            # Diagnostic elements do not have defined channels
            pass

        elif isinstance(elem, (DriftElement,ValveElement, PortElement)):
            # Passtive elements do not have defined channels
            pass

        else:
            raise RuntimeError("read_layout: Element type '{}' not supported".format(elem.ETYPE))

    return data

