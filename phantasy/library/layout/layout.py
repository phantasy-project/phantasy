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

from .accel import BLMElement
from .accel import BPMElement
from .accel import BLElement
from .accel import PMElement
from .accel import BCMElement
from .accel import ColumnElement
from .accel import DriftElement
from .accel import ValveElement
from .accel import PortElement
from .accel import CavityElement
from .accel import EBendElement
from .accel import EMSElement
from .accel import EQuadElement
from .accel import ElectrodeElement
from .accel import FCElement
from .accel import HCorElement
from .accel import VCorElement
from .accel import CorElement
from .accel import SolCorElement
from .accel import SeqElement
from .accel import SolElement
from .accel import StripElement
from .accel import BendElement
from .accel import QuadElement
from .accel import SextElement
from .accel import VDElement
from .accel import SlitElement
from .accel import ChopperElement
from .accel import ApertureElement
from .accel import DumpElement
from .accel import AttenuatorElement

_LOGGER = logging.getLogger(__name__)


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

        def buildEtype(row):
            return row[header.index("type")]

        def buildElement(row, ElemType):
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

            etype = buildEtype(row)

            if etype == DriftElement.ETYPE:
                elements.append(buildElement(row, DriftElement))

            elif etype == PortElement.ETYPE:
                elements.append(buildElement(row, PortElement))

            elif etype == ValveElement.ETYPE:
                elements.append(buildElement(row, ValveElement))

            elif etype == CavityElement.ETYPE:
                elements.append(buildElement(row, CavityElement))

            elif etype == PMElement.ETYPE:
                elements.append(buildElement(row, PMElement))

            elif etype == BLElement.ETYPE:
                elements.append(buildElement(row, BLElement))

            elif etype == BLMElement.ETYPE:
                elements.append(buildElement(row, BLMElement))

            elif etype == BPMElement.ETYPE:
                elements.append(buildElement(row, BPMElement))

            elif etype == BCMElement.ETYPE:
                elements.append(buildElement(row, BCMElement))

            elif etype == FCElement.ETYPE:
                elements.append(buildElement(row, FCElement))

            elif etype == VDElement.ETYPE:
                elements.append(buildElement(row, VDElement))

            elif etype == EMSElement.ETYPE:
                elements.append(buildElement(row, EMSElement))

            elif etype == ColumnElement.ETYPE:
                elements.append(buildElement(row, ColumnElement))

            elif etype == SolElement.ETYPE:
                elements.append(buildElement(row, SolElement))

            elif etype == SolCorElement.ETYPE or etype == CorElement.ETYPE:
                if etype == SolCorElement.ETYPE:
                    elem = buildElement(row, SolCorElement)
                else:
                    elem = buildElement(row, CorElement)

                for _ in range(2):
                    row = next(csvstream)
                    etype = buildEtype(row)
                    if etype == HCorElement.ETYPE:
                        if elem.h is None:
                            elem.h = buildElement(row, HCorElement)
                        else:
                            raise RuntimeError(
                                "build_layout: HCorElement already found")
                    elif etype == VCorElement.ETYPE:
                        if elem.v is None:
                            elem.v = buildElement(row, VCorElement)
                        else:
                            raise RuntimeError(
                                "build_layout: VCorElement already found")

                elements.append(elem)

            elif etype == BendElement.ETYPE:
                elements.append(buildElement(row, BendElement))

            elif etype == QuadElement.ETYPE:
                elements.append(buildElement(row, QuadElement))

            elif etype == SextElement.ETYPE:
                elements.append(buildElement(row, SextElement))

            elif etype == EBendElement.ETYPE:
                elements.append(buildElement(row, EBendElement))

            elif etype == EQuadElement.ETYPE:
                elements.append(buildElement(row, EQuadElement))

            elif etype == StripElement.ETYPE:
                elements.append(buildElement(row, StripElement))

            elif etype == ElectrodeElement.ETYPE:
                elements.append(buildElement(row, ElectrodeElement))

            elif etype == SlitElement.ETYPE:
                elements.append(buildElement(row, SlitElement))

            elif etype == ChopperElement.ETYPE:
                elements.append(buildElement(row, ChopperElement))

            elif etype == ApertureElement.ETYPE:
                elements.append(buildElement(row, ApertureElement))

            elif etype == DumpElement.ETYPE:
                elements.append(buildElement(row, DumpElement))

            elif etype == AttenuatorElement.ETYPE:
                elements.append(buildElement(row, AttenuatorElement))

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

        def buildElemDict(element):
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
            elemdicts.append(buildElemDict(element))
            if isinstance(element, (CorElement, SolCorElement)):
                elemdicts.append(buildElemDict(element.h))
                elemdicts.append(buildElemDict(element.v))

        fixedkeys = ["name", "type", "L", "s", "apx", "apy"]

        metakeys = list(metakeys)

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

