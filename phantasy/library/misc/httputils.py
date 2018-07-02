#!/usr/bin/env python

"""Multi-threading enabled HTTP fetch.

Tong Zhang <zhangt@frib.msu.edu>
2017-08-04 10:49:54 AM EDT
"""

import threading

try:
    import Queue
except ImportError:
    import queue


def cofetch(f):
    """Decorator support *f* with multi-threading processing.

    >>> @cofetch
        def get_data(urls):
            return requests.get(urls).json()

    In this example, *urls* is a list of URL, returned one is a dict
    with key of each element of *urls* and value of original returned json
    list.
    """
    class _WorkerThread(threading.Thread):
        def __init__(self, q, f, target, **kws):
            super(self.__class__, self).__init__(target=target)
            self._q = q
            self._f = f
            self._t = target
            self._k = kws
        def run(self):
            while True:
                k, url = self._q.get()
                r = self._f(url, **self._k)
                self._t[k] = r
                self._q.task_done()

    def wrapper(x_list, **kws):
        r = {}
        q = Queue.Queue()
        n = len(x_list)
        for _ in range(n):
            w = _WorkerThread(q, f, r, **kws)
            w.daemon = True
            w.start()
        for x in x_list:
            q.put((x, x))
        q.join()
        return r

    return wrapper
