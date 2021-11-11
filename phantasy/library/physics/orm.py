#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for orbit response matrix calculation.
"""

import time
from functools import reduce

import numpy as np
import numpy.linalg as linalg

from phantasy.library.misc import epoch2human
from phantasy.library.misc import truncate_number

from .devices import process_devices

TS_FMT = "%Y-%m-%d %H:%M:%S"


def get_orm(correctors, monitors, **kws):
    """Calculate orbit response matrix (ORM) with defined input parameters.

    The length of *monitors* is ``m``, the length of correctors is ``n``,
    if both x and y directions are monitored, the length of *monitors* should
    be doubled. The final calculated ORM should be of the shape of ``(m, n)``.

    For each iteration of correctors updates, which could be defined by ``scan``
    keyword parameter, a serie of measured orbit data would be returned from
    :func:`get_orbit`, doing linear polynomial fitting against the feeded
    ``scan`` list of values should return one column of ORM data.
    The column-wise returned matrix is the final ORM.

    Parameters
    ----------
    correctors : List[CaElement]
        List of correctors from *lattice*.
    monitors : List[CaElement]
        List of monitors, usually BPMs, to measure the beam orbit.

    Keyword Arguments
    -----------------
    source : str
        Orbit data source, ``control`` (default) or ``model``. If ``control``
        is defined, ORM will be measured within *control* environment,
        or ORM will be from *model*, e.g. FLAME model.
    scan : array
        Scan array for correctors, unit: *rad*, default array is
        ``[-0.003, -0.0015, 0, 0.0015, 0.003]``.
    cor_field : str
        Field name for correctors, ``'ANG'`` by default.
    orb_field : tuple[str]
        Field names for monitors to retrieve orbit data, ``('X', 'Y')`` for
        *x* and *y* directions by default.
    wait : float
        Wait time after set value, in *sec*, 1.0 by default.
    reset_wait : float
        Wait time after set value to original value, in *sec*, 1.0 by default.
    xoy : str
        'x'('y') for monitoring 'x'('y') direction,'xy' for both (default).
    lattice : Lattice
        High-level lattice object.
    msg_queue : Queue
        A queue that keeps log messages.

    Returns
    -------
    ret : array
        ORM with shape ``(m, n)``.

    Todo
    ----
    case of ``source == 'model'``, require kws 'lattice'.
    """
    lattice = kws.get('lattice', None)
    source = kws.get('source', 'control')
    scan = kws.get('scan', np.linspace(-0.003, 0.003, 5))
    cor_field = kws.get('cor_field', 'ANG')
    xoy = kws.get('xoy', 'xy')
    wait = kws.get('wait', 1.0)
    reset_wait = kws.get('reset_wait', 1.0)
    q_msg = kws.get('msg_queue', None)

    m = len(monitors) * len(xoy)
    n = len(correctors)
    mat_mn = np.zeros([m, n])

    # i <-- 0, m-1
    # B[i] = \Sigma_j=0^{n-1} R[i,j] C[j]
    # ---> iff C[j] != 0 ==> B[i] = R[i,j] C[j]
    # ==> R[i,j] = B[i]/C[j]
    # ==> or: R[i,j] = polyfit(C[i], B[i], 1)[0]
    #
    ns = len(scan)
    for i, cor in enumerate(correctors):
        orbit_arr = np.zeros([len(scan), m])
        cor_val0 = cor.current_setting(cor_field)
        for iscan, val in enumerate(scan):
            setattr(cor, cor_field, val)
            time.sleep(wait)
            v_rd = getattr(cor, cor_field)
            msg = "[{0}] Set [{1:02d}] {2} [{3}]: {4:>10.6f} (RD: {5:>10.6f})".format(
                    epoch2human(time.time(), fmt=TS_FMT), i + 1, cor.name,
                    cor_field, val, v_rd)
            if q_msg is not None:
                q_msg.put(((i * ns + iscan) * 100.0 / n / ns, msg))
            print(msg)
            orbit_arr[iscan] = get_orbit(monitors, **kws)

        ## get mat_mn(k,i)
        #for k in range(m):
        #    mat_mn[k, i] = np.polyfit(scan, orbit_arr[:, k], 1)[0]
        mat_mn[:, i] = [np.polyfit(scan, orbit_arr[:, k], 1)[0] for k in range(m)]

        # reset cor and process next col
        setattr(cor, cor_field, cor_val0)
        time.sleep(reset_wait)
    return mat_mn


def get_orm_for_one_corrector(corrector, monitors, **kws):
    """Get column-wise ORM data for one corrector.

    Parameters
    ----------
    correctors : CaElement
        Selected corrector element.
    monitors : List[CaElement]
        List of monitors, usually BPMs, to measure the beam orbit.

    Keyword Arguments
    -----------------
    scan : array
        Scan array for correctors, unit: *rad*, default array is
        ``[-0.003, -0.0015, 0, 0.0015, 0.003]``.
    cor_field : str
        Field name for correctors, ``'ANG'`` by default.
    orb_field : tuple[str]
        Field names for monitors to retrieve orbit data, ``('X', 'Y')`` for
        *x* and *y* directions by default.
    wait : float
        Wait time after set value, in *sec*, 1.0 by default.
    reset_wait : float
        Wait time after set value to original value, in *sec*, 1.0 by default.
    xoy : str
        'x'('y') for monitoring 'x'('y') direction,'xy' for both (default).
    msg_queue : Queue
        A queue that keeps log messages.
    idx : int
        Index of selected corrector of all selected ones.
    ncor : int
        Total number of selected correctors.
    ndigits : int
        Number of effective digits to keep for a float number.
    keep_all : bool
        Return all measured data or not, default is False.
    tol : float
        Absolute tolerance between setpoint and readback.

    Returns
    -------
    ret : tuple
        Column-wised ORM data with the size of ``m``, if keep_all is True,
        return all data as the second element of tuple.

    See Also
    --------
    get_orm: Measurem ORM.
    """

    scan = kws.get('scan', np.linspace(-0.003, 0.003, 5))

    print("--- Scan Range: ", scan, "---")

    cor_field = kws.get('cor_field', 'ANG')
    xoy = kws.get('xoy', 'xy')
    wait = kws.get('wait', 1.0)
    reset_wait = kws.get('reset_wait', 1.0)
    idx = kws.get('idx', 0.0)  # index of correctors
    n = kws.get('ncor', 1)     # total number of correctors
    q_msg = kws.get('msg_queue', None)
    n_trun = kws.get('ndigits', 6)
    tol = kws.get('tol', 0.1)

    print(f"{corrector.name}, tol: {tol}")

    ns = len(scan)
    nn = n * ns

    m = len(monitors) * len(xoy)
    orbit_arr = np.zeros([len(scan), m])
    cor_val0 = corrector.current_setting(cor_field)
    scan_rdbk = []
    for iscan, val in enumerate(scan):
        v_to_set =  truncate_number(val, n_trun)

        # ensure put
        corrector.ensure_put(cor_field, v_to_set, tol=tol, timeout=wait)

        # setattr(corrector, cor_field, v_to_set)
        # time.sleep(wait)
        scan_rdbk.append(getattr(corrector, cor_field))

        msg = "[{0}] Set [{1:02d}] {2} [{3}]: {4:>10.6f} (RD: {5:>10.6f})".format(
                epoch2human(time.time(), fmt=TS_FMT), idx + 1, corrector.name,
                cor_field, v_to_set, getattr(corrector, cor_field))
        if q_msg is not None:
            q_msg.put(((ns * idx + iscan)* 100.0 / nn, msg))
        print(msg)
        orbit_arr[iscan] = get_orbit(monitors, **kws)

    # ensure put
    corrector.ensure_put(cor_field, cor_val0, tol=tol, timeout=reset_wait)

    # setattr(corrector, cor_field, cor_val0)
    # time.sleep(reset_wait)

    msg = "[{0}] Set [{1:02d}] {2} [{3}]: {4:>10.6f} (RD: {5:>10.6f}) [RESET]".format(
            epoch2human(time.time(), fmt=TS_FMT), idx + 1, corrector.name,
            cor_field, cor_val0, getattr(corrector, cor_field))
    if q_msg is not None:
        q_msg.put((-1, msg))
    print(msg)

    r = np.asarray([np.polyfit(scan_rdbk, orbit_arr[:, k], 1)[0] for k in range(m)])

    if kws.get('keep_all', False):
        return r, np.asarray(orbit_arr)
    else:
        return r, None


def inverse_matrix(m):
    """Get inverse matrix of *m* based on SVD approach, *m* should be general
    rectangle shaped.

    Parameters
    ----------
    m : array
        Matrix.

    Returns
    -------
    ret : array
        Inverse matrix.

    See Also
    --------
    get_orm : Measure orbit response matrix.
    """
    U, s, V = linalg.svd(m)
    min_shape = min(m.shape)
    S_inv = np.zeros(m.shape[::-1], dtype=float)
    S_inv[:min_shape, :min_shape] = np.diag(1.0/s)
    m_inv = reduce(np.dot, (V.T, S_inv, U.T))
    return m_inv


def get_orbit(monitors, **kws):
    """Get beam orbit from defined *monitors*.

    Parameters
    ----------
    monitors : List[CaElement]
        List of monitors, usually BPMs, to measure the beam orbit.

    Keyword Arguments
    -----------------
    orb_field : tuple[str]
        Field names for monitors to retrieve orbit data, ``('X', 'Y')`` for
        *x* and *y* directions by default.
    xoy : str
        'x'('y') for monitoring 'x'('y') direction,'xy' for both (default).
    rate : int
        DAQ frequency, default is 1.
    nshot : int
        Total shot number for DAQ process, default is 1.
    slow_mode_on : bool
        If set, apply processor for slow device, e.g. PM, default is True,
        set False might be useful for orbit evaluation of ORM correction.

    Returns
    -------
    ret : array
        Monitors readings as beam orbit.

    Note
    ----
    The returned array lines all 'X' readings first, then follows all 'Y's.
    """
    nshot = kws.get('nshot', 1)
    rate = kws.get('rate', 1)
    delt = 1.0 / rate
    orb_field = kws.get('orb_field', ('X', 'Y'))
    xoy = kws.get('xoy', 'xy')
    slow_mode_on = kws.get('slow_mode_on', True)
    xyfld = list(zip(range(len(xoy)), orb_field))
    arr = np.zeros((nshot, len(xoy) * len(monitors)))
    #
    if slow_mode_on:
        process_devices(monitors, **kws)
    #
    for i in range(nshot):
        a = [[getattr(elem, fld) for elem in monitors] for _, fld in xyfld]
        arr[i, :] = np.asarray(a).flatten()
        time.sleep(delt)
    return arr.mean(axis=0)


def get_correctors_settings(orm, orbit_diff, inverse=False):
    """Calculate new settings of correctors regarding to BPM readings after
    correction.

    Parameters
    ----------
    orm : array
        Orbit response matrix.
    orbit_diff : array
        Orbit (BPM readings) difference after and before correction.
    inverse : True or False
        If *orm* has already been inversed or not (default).

    Returns
    -------
    ret : array
        Array of corrector settings that should be added to original ones.

    See Also
    --------
    get_orm : Measure orbit response matrix.
    inverse_matrix : Inverse matrix by SVD.
    """
    if not inverse:
        m_inv = inverse_matrix(orm)
    else:
        m_inv = orm

    return np.dot(m_inv, orbit_diff)


def get_index_grid(lattice, correctors, monitors, xoy='xy'):
    """Return the index grid of sub ORM from global ORM for selected
    *correctors* and *monitors* w/ *xoy*.

    The global ORM is measured with all correctors (H + V) and BPMs for
    both x and y direction.

    Parameters
    ----------
    lattice : Lattice
        High-level lattice object.
    correctors : List[CaElement]
        List of correctors from *lattice*.
    monitors : List[CaElement]
        List of monitors, usually BPMs, to measure the beam orbit.
    xoy : str
        'x'('y') for monitoring 'x'('y') direction,'xy' for both (default).

    See Also
    --------
    get_orm : Measure orbit response matrix.
    """
    all_cors = lattice.get_elements(type='HCOR') +  \
               lattice.get_elements(type='VCOR')
    all_bpms = lattice.get_elements(type='BPM')
    # selected correctors columns
    col_idx = [all_cors.index(i) for i in correctors]
    # selected BPM rows, x,x,x....y,y,y...
    bpm_idx = [all_bpms.index(i) for i in monitors]
    if xoy == 'xy':
        bpm_cnt = len(all_bpms)
        row_idx = bpm_idx + [i+bpm_cnt for i in bpm_idx]
    elif xoy == 'x':
        row_idx = bpm_idx
    elif xoy == 'y':
        bpm_cnt = len(all_bpms)
        row_idx = [i+bpm_cnt for i in bpm_idx]
    return np.ix_(row_idx, col_idx)
