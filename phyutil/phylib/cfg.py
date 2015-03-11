# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os.path, platform

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError


OPTION_BETA = "beta"

OPTION_LENGTH = "length"

OPTION_VOLTAGE = "voltage"

OPTION_FREQUENCY = "frequency"

OPTION_DIAMETER = "diameter"

OPTION_SETTINGS_FILE = "settings_file"

OPTION_XLF_FILE = "xlf_file"

OPTION_FIELD_DATA_DIR = "impact_rfdata_dir"


DEFAULT_LOCATIONS = [
        "${PHYUTIL_CFG}",
        os.path.join(".", "phyutil.cfg"),
        os.path.join("~", ".phyutil.cfg"),
        os.path.join("~", "_phyutil.cfg"),
    ]

if platform.system() == "Linux":
    DEFAULT_LOCATIONS.append("/etc/phyutil/phyutil.cfg")


# glabal configuration
config = None


def load(cfgpath=DEFAULT_LOCATIONS):
    """Load the global configuration from the specified file path or
       list of file paths. The existing configuration is always replaced.
       If a list of paths is provided then an attempt is made to read
       each file is the order specified and processing stops after a configuration
       file has been successfully loaded. To load multiple files into the
       configuration use the Configuration.read() method.

       :params cfgpath: configuration file path or list of file paths
       :return: the configuration file path that was successfully loaded
    """
    global config
    c = Configuration()

    if isinstance(cfgpath , (tuple,list)):
        raise_error = False
    else:
        cfgpath = [ cfgpath ]
        raise_error = True

    for path in cfgpath:
        try:
            path = os.path.expanduser(path)
            path = os.path.expandvars(path)
            print(path)
            with open(path, "r") as fp:
                c.readfp(fp)
                break
        except Exception as e:
            if raise_error:
                raise e

    config = c
    return path


class Configuration(SafeConfigParser):
    """Configuration wraps the standand python config
       parser to provide convenient helper methods.
    """
    
    _DEFAULT_SECTION = "DEFAULT"

    def get_default(self, option):
        return self.get(self._DEFAULT_SECTION, option)

    def getint_default(self, option):
        return self.getint(self._DEFAULT_SECTION, option)

    def getfloat_default(self, option):
        return self.getfloat(self._DEFAULT_SECTION, option)

    def has_default(self, option):
        return self.has_option(self._DEFAULT_SECTION, option)

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
        return SafeConfigParser.has_option(self, section, option) or (check_default and self.has_default(option))


# initialize the global configuration
load()

