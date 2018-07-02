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
        """Due to the custom class initializer the default deepcopy
		implementation is broken. Override it to make it work again.
		"""
        s = Settings()
        s.update(deepcopy(self.items(), memo))
        return s


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
    f = open(snpfile, 'r')
    csv_data = csv.reader(f, delimiter=',', skipinitialspace=True)
    csv_data.next()
    header = csv_data.next()
    ipv, ival = header.index('PV'), header.index('VALUE')
    settings = {line[ipv]: line[ival] for line in csv_data if line}
    f.close()
    return settings


def get_setting(settings, element, **kws):
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
    """
    only_phy = kws.get('only_physics', False)
    elem_setting = {}
    for f in element.get_eng_fields():
        # mag_pv = "{}:{}_CSET".format(element.name, f) # engineering dynamic field, I/V
        # if mag_pv in settings:
        #     elem_setting.update({f: float(settings[mag_pv])})
        # else: # search by PS PVs
        # FRIB rule
        pv = element.pv(handle='setpoint')[-1]
        if pv in settings:
            v = float(settings[pv])
            phy_field = element.get_phy_fields()
            if phy_field and phy_field[0] != f:
                elem_setting.update({phy_field[0]: element._unicorn_e2p(v)})
            if not only_phy:
                elem_setting.update({f: v})
    return elem_setting


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
    only_phy = kws.get('only_physics')
    settings_new = snp2dict(snpfile)
    settings = Settings()
    for elem in (i for i in lattice if i.name in lattice.settings):
        elem_settings = {
            k: v
            for k, v in lattice.settings.get(elem.name).items()
        }
        elem_settings.update(get_setting(settings_new, elem,
                                         only_physics=only_phy))
        settings.update({elem.name: elem_settings})
    return settings
