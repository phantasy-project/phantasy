#!/usr/bin/python

"""Generate lattice settings from MachinePortal object.

Tong Zhang <zhangt@frib.msu.edu>
2016-12-19 14:36:29 PM EST
"""

import os

from phyapps import flowutils
from phyutil.phytool.common import loadSettings
from phyutil.phylib.settings import Settings

mpath = os.path.abspath(os.path.join('./', 'FRIB_FLAME_example'))
mp = flowutils.MachinePortal(facility=mpath, segment='LINAC')
lat = mp.work_lattice_conf

lattice_settings = Settings()
print(lattice_settings)


