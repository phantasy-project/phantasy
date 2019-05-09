#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import numpy as np
from numpy import ndarray


class Data(object):
    """Class for post-processing of data from allison-scanner.
    """
    # kws: array, file
    def __init__(self, model, **kws):
        self.model = model
        self.device = device = model.device
        self.update_pos_conf(
                {"begin": device.pos_begin,
                 "end": device.pos_end,
                 "step": device.pos_step})
        self.update_volt_conf(
                {"begin": device.volt_begin,
                 "end": device.volt_end,
                 "step": device.volt_step})
        # raw intensity array
        self.intensity = self.read_data(**kws)
        #
        self.x_grid, self.xp_grid, self.volt_grid, self.weight_grid = \
                self.initial_data_grid()


    def read_data(self, **kws):
        # 1. array?: for online analysis
        # 2. file? (json) : for offline analysis
        array = kws.get('array', None)
        if array is not None and isinstance(array, ndarray):
            return array
        else:
            jsonfile = kws.get('file', None)
            if jsonfile is None:
                return None
            else:
                with open(jsonfile, 'r') as fp:
                    f = json.load(fp)
                    data = np.flipud(f['data']['array'])
                    self.update_pos_conf(f['position'])
                    self.update_volt_conf(f['voltage'])
                return data

    def update_pos_conf(self, conf):
        # update position config.
        self._pos_begin = conf['begin']
        self._pos_end = conf['end']
        self._pos_step = conf['step']
        assert (self._pos_end - self._pos_begin) % self._pos_step == 0
        self._pos_dim = int((self._pos_end - self._pos_begin) / self._pos_step) + 1

    def update_volt_conf(self, conf):
        # update voltage config.
        self._volt_begin = conf['begin']
        self._volt_end = conf['end']
        self._volt_step = conf['step']
        assert (self._volt_end - self._volt_begin) % self._volt_step == 0
        self._volt_dim = int((self._volt_end - self._volt_begin) / self._volt_step) + 1

    def initial_data_grid(self):
        """Initial data grid.

        Returns
        -------
        r : tulpe
            Tuple of x, xp, voltage, weight arrays.
        """
        # original position, voltage data grid
        pos_grid, volt_grid = np.meshgrid(
                np.linspace(self._pos_begin, self._pos_end, self._pos_dim),
                np.linspace(self._volt_begin, self._volt_end, self._volt_dim))
        x_grid = pos_grid  # mm

        model = self.model
        volt_col = volt_grid[:, 0]
        v2d_arr = np.asarray([model.voltage_to_divergence(v) for v in volt_col])

        # x' data grid
        xp_grid, _ = np.meshgrid(v2d_arr[:, 1], x_grid[0])
        xp_grid *= 1000  # rad -> mrad
        xp_grid = xp_grid.T

        # weight factor data grid
        weight_grid, _ = np.meshgrid(v2d_arr[:, 3], x_grid[0])
        weight_grid = weight_grid.T

        # ratio of grid unit size to resolution
        dxp = model.voltage_to_divergence(self._volt_step)[1]
        self.grid_to_res_ratio = dxp * self._pos_step / 1000.0 \
                / self.device.dxp0 / self.device.slit_width

        return x_grid, xp_grid, volt_grid, weight_grid,

    def calculate_beam_parameters(self, x=None, xp=None, intensity=None, **kws):
        # kws: weight_correction
        x = self.x_grid if x is None else x
        xp = self.xp_grid if xp is None else xp
        intensity = self.intensity if intensity is None else intensity
        if kws.get('weight_correction', True):
            intensity *= 1./self.weight_grid * self.grid_to_res_ratio
        return calculate_beam_parameters(x, xp, intensity,
                                         self.model.bg, self.device.xoy)

    def filter_initial_background_noise(self, intensity=None,
                                        n_elements=2, threshold=5):
        intensity = self.intensity if intensity is None else intensity
        return filter_initial_background_noise(
                    intensity, n_elements, threshold)


def filter_initial_background_noise(m_intensity, n_elements=2, threshold=5):
    """Estimate initial background noise based on sampling regions from
    the four corners by selecting *n* x *n* squares, respectively, apply
    the noise substraction from the input intensity matrix, return the
    filtered one.

    Parameters
    ----------
    m_intensity : array
        Intensity matrix.
    n_elements : int
        Selected square region, of the shape `n_elements` by `n_elements`.
    threshold : int
        Define how many standard deviation of sampled noise above maximum
        noise level should be treated as non-zero signal.

    Returns
    -------
    m : array
        Intensity matrix over sampled noise threshold.
    """
    m = m_intensity
    n = n_elements
    _range = range(-n, n)
    subm = m_intensity[np.ix_(_range, _range)]
    mmax, mmin, mavg, mstd = subm.max(), subm.min(), subm.mean(), subm.std()
    idx = m >= (mmax + threshold * mstd)
    return (m - mavg) * idx


def calculate_beam_parameters(x, xp, intensity, bg, xoy):
    """Calculate beam parameters from input 2D arrays.

    Parameters
    ----------
    x : array
        2D array of position, [mm].
    xp : array
        2D array of divergence, [mrad].
    intensity : array
        2D array of intensity.
    bg : float
        Lorentz energy.
    xoy : str
        'X' or 'Y'.

    Returns
    -------
    r : dict
        k: <u>_cen, <u>_pcen, <u>_rms, <u>_<u>p, <u>p_rms, <u>_emit, <u>_emitn,
        alpha_<u>, beta_<u>, gamma_<u>, I_total, <u> could be 'x' or 'y'.
    """
    x, xp = np.copy(x), np.copy(xp)
    dx = abs(x[1,1] - x[0,0])
    dxp = abs(xp[1,1] - xp[0,0])
    j = intensity / (dx * dxp)
    intensity_total = intensity.sum()
    x_avg = np.sum(x * intensity) / intensity_total
    xp_avg = np.sum(xp * intensity) / intensity_total

    x -= x_avg
    xp -= xp_avg

    x_up = x + dx / 2.0
    x_down = x - dx / 2.0
    xp_up = xp + dxp / 2.0
    xp_down = xp - dxp / 2.0

    xx = abs(dxp * np.sum((x_up ** 3 - x_down ** 3)/3.0 * j)) / intensity_total
    xxp = np.sum(x * xp * intensity) / intensity_total
    xpxp = abs(dx * np.sum((xp_up ** 3 - xp_down ** 3)/3.0 * j)) / intensity_total

    x_rms, xp_rms = np.sqrt(xx), np.sqrt(xpxp)
    x_emit = np.sqrt(xx * xpxp - xxp ** 2)
    x_emit_n = x_emit * bg

    alpha, beta, gamma = -xxp / x_emit, xx / x_emit, xpxp / x_emit

    v = (x_avg, xp_avg, x_rms, xxp, xp_rms, x_emit, x_emit_n,
         alpha, beta, gamma, intensity_total)
    l = ('{u}_cen', '{u}p_cen', '{u}_rms', '{u}_{u}p', 'xp_rms', '{u}_emit', '{u}_emitn',
         'alpha_{u}', 'beta_{u}', 'gamma_{u}', 'total_intensity')
    k = [i.format(u=xoy.lower()) for i in l]
    return dict(zip(k, v))

