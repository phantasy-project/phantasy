# -*- coding: utf-8 -*-
"""EPICS tools.
"""

from epics import caget as epics_caget
from epics import caput as epics_caput
from epics import cainfo as epics_cainfo
from epics import camonitor as epics_camonitor
from epics import ca

import epics
import logging
import time
from functools import partial
from queue import Queue, Empty
from typing import List
import click
from threading import Thread, Event
import pandas as pd

from phantasy.library.exception import TimeoutError
from phantasy.library.exception import GetFinishedException
from phantasy.library.exception import PutFinishedException
from phantasy.library.exception import FetchDataFinishedException
from phantasy.library.misc import epoch2human

_LOGGER = logging.getLogger(__name__)


def caget(pvname, count=None, timeout=None, **kws):
    return epics_caget(pvname, **kws)


def caput(pvname, value, timeout=30, **kws):
    if kws.get('callback', None) is None:
        return epics_caput(pvname,
                           value,
                           wait=kws.get('wait', True),
                           timeout=timeout)
    else:
        pass
    # create convenient function to work with CaElement.
    # FIX caget error, when working with epics package.


def cainfo(pvname, **kws):
    return epics_cainfo(pvname, kws.get('print_out', True))


def camonitor(pvname, callback=None, **kws):
    return epics_camonitor(pvname, kws.get('writer', None), callback)


def ensure_get(pvname, timeout=None):
    """Get the not-None value from *field* object within the max *timeout* time period in
    seconds.

    Parameters
    ----------
    pvname : str
        PV name string.
    timeout : float
        Maximum wait time for this action, default is 5.0 seconds.

    Return
    ------
    r :
        Value from caget(pvname) or None
    """
    def _on_val_changed(q_val, **kws):
        q_val.put((kws.get('value'), time.time()))

    timeout = 5 if timeout is None else timeout
    q_val = Queue()
    chid = epics.ca.create_channel(pvname)
    try:
        _, _, evtid = epics.ca.create_subscription(chid,
                                                   callback=partial(
                                                       _on_val_changed, q_val))
    except epics.ca.ChannelAccessException:
        print("Error: ChannelAccessException")
        return None
    t0 = time.time()
    while True:
        try:
            v, ts = q_val.get(timeout=timeout)
            if ts - t0 > timeout: raise TimeoutError
            if v is not None:
                raise GetFinishedException
        except Empty:
            r = None
            break
        except GetFinishedException:
            r = v
            break
    epics.ca.clear_subscription(evtid)
    return r


