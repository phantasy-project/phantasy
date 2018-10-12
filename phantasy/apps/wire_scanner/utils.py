#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        if val == self.goal
            self.q.put(val)
            idx, obj = kws.get('cb_info')
            obj.remove_callback(idx)


def wait(pv, goal, timeout=60):
    q = Queue(1)
    cid = pv.add_callback(QCallback(q, goal))
    try:
        if q.get(timeout=timeout):
            print("unblocking, pv reaches {}...".format(goal))
    except Empty:
        print("Timeout")
        pv.remove_callback(cid)

