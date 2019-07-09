#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import time


SLOW_MONI_TYPES = ("PM", "VD", )


def process_devices(elems):
    for elem in elems:
        if elem.family in SLOW_MONI_TYPES:
            process_device(elem, elem.family)


def process_device(elem, dtype):
    if dtype == "PM":
        _process_pm_device(elem)
    elif dtype == "VD":
        _process_vd_device(elem)


def _process_pm_device(elem):
    etype, ename = elem.family, elem.name
    print("[{}] Processing [{}] {}...".format(
        time_now(), etype, ename))
    time.sleep(2.0)
    print("[{}] Device {} is processed.".format(
        time_now(), ename))


def _process_vd_device(elem):
    etype, ename = elem.family, elem.name
    print("[{}] Processing [{}] {}...".format(
        time_now(), etype, ename))
    time.sleep(2.0)
    print("[{}] Device {} is processed.".format(
        time_now(), ename))


def time_now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
