# encoding: UTF-8

"""
Common utilities used by phytool commands.

:author: Dylan Maxwell <maxwelld@frib.msu.edu>
:date: 2015-06-18
"""


import os.path, logging, re

from ..phylib.settings import Settings
from ..phylib.cfg import Configuration 
from ..phylib.layout.layout import build_layout
from ..phylib.common.csv_utils import read_csv
from ..phylib.chanfinder.chanfinderAgent import ChannelFinderAgent

from ..machine import findMachineConfig



_CONFIG_COMMON_SECTION = "COMMON"

_CONFIG_DEFAULT_SUBMACHINE = "default_submachine"

_CONFIG_CONFIG_FILE = "config_file"

_CONFIG_SETTINGS_FILE = "settings_file"

_CONFIG_LAYOUT_FILE = "layout_file"

_CONFIG_CFS_URL = "cfs_url"

_CONFIG_CFS_TAG = "cfs_tag"

_LOGGER = logging.getLogger(__name__)



def loadMachineConfig(machine, submach):
    """Find the configuration for the specified machine.

       :param machine: name or path of machine to load
       :return: configuration or None
    """
    if machine is not None:
        mconfig, _, _ = findMachineConfig(machine)
    else:
        mconfig = None

    if submach is None:
        if mconfig is not None:
            if mconfig.has_option(_CONFIG_COMMON_SECTION, _CONFIG_DEFAULT_SUBMACHINE):
                submach = mconfig.get(_CONFIG_COMMON_SECTION, _CONFIG_DEFAULT_SUBMACHINE)
            else:
                raise RuntimeError("Error: default submachine not specified")
        else:
            submach = None
    else:
        submach = submach.strip()

    return mconfig, submach


def loadLayout(layoutPath, mconfig, submach):
    """Load the layout from the specified path or find the path in the configuration.

       :param layoutPath: path of layout file or None
       :param mconfig: machine configuration
       :param submach: name of submachine
       :return: accelerator layout
    """
    if layoutPath is None:
        if mconfig is not None and submach is not None \
                and mconfig.has_option(submach, _CONFIG_LAYOUT_FILE):
            layoutPath = mconfig.getabspath(submach, _CONFIG_LAYOUT_FILE)
        else:
            raise RuntimeError("Error: layout path option not specified")

    return build_layout(layoutPath)


def loadSettings(settingsPath, mconfig, submach):
    """Load the settings from the specified path or find the path in the configuration.

       :param settingsPath: path of settings file or None
       :param mconfig: machine configuration
       :param submach: name of submachine
       :return: accelerator settings
    """
    if settingsPath is None:
        if mconfig is not None and submach is not None \
                and mconfig.has_option(submach, _CONFIG_SETTINGS_FILE):
            settingsPath = mconfig.getabspath(submach, _CONFIG_SETTINGS_FILE)
        else:
            raise RuntimeError("Error: settings path option not specified")

    return Settings(settingsPath)


def loadLatticeConfig(configPath, mconfig, submach):
    """Load the configuration from the specified path or find the path in the configuration.

       :param configPath: path of configuration file or None
       :param mconfig: machine configuration
       :param submach: name of submachine
       :return: lattice configuration
    """
    if configPath is None:
        if mconfig is not None and submach is not None \
                and mconfig.has_option(submach, _CONFIG_CONFIG_FILE):
            configPath = mconfig.getabspath(submach, _CONFIG_CONFIG_FILE)
        else:
            raise RuntimeError("Error: config path option not specified")

    return Configuration(configPath)


def loadChannels(source, cfstag, mconfig, submach):
    """Load channel names from the given url or find the url in the configuration.

       :param cfsurl: CFS URL or local file path or None
       :param cfstag: CFS tag to query or None
       :param mconfig: machine configuration
       :param submach: name of submachine
       :return: list of channels with tuples (name, properties, tags)
    """
    if source is None:
        if mconfig is not None and submach is not None \
                and mconfig.has_option(submach, _CONFIG_CFS_URL):
            cfsurl = mconfig.get(submach, _CONFIG_CFS_URL)
        else:
            raise RuntimeError("Error: Channel Finder URL option not specified")
    else:
        cfsurl = source

    if re.match(r"https?://.*", cfsurl, re.I):
        _LOGGER.info("loadChannels: using service '%s' for '%s'" % (cfsurl, submach))
        if cfstag is None:
            if mconfig is not None and submach is not None \
                    and mconfig.has_option(submach, _CONFIG_CFS_TAG):
                cfstag = mconfig.get(submach, _CONFIG_CFS_TAG)
            else:
                cfstag = "phyutil.sys.%s" % submach
        cfa = ChannelFinderAgent()
        cfa.downloadCfs(source=cfsurl, property=[('elemName', '*'),], tagName=cfstag)
        return cfa.results

    if source is None:
        if mconfig is not None and submach is not None \
                and mconfig.has_option(submach, _CONFIG_CFS_URL):
            cfspath = mconfig.getabspath(submach, _CONFIG_CFS_URL)
        else:
            raise RuntimeError("Error: Channel Finder URL option not specified")
    else:
        cfspath = os.path.abspath(source)

    if cfspath.endswith(".sqlite") and os.path.isfile(cfspath):
        _LOGGER.info("loadChannels: using SQLite '%s'" % (cfspath,))
        cfa = ChannelFinderAgent()
        cfa.downloadCfs(source=cfspath)
        return cfa.results

    if cfspath.endswith(".csv") and os.path.isfile(cfspath):
        _LOGGER.info("loadChannels: using CSV '%s'" % (cfspath,))
        return read_csv(cfspath)

    raise RuntimeError("Error loading channels from source: {}".format(cfsurl))


