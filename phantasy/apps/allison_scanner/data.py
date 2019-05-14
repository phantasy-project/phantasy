#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray

from phantasy.apps.quad_scan import draw_beam_ellipse
from .utils import point_in_ellipse


class Data(object):
    """Class for post-processing of data from allison-scanner.
    """

    # kws: array, file
    def __init__(self, model, **kws):
        self.model = model
        self.device = device = model.device
        self.xoy = device.xoy
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
        self.grid_to_res_ratio = dxp * self._pos_step / 1000.0 / self.device.dxp0 / self.device.slit_width

        return x_grid, xp_grid, volt_grid, weight_grid,

    def calculate_beam_parameters(self, intensity=None, x=None, xp=None, **kws):
        """Calculator beam Twiss parameters and more.

        Parameters
        ----------
        intensity : array
            Array for intensity.
        x : array
            Array for position, [mm].
        xp : array
            Array for divergence, [mrad].

        Keyword Arguments
        -----------------
        weight_correction : bool
            If apply weighted correction or not, default is True.

        Returns
        -------
        r : dict
            The keys with unit of dict are: `alpha_u`, `beta_u` [m],
            `gamma_u` [1/m], `total_intensity`, `u_cen` [mm], `up_cen` [mrad],
            `u_rms` [m], `up_rms` [m], `u_up` [mm.mrad], `u_emit` [mm.mrad],
            `u_emitn` [mm.mrad], where `u` could be `x` or `y`.
        """
        x = self.x_grid if x is None else x
        xp = self.xp_grid if xp is None else xp
        intensity = self.intensity.copy() if intensity is None else intensity.copy()
        if kws.get('weight_correction', True):
            intensity *= 1. / self.weight_grid * self.grid_to_res_ratio
        return calculate_beam_parameters(x, xp, intensity,
                                         self.model.bg, self.xoy)

    def filter_initial_background_noise(self, intensity=None,
                                        n_elements=2, threshold=5):
        intensity = self.intensity.copy() if intensity is None else intensity.copy()
        return filter_initial_background_noise(
            intensity, n_elements, threshold)

    def plot(self, intensity=None, raw_view=False, results={},
             with_return=False, **kws):
        """Plot intensity as image.

        Parameters
        ----------
        intensity : array
            If not defined, use the default one (unprocessed).
        raw_view : bool
            If set, plot y axis with voltage, or x'.
        with_return : bool
            If set, return tuple will be enabled.
        results : dict
            If defined, print Twiss paramters on the figure.

        Returns
        -------
        r : tuple
            Tuple of figure and axes, if *with_return* is True.
        """
        data = self.intensity if intensity is None else intensity
        fig, ax = plt.subplots()

        im = ax.imshow(data, origin="left", aspect="auto", **kws)
        fig.colorbar(im)

        xlbl = r"$x\,\mathrm{[mm]}$"
        x = self.x_grid
        if raw_view:
            y = self.volt_grid
            ylbl = r"Voltage [V]"
        else:
            y = self.xp_grid
            ylbl = r"$x'\,\mathrm{[mrad]}$"
        ax.set_xlabel(xlbl)
        ax.set_ylabel(ylbl)
        im.set_extent((x[0, 0], x[-1, -1], y[0, 0], y[-1, -1]))

        if results:
            print(results)
            xoy = self.xoy.lower()
            a = r'$\alpha = {0:.3f}$'.format(results.get('alpha_{}'.format(xoy)))
            b = r'$\beta = {0:.3}\,\mathrm{{[m]}}$'.format(results.get('beta_{}'.format(xoy)))
            g = r'$\gamma = {0:.3}\,\mathrm{{[m^{{-1}}]}}$'.format(results.get('gamma_{}'.format(xoy)))
            en = r'$\epsilon_n = {0:.3}\,\mathrm{{[mm \cdot mrad]}}$'.format(results.get('emitn_{}'.format(xoy)))
            info = '\n'.join((a, b, g, en))
            props = dict(boxstyle='round', facecolor='w', alpha=0.5)
            ax.text(0.05, 0.95, info, transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props,)

        if with_return:
            return fig, ax

    def _get_points(self):
        x, y = self.x_grid[0, :], self.xp_grid[:, 0]
        return np.asarray([(i, j) for j in y for i in x])

    def tag_noise_signal(self, ellipse, factor=1.0):
        """Return array of boolean, to indicate if point is noise (False) or
        signal (True).
        """
        _xp1 = self.xp_grid[:, 0]
        _x1 = self.x_grid[0, :]
        z = np.zeros(self.x_grid.shape)
        for j, yi in enumerate(_xp1):
            for i, xi in enumerate(_x1):
                if point_in_ellipse(xi, yi, ellipse, factor=factor):
                    z[j, i] = True  # signal
                else:
                    z[j, i] = False  # noise
        return z

    def noise_correction(self, noise_signal_array, intensity=None, **kws):
        """
        Parameters
        ----------
        noise_signal_array : array
            Boolean array with True as signal, and False as False tagging.
        intensity : array:
            Intensity array, if not defined, use the initial one.

        Keyword Arguments
        -----------------
        threshold_sigma : float
            Additional threshold for noise level measured by noise
            standard deviation, default is 2.0.

        Returns
        -------
        m : array:
            Intensity after noise correction.
        """
        intensity = self.intensity.copy() if intensity is None else intensity.copy()
        return noise_correction(intensity, noise_signal_array, **kws)


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
    dx = abs(x[1, 1] - x[0, 0])
    dxp = abs(xp[1, 1] - xp[0, 0])
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

    xx = abs(dxp * np.sum((x_up ** 3 - x_down ** 3) / 3.0 * j)) / intensity_total
    xxp = np.sum(x * xp * intensity) / intensity_total
    xpxp = abs(dx * np.sum((xp_up ** 3 - xp_down ** 3) / 3.0 * j)) / intensity_total

    x_rms, xp_rms = np.sqrt(xx), np.sqrt(xpxp)
    x_emit = np.sqrt(xx * xpxp - xxp ** 2)
    x_emit_n = x_emit * bg

    alpha, beta, gamma = -xxp / x_emit, xx / x_emit, xpxp / x_emit

    v = (x_avg, xp_avg, x_rms, xxp, xp_rms, x_emit, x_emit_n,
         alpha, beta, gamma, intensity_total)
    l = ('{u}_cen', '{u}p_cen', '{u}_rms', '{u}_{u}p', '{u}p_rms', 'emit_{u}', 'emitn_{u}',
         'alpha_{u}', 'beta_{u}', 'gamma_{u}', 'total_intensity')
    k = [i.format(u=xoy.lower()) for i in l]
    return dict(zip(k, v))


