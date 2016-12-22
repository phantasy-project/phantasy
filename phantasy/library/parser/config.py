# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os.path
import platform
import logging
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError


_LOGGER = logging.getLogger(__name__)

# HOME = os.environ['HOME'] will NOT work on Windows,
# unless %HOME% is set on Windows, which is not the case by default.
_home_hla = os.path.join(os.path.expanduser('~'), '.phyutil')
PHYUTIL_CONFIG_DIR = os.environ.get("PHYUTIL_CONFIG_DIR", _home_hla)

# global configuration
#config = None
#
#def load(cfgpath=None):
#    """Load the global configuration from the specified file path or
#    list of file paths. The existing configuration is always replaced.
#    If a list of paths is provided then an attempt is made to read
#    each file is the order specified and processing stops after a
#    configuration file has been successfully loaded. 
#    To load multiple files into the configuration use the 
#    ``Configuration.read()`` method.
#
#    Parameters
#    ----------
#    cfgpath :
#        Configuration file path or list of file paths.
#    
#    Returns
#    -------
#    ret : True or False
#        True if configuration file loaded successfully, otherwise False.
#    """
#    global config
#    config = Configuration()
#
#    if cfgpath == None:
#        # simply initialize an empty configuration
#        return True
#
#    if isinstance(cfgpath , (tuple,list)):
#        raise_error = False
#    else:
#        cfgpath = [ cfgpath ]
#        raise_error = True
#
#    for path in cfgpath:
#        try:
#            if isinstance(path, basestring):
#                path = os.path.expanduser(path)
#                path = os.path.expandvars(path)
#                _LOGGER.debug("Attempting to load configuration file: %s", path)
#                with open(path, "r") as fp:
#                    config.readfp(fp)
#                    config.configPath = path
#                    _LOGGER.info("Successfully loaded configuration file: %s", path)
#                    return True
#            else:
#                TypeError("Configuration file path must have type string")
#
#        except Exception as e:
#            if raise_error:
#                raise e
#
#    return False


class Configuration(SafeConfigParser):
    """Configuration wraps the standand python config
    parser to provide convenient helper methods.
       
    Parameters
    ----------
    configPath : str
        Location of configuration file to read (optional)
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

        Parameters
        ----------
        option :
            Name of configuration option.
        cmd : 
            If True, then relative paths must start with a '.' or contain a
            path separator otherwise it is considered absolute,
            ``False`` by default.

        Returns
        -------
        ret :
            Absolute path.
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

        Parameters
        ----------
        option :
            Name of configuration option.
        check_default :
            Check the default section for the option (default: False).
        cmd : 
            If True, then relative paths must start with a '.' or contain a
            path separator otherwise it is considered absolute,
            ``False`` by default.

        Returns
        -------
        ret :
            Absolute path.
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


def _find_machine_path(machine):
    """Try to find a machine configuration path.
    If *machine* comes with a full path, it assume the configuration file is
    under the same path.
    
    It searches 3 different ways:
      - a absolute path from parameter
      - environment variable: PHYUTIL_CONFIG_DIR,
      - the package directory
    
    Parameters
    ----------
    machine : str
        Facility/machine name, or directory path.

    Returns:
    ret : tuple
        Tuple of mpath and mname, where mpath is the full path of machine
        configuration files, and mname is the name of machine; if not found,
        return None, "".
    """
    # if machine is an abs path
    _LOGGER.info("searching configuration in relative or absolute path: '%s'" % machine)
    if os.path.isdir(machine):
        machine = os.path.realpath(machine)
        mname = os.path.basename(machine)
        return machine, mname

    # try "machine" in PHYUTIL_CONFIG_DIR and ~/.phyutil/ (default)
    _LOGGER.info("searching configuration under path: '%s' '%s'" % (PHYUTIL_CONFIG_DIR, machine))
    home_machine = os.path.join(PHYUTIL_CONFIG_DIR, machine)
    if os.path.isdir(home_machine):
        mname = os.path.basename(os.path.realpath(machine))
        return home_machine, mname

    # try the package
    pkg_machine = resource_filename(__name__, machine)
    _LOGGER.info("trying system dir '%s'" % pkg_machine)
    if os.path.isdir(pkg_machine):
        mname = os.path.basename(os.path.realpath(pkg_machine))
        return pkg_machine, mname

    _LOGGER.warn("can not find machine dir")
    return None, ""


def find_machine_config(machine, **kwargs):
    """Find the configuration (ini) file for the specified machine, by default
    the name of configuration file should be 'phyutil.ini'.

    Parameters
    ----------
    machine : str
        Name or directory path of machine configuration.
    verbose : True or False
        Display more information (default: False)

    Returns
    -------
    ret : tuple
        Tuple of (config, machdir, machname), where *config* is 
        ``Configuration`` object, *machdir* is full path of the machine,
        *machname* is name of the machine.

    Examples
    --------
    >>> # PHYUTIL_CONFIG_DIR: /home/tong1/work/FRIB/projects/machines
    >>> print(find_machine_config("FRIB"))
    (<config.Configuration instance at 0x7fcaf20650e0>,
     '/home/tong1/work/FRIB/projects/machines/FRIB',
     'FRIB')
    """
    verbose = kwargs.get('verbose', 0)

    machdir, machname = _find_machine_path(machine)
    if verbose:
        print("loading machine data '%s: %s'" % (machname, machdir))

    if machdir is None:
        msg = "Cannot find machine data directory for '%s'" % machine
        _LOGGER.error(msg)
        raise RuntimeError(msg)

    _LOGGER.info("Importing '%s' from '%s'" % (machine, machdir))

    try:
        cfg = Configuration(os.path.join(machdir, "phyutil.ini"))
        _LOGGER.info("Using config file: 'phyutil.ini'")
    except:
        raise RuntimeError("can not open '%s' to read configurations" %
                (os.path.join(machdir, "phyutil.ini")))

    return cfg, machdir, machname
