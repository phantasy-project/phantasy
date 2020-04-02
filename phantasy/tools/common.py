#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Common utilities used by phytool commands.
"""

import os.path
import logging
import re

from phantasy.library.settings import Settings
from phantasy.library.parser import Configuration
from phantasy.library.parser import find_machine_config
from phantasy.library.layout import build_layout
from phantasy.library.channelfinder import read_csv
from phantasy.library.pv import DataSource

_CONFIG_COMMON_SECTION = "COMMON"
_CONFIG_DEFAULT_SEGMENT = "default_segment"
_CONFIG_CONFIG_FILE = "config_file"
_CONFIG_SETTINGS_FILE = "settings_file"
_CONFIG_LAYOUT_FILE = "layout_file"
_CONFIG_CFS_URL = "cfs_url"
_CONFIG_CFS_TAG = "cfs_tag"

_LOGGER = logging.getLogger(__name__)


def loadMachineConfig(machine, segment=None, **kws):
    """Find the configuration for the specified machine.

    Parameters
    ----------
    machine : str
        Name (search path) or path (rel or abs) of machine to load.

    segment : str
        Name of segment of machine, if not given, use default.

    Keyword Arguments
    -----------------
    verbose : True or False
        Display more information (default: False)

    Returns
    -------
    ret : tuple
        Machine configuration object and name of lattice.
    """
    if os.path.isdir(machine):
        machine = os.path.abspath(machine)

    if machine is not None:
        mconfig, _, _ = find_machine_config(machine, **kws)
    else:
        mconfig = None

    if segment is None:
        if mconfig is not None:
            if mconfig.has_option(_CONFIG_COMMON_SECTION, _CONFIG_DEFAULT_SEGMENT):
                segment = mconfig.get(_CONFIG_COMMON_SECTION, _CONFIG_DEFAULT_SEGMENT)
            else:
                raise RuntimeError("Error: default segment not specified")
        else:
            segment = None
    else:
        segment = segment.strip()

    return mconfig, segment


def loadLayout(layoutPath, mconfig=None, segment=None):
    """Load the layout from the specified path or find the path in the
    configuration.

    Parameters
    ----------
    layoutPath :
        Path of layout file or None.
    mconfig :
        Machine configuration.
    segment : str
        Name of segment.

    Returns
    -------
    ret :
        Accelerator layout object.
    """
    if layoutPath is None:
        if mconfig is not None and segment is not None \
                and mconfig.has_option(segment, _CONFIG_LAYOUT_FILE):
            layoutPath = mconfig.getabspath(segment, _CONFIG_LAYOUT_FILE)
        else:
            raise RuntimeError("Error: layout path option not specified")

    return build_layout(layoutPath)


def loadSettings(settingsPath, mconfig=None, segment=None):
    """Load the settings from the specified path or find the path in the
    configuration.

    Parameters
    ----------
    settingsPath :
        Path of settings file or None.
    mconfig :
        Machine configuration.
    segment : str
        Name of segment.

    Returns
    -------
    ret :
        Accelerator settings object.
    """
    if settingsPath is None:
        if mconfig is not None and segment is not None \
                and mconfig.has_option(segment, _CONFIG_SETTINGS_FILE):
            settingsPath = mconfig.getabspath(segment, _CONFIG_SETTINGS_FILE)
        else:
            raise RuntimeError("Error: settings path option not specified")

    return Settings(settingsPath)


def loadLatticeConfig(config_path, mconfig=None, segment=None):
    """Load the configuration from the specified path or find the path in the
    configuration.

    Parameters
    ----------
    config_path :
        Path of configuration file or None.
    mconfig :
        Machine configuration.
    segment : str
        Name of segment.

    Returns
    -------
    ret :
        Lattice configuration object.
    """
    if config_path is None:
        if mconfig is not None and segment is not None \
                and mconfig.has_option(segment, _CONFIG_CONFIG_FILE):
            config_path = mconfig.getabspath(segment, _CONFIG_CONFIG_FILE)
        else:
            raise RuntimeError("Error: config path option not specified")

    return Configuration(config_path)


def loadChannels(source, cfstag, mconfig, segment):
    """Load channel names from the given url or find the url from the
    configuration files.

    Parameters
    ----------
    cfsurl :
        CFS URL or local file path or None.
    cfstag :
        CFS tag to query or None.
    mconfig :
        Machine configuration.
    segment :
        Name of segment.

    Returns
    -------
    ret :
        List of channels with tuples (name, properties, tags).
    """
    if source is None:
        if mconfig is not None and segment is not None \
                and mconfig.has_option(segment, _CONFIG_CFS_URL):
            cfsurl = mconfig.get(segment, _CONFIG_CFS_URL)
        else:
            raise RuntimeError("Error: Channel Finder URL option not specified")
    else:
        cfsurl = source

    if re.match(r"https?://.*", cfsurl, re.I):
        _LOGGER.info("Loading channels from %s for %s" % (cfsurl, segment))
        if cfstag is None:
            if mconfig is not None and segment is not None \
                    and mconfig.has_option(segment, _CONFIG_CFS_TAG):
                cfstag = mconfig.get(segment, _CONFIG_CFS_TAG)
            else:
                cfstag = "phantasy.sys.%s" % segment
        ds = DataSource(source=cfsurl)
        data = ds.get_data(tag_filter=cfstag)
        pvdata = [
                  [d['name'],
                  {p['name']:p['value'] for p in d['properties']},
                  [t['name'] for t in d['tags']]]
                  for d in data
                 ]
        return pvdata

    if source is None:
        if mconfig is not None and segment is not None \
                and mconfig.has_option(segment, _CONFIG_CFS_URL):
            cfspath = mconfig.getabspath(segment, _CONFIG_CFS_URL)
        else:
            raise RuntimeError("Error: Channel Finder URL option not specified")
    else:
        cfspath = os.path.abspath(source)

    if cfspath.endswith(".sqlite") and os.path.isfile(cfspath):
        _LOGGER.info("Loading channels from %s" % (cfspath,))
        ds = DataSource(source=cfspath)
        data = ds.get_data()
        pvdata = [
                  [d['name'],
                  {p['name']:p['value'] for p in d['properties']},
                  [t['name'] for t in d['tags']]]
                  for d in data
                 ]
        return pvdata

    if cfspath.endswith(".csv") and os.path.isfile(cfspath):
        _LOGGER.info("Loading channels from %s" % (os.path.abspath(cfspath),))
        return read_csv(cfspath)

    raise RuntimeError("Error loading channels from source: {}".format(cfsurl))