def draw_beam_ellipse_with_params(params, ax=None, factor=4.0, xoy='x', **kws):
    """Draw beam ellipse with beam Twiss parameters calculated from function:
    :func:`~calculate_beam_parameters`.

    Parameters
    ----------
    params : dict
        Beam Twiss parameters.
    ax :
        If set, draw on defined one.
    factor : float
        Scaling factor applied to ellipse width and height, default is 4.0.
    xoy : str
        'x' or 'y'.

    Keyword Arguments
    -----------------
    color : str
        Ellipse border color, default is black.
    clear : bool
        Clear axes or not before drawing, default is True.
    fill :
        Fill ellipse with color or not, defalut is 'green', or False.
    anote : bool
        Put annotations or not, default is True.

    Returns
    -------
    r : tuple
        Return tuple of ellipse, figure, axes, iff input *ax* is not defined,
        or return tuple of ellipse, None, None.
    """
    a, b, g, epsilon = [params.get('{}_{}'.format(k, xoy))
               for k in ('alpha', 'beta', 'gamma', 'emit')]
    xc, yc = [params.get('{}{}'.format(xoy, k)) for k in ('_cen', 'p_cen')]

    color = kws.get('color', 'w')
    clear = kws.get('clear', False)
    anote = kws.get('anote', False)
    fill = kws.get('fill', False)  # or color

    auto_scale = False
    if ax is None:
        fig, ax = plt.subplots()
        auto_scale = True
    e1 = draw_beam_ellipse(ax=ax, alpha=a, beta=b, gamma=g, epsilon=epsilon / 1.0e6,
                           xc=xc, yc=yc, factor=factor, color=color,
                           clear=clear, anote=anote, fill=fill)
    if auto_scale:
        ax.autoscale()
        return e1, fig, ax
    else:
        return e1, None, None


def noise_correction(intensity, noise_signal_array, threshold_sigma=2.0):
    """Apply noise correction to the *intensity* matrix, the noise threshold
    is defined by average noise and noise standard deviation defined
    multiplied by *threshold_sigma*, signal and noise is defined in
    *noise_signal_array*.

    Parameters
    ----------
    intensity : array
        Intensity matrix.
    noise_signal_array : array
        Boolean array with True as signal, and False as False tagging.
    threshold_sigma : float
        Additional noise threshold level.

    Returns
    -------
    m : array:
        Matrix of signal after noise correction.
    """
    noise_arr = intensity[noise_signal_array == False]
    noise_avg = noise_arr.mean()
    noise_std = noise_arr.std()

    shape = intensity.shape
    arr_flat = intensity.flatten()
    noise_threshold = threshold_sigma * noise_std + noise_avg
    for i, v in enumerate(arr_flat):
        if v < noise_threshold:
            arr_flat[i] = 0
        else:
            arr_flat[i] -= noise_avg
    m = arr_flat.reshape(shape)
    m[noise_signal_array == False] = 0
    return m
