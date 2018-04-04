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
            with open(settingsPath, "rb") as fp:
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
    f = open(snpfile, 'rb')
    csv_data = csv.reader(f, delimiter=',', skipinitialspace=True)
    csv_data.next()
    header = csv_data.next()
    ipv, ival = header.index('PV'), header.index('VALUE')
    settings = {line[ipv]: line[ival] for line in csv_data if line}
    f.close()
    return settings


def get_setting(settings, element):
    """Get *element* field settings from *settings*.

    Parameters
    ----------
    settings : dict
        Dict contains key-values of PV name and set values.
    element :
        CaElement object.

    Returns
    -------
    r : dict
        Dict of `{field: field_setting}` for element.

    See Also
    --------
    snp2dict
    :class:`~phantasy.library.lattice.element.CaElement`
    """
    elem_setting = {}
    for f in element.fields:
        # mag_pv = "{}:{}_CSET".format(element.name, f) # engineering dynamic field, I/V
        # if mag_pv in settings:
        #     elem_setting.update({f: float(settings[mag_pv])})
        # else: # search by PS PVs
        # FRIB rule
        pv = element.pv(handle='setpoint')[-1]
        if pv in settings:
            elem_setting.update({f: float(settings[pv])})
        return elem_setting


def generate_settings(snpfile, lattice):
    """Generate settings (Settings object) from .snp file.

    Parameters
    ----------
    snpfile : str
        Filename of snp file from save&restore app.
    lattice :
        Lattice object, usually created after `MachinePortal` instantiation.

    Returns
    -------
    r :
        Settings object.

    See Also
    --------
    :class:`~phantasy.library.settings.common.Settings`
    """
    settings_new = snp2dict(snpfile)
    settings = Settings()
    for elem in (i for i in lattice if i.name in lattice.settings):
        elem_settings = {
            k: v
            for k, v in lattice.settings.get(elem.name).items()
        }
        elem_settings.update(get_setting(settings_new, elem))
        settings.update({elem.name: elem_settings})
    return settings
