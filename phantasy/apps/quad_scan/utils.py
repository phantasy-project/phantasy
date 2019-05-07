# -*- coding: utf-8 -*-
from matplotlib import patches
import numpy as np


def draw_beam_ellipse(ax, alpha, beta, gamma, epsilon, **kws):
    """Draw beam ellipse with given Twiss parameters.

    Parameters
    ----------
    ax : obj
        Axes object of figure.
    alpha : float
        Twiss parameter: alpha.
    beta : float
        Twiss parameter: beta, [m].
    gamma : float
        Twiss parameter: gamma, [1/m].
    epsilon : float
        Geometrical transverse emittance, [m.rad].

    Keyword Arguments
    -----------------
    xc : float
        X coord for the central of ellipse, default is 0.
    yc : float
        Y coord for the central of ellipse, default is 0.
    color : str
        Ellipse border color, default is black.
    clear : bool
        Clear axes or not before drawing, default is True.
    fill :
        Fill ellipse with color or not, defalut is 'green', or False.
    anote : bool
        Put annotations or not, default is True.
    factor : float
        Scaling factor applied to ellipse width and height, default is 1.0.
    """
    anote = kws.get('anote', True)
    clear_ax = kws.get('clear', True)
    color = kws.get('color', 'k')
    factor = kws.get('factor', 1.0)
    if clear_ax:
        ax.clear()

    xc, yc = kws.get('xc', 0), kws.get('yc', 0)

    w = (2 * epsilon / (beta + gamma + ((beta + gamma)**2 - 4)**0.5))**0.5
    h = (0.5 * epsilon * (beta + gamma + ((beta + gamma)**2 - 4)**0.5))**0.5

    angle = np.arctan(2 * alpha / (gamma - beta)) / 2.0  # radian
    if angle >= 0:
        phi_coord = (0.54, 0.51)
    else:
        phi_coord = (0.54, 0.47)

    w, h = factor * w * 1e3, factor * h * 1e3  # m -> mm, rad -> mrad

    theta = np.deg2rad(np.arange(0.0, 360.0, 1.0))

    x = 0.5 * w * np.cos(theta)
    y = 0.5 * h * np.sin(theta)

    m_rot = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)],
    ])

    x, y = np.dot(m_rot, np.array([x, y]))

    x += xc
    y += yc

    cfill = kws.get('fill', 'green')
    if cfill:
        ax.fill(x, y, alpha=0.2, facecolor=cfill, edgecolor=cfill, zorder=1)
    e1 = patches.Ellipse(
        (xc, yc),
        w,
        h,
        angle=np.rad2deg(angle),
        linewidth=2,
        fill=False,
        zorder=2,
        color=color)

    ax.add_patch(e1)

    if not anote:
        return

    xm, y_xm = x.max(), y[np.where(x == x.max())][0]
    ym, x_ym = y.max(), x[np.where(y == y.max())][0]

    ax.plot((xc, xm), (yc, y_xm), '--', lw=2, color='g')
    ax.plot((xm, xm), (y_xm, yc), '--', lw=2, color='g')

    ax.plot((x_ym, xc), (ym, ym), '--', lw=2, color='b')
    ax.plot((xc, x_ym), (yc, ym), '--', lw=2, color='b')

    xline = np.asarray([x.min(), xc, xm])
    yline = np.tan(angle) * (xline - xc) + yc
    ax.plot(xline, yline, '--', lw=2, color='m')

    ax.arrow(
        x.min(),
        yc, (x.max() - x.min()) * 1.1,
        0,
        head_width=0.02,
        head_length=0.05,
        fc='m',
        ec='m')
    ax.arrow(
        xc,
        y.min(),
        0, (y.max() - y.min()) * 1.1,
        head_width=0.02,
        head_length=0.05,
        fc='k',
        ec='k')

    ax.annotate(
        r"$\sqrt{\epsilon\;\beta)}$", (0.5 * (xm + xc), yc), (0, -40),
        textcoords='offset points',
        fontsize=20)
    ax.annotate(
        r"$\sqrt{\epsilon\;\gamma)}$", (xc, 0.5 * (ym + yc)), (-50, 0),
        textcoords='offset points',
        fontsize=20)
    ax.annotate(
        r"$\tan(2\phi)\;=\;\frac{2\alpha}{\gamma-\beta}$",
        (0.5 * xm, np.abs(y_xm)),
        fontsize=20)
    ax.annotate(
        r"$\phi$", (xc, yc), phi_coord,
        textcoords='axes fraction',
        fontsize=20)

    ax.annotate(
        r"$Area\;=\;\pi\epsilon$", (xline[0], yline[0]), (0.3, 0),
        textcoords='axes fraction',
        fontsize=20)

    ax.annotate(r"$u$", (xc + (xm - xc) * 1.3, yc), fontsize=20)
    ax.annotate(r"$u'$", (xc, yc + (ym - yc) * 1.3), fontsize=20)

    ax.set_xlim((1.5 * x.min(), 1.5 * x.max()))
    ax.set_ylim((1.5 * y.min(), 1.5 * y.max()))

    ax.set_title(
        r"$\phi={0:.1f}^\degree$".format(np.rad2deg(angle)), fontsize=20)

    if clear_ax:
        ax.axis('off')
