#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from .device_processors import pm_processor
from .device_processors import vd_processor

SLOW_MONI_TYPES = ("PM", "VD", )


device_processors = {
    'PM': pm_processor,
    'VD': vd_processor,
}


def process_devices(elems, **kws):
    for elem in elems:
        if elem.family in SLOW_MONI_TYPES:
            process_device(elem, elem.family, **kws)


def process_device(elem, dtype, **kws):
    q_msg = kws.get('msg_queue', None)
    etype, ename = elem.family, elem.name

    msg1 = "[{}] - Processing [{}] {}...".format(time_now(), etype, ename)
    print(msg1)
    if q_msg is not None:
        q_msg.put((-1, msg1))
    #
    device_processors[dtype](elem)
    #
    msg2 = "[{}] - Device {} is processed.".format(time_now(), ename)
    print(msg2)
    if q_msg is not None:
        q_msg.put((-1, msg2))


def time_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
