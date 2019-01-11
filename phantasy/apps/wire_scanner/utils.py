#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from mpl4qt.widgets.utils import MatplotlibCurveWidgetSettings

_LOGGER = logging.getLogger(__name__)

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


class QCallback(object):
    def __init__(self, q, goal):
        self.q = q
        self.goal = goal

    def __call__(self, **kws):
        val = kws.get('value')
        if val == self.goal:
            self.q.put(val)
            idx, obj = kws.get('cb_info')
            obj.remove_callback(idx)


def wait(pv, goal, timeout=60):
    if pv.value == goal:
        _LOGGER.warning("Already reached {}...".format(goal))
        return
    q = Queue(1)
    cid = pv.add_callback(QCallback(q, goal))
    try:
        if q.get(timeout=timeout):
            _LOGGER.info("{} reached, unblocking...".format(goal))
    except Empty:
        _LOGGER.warning("Timeout, no changes detected.")
        pv.remove_callback(cid)


def find_dconf():
    """Find parameter configuration file for wire-scanners.
    searching the following locations:
    * ~/.phantasy/ws.ini
    * /etc/phantasy/ws.ini
    * package location: apps/wire_scanner/config/ws.ini
    """
    home_conf = os.path.expanduser('~/.phantasy/ws.ini')
    sys_conf = '/etc/phantasy/ws.ini'
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config/ws.ini')


def find_mplconf():
    """Find configuration file (JSON) for matplotlibcurvewidget,
    searching the following locations:
    * ~/.phantasy/mpl_settings_ws.json
    * /etc/phanasy/mpl_settings_ws.json
    * package root location for this apps/wire_scanner/config/mpl_settings_ws.json
    """
    home_conf = os.path.expanduser('~/.phantasy/mpl_settings_ws.json')
    sys_conf = '/etc/phantasy/mpl_settings_ws.json'
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config/mpl_settings_ws.json')


def apply_mplcurve_settings(mplcurveWidget, json_path=None):
    """Apply JSON settings read from *json_path* to *mplcurveWidget*.

    Parameters
    ----------
    mplcurveWidget : MatplotlibCurveWidget
        Instance of MatplotlibCurveWidget.
    json_path : str
        Path of JSON settings file.
    """
    if json_path is None:
        json_path = find_mplconf()
    s = MatplotlibCurveWidgetSettings(json_path)
    mplcurveWidget.apply_mpl_settings(s)
