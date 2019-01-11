# -*- coding: utf-8 -*-

import re
from PyQt5.QtWidgets import QFileDialog


def get_open_filename(obj, filter=None, caption=None):
    """Get file for reading.

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
    r : tuple
        Selected filename and its extension.
    """
    filepath, filter = QFileDialog.getOpenFileName(obj, caption, "", filter)
    if not filepath:
        return None, None
    ext = re.match(r'.*\.(.*)\)', filter).group(1)
    return filepath, ext


def get_save_filename(obj, filter=None, cdir='', caption=None):
    """Get file for saving data.

    Parameters
    ----------
    obj :
        Parent widget of QFileDialog.
    filter : str
        File fileters, see `QFileDialog.setNameFilter`,
        e.g. ``JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)``
    cdir : str
        Current directory to locate.
    caption : str
        Caption of file dialog.

    Returns
    -------
    r : tuple
        Selected filename and its extension.
    """
    filepath, filter = QFileDialog.getSaveFileName(
            obj, caption, cdir, filter)
    if not filepath:
        return None, None
    ext = re.match(r'.*\.(.*)\)', filter).group(1)
    if re.match(r'.*\..*', filepath) is not None:
        filename = re.sub(r'([^.]*)(\.)(.*)', r'\1.{}'.format(ext), filepath)
    else:
        filename = re.sub(r'(.*)', r'\1.{}'.format(ext), filepath)

    return filename, ext


def uptime(t):
    """Convert *t* in second to uptime with the tuple of days, hours,
    minutes, and seconds, and return string of uptime.

    Examples
    --------
    >>> assert uptime(12345) == "03:25:45"
    >>> assert uptime(123455) == "1 day, 10:17:35"
    >>> assert uptime(1234555) == "14 days, 06:55:55"
    """
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    days = int(t / DAY)
    hours = int((t % DAY) / HOUR)
    minutes = int((t % HOUR) / MINUTE)
    seconds = int(t % MINUTE)

    s = ''
    if days > 0:
        s += str(days) + " " + (days == 1 and "day" or "days") + ", "
    s += '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return s


if __name__ == '__main__':
    t = 12345
    assert uptime(t) == "03:25:45"

    t = 123455
    assert uptime(t) == "1 day, 10:17:35"

    t = 1234555
    assert uptime(t) == "14 days, 06:55:55"