def ensure_put(field, goal, tol=None, timeout=None, verbose=False):
    """Put operation to *field* object, ensure to reach the value
    of *goal* within the discrepancy tolerance defined by *tol*, within the
    time period defined by *timeout*.

    Parameters
    ----------
    field : CaField, PVElement
        Instance of dynamic field of CaElement or PVElement.
    goal : float
        The final value that the field of element would like to reach.
    tol : float
        Tolerance for discrepancy between current readback
        value and the set goal, default is 0.01.
    timeout : float
        Maximum wait time, default is 10.0 sec.

    Returns
    -------
    r : str
        One of "Empty" (1), "Timeout" (2) and "PutFinished" (3), (1) and (2)
        indicate operation reaches defined timeout, only (3) indicates put
        works as expected, (1) is rare.

    Examples
    --------
    >>> # get element, e.g. elem = mp.get_elements(name='*D0874*')[0]
    >>> # set 'V' field of element to 1000
    >>> fld = elem.get_field('V')
    >>> ensure_put(fld, 1000)
    >>> # set 'V' field to 1, but with *tol* never could be reached,
    >>> # will return after 10 sec.
    >>> ensure_put(fld, 1, tol=1e-10)
    >>> # if set *timeout* as 2, will return after 2 sec.
    >>> ensure_put(fld, 1, tol=1e-10, timeout=2.0)
    >>> # ensure_put as the method of CaElement
    >>> elem.ensure_put('V', goal=1, tol=1e-3, timeout=1.0)

    See Also
    --------
    :func:`~phantasy.library.PVElement`
    """
    tol = 0.01 if tol is None else tol
    timeout = 10.0 if timeout is None else timeout

    def callback(sq, fld, **kws):
        val = kws.get('value')
        ts = kws.get('timestamp')
        sq.put((fld.value, ts))

    def is_equal(v, goal, tol):
        return abs(v - goal) < tol

    pv = field.readback_pv[0]
    am0 = field.get_auto_monitor()
    field.set_auto_monitor()
    q = Queue()
    cid = pv.add_callback(partial(callback, q, field))
    field.value = goal
    t0 = time.time()
    v = field.value
    ename = field.ename
    fname = field.name
    while True:
        try:
            if is_equal(v, goal, tol): raise PutFinishedException
            v, ts = q.get(timeout=timeout)
            if verbose:
                print(
                    f"[{epoch2human(ts)[:-3]}]{ename}[{fname}] now is {v} (goal: {goal})"
                )
            if ts - t0 > timeout: raise TimeoutError
            _LOGGER.debug(
                f"Field '{fname}' of '{ename}' reached: {v}[{goal}].")
        except Empty:
            _LOGGER.info(
                f"Field '{fname}' of '{ename}' reached: {field.value}.")
            pv.remove_callback(cid)
            field.set_auto_monitor(am0)
            ret = "Empty"
            if verbose:
                print(
                    f"[{epoch2human(ts)[:-3]}]{ename}[{fname}] now is {field.value} (goal: {goal})"
                )
                print(f"Return '{ret}'")
            break
        except TimeoutError:
            _LOGGER.info(
                f"Field '{fname}' of '{ename}' reached: {field.value}.")
            pv.remove_callback(cid)
            field.set_auto_monitor(am0)
            ret = "Timeout"
            if verbose:
                print(
                    f"[{epoch2human(ts)[:-3]}]{ename}[{fname}] now is {field.value} (goal: {goal})"
                )
                print(f"Return '{ret}'")
            break
        except PutFinishedException:
            _LOGGER.info(
                f"Field '{fname}' of '{ename}' reached: {field.value}.")
            pv.remove_callback(cid)
            field.set_auto_monitor(am0)
            ret = "PutFinished"
            if verbose:
                print(
                    f"[{epoch2human(ts)[:-3]}]{ename}[{fname}] now is {field.value} (goal: {goal})"
                )
                print(f"Return '{ret}'")
            break
    return ret


def caget_many(pvlist,
               as_string=False,
               count=None,
               as_numpy=True,
               timeout=1.0,
               raises=False):
    """get values for a list of PVs
    This does not maintain PV objects, and works as fast
    as possible to fetch many values.

    Original author: Bruno Martins.
    """

    chids = [
        ca.create_channel(name, auto_cb=False, connect=False)
        for name in pvlist
    ]

    t = time.time()
    for chid in chids:
        ca.connect_channel(chid, timeout=0.001)

    pvstatus = [ca.isConnected(chid) for chid in chids]

    t = time.time()

    while not all(pvstatus) and time.time() - t < timeout:
        ca.poll()
        pvstatus = [ca.isConnected(chid) for chid in chids]

    for chid, connected in zip(chids, pvstatus):
        if connected:
            ca.get(chid,
                   count=count,
                   as_string=as_string,
                   as_numpy=as_numpy,
                   wait=False)

    out = [
        ca.get_complete(chid,
                        count=count,
                        as_string=as_string,
                        as_numpy=as_numpy,
                        timeout=timeout) if connected else None
        for chid, connected in zip(chids, pvstatus)
    ]

    if raises and None in out:
        raise RuntimeError('Not all PVs were found')

    return out


