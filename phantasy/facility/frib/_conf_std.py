#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Define FRIB standard machine configuration file.
"""

import os
import sys
import logging
from collections import OrderedDict


_LOGGER = logging.getLogger(__name__)

# namelist of machine configuration file, e.g. phantasy.ini
# INI_DICT is designed to be highly configurable.
INI_DICT = dict()

INI_DICT['INI_NAME'] = 'phantasy.ini'
INI_DICT['COMMON_SECTION_NAME'] = 'COMMON'
INI_DICT['KEYNAME_CONTROLS_PROTOCOL'] = 'controls_protocol'
INI_DICT['DEFAULT_CONTROLS_PROTOCOL'] = 'EPICS'

# HLA MARCOs
HLA_TAG_PREFIX = 'phantasy'
HLA_TAG_SYS_PREFIX = HLA_TAG_PREFIX + '.sys'
HLA_VFAMILY = 'HLA:VIRTUAL'

INI_DICT['HLA_TAG_PREFIX'] = HLA_TAG_PREFIX
INI_DICT['HLA_TAG_SYS_PREFIX'] = HLA_TAG_SYS_PREFIX
INI_DICT['HLA_VFAMILY'] = HLA_VFAMILY

## namelist defined in phantasy.ini

# segment and default_segment
KEYNAME_SEGMENTS = "segments"
DEFAULT_SEGMENTS = None
KEYNAME_DEFAULT_SEGMENT = "default_segment"
DEFAULT_DEFAULT_SEGMENT = None

INI_DICT['KEYNAME_SEGMENTS'] = KEYNAME_SEGMENTS
INI_DICT['DEFAULT_SEGMENTS'] = DEFAULT_SEGMENTS
INI_DICT['KEYNAME_DEFAULT_SEGMENT'] = KEYNAME_DEFAULT_SEGMENT
INI_DICT['DEFAULT_DEFAULT_SEGMENT'] = DEFAULT_DEFAULT_SEGMENT

# root directory for temp output data
KEYNAME_ROOT_DATA_DIR = 'root_data_dir'
DEFAULT_ROOT_DATA_DIR = "~/data" # sub-dir, created as date, e.g. 20170112

INI_DICT['KEYNAME_ROOT_DATA_DIR'] = KEYNAME_ROOT_DATA_DIR
INI_DICT['DEFAULT_ROOT_DATA_DIR'] = DEFAULT_ROOT_DATA_DIR

# scan server address
KEYNAME_SCAN_SVR_URL = 'ss_url'
DEFAULT_SCAN_SVR_URL = None

INI_DICT['KEYNAME_SCAN_SVR_URL'] = KEYNAME_SCAN_SVR_URL
INI_DICT['DEFAULT_SCAN_SVR_URL'] = DEFAULT_SCAN_SVR_URL

# simulating code, or model
KEYNAME_SIMULATION_CODE = 'model'
DEFAULT_SIMULATION_CODE = None

INI_DICT['KEYNAME_SIMULATION_CODE'] = KEYNAME_SIMULATION_CODE
INI_DICT['DEFAULT_SIMULATION_CODE'] = DEFAULT_SIMULATION_CODE

# model data dir, extra resources to support simulation
KEYNAME_MODEL_DATA_DIR = 'model_data_dir'
#DEFAULT_MODEL_DATA_DIR = os.path.expanduser(
#        os.path.join(DEFAULT_ROOT_DATA_DIR, 'model_data'))

INI_DICT['KEYNAME_MODEL_DATA_DIR'] = KEYNAME_MODEL_DATA_DIR
#INI_DICT['DEFAULT_MODEL_DATA_DIR'] = DEFAULT_MODEL_DATA_DIR

# config file, e.g. phantasy.cfg
KEYNAME_CONFIG_FILE = 'config_file'
DEFAULT_CONFIG_FILE = None

INI_DICT['KEYNAME_CONFIG_FILE'] = KEYNAME_CONFIG_FILE
INI_DICT['DEFAULT_CONFIG_FILE'] = DEFAULT_CONFIG_FILE

# lattice layout file
KEYNAME_LAYOUT_FILE = 'layout_file'
DEFAULT_LAYOUT_FILE = None

INI_DICT['KEYNAME_LAYOUT_FILE'] = KEYNAME_LAYOUT_FILE
INI_DICT['DEFAULT_LAYOUT_FILE'] = DEFAULT_LAYOUT_FILE

# lattice settings file
KEYNAME_SETTINGS_FILE = 'settings_file'
DEFAULT_SETTINGS_FILE = None

INI_DICT['KEYNAME_SETTINGS_FILE'] = KEYNAME_SETTINGS_FILE
INI_DICT['DEFAULT_SETTINGS_FILE'] = DEFAULT_SETTINGS_FILE

# channel finder server address
KEYNAME_CF_SVR_URL = 'cfs_url'
DEFAULT_CF_SVR_URL = None

INI_DICT['KEYNAME_CF_SVR_URL'] = KEYNAME_CF_SVR_URL
INI_DICT['DEFAULT_CF_SVR_URL'] = DEFAULT_CF_SVR_URL

# channel finder tag
# tagging rule: phantasy.sys.{LATTICE}, e.g. phantasy.sys.LINAC
KEYNAME_CF_SVR_TAG = 'cfs_tag'
DEFAULT_CF_SVR_TAG =  lambda x: '{0}.{1}'.format(HLA_TAG_SYS_PREFIX, x)

INI_DICT['KEYNAME_CF_SVR_TAG'] = KEYNAME_CF_SVR_TAG
INI_DICT['DEFAULT_CF_SVR_TAG'] = DEFAULT_CF_SVR_TAG

# channel finder property names
KEYNAME_CF_SVR_PROP = 'cfs_property_names'
DEFAULT_CF_SVR_PROP = '*'

INI_DICT['KEYNAME_CF_SVR_PROP'] = KEYNAME_CF_SVR_PROP
INI_DICT['DEFAULT_CF_SVR_PROP'] = DEFAULT_CF_SVR_PROP

# machine type, loop (1) or not (0)
KEYNAME_MTYPE = 'loop'
DEFAULT_MTYPE = 0

INI_DICT['KEYNAME_MTYPE'] = KEYNAME_MTYPE
INI_DICT['DEFAULT_MTYPE'] = DEFAULT_MTYPE

# the properties used for initializing Element are different from those defined
# by cfs or sqlite, re-name property to Element property may needed.
_cf_map = {'elemName' : 'name',
           'elemField_eng': 'field_eng',
           'elemField_phy': 'field_phy',
           'elemType' : 'family',
           'elemHandle' : 'handle',
           'elemIndex' : 'index',
           'elemPosition' : 'se',
           'elemLength' : 'length',
           'physicsType': 'phy_type',
           'physicsName': 'phy_name',
           'machine': 'machine',
           'pvPolicy': 'pv_policy',

           'system' : 'system',
           'subsystem': 'subsystem',

           'devName' : 'devname',
           'elemGroups' : 'groups',
}

INI_DICT['CF_NAMEMAP'] = _cf_map

INI_DCONF = OrderedDict()
# COMMON SECTION
dcomm = OrderedDict()
dcomm[INI_DICT['KEYNAME_SEGMENTS']] = 'LINAC'
dcomm[INI_DICT['KEYNAME_DEFAULT_SEGMENT']] = 'LINAC'
dcomm[INI_DICT['KEYNAME_ROOT_DATA_DIR']] = '~/phantasy_data'
INI_DCONF[INI_DICT['COMMON_SECTION_NAME']] = dcomm
# LINAC SECTION
dsect_linac = OrderedDict()
dsect_linac[INI_DICT['KEYNAME_CONTROLS_PROTOCOL']] = 'EPICS'
dsect_linac[INI_DICT['KEYNAME_MTYPE']] = '0'
dsect_linac[INI_DICT['KEYNAME_SIMULATION_CODE']] = 'flame'
dsect_linac[INI_DICT['KEYNAME_MODEL_DATA_DIR']] = 'model_data'
dsect_linac[INI_DICT['KEYNAME_SETTINGS_FILE']] = 'baseline_settings.json'
dsect_linac[INI_DICT['KEYNAME_LAYOUT_FILE']] = 'baseline_layout.csv'
dsect_linac[INI_DICT['KEYNAME_CONFIG_FILE']] = 'phantasy.cfg'
dsect_linac[INI_DICT['KEYNAME_CF_SVR_URL']] = 'https://localhost:8181/ChannelFinder'
dsect_linac[INI_DICT['KEYNAME_CF_SVR_TAG']] = 'phantasy.sys.LINAC'
dsect_linac[INI_DICT['KEYNAME_CF_SVR_PROP']] = 'elem*'
dsect_linac[INI_DICT['KEYNAME_SCAN_SVR_URL']] = 'http://localhost:4810'
INI_DCONF['LINAC'] = dsect_linac


def generate_inifile(dconf=None, out=None):
    """Generate template of ini configure file.

    Parameters
    ----------
    dconf : dict
        Dict of configuration, if not given, use template dict.
    out :
        output stream, stdout by default.

    Examples
    --------
    1. Generate default config file:

    >>> with open('phantasy.ini', 'w') as f:
    >>>     generate_inifile(out=f)
    """
    from configparser import ConfigParser

    if dconf is None:
        dconf = INI_DCONF

    out = sys.stdout if out is None else out

    p = ConfigParser()
    p.optionxform = str
    for sn in dconf:
        p.add_section(sn)
        [p.set(sn, k, v) for k, v in dconf[sn].items()]
    p.write(out)
    try:
        _LOGGER.info("Write configuration into: {0}".format(out.name))
    except AttributeError:
        _LOGGER.info("Write configuration into: stringio.")
