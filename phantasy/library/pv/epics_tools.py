# -*- coding: utf-8 -*-
"""EPICS tools.
"""

from epics import caget as epics_caget
from epics import caput as epics_caput
from epics import cainfo as epics_cainfo
from epics import camonitor as epics_camonitor

import logging
from functools import partial

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

_LOGGER = logging.getLogger(__name__)


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


def ensure_put(element, field, goal, tol=None, timeout=None):
    """Ensure put operation to the *field* of *element* to reach the value
    of *goal* within the difference tolerance defined by *tol*.

    Parameters
    ----------
    element : CaElement
        High-level element object.
    field : str
        Name of dynamic field of element to control.
    goal : float
        The final value that the field of element would like to reach.
    tol : float
        Tolerance for discrepancy between current readback
        value and the set goal, default is 0.01.
    timeout : float
        Maximum wait time, default is 10 sec.

    Examples
    --------
    >>> # get element, e.g. elem = mp.get_elements(name='*D0874*')[0]
    >>> # set 'V' field of element to 1000
    >>> ensure_put(elem, 'V', 1000)
    """

    def callback(sq, fld, **kws):
        val = kws.get('value')
        sq.put(fld.value)

    def is_equal(v, goal, tol):
        return abs(v - goal) < tol

    fld = element.get_field(field)
    pv = fld.readback_pv[0]
    q = Queue()
    cid = pv.add_callback(partial(callback, q, fld))
    fld.value = goal

    tol = 0.01 if tol is None else tol
    timeout = 10.0 if timeout is None else timeout
    while True:
        v = fld.value
        try:
            if is_equal(v, goal, tol): raise Empty
            v = q.get(timeout=timeout)
            _LOGGER.debug(
                "Field '{fname}' of '{ename}' reached: {v}[{g}].".format(
                    fname=field, ename=element.name, v=v, g=goal))
        except Empty:
            _LOGGER.info(
                "Field '{fname}' of '{ename}' reached: {v}.".format(
                    fname=field, ename=element.name, v=fld.value))
            pv.remove_callback(cid)
            break

