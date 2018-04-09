# -*- coding: utf-8 -*-
"""EPICS tools.
"""

from epics import caget as epics_caget
from epics import caput as epics_caput
from epics import cainfo as epics_cainfo
from epics import camonitor as epics_camonitor


def caget(pvname, count=None, timeout=None, **kws):
    return epics_caget(pvname, **kws)


def caput(pvname, value, timeout=30, **kws):
    if kws.get('callback', None) is None:
        return epics_caput(pvname, value,
                wait=kws.get('wait', True),
                timeout=timeout)
    else:
        pass
    # create convenient function to work with CaElement.
    # FIX caget error, when working with epics package.


def cainfo(pvname, **kws):
    return epics_cainfo(pvname, kws.get('print_out', True))

def camonitor(pvname, callback=None, **kws):
    return epics_camonitor(pvname, kws.get('writer', None), callback)
