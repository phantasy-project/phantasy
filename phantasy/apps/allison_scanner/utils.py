#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from phantasy import MachinePortal


def find_dconf():
    """Find parameter configuration file for wire-scanners.
    searching the following locations:
    * ~/.phantasy/ems.ini
    * /etc/phantasy/ems.ini
    * package location: apps/allison_scanner/config/ems.ini
    """
    home_conf = os.path.expanduser('~/.phantasy/ems.ini')
    sys_conf = '/etc/phantasy/ems.ini'
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config/ems.ini')


def get_all_devices(machine="FRIB", segment="LEBT", type="EMS"):
    """Return dict of `(name, elem)`.
    """
    mp = MachinePortal(machine, segment)
    elems = mp.get_elements(type=type)
    r = [(i.name, i) for i in sorted(elems, key=lambda x:x.name[-4:])]
    return OrderedDict(r)
