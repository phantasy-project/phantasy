# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os, os.path, platform, logging

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

from .. import phylib


OPTION_SETTINGS_FILE = "settings_file"

OPTION_FIELD_DATA_DIR = "impact_rfdata_dir"


_LOGGER = logging.getLogger(__name__)


DEFAULT_LOCATIONS = [
        "${PHYUTIL_CFG}",
        os.path.join(".", "phyutil.cfg"),
        os.path.join("~", ".phyutil.cfg"),
        os.path.join("~", "_phyutil.cfg"),
    ]

if platform.system() == "Linux":
    DEFAULT_LOCATIONS.append("/etc/phyutil/phyutil.cfg")


# global configuration
config = None
# global configuration file path
config_path = None


def load(cfgpath=None):
    """Load the global configuration from the specified file path or
       list of file paths. The existing configuration is always replaced.
       If a list of paths is provided then an attempt is made to read
       each file is the order specified and processing stops after a configuration
       file has been successfully loaded. To load multiple files into the
       configuration use the Configuration.read() method.

       :params cfgpath: configuration file path or list of file paths
       :return: True if configuration file loaded successfully, otherwise False
    """
    global config, config_path
    config = Configuration()
    config_path = os.getcwd()

    if cfgpath == None:
        # simply initialize an empty configuration
        return True

    if isinstance(cfgpath , (tuple,list)):
        raise_error = False
    else:
        cfgpath = [ cfgpath ]
        raise_error = True

    for path in cfgpath:
        try:
            if isinstance(path, basestring):
                path = os.path.expanduser(path)
                path = os.path.expandvars(path)
                _LOGGER.debug("Attempting to load configuration file: %s", path)
                with open(path, "r") as fp:
                    config.readfp(fp)
                    config_path = path
                    _LOGGER.debug("Successfully loaded configuration file: %s", path)
                    return True
            else:
                TypeError("Configuration file path must have type string")

        except Exception as e:
            if raise_error:
                raise e

    return False


def _auto_load():
    """
    Auto load the configuration file if enabled.
    """
    if phylib.AUTO_CONFIG:
        if load(DEFAULT_LOCATIONS):
            _LOGGER.info("Auto load configuration file found: %s", config_path)
        else:
            _LOGGER.warning("Auto load configuration file not found: %s", DEFAULT_LOCATIONS)


class Configuration(SafeConfigParser):
    """Configuration wraps the standand python config
       parser to provide convenient helper methods.
    """
    
    _DEFAULT_SECTION = "DEFAULT"

    def get_default(self, option):
        return self.get(self._DEFAULT_SECTION, option, check_default=False)

    def getint_default(self, option):
        return self.getint(self._DEFAULT_SECTION, option, check_default=False)

    def getfloat_default(self, option):
        return self.getfloat(self._DEFAULT_SECTION, option, check_default=False)

    def has_default(self, option):
        return self.has_option(self._DEFAULT_SECTION, option, check_default=False)

    def get(self, section, option, check_default=True):
        if self.has_option(section, option, False):
            return SafeConfigParser.get(self, section, option)
        elif check_default and self.has_default(option):
            return self.get_default(option)
        elif not self.has_section(section):
            raise NoSectionError("No section found: " + str(section))
        else:
            raise NoOptionError("No option found: " + str(option))

    def getint(self, section, option, check_default=True):
        if self.has_option(section, option, False):
            return SafeConfigParser.getint(self, section, option)
        elif check_default and self.has_default(option):
            return self.getint_default(option)
        elif not self.has_section(section):
            raise NoSectionError("No section found: " + str(section))
        else:
            raise NoOptionError("No option found: " + str(option))

    def getfloat(self, section, option, check_default=True):
        if self.has_option(section, option, False):
            return SafeConfigParser.getfloat(self, section, option)
        elif check_default and self.has_default(option):
            return self.getfloat_default(option)
        elif not self.has_section(section):
            raise NoSectionError("No section found: " + str(section))
        else:
            raise NoOptionError("No option found: " + str(option))

    def has_option(self, section, option, check_default=True):
        # There is an inconsistency in the SafeConfigParser implementations
        # of the has_option() and get() methods.  The has_option() method
        # considers any sections which is 'falsy' (ie empty string or list)
        # as synonymous with the default section. However, the get() method
        # will raise exception if a 'falsy' section is used.  In this method,
        # if the provided section is 'falsy' then then it is considered
        # to not exist in the configuration.
        return (bool(section) and SafeConfigParser.has_option(self, section, option)) or \
                    (check_default and self.has_default(option))


# initialize the global configuration
_auto_load()


