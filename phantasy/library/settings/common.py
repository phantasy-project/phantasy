# -*- coding: utf-8 -*-

import os
import json
import csv
import logging
import numpy as np

from copy import deepcopy
from collections import OrderedDict

_LOGGER = logging.getLogger(__name__)


class Settings(OrderedDict):
    """Settings is a simple extention of :class:`OrderedDict` with
    the addition of some utility functions for use within the library.
    """
    def __init__(self, settingsPath=None):
        super(Settings, self).__init__()
        # if settingsPath is not None:
        if isinstance(settingsPath, str) and \
                os.path.isfile(settingsPath):
            with open(settingsPath, "r") as fp:
                self.readfp(fp)

    def readfp(self, fp):
        """Read settings from file-like object in JSON format.

        Parameter
        ----------
        fp :
            File-like object to read settings.
        """
        self.update(json.load(fp, object_pairs_hook=OrderedDict))

    def __deepcopy__(self, memo):
        # Due to the custom class initializer the default deepcopy
        # implementation is broken. Override it to make it work again.
        s = Settings()
        s.update(deepcopy(list(self.items()), memo))
        return s

    def write(self, filepath, indent=2):
        """Save settings into *filepath*.

        Parameters
        ----------
        filepath : str
            JSON file name.
        indent : int
            Indentation with spaces.
        """
        with open(filepath, 'w') as fp:
            json.dump(self, fp, indent=indent)


def snp2dict(snpfile):
    """Get settings of dict from .snp file exported from save&restore app.

    Parameters
    ----------
    snpfile : str
        Filename of snp file exported from save&restore app.

    Returns
    -------
    r : dict
        Dict of pairs of PV name and setpoint value.
    """
    with open(snpfile, 'r') as fp:
        csv_data = csv.reader(fp, delimiter=',', skipinitialspace=True)
        next(csv_data)
        header = next(csv_data)
        ipv, ival = header.index('PV'), header.index('VALUE')
        settings = {line[ipv]: line[ival] for line in csv_data if line}
    return settings


def get_element_settings(settings, element, **kws):
    """Get *element* field settings from *settings* dict.

    Parameters
    ----------
    settings : dict
        Key-value pairs of PV name and set values.
    element :
        CaElement object.

    Keyword Arguments
    -----------------
    only_physics : bool
        If True, only return physics settings, default is False.

    Returns
    -------
    r : dict
        Dict of `{field: field_setting}` for element.

    Note
    ----
    The way to locate element field by searching PV names depends on
    the PVs saved in the snp file, any other mapping rules should
    defined here in case not follow 'phantasy' internal Element->Field
    design rules.

    See Also
    --------
    snp2dict
    :class:`~phantasy.library.lattice.element.CaElement`
    :meth:`~phantasy.library.lattice.element.CaElement.get_settings`
    """
    only_phy = kws.get('only_physics', False)
    elem_settings = {}
    eng_flds = element.get_eng_fields()
    phy_flds = element.get_phy_fields()
    if phy_flds == []:  # for some element, no physics fields, ENG is PHY
        phy_flds = eng_flds
        only_phy = True

    for eng_f, phy_f in zip(eng_flds, phy_flds):
        phy_v = element.get_settings(phy_f, settings)

        # debug
        # print("{}, ENG: {}, PHY: {} ({})".format(element.name, eng_f, phy_f, phy_v))
        #

        if phy_v is None: phy_v = np.nan
        elem_settings.update({phy_f: phy_v})

        if not only_phy:
            eng_v = element.get_settings(eng_f, settings)
            if eng_v is None: eng_v = np.nan
            elem_settings.update({eng_f: eng_v})

        # debug
        # print("{} settings: {}".format(element.name, elem_settings))
        #
    return elem_settings


def generate_settings(snpfile, lattice, **kws):
    """Generate settings (Settings object) from .snp file. The generated
    settings are lattice-wised, so be sure the machine/segment configuration
    does have settings file for loading, typical settings file are named as
    settings.json, which could be defined in phantasy.cfg file.

    The generated settings may has both PHY and ENG fields, e.g. settings
    for solenoid should have 'I' and 'B' as keys in the returned dict.

    Parameters
    ----------
    snpfile : str
        Filename of snp file from save&restore app.
    lattice :
        Lattice object, usually created after `MachinePortal` instantiation.

    Keyword Arguments
    -----------------
    only_physics : bool
        If True, only return physics settings, default is False.

    Returns
    -------
    r :
        Settings object.

    See Also
    --------
    :class:`~phantasy.library.settings.common.Settings`
    :class:`~phantasy.library.operation.MachinePortal`
    """
    only_phy = kws.get('only_physics', False)
    settings_new = snp2dict(snpfile)
    settings = Settings()

    lat_settings = lattice.settings
    for elem in (i for i in lattice if i.name in lat_settings):
        elem_settings = {
            k: v
            for k, v in lat_settings.get(elem.name).items()
        }
        elem_settings.update(
                get_element_settings(settings_new, elem,
                                     only_physics=only_phy))
        settings.update({elem.name: elem_settings})
    return settings


