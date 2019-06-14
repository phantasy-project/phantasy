# -*- utf-8 -*-

"""
The Accelerator Layout is a data model developed to capture the accelerator
element positions independent of file format and/or simulation tool.
It is used as intermediate data structure when converting between formats
or generating lattice files for use with various simulation tools.

The file format used by the accelerator layout data is a simple CSV format
with mandatory columns 'name', 'type', 'L', 's', 'apx', 'apy' and then followed
by the names of optional columns:

name,type,L,s,apx,apy [, OPTIONAL COLUMN NAMES ]
ElementName,ElementType,Length,Position,ApertureX,ApertureY[, OPTIONAL COLUMN VALUES ]
[...]

For example:

name,type,L,s,apx,apy,subsystem,dtype,system,inst,device,desc
LS1_CA01:GV_D1124,VALVE,0.072,112.40799996,0.04,0.04,CA01,NONE,LS1,NONE,GV,gate valve
DRIFT,DRIFT,0.1350635,112.49540846,0.04,0.04,NONE,NONE,NONE,NONE,NONE,bellows
LS1_CA01:CAV1_D1127,CAV,0.24,112.69906346,0.034,0.034,CA01,CAV_B04,LS1,D1127,CAV1,b04 cavity
LS1_CA01:BLM_D1128,BLM,0.0,112.78681696,0.034,0.034,CA01,NONE,LS1,NONE,BLM,outside loss monitor
DRIFT,DRIFT,0.06426334,112.86731838,0.04,0.04,NONE,NONE,NONE,NONE,NONE,bellow
LS1_CA01:BPM_D1129,BPM,0.0,112.8833268,0.04,0.04,CA01,BPM6,LS1,D1129,BPM,"position monitor, BPMc"
[...]
"""

import csv
import logging
import os.path

from .accel import ApertureElement
from .accel import AttenuatorElement
from .accel import BCMElement
from .accel import BLElement
from .accel import BLMElement
from .accel import BPMElement
from .accel import BendElement
from .accel import CavityElement
from .accel import ChopperElement
from .accel import CollimatorElement
from .accel import ColumnElement
from .accel import CorElement
from .accel import DriftElement
from .accel import DumpElement
from .accel import EBendElement
from .accel import EMSElement
from .accel import EQuadElement
from .accel import ElectrodeElement
from .accel import FCElement
from .accel import HCorElement
from .accel import HMRElement
from .accel import ICElement
from .accel import NDElement
from .accel import PMElement
from .accel import PortElement
from .accel import QuadElement
from .accel import RotElement
from .accel import SDElement
from .accel import SeqElement
from .accel import SextElement
from .accel import SlitElement
from .accel import SolCorElement
from .accel import SolElement
from .accel import StripElement
from .accel import VCorElement
from .accel import VDElement
from .accel import ValveElement

_LOGGER = logging.getLogger(__name__)

ELEMENT_CLASS_LIST = (
    DriftElement, PortElement, ValveElement, CavityElement, PMElement,
    BLElement, BLMElement, NDElement, ICElement, BPMElement,
    BCMElement, FCElement,
    VDElement, SDElement, EMSElement, ColumnElement, SolElement,
    HCorElement, VCorElement, RotElement, BendElement, QuadElement,
    SextElement, EBendElement, EQuadElement, StripElement,
    ElectrodeElement, SlitElement, ChopperElement, ApertureElement,
    DumpElement, AttenuatorElement, HMRElement, CollimatorElement,
)

ELEMENT_ETYPE_DICT = {getattr(cls, 'ETYPE'): cls for cls in ELEMENT_CLASS_LIST}


