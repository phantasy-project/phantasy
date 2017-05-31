#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for orbit response matrix calculation.
"""

from __future__ import division
from __future__ import print_function

import time
from functools import reduce

import numpy as np
import numpy.linalg as linalg


def get_orm(lattice, correctors, monitors, **kws):
    """Calculate orbit response matrix (ORM) with defined input.

    Size of *monitors* is ``m``, size of correctors is ``n``, if both x and y
    directions are monitored, size of *monitors* should be doubled. The final
    calculated ORM should be of the shape of ``(m, n)``.
    
    Every iteration of correctors update, which could be defined by ``scan``
    keyword parameter, series of measured orbit data would be returned from
    :func:`get_orbit`, doing linear polynomial fitting against feeded ``scan``
    values should return one column of ORM data. The column-wise returned
    matrix is the final ORM.

    Parameters
    ----------
    lattice : Lattice
        High-level lattice object.
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
    xoy : str
        'x'('y') for monitoring 'x'('y') direction,'xy' for both (default).

    Returns
    -------
    ret : array
        ORM with shape ``(m, n)``.

    Todo
    ----
    case of ``source == 'model'``.
    """
    source = kws.get('source', 'control')
    scan = kws.get('scan', np.linspace(-0.003, 0.003, 5))
    cor_field = kws.get('cor_field', 'ANG')
    xoy = kws.get('xoy', 'xy')
    wait = kws.get('wait', 1.0)

    m = len(monitors) * len(xoy)
    n = len(correctors)
    mat_mn = np.zeros([m, n])

    # i <-- 0, m-1
    # B[i] = \Sigma_j=0^{n-1} R[i,j] C[j]
    # ---> iff C[j] != 0 ==> B[i] = R[i,j] C[j]
    # ==> R[i,j] = B[i]/C[j]
    # ==> or: R[i,j] = polyfit(C[i], B[i], 1)[0]
    # 
    for i, cor in enumerate(correctors):
        orbit_arr = np.zeros([len(scan), m])
        cor_val0 = getattr(cor, cor_field)
        for iscan, val in enumerate(scan):
            print("Set [{0}] {1}:{2}".format(i+1, cor.name, val))
            setattr(cor, cor_field, val)
            time.sleep(wait)
            orbit_arr[iscan] = get_orbit(monitors, **kws)
        
        # get mat_mn(k,i)
        for k in range(m):
            mat_mn[k, i] = np.polyfit(scan, orbit_arr[:, k], 1)[0]

        # reset cor and process next col
        setattr(cor, cor_field, cor_val0)
    return mat_mn


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

    Returns
    -------
    ret : array
        Monitors readings as beam orbit.
    """
    orb_field = kws.get('orb_field', ('X', 'Y'))
    xoy = kws.get('xoy', 'xy')
    xyfld = zip(range(len(xoy)), orb_field)
    xys = [[getattr(elem, fld) for elem in monitors] for _, fld in xyfld]
    return np.asarray(xys).flatten()


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
