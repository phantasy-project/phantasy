# -*- coding: utf-8 -*-

import json
import csv

from copy import deepcopy
from collections import OrderedDict

try:
    basestring
except:
    basestring = str


class Settings(OrderedDict):
    """Settings is a simple extention of :class:`OrderedDict` with
    the addition of some utility functions for use within the library.
    """
    def __init__(self, settingsPath=None):
        super(Settings, self).__init__()
        # if settingsPath is not None:
        if isinstance(settingsPath, basestring):
            with open(settingsPath, "r") as fp:
                self.readfp(fp)

    def readfp(self, fp):
        """Read settings from file-like object in JSON format.

        Parameters
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
        Filename of snp file from save&restore app.

    Returns
    -------
    r : dict
        Dict of PV names and setpoint values.
    """
    with open(snpfile, 'r') as fp:
        csv_data = csv.reader(fp, delimiter=',', skipinitialspace=True)
        next(csv_data)
        header = next(csv_data)
        ipv, ival = header.index('PV'), header.index('VALUE')
        settings = {line[ipv]: line[ival] for line in csv_data if line}
    return settings


def get_element_settings(settings, element, **kws):
    """Get *element* field settings from *settings*.

    Parameters
    ----------
    settings : dict
        Dict contains key-values of PV name and set values.
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

    See Also
    --------
    snp2dict
    :class:`~phantasy.library.lattice.element.CaElement`
    :meth:`~phantasy.library.lattice.eleemnt.CaElement.get_settings`
    """
    only_phy = kws.get('only_physics', False)
    elem_settings = {}
    eng_flds = element.get_eng_fields()
    phy_flds = element.get_phy_fields()
    if phy_flds == []:  # for some element, no physics fields, the eng if phy
        phy_flds = eng_flds
        only_phy = True

    for eng_f, phy_f in zip(eng_flds, phy_flds):
        phy_v = element.get_settings(phy_f, settings)
        if phy_v is None:
            continue
        else:
            elem_settings.update({phy_f: phy_v})

        if not only_phy:
            eng_v = element.get_settings(eng_f, settings)
            elem_settings.update({eng_f: eng_v})

    return elem_settings


def generate_settings(snpfile, lattice, **kws):
    """Generate settings (Settings object) from .snp file.
    ##
    # The generated settings may has both PHY and ENG fields, e.g. settings
    # for solenoid should have 'I' and 'B' as keys in the returned dict.
    ##

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