def build_layout(layoutPath=None, **kwargs):
    """Build the accelerator layout from a layout data file.

    Parameters
    ----------
    layoutPath :
        Path to layout data file
    """

    if layoutPath is None:
        raise RuntimeError("build_layout: layout data file not specified")

    if not os.path.isfile(layoutPath):
        raise RuntimeError(
            "build_layout: layout data file not found: {}".format(layoutPath))

    with open(layoutPath, "r") as layoutFile:

        csvstream = csv.reader(layoutFile, delimiter=',', skipinitialspace=True)

        fixedkeys = ["name", "type", "L", "s", "apx", "apy"]

        elements = []

        header = next(csvstream)

        def build_etype(row):
            return row[header.index("type")]

        def build_element(row, ElemType):
            name = row[header.index("name")]
            length = float(row[header.index("L")])
            z = float(row[header.index("s")])
            apx = float(row[header.index("apx")])
            apy = float(row[header.index("apx")])
            meta = {}
            for idx in range(len(header)):
                if header[idx] not in fixedkeys:
                    if row[idx] != "NONE":
                        meta[header[idx]] = row[idx]
                    else:
                        meta[header[idx]] = ''
            return ElemType(z, length, (apx, apy), name, **meta)

        while True:
            try:
                row = next(csvstream)
            except StopIteration:
                break

            etype = build_etype(row)

            if etype in (SolCorElement.ETYPE, CorElement.ETYPE):
                if etype == SolCorElement.ETYPE:
                    elem = build_element(row, SolCorElement)
                else:
                    elem = build_element(row, CorElement)
                for _ in range(2):
                    row = next(csvstream)
                    etype = build_etype(row)
                    if etype == HCorElement.ETYPE:
                        if elem.h is None:
                            elem.h = build_element(row, HCorElement)
                        else:
                            raise RuntimeError(
                                "build_layout: HCorElement already found")
                    elif etype == VCorElement.ETYPE:
                        if elem.v is None:
                            elem.v = build_element(row, VCorElement)
                        else:
                            raise RuntimeError(
                                "build_layout: VCorElement already found")
                elements.append(elem)
            elif etype in ELEMENT_ETYPE_DICT:
                elements.append(build_element(row, ELEMENT_ETYPE_DICT[etype]))
            else:
                raise RuntimeError(
                    "read_layout: Element type '{}' not supported".format(etype))

    return Layout(os.path.basename(layoutPath), elements)


class Layout(SeqElement):
    """Layout represents a sequence of elements.

    Parameters
    ----------
    name : str
        Name of this element.
    elements : list
        List of elements.
    """
    def __init__(self, name, elements=None, **meta):
        super(Layout, self).__init__(name, elements=elements, **meta)

    def write(self, stream, start=None, end=None):
        """Write the layout elements to the specified output stream.

        Parameters
        ----------
        stream :
            File-like output stream.
        start :
            Name of start element.
        end :
            Name of end element.
        """

        def build_elem_dict(element):
            metakeys.update(element.meta.keys())
            elemdict = dict(element.meta)
            elemdict["name"] = element.name
            elemdict["type"] = element.ETYPE
            elemdict["L"] = element.length
            elemdict["s"] = element.z
            elemdict["apx"] = element.apertureX
            elemdict["apy"] = element.apertureY
            _LOGGER.debug("Layout: write element: %s", elemdict)
            return elemdict

        metakeys = set()
        elemdicts = []

        for element in self.iter(start, end):
            elemdicts.append(build_elem_dict(element))
            if isinstance(element, (CorElement, SolCorElement)):
                elemdicts.append(build_elem_dict(element.h))
                elemdicts.append(build_elem_dict(element.v))

        fixedkeys = ["name", "type", "L", "s", "apx", "apy"]

        metakeys = sorted(metakeys, reverse=True)

        csvstream = csv.writer(stream, delimiter=',')

        csvstream.writerow(fixedkeys + metakeys)

        for element in elemdicts:
            row = []
            for key in fixedkeys:
                row.append(str(element[key]))
            for key in metakeys:
                if key in element:
                    row.append(str(element[key]))
                else:
                    row.append("NONE")
            csvstream.writerow(row)
