#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for handling configuration file.
"""

import logging
import os.path
from collections import OrderedDict

from configparser import ConfigParser
from configparser import NoSectionError
from configparser import NoOptionError


_LOGGER = logging.getLogger(__name__)

# HOME = os.environ['HOME'] will NOT work on Windows,
# unless %HOME% is set on Windows, which is not the case by default.
_HOME_DEFAULT = os.path.join(os.path.expanduser('~'), '.phantasy')


class Configuration(ConfigParser):
    """Configuration wraps the standand python config
    parser to provide convenient helper methods.

    Parameters
    ----------
    config_path : str
        Location of configuration file to read (optional)
    """
    _DEFAULT_SECTION = "DEFAULT"

    def __init__(self, config_path=None):
        ConfigParser.__init__(self)
        if config_path is not None:
            if os.path.isabs(config_path):
                self.config_path = config_path
            else:
                self.config_path = os.path.abspath(config_path)
            with open(self.config_path, "r") as fp:
                self.read_file(fp)
        else:
            self.config_path = None

    def get_default(self, option, **kws):
        return self.get(self._DEFAULT_SECTION, option, check_default=False, **kws)

    def getint_default(self, option, **kws):
        return self.getint(self._DEFAULT_SECTION, option, check_default=False, **kws)

    def getfloat_default(self, option, **kws):
        return self.getfloat(self._DEFAULT_SECTION, option, check_default=False, **kws)

    def getarray_default(self, option, sep=None, conv=None, **kws):
        return self.getarray(self._DEFAULT_SECTION, option, check_default=False, sep=sep, conv=conv, **kws)

    def getabspath_default(self, option, cmd=False, **kws):
        """Get the given option and convert to an absolute path.
        If the value of the option is not already an absolute
        path, than resolve the relative path against the config_path
        property. If config_path is None, then raise a runtime error.

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
        return self.getabspath(self._DEFAULT_SECTION, option, check_default=False, cmd=cmd, **kws)

    def has_default(self, option):
        return self.has_option(self._DEFAULT_SECTION, option, check_default=False)

    def get(self, section, option, check_default=True, **kws):
        if self.has_option(section, option, False):
            return ConfigParser.get(self, section, option, **kws)
        elif check_default and self.has_default(option):
            return self.get_default(option, **kws)
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getint(self, section, option, check_default=True, **kws):
        if self.has_option(section, option, False):
            return ConfigParser.getint(self, section, option, **kws)
        elif check_default and self.has_default(option):
            return self.getint_default(option, **kws)
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getfloat(self, section, option, check_default=True, **kws):
        if self.has_option(section, option, False):
            return ConfigParser.getfloat(self, section, option, **kws)
        elif check_default and self.has_default(option):
            return self.getfloat_default(option, **kws)
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getarray(self, section, option, check_default=True, sep=None, conv=None, **kws):
        def parsearray(s):
            spt = s.split(sep)
            if callable(conv):
                tmp = []
                for s in spt:
                    tmp.append(conv(s))
                spt = tmp
            return spt

        if self.has_option(section, option, False):
            return parsearray(ConfigParser.get(self, section, option, **kws))
        elif check_default and self.has_default(option):
            return parsearray(self.get_default(option, **kws))
        elif not self.has_section(section):
            raise NoSectionError(section)
        else:
            raise NoOptionError(option, section)

    def getabspath(self, section, option, check_default=True, cmd=False, **kws):
        """Get the given option and convert to an absolute path.
        If the value of the option is not already an absolute
        path, than resolve the relative path against the config_path
        property. If config_path is None, then raise a runtime error.

        Parameters
        ----------
        section : str
            Name of section.
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
        path = self.get(section, option, check_default=check_default, **kws)
        if os.path.isabs(path):
            return path
        elif cmd and not path.startswith(".") and (os.path.sep not in path):
            return path
        elif self.config_path is not None:
            return os.path.join(os.path.dirname(self.config_path), path)
        else:
            raise RuntimeError("config_path is None: cannot resolve relative path")

    def has_option(self, section, option, check_default=True):
        # There is an inconsistency in the ConfigParser implementations
        # of the has_option() and get() methods.  The has_option() method
        # considers any sections which is 'falsy' (ie empty string or list)
        # as synonymous with the default section. However, the get() method
        # will raise exception if a 'falsy' section is used.  In this method,
        # if the provided section is 'falsy' then then it is considered
        # to not exist in the configuration.
        return (bool(section) and ConfigParser.has_option(self, section, option)) or \
                    (check_default and self.has_default(option))

    def to_dict(self, flat=False, ordered=True):
        """Convert configuration into dict.

        Parameters
        ----------
        flat : True or False
            If True, return flat dict, overidden same key(s), False by default.
        ordered : True or False
            If False, return dict will not maintain key order, True by default.

        Returns
        -------
        ret : dict
            Inherit all keys from configuration.
        """
        fdict = OrderedDict if ordered else dict
        rdict = fdict()
        if flat:
            for sn in self.sections():
                for k, v in self.items(sn):
                    rdict[k] = v
        else:
            for sn in self.sections():
                    rdict[sn] = fdict(self.items(sn))
        return rdict


def _find_machine_path(machine):
    """Try to find a machine configuration path.
    If *machine* comes with a full path, it assume the configuration file is
    under the same path.

    Searching priority from high to low:
    - Path of user-defined directory;
    - Path of current working directory;
    - Path defined by env: ``PHANTASY_CONFIG_DIR``;
    - Current user's home folder: ``~/.phantasy``;
    - Path of phantasy-machines if installed via pip.

    Parameters
    ----------
    machine : str
        Facility/machine name, or directory path.

    Returns
    -------
    ret : tuple
        Tuple of mpath and mname, where mpath is the full path of machine
        configuration files, and mname is the name of machine; if not found,
        return None, "".
    """
    # if machine is an abs path
    _LOGGER.debug("Searching configuration in relativer/absolute path: '%s'" % machine)
    if os.path.isdir(machine):
        machine = os.path.realpath(machine)
        mname = os.path.basename(machine)
        return machine, mname

    # search in PHANTASY_CONFIG_DIR and ~/.phantasy/ (default)
    phantasy_config_dir = os.environ.get("PHANTASY_CONFIG_DIR", _HOME_DEFAULT)
    _LOGGER.debug("Searching configuration in: '%s' for '%s'" % (phantasy_config_dir, machine))
    home_machine = os.path.join(phantasy_config_dir, machine)
    if os.path.isdir(home_machine):
        mname = os.path.basename(os.path.realpath(machine))
        return home_machine, mname

    # search if phantasy-machines pacakge is installed
    _LOGGER.debug("Searching configuration in phantasy-machines package.")
    try:
        import phantasy_machines
    except ImportError:
        print("'phantasy-machines' is not installed.")
    else:
        phantasy_config_dir = phantasy_machines.__path__[0]
        mpath = os.path.join(phantasy_config_dir, machine)
        return mpath, machine

    _LOGGER.critical("Can not find machine dir")
    return None, ""


def find_machine_config(machine, **kwargs):
    """Find the configuration (ini) file for the specified machine, by default
    the name of configuration file should be 'phantasy.ini'.

    Parameters
    ----------
    machine : str
        Name or directory path of machine configuration.

    Keyword Arguments
    -----------------
    verbose : True or False
        Display more information, False by default.
    filename : str
        File name of target configuration file, 'phantasy.ini' by default.

    Returns
    -------
    ret : tuple
        Tuple of (config, machdir, machname), where *config* is
        ``Configuration`` object, *machdir* is full path of the machine,
        *machname* is name of the machine.

    Examples
    --------
    >>> # PHANTASY_CONFIG_DIR: /home/tong1/work/FRIB/projects/machines
    >>> print(find_machine_config("FRIB"))
    (<config.Configuration instance at 0x7fcaf20650e0>,
     '/home/tong1/work/FRIB/projects/machines/FRIB',
     'FRIB')
    """
    verbose = kwargs.get('verbose', 0)
    filename = kwargs.get('filename', 'phantasy.ini')

    machdir, machname = _find_machine_path(machine)
    if verbose:
        print("Loading machine data '%s: %s'" % (machname, machdir))

    if machdir is None:
        msg = "Cannot find machine data directory for '%s'" % machine
        _LOGGER.error(msg)
        raise RuntimeError(msg)

    _LOGGER.info("Importing %s from %s" % (machine, machdir))

    try:
        cfg = Configuration(os.path.join(machdir, filename))
        _LOGGER.info("Loading machine configuration from {0}".format(
            cfg.config_path))
    except:
        raise RuntimeError("Can not open '%s' to read machine configurations" %
                (os.path.join(machdir, filename)))

    return cfg, machdir, machname
