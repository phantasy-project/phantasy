# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os.path, platform, logging

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError


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
    global config
    config = Configuration()

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
                    config.configPath = path
                    _LOGGER.info("Successfully loaded configuration file: %s", path)
                    return True
            else:
                TypeError("Configuration file path must have type string")

        except Exception as e:
            if raise_error:
                raise e

    return False



class Configuration(SafeConfigParser):
    """Configuration wraps the standand python config
       parser to provide convenient helper methods.
       
       :param configPath: location of configuration file to read (optional)
    """
    
    _DEFAULT_SECTION = "DEFAULT"

    def __init__(self, configPath=None):
        SafeConfigParser.__init__(self)
        if configPath is not None:
            if os.path.isabs(configPath):
                self.configPath = configPath
            else:
                self.configPath = os.path.abspath(configPath)
            with open(self.configPath, "r") as fp:
                self.readfp(fp)
        else:
            self.configPath = None

    def get_default(self, option):
        return self.get(self._DEFAULT_SECTION, option, check_default=False)

    def getint_default(self, option):
        return self.getint(self._DEFAULT_SECTION, option, check_default=False)

    def getfloat_default(self, option):
        return self.getfloat(self._DEFAULT_SECTION, option, check_default=False)

    def getarray_default(self, option, sep=None, conv=None):
        return self.getarray(self._DEFAULT_SECTION, option, check_default=False, sep=sep, conv=conv)

    def getabspath_default(self, option, cmd=False):
        """Get the given option and convert to an absolute path.
           If the value of the option is not already an absolute
           path, than resolve the relative path against the configPath
           property. If configPath is None, then raise a runtime error.

           :param option: name of configuration option
           :param cmd: If True, then relative paths must start with a '.' or contain a path
                       separator otherwise it is considered absolute. (default: False)
           :return: absolute path
        """
        return self.getabspath(self._DEFAULT_SECTION, option, check_default=False, cmd=cmd)

    def has_default(self, option):
        return self.has_option(self._DEFAULT_SECTION, option, check_default=False)

    def get(self, section, option, check_default=True):
        if self.has_option(section, option, False):
            return SafeConfigParser.get(self, section, option)
        elif check_default and self.has_default(option):
            return self.get_default(option)
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getint(self, section, option, check_default=True):
        if self.has_option(section, option, False):
            return SafeConfigParser.getint(self, section, option)
        elif check_default and self.has_default(option):
            return self.getint_default(option)
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getfloat(self, section, option, check_default=True):
        if self.has_option(section, option, False):
            return SafeConfigParser.getfloat(self, section, option)
        elif check_default and self.has_default(option):
            return self.getfloat_default(option)
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getarray(self, section, option, check_default=True, sep=None, conv=None):
        def parsearray(s):
            spt = s.split(sep)
            if callable(conv):
                tmp = []
                for s in spt:
                    tmp.append(conv(s))
                spt = tmp
            return spt

        if self.has_option(section, option, False):
            return parsearray(SafeConfigParser.get(self, section, option))
        elif check_default and self.has_default(option):
            return parsearray(self.get_default(option))
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getabspath(self, section, option, check_default=True, cmd=False):
        """Get the given option and convert to an absolute path.
           If the value of the option is not already an absolute
           path, than resolve the relative path against the configPath
           property. If configPath is None, then raise a runtime error.

           :param option: name of configuration option
           :param check_default: check the default section for the option (default: False)
           :param cmd: If True, then relative paths must start with a '.' or contain a path
                       separator otherwise it is considered absolute. (default: False)
           :return: absolute path
        """
        path = self.get(section, option, check_default=check_default)
        if os.path.isabs(path):
            return path
        elif cmd and not path.startswith(".") and (os.path.sep not in path):
            return path
        elif self.configPath is not None:
            return os.path.join(os.path.dirname(self.configPath), path)
        else:
            raise RuntimeError("configPath is None: cannot resolve relative path")

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


