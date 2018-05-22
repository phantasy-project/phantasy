# -*- coding: utf-8 -*-
"""Plot orbit (FLAME)
"""

import matplotlib.pyplot as plt

from phantasy.library.misc import flatten
from flame_utils import ModelFlame

plt.rcParams['font.size'] = 16
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['figure.dpi'] = 80


def plot_orbit(*args, **kwargs):
    """Plot orbit (x,y) from FLAME lattice file or model instance,
    first passing interested data columns as tuples, see the following
    examples.

    Keyword Arguments
    -----------------
    latfile : str
        Name of FLAME lattice file.

    flame_model :
        ModelFlame object.

    Returns
    -------
    r : dict
        Orignal data.

    Examples
    --------
    >>> fm = ModelFlame(latfile)
    >>> # plot two curves: s v.s. x,y
    >>> plot_orbit(('pos', 'xcen'), ('pos', 'ycen'), flame_model=fm)
    >>>
    
    See Also
    --------
    ModelFlame
    """
    latfile = kwargs.get('latfile', None)
    flame_model = kwargs.get('flame_model', None)
    if latfile is not None:
        fm = ModelFlame(lat_file=latfile)
    elif flame_model is not None:
        fm = flame_model
    else:
        print("Please define 'latfile' or 'flame_model'.")
        return None

    ks = flatten(args)
    monitors = range(len(fm.machine))
    r, s = fm.run(monitor=monitors)
    data = fm.collect_data(r, **dict(zip(ks, [True]*len(ks))))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for xlbl, ylbl in args:
        ax.plot(data[xlbl], data[ylbl], label='${}$'.format(ylbl.upper()))
    ax.set_xlabel('${}$'.format(xlbl.upper()))
    ax.legend(loc='best')
    plt.show()
    return data