def get_settings_from_element_list(elem_list, data_source='control',
                                   settings=None,
                                   field_of_interest=None,
                                   only_physics=True,
                                   **kws):
    """Get settings from a list of CaElement, for both engineering and
    physics fields (based on *only_physics* parameter). If *data_source* is
    defined as 'model', will try to pull the element field settings from
    *settings*, if not available, pull from the controls network; if
    *data_source* is defined as 'control', always pull element settings from
    controls network. The interested physics fields of elements could be
    defined by *field_of_interest*, which is a key-value pairs of element
    name and a list of interested physics fields for each element, if not
    defined, all the physics fields will be used.

    Parameters
    ----------
    elem_list : list
        List of CaElement.
    data_source : str
        'model' or 'control', get element settings from MODEL environment if
        *data_source* is 'model', otherwise get live settings from controls
        network. If is 'model', *settings* parameter is required.
    settings : Settings
        Predefined physics Settings from '.json' file which should includes
        all the elements in *elem_list*.
    field_of_interest : dict
        Dict of interested physics fields for each element type or element name,
        element name has higher priority.
    only_physics : bool
        If True, only get physics settings, otherwise, get engineering
        settings as well.

    Keyword Arguments
    -----------------
    skip_none : bool
        If set, skip field that returns None (not reachable), default is True.

    Returns
    -------
    s : Settings
        Settings object contains all the physics settings of all interested
        physics fields of input elements if only_physics is True, otherwise,
        including engineering field settings, too.

    See Also
    --------
    :class:`~phantasy.library.settings.common.Settings`
    """
    def get_phy_field_setting(elem, phy_fld, settings, data_source):
        # get the value of current physics field setting.
        phy_val = elem.current_setting(phy_fld)
        if data_source == 'model':
            m_settings = settings.get(ename, {})
            if phy_fld in m_settings:
                phy_val = m_settings[phy_fld]
        if phy_val is None:
            _LOGGER.warning("{} [{}] is not reachable.".format(elem.name, phy_fld))
        return phy_val

    _skip_none = kws.get('skip_none', True)

    if data_source == 'model' and settings is None:
        return None
    if field_of_interest is None:
        field_of_interest = {}

    s = Settings()
    for elem in elem_list:
        # elemeng name
        ename = elem.name
        etype = elem.family
        # skip diag elements
        if elem.is_diag():
            _LOGGER.debug("Skip {} [{}] for settings.".format(ename, etype))
            continue
        # field-of-interest for elem, if not defined, use all physics field
        all_phy_fields = elem.get_phy_fields()
        all_eng_fields = elem.get_eng_fields()
        if etype in field_of_interest:
            if ename in field_of_interest:
                field_list = field_of_interest[ename]
            else:
                field_list = field_of_interest[etype]
        else:
            field_list = all_phy_fields[:]

        #
        elem_settings = OrderedDict()
        phy_flds = []
        eng_flds = []
        for i, j in zip(all_phy_fields, all_eng_fields):
            if i in field_list:
                phy_flds.append(i)
                eng_flds.append(j)
        if only_physics:
            for phy_fld in phy_flds:
                # for data_source of 'model':
                # if phy_fld can find 'model' settings, get 'model' settings
                # otherwise use live settings.
                phy_val = get_phy_field_setting(elem, phy_fld, settings, data_source)
                if phy_val is None:
                    _LOGGER.warning("Skip unreachable {} [{}] for settings.".format(ename, phy_fld))
                    if _skip_none:
                        continue
                elem_settings.update([(phy_fld, phy_val)])
        else:
            for phy_fld, eng_fld in zip(phy_flds, eng_flds):
                phy_val = get_phy_field_setting(elem, phy_fld, settings, data_source)
                if phy_val is None:
                    _LOGGER.warning("Skip unreachable {} [] for settings.".format(ename, phy_fld))
                    if _skip_none:
                        continue
                eng_val = elem.convert(from_field=phy_fld, value=phy_val)
                elem_settings.update([(phy_fld, phy_val), (eng_fld, eng_val)])
        if elem_settings:
            s.update([(ename, elem_settings)])

    return s
