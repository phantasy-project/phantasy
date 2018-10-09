# -*- coding: utf-8 -*-

import epics
import time
import re

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox


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
        self._putPV = epics.PV(put_pv_name)
        self._getPV = epics.PV(get_pv_name)

    @property
    def fname(self):
        """Default CA field name.
        """
        return "<generic field>"

    @property
    def value(self):
        """generic attribute name to present this PV element's value.
        """
        return self._getPV.get()

    @value.setter
    def value(self, x):
        self._putPV.put(x)

    @property
    def connected(self):
        return self._putPV.connected and self._getPV.connected

    def __repr__(self):
        return str(self._getPV), str(self._putPV)

    @property
    def get_pvname(self):
        return self._get_pvname

    @property
    def put_pvname(self):
        return self._put_pvname

    @property
    def pvname(self):
        return self._put_pvname, self._get_pvname

    @property
    def name(self):
        """just guess element name.
        """
        a, b = self.get_pvname, self.put_pvname
        n = set(a.rsplit(':', 1)).intersection(b.rsplit(':', 1))
        if n:
            return n.pop()
        else:
            return 'undefined'

    @property
    def readback(self):
        return [self.get_pvname]

    @property
    def setpoint(self):
        return [self.put_pvname]


class PVElementReadonly(object):
    """Unified interface for `get` to a PV, i.e. readonly.

    Examples
    --------
    >>> elem = PVElement('VA:LS1_BTS:QH_D1942:I_RD')
    >>> elem.value # get value
    """
    def __init__(self, get_pv_name):
        self._get_pvname = get_pv_name
        self._getPV = epics.PV(get_pv_name)

    @property
    def fname(self):
        """Default CA field name.
        """
        return "<generic field>"

    @property
    def value(self):
        """generic attribute name to present this PV element's value.
        """
        return self._getPV.get()

    @property
    def connected(self):
        return self._getPV.connected

    def __repr__(self):
        return str(self._getPV)

    @property
    def get_pvname(self):
        return self._get_pvname

    @property
    def pvname(self):
        return (self._get_pvname,)

    @property
    def name(self):
        """just guess element name.
        """
        return self.get_pvname.rsplit(':', 1)[0]

    @property
    def readback(self):
        return [self.get_pvname]


def delayed_exec(f, delay, *args, **kws):
    """Execute *f* after *delay* msecm `*args` and `**kws` is for *f*.
    """
    def func():
        return f(*args, **kws)
    QTimer.singleShot(delay, func)


def milli_sleep(qApp, msec):
    t0 = time.time()
    while (time.time() - t0) * 1000 < msec:
        qApp.processEvents()


def delayed_check_pv_status(obj, pvelem, delay=1000):
    """Check PV element connected or not.

    Parameters
    ----------
    obj :
        Widget, as parent.
    pvelem : obj
        Instance of `epics.PV`, `PVElement`, `PVElementReadonly`.
    delay : float
        Delay milliseconds to check PV status.
    """
    def check_status(elem):
        if not elem.connected:
            QMessageBox.warning(obj, "Warning",
                    "Cannot connect to the input PV(s).",
                    QMessageBox.Ok)
    QTimer.singleShot(delay, lambda: check_status(pvelem))
