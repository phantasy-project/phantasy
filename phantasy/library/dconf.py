# -*- coding: utf-8 -*-


import os
import logging
from phantasy.library.parser import find_machine_config
from phantasy.library.parser import Configuration

_LOGGER = logging.getLogger(__name__)


try:
    DEFAULT_PHANTASY_CONFIG_MACHINE = '/etc/phantasy/config/frib/'
    DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_PHANTASY_CONFIG_MACHINE, 'phantasy.cfg')
    _DEFAULT_MCONF, _DEFAULT_MPATH, _DEFAULT_MNAME = find_machine_config(
        DEFAULT_PHANTASY_CONFIG_MACHINE)
    _DEFAULT_MCONFIG = Configuration(DEFAULT_CONFIG_FILE)
except:
    _DEFAULT_MCONFIG = None
    _DEFAULT_MCONF = None
    _DEFAULT_MPATH = ''
    _DEFAULT_MNAME = ''
    _LOGGER.warn('Default configuration does not exist.')

