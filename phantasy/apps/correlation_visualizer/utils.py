# -*- coding: utf-8 -*-

import epics
import time
import re
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog


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
    def ename(self):
        """just guess element name.
        """
        a, b = self.get_pvname, self.put_pvname
        n = set(a.rsplit(':', 1)).intersection(b.rsplit(':', 1))
        if n:
            return n.pop()
        else:
            return 'undefined'


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
    def ename(self):
        """just guess element name.
        """
        return self.get_pvname.rsplit(':', 1)[0]


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


def get_save_filename(obj, filter=None, caption=None):
    """Get file for saving data.

    Parameters
    ----------
    obj :
        Parent widget of QFileDialog.
    filter : str
        File fileters, see `QFileDialog.setNameFilter`,
        e.g. ``JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)``
    caption : str
        Caption of file dialog.

    Returns
    -------
    r : str
        Selected filename.
    """
    filepath, filter = QFileDialog.getSaveFileName(
            obj, caption, "", filter)
    if not filepath:
        return None
    ext = re.match(r'.*\.(.*)\)', filter).group(1)
    if re.match(r'.*\..*', filepath) is not None:
        filename = re.sub(r'([^.]*)(\.)(.*)', r'\1.{}'.format(ext), filepath)
    else:
        filename = re.sub(r'(.*)', r'\1.{}'.format(ext), filepath)

    return filename

