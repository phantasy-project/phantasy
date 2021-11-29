#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build channels names based on FRIB naming convention.

Reading external csv sheet for power supply PV information.
"""

from collections import OrderedDict
import csv
import logging
import re

from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import FoilElement
from phantasy.library.layout import NDElement
from phantasy.library.layout import ICElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import HCorElement
from phantasy.library.layout import VCorElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import EBendElement
from phantasy.library.layout import ElectrodeElement
from phantasy.library.layout import EMSElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import FCElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import VDElement
from phantasy.library.layout import SDElement
from phantasy.library.layout import ValveElement
from phantasy.library.layout import ApertureElement
from phantasy.library.layout import AttenuatorElement
from phantasy.library.layout import SlitElement
from phantasy.library.layout import DumpElement
from phantasy.library.layout import ChopperElement
from phantasy.library.layout import HMRElement
from phantasy.library.layout import CollimatorElement
from phantasy.library.layout import RotElement
from phantasy.library.layout import TargetElement
from phantasy.library.layout import OctElement
from phantasy.library.layout import WedgeElement
from phantasy.library.layout import ELDElement

_LOGGER = logging.getLogger(__name__)

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
_PVPOLICY_PROPERTY = 'pvPolicy'
_MISC_PROPERTY = "misc"

ETYPES_TO_SKIP = (
    ELDElement,
    FoilElement,
)  # Etypes to skip.


def build_item(row):
    """Build dict item from row configuration.

    Returns
    -------
    r : dict
        `{'element_name': {'pv_prefix', 'pv_field(I/V)', 'policy_name'}}`
    """
    e_name, ps1, ps2, ps1_sign, ps2_sign, value_sign, note = row
    r1, r2 = [re.match(".*:(.*)_.*:.*", s) for s in (ps1, ps2)]
    dev_ps = [r.group(1) for r in (r1,r2) if r is not None]
    if 'Focusing' in note:
        policy = 'EQUAD'
    elif 'bend' in note:
        policy = 'EBEND'
    else:
        policy = 'DEFAULT'
    return {e_name: (dev_ps, policy)}


def get_all_pspvs(psfile):
    with open(psfile, 'r') as f_ps:
        csv_stream = csv.reader(f_ps, delimiter=',', skipinitialspace=True)

        elem_pv_rules = {}

        try:
            header = next(csv_stream)
            for line in csv_stream:
                elem_pv_rules.update(build_item(line))
            _LOGGER.info("Loaded CSV file for power supply PV config.")
        except ValueError:
            _LOGGER.warning("Cannot load CSV file for power supply PV config.")
    return elem_pv_rules


def build_channels(layout, psfile, machine=None, **kws):
    """Build channels using FRIB naming convention from accelerator layout.

    Parameters
    ----------
    layout :
        Accelerator layout object
    psfile : str
        Name of the csv file which contains power supply PVs for each element.
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
    elem_pv_rules = get_all_pspvs(psfile)

    if machine is None:
        machine = "LIVE"
        prefix = ""
    else:
        prefix = machine + ":"

    data = []
    index = 0
    offset = kws.get('offset', None)
    # if offset is not defined,
    # the offset will be set as (z-l/2.0) of the first element.

    fmt = kws.get('fmt', '{:.6f}')

    _start = kws.get('start', None)
    _end = kws.get('end', None)
    for elem in layout.iter(_start, _end):
        index += 1

        if offset is None:
            offset = elem.z - (elem.length / 2.0)

        def buildChannel_cor(element):
            if element.ETYPE == 'HCOR':
                channel = "{}{elem.system}_{elem.subsystem}:PSC2_{elem.inst}".format(
                        prefix, elem=element)
            elif element.ETYPE == 'VCOR':
                channel = "{}{elem.system}_{elem.subsystem}:PSC1_{elem.inst}".format(
                        prefix, elem=element)

            props = OrderedDict()
            props[_INDEX_PROPERTY] = index
            props[_POSITION_PROPERTY] = fmt.format(element.z + (element.length / 2.0) - offset)
            props[_LENGTH_PROPERTY] = fmt.format(element.length)
            props[_MACHINE_PROPERTY] = machine
            props[_NAME_PROPERTY] = element.name
            props[_HANDLE_PROPERTY] = ""
            props[_FIELD_PHY_PROPERTY] = ""
            props[_FIELD_ENG_PROPERTY] = ""
            props[_TYPE_PROPERTY] = ""
            props[_PHYTYPE_PROPERTY] = element.dtype
            props[_PHYNAME_PROPERTY] = element.desc
            props[_PVPOLICY_PROPERTY] = 'DEFAULT'
            tags = []
            tags.append("phantasy.sys." + element.system)
            tags.append("phantasy.sub." + element.subsystem)
            return [channel], props, tags

        def buildChannel(element):
            if isinstance(element, CavityElement):
                channel = "{}{elem.system}_{elem.subsystem}:RFC_{elem.inst}".format(prefix, elem=element)
            elif isinstance(element, QuadElement):
                channel = "{}{elem.system}_{elem.subsystem}:PSQ_{elem.inst}".format(prefix, elem=element)
            elif isinstance(element, BendElement):
                channel = "{}{elem.system}_{elem.subsystem}:PSD_{elem.inst}".format(prefix, elem=element)
            elif isinstance(element, SolCorElement):
                channel = "{}{elem.system}_{elem.subsystem}:PSOL_{elem.inst}".format(prefix, elem=element)
            elif isinstance(element, SextElement):
                channel = "{}{elem.system}_{elem.subsystem}:PSS_{elem.inst}".format(prefix, elem=element)
            elif isinstance(element, OctElement):
                channel = "{}{elem.system}_{elem.subsystem}:PSO_{elem.inst}".format(prefix, elem=element)
            else:
                channel = "{}{elem.system}_{elem.subsystem}:{elem.device}_{elem.inst}".format(prefix, elem=element)

            props = OrderedDict()
            props[_INDEX_PROPERTY] = index
            props[_POSITION_PROPERTY] = fmt.format(element.z + (element.length / 2.0) - offset)
            props[_LENGTH_PROPERTY] = fmt.format(element.length)
            props[_MACHINE_PROPERTY] = machine
            props[_NAME_PROPERTY] = element.name
            props[_HANDLE_PROPERTY] = ""
            props[_FIELD_PHY_PROPERTY] = ""
            props[_FIELD_ENG_PROPERTY] = ""
            props[_TYPE_PROPERTY] = ""
            props[_PHYTYPE_PROPERTY] = element.dtype
            props[_PHYNAME_PROPERTY] = element.desc
            props[_PVPOLICY_PROPERTY] = 'DEFAULT'
            tags = []
            tags.append("phantasy.sys." + element.system)
            tags.append("phantasy.sub." + element.subsystem)
            return channel, props, tags

        def buildChannel_pspv(element):
            # EQUAD, E-Dipole, COR, SOL, BEND
            #
            _LOGGER.info("Building channels for {}".format(element.name))
            #
            pv_rules = elem_pv_rules.get(element.name, None)
            if pv_rules is None:
                if isinstance(element, EQuadElement):
                    raise PSPVRulesNotFoundForEQUAD
                elif isinstance(element, BendElement):
                    raise PSPVRulesNotFoundForBEND
                elif isinstance(element, EBendElement):
                    raise PSPVRulesNotFoundForEBEND
                elif isinstance(element, (HCorElement, VCorElement)):
                    raise PSPVRulesNotFoundForCOR
                elif isinstance(element, SolElement):
                    raise PSPVRulesNotFoundForSOL

            dev_ps, policy = pv_rules
            channels = []
            for i in dev_ps:
                channels.append(
                    "{}{elem.system}_{elem.subsystem}:{dev}_{elem.inst}".format(prefix, dev=i, elem=element)
                )
            props = OrderedDict()
            props[_INDEX_PROPERTY] = index
            props[_POSITION_PROPERTY] = fmt.format(element.z + (element.length / 2.0) - offset)
            props[_LENGTH_PROPERTY] = fmt.format(element.length)
            props[_MACHINE_PROPERTY] = machine
            props[_NAME_PROPERTY] = element.name
            props[_HANDLE_PROPERTY] = ""
            props[_FIELD_PHY_PROPERTY] = ""
            props[_FIELD_ENG_PROPERTY] = ""
            props[_TYPE_PROPERTY] = ""
            props[_PHYTYPE_PROPERTY] = element.dtype
            props[_PHYNAME_PROPERTY] = element.desc
            props[_PVPOLICY_PROPERTY] = policy
            tags = []
            tags.append("phantasy.sys." + element.system)
            tags.append("phantasy.sub." + element.subsystem)
            return channels, props, tags

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
            data.append((channel + ":PHA_RD_CAVS", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.phase_crest
            props[_FIELD_PHY_PROPERTY] = elem.fields.phase_crest_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel.replace('RFC', 'CAV') + ":PHA_CREST_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel.replace('RFC', 'CAV') + ":PHA_CREST_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.amplitude
            props[_FIELD_PHY_PROPERTY] = elem.fields.amplitude_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":E_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":E_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":E_RD_CAVS", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.amplitude_coef
            props[_FIELD_PHY_PROPERTY] = elem.fields.amplitude_coef_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel.replace('RFC', 'CAV') + ":E_COEF_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel.replace('RFC', 'CAV') + ":E_COEF_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.lock_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.lock_status_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":LOCK_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.interlock_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.interlock_status_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ILK_LTCH_ANY", OrderedDict(props), list(tags)))

        elif isinstance(elem, SolCorElement):
            print("SolCor: ", elem.name)
            props[_TYPE_PROPERTY] = "SOL"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

            channels, props, tags = buildChannel_cor(elem.h)
            channel = channels[0]
            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_ENG_PROPERTY] = elem.h.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.h.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.h.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.h.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

            channels, props, tags = buildChannel_cor(elem.v)
            channel = channels[0]
            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_ENG_PROPERTY] = elem.v.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.v.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.v.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.v.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, SolElement):
            try:
                channels, props, tags = buildChannel_pspv(elem)
                print("SOL (find rules): ", elem.name)
            except PSPVRulesNotFoundForSOL:
                channel, props, tags = buildChannel(elem)
                channels = (channel, )
                print("SOL (no rules): ", elem.name)

            props[_TYPE_PROPERTY] = "SOL"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readset"
                data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, HCorElement):
            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_ENG_PROPERTY] = elem.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, VCorElement):
            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_ENG_PROPERTY] = elem.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.fields.angle_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, CorElement):
            try:
                channels, props, tags = buildChannel_pspv(elem.h)
            except PSPVRulesNotFoundForCOR:
                channels, props, tags = buildChannel_cor(elem.h)

            props[_TYPE_PROPERTY] = "HCOR"
            props[_FIELD_ENG_PROPERTY] = elem.h.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.h.fields.angle_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readset"
                data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.h.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.h.fields.power_status_phy
            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

            try:
                channels, props, tags = buildChannel_pspv(elem.v)
            except PSPVRulesNotFoundForCOR:
                channels, props, tags = buildChannel_cor(elem.v)

            props[_TYPE_PROPERTY] = "VCOR"
            props[_FIELD_ENG_PROPERTY] = elem.v.fields.angle
            props[_FIELD_PHY_PROPERTY] = elem.v.fields.angle_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readset"
                data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.v.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.v.fields.power_status_phy
            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

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

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, BendElement):
            try:
                channels, props, tags = buildChannel_pspv(elem)
            except PSPVRulesNotFoundForBEND:
                channel, props, tags = buildChannel(elem)
                channels = (channel, )
            props[_TYPE_PROPERTY] = "BEND"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readset"
                data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, SextElement):
            props[_TYPE_PROPERTY] = "SEXT"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, OctElement):
            props[_TYPE_PROPERTY] = "OCT"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":I_CSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readset"
            data.append((channel + ":I_RSET", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":I_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, BPMElement):
            props[_TYPE_PROPERTY] = "BPM"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XPOS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YPOS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.phase
            props[_FIELD_PHY_PROPERTY] = elem.fields.phase_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":PHASE_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.energy
            props[_FIELD_PHY_PROPERTY] = elem.fields.energy_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":ENG_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.magnitude
            props[_FIELD_PHY_PROPERTY] = elem.fields.magnitude_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":MAG_RD", OrderedDict(props), list(tags)))

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

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:setOn", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:isOn", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.bias_voltage
            props[_FIELD_PHY_PROPERTY] = elem.fields.bias_voltage_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:VoltageSet", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:VoltageMeasure", OrderedDict(props), list(tags)))

        elif isinstance(elem, EBendElement):
            try:
                channels, props, tags = buildChannel_pspv(elem)
            except PSPVRulesNotFoundForEBEND:
                channel, props, tags = buildChannel(elem)
                channels = (channel, )
            props[_TYPE_PROPERTY] = "EBEND"
            props[_FIELD_ENG_PROPERTY] = elem.fields.field
            props[_FIELD_PHY_PROPERTY] = elem.fields.field_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":V_CSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readset"
                data.append((channel + ":V_RSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":V_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, EQuadElement):
            try:
                channels, props, tags = buildChannel_pspv(elem)
            except PSPVRulesNotFoundForEQUAD:
                channel, props, tags = buildChannel(elem)
                channels = (channel, )
            props[_TYPE_PROPERTY] = "EQUAD"
            props[_FIELD_ENG_PROPERTY] = elem.fields.gradient
            props[_FIELD_PHY_PROPERTY] = elem.fields.gradient_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":V_CSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readset"
                data.append((channel + ":V_RSET", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":V_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy

            for channel in channels:
                props[_HANDLE_PROPERTY] = "setpoint"
                data.append((channel + ":ON_CMD", OrderedDict(props), list(tags)))
                props[_HANDLE_PROPERTY] = "readback"
                data.append((channel + ":ON_RSTS", OrderedDict(props), list(tags)))

        elif isinstance(elem, StripElement):
            # Charge Stripper has no channels
            pass

        elif isinstance(elem, (BLElement, BLMElement, )):
            # Diagnostic elements do not have defined channels
            pass

        elif isinstance(elem, RotElement):
            # rotation virtual element
            pass

        elif isinstance(elem, NDElement):
            # Beam loss monitor (ND)
            props[_TYPE_PROPERTY] = "ND"

            props[_FIELD_ENG_PROPERTY] = elem.fields.current
            props[_FIELD_PHY_PROPERTY] = elem.fields.current_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AVG_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.event
            props[_FIELD_PHY_PROPERTY] = elem.fields.event_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":EVT_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.bias_voltage
            props[_FIELD_PHY_PROPERTY] = elem.fields.bias_voltage_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:VoltageSet", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:VoltageMeasure", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:setOn", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:isOn", OrderedDict(props), list(tags)))

        elif isinstance(elem, ICElement):
            # Beam loss monitor (IC)
            props[_TYPE_PROPERTY] = "IC"

            props[_FIELD_ENG_PROPERTY] = elem.fields.current
            props[_FIELD_PHY_PROPERTY] = elem.fields.current_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AVG_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.dose
            props[_FIELD_PHY_PROPERTY] = elem.fields.dose_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":DOSE_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.bias_voltage
            props[_FIELD_PHY_PROPERTY] = elem.fields.bias_voltage_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:VoltageSet", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:VoltageMeasure", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:setOn", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:isOn", OrderedDict(props), list(tags)))

        elif isinstance(elem, BCMElement):
            props[_TYPE_PROPERTY] = "BCM"

            props[_FIELD_ENG_PROPERTY] = elem.fields.current_avg
            props[_FIELD_PHY_PROPERTY] = elem.fields.current_avg_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AVG_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.current_peak
            props[_FIELD_PHY_PROPERTY] = elem.fields.current_peak_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AVGPK_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, (DriftElement, ValveElement, PortElement)):
            # Passive elements do not have defined channels
            pass

        elif isinstance(elem, (AttenuatorElement, ApertureElement,
                               ChopperElement, SlitElement)):
            # for element identification only
            pass

        elif isinstance(elem, EMSElement):
            pass

        elif isinstance(elem, HMRElement):
            # Halo ring
            props[_TYPE_PROPERTY] = "HMR"

            props[_FIELD_ENG_PROPERTY] = elem.fields.current
            props[_FIELD_PHY_PROPERTY] = elem.fields.current_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AVG_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.bias_voltage
            props[_FIELD_PHY_PROPERTY] = elem.fields.bias_voltage_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:VoltageSet", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:VoltageMeasure", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:setOn", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:isOn", OrderedDict(props), list(tags)))

        elif isinstance(elem, CollimatorElement):
            pass

        elif isinstance(elem, SDElement):
            pass

        elif isinstance(elem, VDElement):
            # viewer camera
            props[_TYPE_PROPERTY] = "VD"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.yrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YRMS_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, DumpElement):
            props[_TYPE_PROPERTY] = "DUMP"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.yrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YRMS_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, TargetElement):
            props[_TYPE_PROPERTY] = "PTA"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.yrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YRMS_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, WedgeElement):
            props[_TYPE_PROPERTY] = "WED"

            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.yrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YRMS_RD", OrderedDict(props), list(tags)))

        elif isinstance(elem, ElectrodeElement):
            pass

        elif isinstance(elem, ETYPES_TO_SKIP):
            pass

        elif isinstance(elem, FCElement):
            props[_TYPE_PROPERTY] = "FC"

            props[_FIELD_ENG_PROPERTY] = elem.fields.intensity
            props[_FIELD_PHY_PROPERTY] = elem.fields.intensity_phy
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":AVG_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.bias_voltage
            props[_FIELD_PHY_PROPERTY] = elem.fields.bias_voltage_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:VoltageSet", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:VoltageMeasure", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.power_status
            props[_FIELD_PHY_PROPERTY] = elem.fields.power_status_phy
            props[_HANDLE_PROPERTY] = "setpoint"
            data.append((channel + ":VBS:setOn", OrderedDict(props), list(tags)))
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":VBS:isOn", OrderedDict(props), list(tags)))

            # VA only
            props[_FIELD_ENG_PROPERTY] = elem.fields.x
            props[_FIELD_PHY_PROPERTY] = elem.fields.x
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.y
            props[_FIELD_PHY_PROPERTY] = elem.fields.y
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YCEN_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.xrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.xrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":XRMS_RD", OrderedDict(props), list(tags)))

            props[_FIELD_ENG_PROPERTY] = elem.fields.yrms
            props[_FIELD_PHY_PROPERTY] = elem.fields.yrms
            props[_HANDLE_PROPERTY] = "readback"
            data.append((channel + ":YRMS_RD", OrderedDict(props), list(tags)))

        else:
            raise RuntimeError("read_layout: Element type '{}' not supported".format(elem.ETYPE))

    return data


class PSPVRulesNotFoundForEQUAD(Exception):
    pass


class PSPVRulesNotFoundForEBEND(Exception):
    pass


class PSPVRulesNotFoundForBEND(Exception):
    pass


class PSPVRulesNotFoundForCOR(Exception):
    pass


class PSPVRulesNotFoundForSOL(Exception):
    pass
