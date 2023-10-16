# -*- coding: utf-8 -*-
"""EPICS tools.
"""

from epics import caget as epics_caget
from epics import caput as epics_caput
from epics import cainfo as epics_cainfo
from epics import camonitor as epics_camonitor
from epics import ca
from epics import get_pv

import weakref
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


class DataFetcher:
    """ DataFetcher provides a more robust, flexible and efficient way for fetching data through CA.
    It's wrapping the `fetch_data` function but offers less overhead in terms of managing the
    working objects.

    Parameters
    ----------
    pvlist : List[str]
        A list of PVs with unique names.

    Keyword Arguments
    -----------------
    timeout : float
        The overall connection timeout for all PVs, defaults 5 seconds, meaning if in 5 seconds
        not all the PVs can be reached, raise an error; increase the timeout by set timeout value
        via <DataFetcher instance>.timeout = <new timeout>.
    verbose : bool
        If set, show more print out messages, defaults False.

    See Also
    --------
    fetch_data

    Examples
    --------
    >>> from phantasy import DataFetcher
    >>> pvs = [
    >>>  'VA:LS1_CA01:CAV1_D1127:PHA_RD',
    >>>  'VA:LS1_CA01:CAV2_D1136:PHA_RD',
    >>>  'VA:LS1_CA01:CAV3_D1142:PHA_RD',
    >>>  'VA:SVR:NOISE'
    >>> ]
    >>> # instantiation
    >>> data_fetcher = DataFetcher(pvs, timeout=10)
    >>> # fetch the data, see fetch_data() for the parameters definition.
    >>> avg, df = data_fetcher(time_span=2.0, verbose=True)
    >>> # another fetch
    >>> avg, _ = data_fetcher(1.0)
    >>> # clean up (optional)
    >>> data_fetcher.clean_up()
    >>> # Re-instantiation is required after clean_up if working with the DataFetcher with
    >>> # the same variable name, e.g. data_fetcher = DataFetcher(pvs), ...
    >>> # If working with a large list of PVs for multiple DataFetcher instances,
    >>> # cleaning up the not-needed DataFetcher instances is useful to save computing resources.
    """

    def __init__(self, pvlist: List[str], **kws):
        self.__check_unique_list(pvlist)
        self._pvlist = pvlist
        self._npv = len(pvlist)
        self._pvs = [None] * self._npv  # weakrefs
        self._cb_idx = [None] * self._npv  # cb indices
        #
        self.timeout = kws.get('timeout', 5)
        self.verbose = kws.get('verbose', False)
        # start data accumulating if set.
        self._run = False
        #
        self.pre_setup()

    def __check_unique_list(self, pvlist: List[str]):
        if len(set(pvlist)) != len(pvlist):
            raise RuntimeError("Duplicated PV names!")

    def __check_all_pvs(self):
        # return a boolean if all PVs are ready to work or not.
        return all(self._cb_idx) and \
                all((o() is not None and o().connected for o in self._pvs))

    @property
    def timeout(self):
        """float: Maximum allowed waiting time in seconds before all PVs are ready to work.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, t: float):
        self._timeout = t

    def is_pvs_ready(self):
        """Return if all PVs are ready to work or not.
        """
        return self._all_pvs_ready

    def __del__(self):
        """Cleaning up work.
        """
        print("Clean up callbacks")
        self.clean_up()

    def clean_up(self):
        [o().remove_callback(idx) for o, idx in zip(self._pvs, self._cb_idx)]

    def pre_setup(self):
        """Preparation for the data fetch procedure.
        """
        # clear the data container
        self._data_list = [[] for _ in range(self._npv)]
        # if all PVs are ready, just return
        self._all_pvs_ready = self.__check_all_pvs()
        if self._all_pvs_ready:
            return
        #
        t0 = time.perf_counter()

        def _cb(idx: int, **kws):
            if self._run:
                val = kws.get('value')
                self._data_list[idx].append(val)
                if self.verbose:
                    ts = kws.get('timestamp')
                    click.secho(
                        f"[{epoch2human(ts)[:-3]}] Get {kws.get('pvname')}: {val:<6g}",
                        fg="blue")

        #
        q = Queue()
        conn_sts = [False] * self._npv

        def _f(i: int, pvname: str, conn: bool, **kws):
            if conn:
                conn_sts[i] = True
                if all(conn_sts):
                    q.put(True)

        for i, pvname in enumerate(self._pvlist):
            o = get_pv(pvname,
                       connection_callback=partial(_f, i),
                       auto_monitor=True)
            if self._cb_idx[i] is None:
                self._cb_idx[i] = o.add_callback(partial(_cb, i),
                                                 with_ctrlvars=False)
            self._pvs[i] = weakref.ref(o)

        while True:
            try:
                v = q.get(timeout=self._timeout)
                if v: raise PVsAreReady
            except Empty:
                print(f"Failed connecting to all PVs in {self._timeout:.1f}s.")
                if self.verbose:
                    not_conn_pvs = [
                        o().pvname for o in self._pvs if not o().connected
                    ]
                    click.secho(
                        f"{len(not_conn_pvs)} PVs are not established in {self._timeout:.1f}s.",
                        fg="red")
                    click.secho("{}".format('\n'.join(not_conn_pvs)), fg="red")
                break
            except PVsAreReady:
                if self.verbose:
                    click.secho(
                        f"Established {self._npv} PVs in {(time.perf_counter() - t0) * 1e3:.1f}ms.",
                        fg="green")
                self._all_pvs_ready = True
                break

    def __call__(self,
                 time_span: float = 5.0,
                 abs_z: float = None,
                 with_data: bool = False,
                 **kws):
        verbose = kws.get('verbose', self.verbose)
        self.verbose = verbose
        # initial data list
        self._data_first_shot = [o().value for o in self._pvs]
        self._data_list = [[] for i in range(self._npv)]
        _tq = Queue()
        _evt = Event()

        def _tick_down(q):
            self._run = True
            while True:
                if _evt.is_set():
                    self._run = False
                    break
                q.put(time.time())
                time.sleep(0.001)

        th = Thread(target=_tick_down, args=(_tq, ))
        th.start()
        t0 = time.time()
        t1 = t0 + time_span
        while True:
            try:
                t = _tq.get(timeout=5)
                if t >= t1: raise FetchDataFinishedException
            except FetchDataFinishedException:
                _evt.set()
                if verbose:
                    click.secho(f"Finished fetching data in {t - t0:.1f}s")
                break
        # amend the first element of the list container with initial shot
        for i in range(self._npv):
            if not self._data_list[i]:
                self._data_list[i] = [self._data_first_shot[i]]
        #
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
        df0 = pd.DataFrame(self._data_list, index=self._pvlist)
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


def fetch_data(pvlist: List[str],
               time_span: float = 5.0,
               abs_z: float = None,
               with_data=False,
               verbose=False,
               **kws):
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

    Keyword Arguments
    -----------------
    timeout : float
        Connection timeout for all PVs, defaults 5.0 seconds.

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
    data_fetcher = DataFetcher(pvlist,
                               timeout=kws.get('timeout', 5),
                               verbose=verbose)
    avg, df = data_fetcher(time_span, abs_z, with_data, verbose=verbose)
    return avg, df


class PVsAreReady(Exception):

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)


def establish_pvs(pvs: list, timeout: float = 3.0, **kws):
    """Establish the connections for a given list of PVs within the defined time in seconds.

    Parameters
    ----------
    pvs : list
        A list of PV names.
    timeout : float
        Maximum wait time in seconds allowed before return.

    Keyword Arguments
    -----------------
    verbose : bool
        If set, output log messages.

    Returns
    -------
    r : list
        A list of PVs that are not ready, otherwise None.
    """
    #
    enable_log = kws.get('verbose', False)
    if enable_log:
        t0 = time.perf_counter()
    q = Queue()
    n_pv = len(pvs)
    con_sts = [False] * n_pv

    def _f(i, pvname, conn, **kws):
        if conn:
            con_sts[i] = True
            if all(con_sts):
                q.put(True)

    for i, pv in enumerate(pvs):
        get_pv(pv, connection_callback=partial(_f, i))

    while True:
        try:
            v = q.get(timeout=timeout)
            if v: raise PVsAreReady
        except Empty:
            not_connected_pvs = [
                i for i in pvs if not epics.get_pv(i).connected
            ]
            if enable_log:
                print(
                    f"{len(not_connected_pvs)} PVs are not established in {(time.perf_counter() - t0) * 1e3:.1f} ms."
                )
            return not_connected_pvs
        except PVsAreReady:
            if enable_log:
                print(
                    f"Established {n_pv} PVs in {(time.perf_counter() - t0) * 1e3:.1f} ms."
                )
            return None


if __name__ == '__main__':
    pvs = [
        'FE_ISRC1:BEAM:ELMT_BOOK',
        'FE_ISRC1:BEAM:A_BOOK',
        'FE_ISRC1:BEAM:Z_BOOK',
        'FE_ISRC1:BEAM:Q_BOOK',
        'ACC_OPS:BEAM:Q_STRIP',
        'FE_ISRC2:BEAM:ELMT_BOOK',
        'FE_ISRC2:BEAM:A_BOOK',
        'FE_ISRC2:BEAM:Z_BOOK',
        'FE_ISRC2:BEAM:Q_BOOK',
        #'MYPV',
        'ACS_DIAG:DEST:ACTIVE_ION_SOURCE',
        'ACS_DIAG:DEST:FSEE_LINE_RD',
        'ACS_DIAG:DEST:BEAMDEST_RD',
    ]
    # with open("pvlist.txt", "r") as fp:
    #     pvs = fp.read().split()
    # print(establish_pvs(pvs, timeout=1, verbose=True))
    # print([epics.get_pv(i).value for i in pvs])

    from phantasy import MachinePortal
    mp = MachinePortal("FRIB", "LINAC")
    lat = mp.work_lattice_conf

    pvs = []
    for i in lat:
        pvs.extend(i.pv())

    all_pvs = set(pvs)
    print(f"Total # of PVs: {len(all_pvs)}")
    r = establish_pvs(all_pvs, timeout=5, verbose=True)
    if r is not None:
        print("Non-connected PVs are:")
        for i in sorted(r):
            print(i)
