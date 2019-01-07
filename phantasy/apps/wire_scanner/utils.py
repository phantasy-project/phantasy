#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

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

