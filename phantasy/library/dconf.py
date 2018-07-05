# -*- coding: utf-8 -*-


import os
import logging
from phantasy.library.parser import find_machine_config
from phantasy.library.parser import Configuration

_LOGGER = logging.getLogger(__name__)


try:
    DEMO_PHANTASY_CONFIG_MACHINE = '/etc/phantasy/config/demo_mconfig/accel'
    DEMO_CONFIG_FILE = os.path.join(DEMO_PHANTASY_CONFIG_MACHINE, 'phantasy.cfg')
    _DEMO_MCONF, _DEMO_MPATH, _DEMO_MNAME = find_machine_config(
        DEMO_PHANTASY_CONFIG_MACHINE)
    _DEMO_MCONFIG = Configuration(DEMO_CONFIG_FILE)
except:
    _DEMO_MCONFIG = None
    _DEMO_MCONF = None
    _DEMO_MPATH = ''
    _DEMO_MNAME = ''
    _LOGGER.warning('DEMO configuration does not exist.')