def fetch_data(pvlist: List[str],
               time_span: float = 5.0,
               abs_z: float = None,
               with_data=False,
               verbose=False):
    """Fetch the readback data from a list of given PVs in the given time period in seconds,
    trim the data beyond the given z-score (absolute value), and return the data of interest.

    Parameters
    ----------
    pvlist : List[str]
        A list of PVs.
    time_span : float
        The total time period for fetching data, [second], defaults to 5.0.
    abs_z : float
        The absolute value of z-score, drop the data beyond, if not set, keep all the data.
    with_data : bool
        If set, return data array as the second element of the returned tuple.
    verbose : bool
        If set, print out log messages.

    Returns
    -------
    r : tuple
        Tuple of averaged value of array [and the full data array if 'with_data' is True].

    Examples
    --------
    >>> from phantasy import fetch_data
    >>> pvs = [
    >>>  'VA:LS1_CA01:CAV1_D1127:PHA_RD',
    >>>  'VA:LS1_CA01:CAV2_D1136:PHA_RD',
    >>>  'VA:LS1_CA01:CAV3_D1142:PHA_RD',
    >>>  'VA:SVR:NOISE'
    >>> ]
    >>> # Fetch the average readings of the given list of PVs, for 5 seconds, and drop the data
    >>> # which |z-score| > 3, show the verbose messages.
    >>> avg, _ = fetch_data(pvs, 5, 3, verbose=True)
    >>> # return the data table after filtering together with the average readings
    >>> avg, data = fetch_data(pvs, 5, 3, verbose=True, with_data=True)
    >>> # return the average without data filtering.
    >>> avg, _ = fetch_data(pvs, 5)
    """
    _tq = Queue()
    nsize = len(pvlist)
    _data_list = [[] for _ in range(nsize)]

    def _cb(idx, **kws):
        val = kws.get('value')
        ts = kws.get('timestamp')
        if verbose:
            click.secho(
                f"[{epoch2human(ts)[:-3]}]Get {kws.get('pvname')}: {val:<6g}",
                fg="blue")
        _data_list[idx].append(val)

    _pvs = []
    for idx, pv in enumerate(pvlist):
        o = epics.PV(pv, partial(_cb, idx))
        _pvs.append(o)

    def _clear():
        for i in _pvs:
            i.clear_callbacks()
            del i

    t0 = time.time()
    _evt = Event()

    def _tick_down(q):
        while True:
            if _evt.is_set():
                break
            q.put(time.time())
            time.sleep(0.05)

    th = Thread(target=_tick_down, args=(_tq, ))
    th.start()
    while True:
        try:
            t = _tq.get(timeout=5)
            if t - t0 >= time_span: raise FetchDataFinishedException
        except FetchDataFinishedException:
            _evt.set()
            ret = "FetchDataFinished"
            _clear()
            break

    def _pack_data(_df: pd.DataFrame):
        # pack the data for return
        if with_data:
            n_col = _df.shape[1]
            _col_mean = _df.mean(axis=1)
            _col_std = _df.std(ddof=0, axis=1)
            _df['#'] = _df.apply(lambda i: n_col - i.isna().sum(), axis=1)
            _df['mean'] = _col_mean
            _df['std'] = _col_std
            return _df
        else:
            return None

    # raw data
    df0 = pd.DataFrame(_data_list, index=pvlist)
    # mean, std
    _avg, _std = df0.mean(axis=1), df0.std(ddof=0, axis=1)
    if abs_z is None:
        return _avg.to_numpy(), _pack_data(df0)
    # - mean
    df_sub = df0.sub(_avg, axis=0)
    # idx1: df_sub == 0
    idx1 = df_sub == 0.0
    # ((- mean) / std) ** 2
    df1 = df_sub.div(_std, axis=0)**2
    idx2 = df1 <= abs_z**2
    # data of interest
    df = df0[idx1 | idx2]
    # mean array
    avg_arr = df.mean(axis=1).to_numpy()
    return avg_arr, _pack_data(df)
