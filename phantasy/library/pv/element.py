# -*- coding: utf-8 -*-

"""Class interface for generic RD/SET PVs w.r.t. CaField.
"""
from epics import PV
from .epics_tools import ensure_put


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


def ensure_set(setpoint_pv, readback_pv, goal, tol=0.01, timeout=10):
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
    return ensure_put(elem, goal, tol, timeout)
