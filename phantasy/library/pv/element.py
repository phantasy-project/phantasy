# -*- coding: utf-8 -*-

"""Class interface for generic RD/SET PVs w.r.t. CaField.
"""
from epics import PV
from .epics_tools import ensure_put
from typing import Union, List
from phantasy.library.exception import TimeoutError
from phantasy.library.exception import PutFinishedException
from phantasy.library.misc import epoch2human
from functools import partial
from queue import Queue, Empty
import epics
import time
import numpy as np
import click
import random

COLORS = ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan',
          'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan')


class PVElement(object):
    """Unified interface for `get` and `put` operations to a PV.

    Examples
    --------
    >>> elem = PVElement('VA:LS1_BTS:QH_D1942:I_CSET',
                         'VA:LS1_BTS:QH_D1942:I_RD')
    >>> elem.value # get value
    >>> elem.value = 1 # put with a new value
    """

    def __init__(self, put_pv_name, get_pv_name):
        self._put_pvname = put_pv_name
        self._get_pvname = get_pv_name
        self._putPV = PV(put_pv_name, auto_monitor=True)
        self._getPV = PV(get_pv_name, auto_monitor=True)

    @property
    def fname(self):
        """Default CA field name.
        """
        return self.pvname[0]

    name = fname

    @property
    def value(self):
        """generic attribute name to present this PV element's value.
        """
        if self._getPV.connected:
            return self._getPV.value
        else:
            print(f"{self._get_pvname} is not connected.")
            return None

    @value.setter
    def value(self, x):
        self._putPV.put(x, wait=False)

    @property
    def connected(self):
        return self._putPV.connected and self._getPV.connected

    def __repr__(self):
        return f"Element: {self.name}, cset: {str(self._putPV)}, rd: {str(self._getPV)}"

    def get_pv_name(self, type='readback'):
        if type == 'readback':
            pv = self._get_pvname
        elif type == 'setpoint':
            pv = self._put_pvname
        return pv

    @property
    def pvname(self):
        return self._put_pvname, self._get_pvname

    @property
    def ename(self):
        """just guess element name.
        """
        a, b = self.get_pv_name('readback'), self.get_pv_name('setpoint')
        n = set(a.rsplit(':', 1)).intersection(b.rsplit(':', 1))
        if n:
            return n.pop()
        else:
            return 'undefined'

    @property
    def readback(self):
        return [self._get_pvname]

    @property
    def setpoint(self):
        return [self._put_pvname]

    @property
    def readback_pv(self):
        return [self._getPV]

    @property
    def setpoint_pv(self):
        return [self._putPV]

    def set_auto_monitor(self, auto_monitor=True, handle='readback'):
        for i in self.readback_pv:
            i.auto_monitor = auto_monitor

    def get_auto_monitor(self, handle='readback'):
        return self.readback_pv[0].auto_monitor


class PVElementReadonly(object):
    """Unified interface for `get` to a PV, i.e. readonly.

    Examples
    --------
    >>> elem = PVElement('VA:LS1_BTS:QH_D1942:I_RD')
    >>> elem.value # get value
    """

    def __init__(self, get_pv_name):
        self._get_pvname = get_pv_name
        self._getPV = PV(get_pv_name, auto_monitor=True)

    @property
    def fname(self):
        """Default CA field name.
        """
        return self.pvname[0]

    name = fname

    @property
    def value(self):
        """generic attribute name to present this PV element's value.
        """
        if self._getPV.connected:
            return self._getPV.value
        else:
            return None

    @property
    def connected(self):
        return self._getPV.connected

    def __repr__(self):
        return f"Element: {self.name}, rd: {str(self._getPV)}"

    @property
    def pvname(self):
        return self._get_pvname,

    @property
    def ename(self):
        """just guess element name.
        """
        return self.get_pv_name('readback').rsplit(':', 1)[0]

    @property
    def readback(self):
        return [self.get_pv_name('readback')]

    @property
    def setpoint(self):
        return []

    @property
    def readback_pv(self):
        return [self._getPV]

    def get_pv_name(self, type='readback'):
        if type == 'readback':
            pv = self._get_pvname
        elif type == 'setpoint':
            pv = self._put_pvname
        return pv


