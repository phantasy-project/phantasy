# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os.path, json

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError


OPTION_BETA = "beta"

OPTION_LENGTH = "length"

OPTION_VOLTAGE = "voltage"

OPTION_FREQUENCY = "frequency"

OPTION_DIAMETER = "diameter"

OPTION_SETTINGS_FILE = "settings_file"

OPTION_XLF_FILE = "xlf_file"

OPTION_FIELD_DATA_DIR = "impact_rfdata_dir"


class Configuration(SafeConfigParser):
    """
    Configuration wrapps the standand python config parser
    to provide convenient helper methods.
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


