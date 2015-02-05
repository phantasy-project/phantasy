# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os.path, json

from ConfigParser import SafeConfigParser, NoSectionError


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

    def getint(self, section, option):
        try:
            # SafeConfigParser is old-style class so call
            # parent method with using the 'super' helper.
            return SafeConfigParser.getint(self, section, option)
        except NoSectionError:
            return self.getint_default(option)



class FactoryWithConfig(object):
    """
    FactoryWithConfig is base class for building configuration based factories.
    """
    def __init__(self, config=None):
        if config != None:
            self.config = config
        else:
            self.config = Configuration()


    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not isinstance(config, Configuration):
            raise TypeError("FactoryWithConfig: config must be of type Configuration")
        self._config = config