def ensure_set(setpoint_pv: Union[str, List[str]],
               readback_pv: Union[str, List[str]],
               goal: Union[float, List[float]],
               tol: Union[float, List[float]] = 0.01,
               timeout: float = 10.0,
               verbose: bool = False):
    """Perform ensure CA device set operation against the given setpoint PV(s) and monitor
    the readback PV(s) reaching the goal(s) when the value discrepancy between read and set
    within the range defined by the given tolerance(s), all these actions should be finished
    or terminated in the max allowed seconds defined by timeout.

    Please note: when passing a list of PVs, the size of *setpoint_pv*, *readback_pv*, *goal*
    and *tol* parameters must be the same, while if goal and tol is defined as a single float
    number, they will be expanded to a list of that value for convenience.

    Parameters
    ----------
    setpoint_pv : str, List[str]
        [A list of] setpoint PV(s).
    readback_pv : str, List[str]
        [A list of] readback PV(s), should match the order of setpoint PVs accordingly.
    goal : float, List[float]
        [A list of] set value(s) applied to setpoint PV(s), expand to a list if single number is
        given.
    tol : float, List[float]
        [A list of] tolerance value(s) of the discrepancy between set and read, expand to a list
        if single number is given. Default is 0.01.
    timeout : float
        Max waited time in seconds of the entire set procedure, if reached, 'Timeout' should be
        returned. Default is 10.0.
    verbose : bool
        If set, show verbose log messages. Default is False.

    Examples
    --------
    >>> from phantasy import ensure_set
    >>> sp = ['FE_SCS1:PSQ1_D0726:V_CSET', 'FE_SCS1:PSQ2_D0726:V_CSET']
    >>> rp = ['FE_SCS1:PSQ1_D0726:V_RD', 'FE_SCS1:PSQ2_D0726:V_RD']
    >>> val = [10, 5]
    >>> tol = 0.8
    >>> timeout = 20
    >>> ensure_set(sp, rp, val, tol, timeout, True)
    """
    if isinstance(setpoint_pv, str):
        setpoint_pv = [setpoint_pv,]
    if isinstance(readback_pv, str):
        readback_pv = [readback_pv,]
        #return _ensure_set_single(setpoint_pv, readback_pv, goal, tol, timeout, verbose)
    #else:
    assert len(setpoint_pv) == len(readback_pv)
    return _ensure_set_array(setpoint_pv, readback_pv, goal, tol, timeout, verbose)


def _ensure_set_single(setpoint_pv, readback_pv, goal, tol=0.01, timeout=10, verbose=False):
    """Set *setpoint_pv*, such that the *readback_pv* value reaches the
    *goal* within the value discrepancy of *tol*, in the max time period of
    *timeout* second.

    Parameters
    ----------
    setpoint_pv: str
        PV name for set value.
    readback_pv: str
        PV name for readback value.
    goal : float
        The final value the readback_pv would like to reach.
    tol : float
        Value discrepancy between the set goal and the final reached value.
    timeout : float
        Maximum wait time for this set action.

    Return
    ------
    r : str
        One of 'Timeout', 'Empty' and 'PutFinished'.

    See Also
    --------
    :func:`~phantasy.library.pv.ensure_put`
    """
    if readback_pv is None:
        readback_pv = setpoint_pv
    elem = PVElement(setpoint_pv, readback_pv)
    return ensure_put(elem, goal, tol, timeout, verbose)


def _ensure_set_array(setpoint_pvs, readback_pvs, goals, tols=0.01, timeout=10, verbose=False):
    """Set a list of PVs (setpoint_pv), such that the readback values (readback_pv) all reach the
    goals (goal) within the value discrepancy of tolerance (tol), in the max time period in
    seconds (timeout).
    """
    nsize = len(setpoint_pvs)
    fgcolors = random.choices(COLORS, k=nsize)
    if isinstance(goals, (float, int)):
        goals = [goals] * nsize
    if isinstance(tols, (float, int)):
        tols = [tols] * nsize
    _dval = np.array([False] * nsize)

    def is_equal(v, goal, tol):
        return abs(v - goal) < tol

    def cb(q, idx, **kws):
        val = kws.get('value')
        ts = kws.get('timestamp')
        _dval[idx] = is_equal(val, goals[idx], tols[idx])
        if verbose:
            if _dval[idx]:
                is_reached = "[OK]"
            else:
                is_reached = ""
            click.secho(
                f"[{epoch2human(ts)[:-3]}]{kws.get('pvname')} now is {val:<6g} (goal: {goals[idx]}){is_reached}",
                fg=fgcolors[idx])
        q.put((_dval.all(), ts))

    _read_PVs = []
    q = Queue()
    for idx, pv in enumerate(readback_pvs):
        o = epics.PV(pv, partial(cb, q, idx))
        _read_PVs.append(o)

    def _clear():
        for i in _read_PVs:
            i.clear_callbacks()
            del i

    t0 = time.time()
    [epics.caput(ipv, iv) for ipv, iv in zip(setpoint_pvs, goals)]
    _dval = np.array([
        is_equal(ipv.value, igoal, itol)
        for ipv, igoal, itol in zip(_read_PVs, goals, tols)
    ])
    all_done = _dval.all()
    while True:
        try:
            if all_done: raise PutFinishedException
            all_done, ts = q.get(timeout=timeout)
            if ts - t0 > timeout: raise TimeoutError
        except Empty:
            ret = "Empty"
            _clear()
            if verbose:
                click.secho(f"[{epoch2human(time.time())[:-3]}]Return '{ret}'", fg='red')
            break
        except TimeoutError:
            ret = "Timeout"
            _clear()
            if verbose:
                click.secho(f"[{epoch2human(time.time())[:-3]}]Return '{ret}'", fg='yellow')
            break
        except PutFinishedException:
            ret = 'PutFinished'
            _clear()
            if verbose:
                click.secho(f"[{epoch2human(time.time())[:-3]}]Return '{ret}'", fg='green')
            break
    return ret
