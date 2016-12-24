#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# generate lattice file from lattice object.
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-16 08:54:55 AM EST
#

import os

from phyapps import flowutils

mpath = os.path.abspath(os.path.join('./', 'FRIB_FLAME_example'))

mp = flowutils.MachinePortal(facility=mpath, segment='LINAC')

lat = mp.work_lattice_conf


# 
from phyutil.phytool.common import loadMachineConfig
from phyutil.phytool.common import loadLayout
from phyutil.phytool.common import loadSettings
from phyutil.phytool.common import loadLatticeConfig
from phyutil.phylib.lattice import flame

mach = "FRIB_FLAME_example"
mconfig, submach = loadMachineConfig(mach, 'LINAC')

layout_path = mconfig.getabspath(submach, 'layout_file')
settings_path = mconfig.getabspath(submach, 'settings_file')
config_path = mconfig.getabspath(submach, 'config_file')

lattice_layout = loadLayout(layout_path)
lattice_settings = loadSettings(settings_path)
lattice_config = loadLatticeConfig(config_path)

flame_lattice = flame.build_lattice(lattice_layout,
        config=lattice_config,
        settings=lattice_settings)

print flame_lattice.variables.keys()
e0 = flame_lattice.elements[10]
#print e0[0], e0[1],
for elem in flame_lattice.elements:
    if 'name' in elem[3]:
        print(elem[3]['name'])
    else:
        print(elem[1])
#for idx,x in enumerate(e0):
#    print(idx, x)

import sys
sys.exit(1)

from flame import Machine

machine = Machine(flame_lattice.conf())
#
#latfile_name = 'newfile.lat'
#with open(latfile_name, 'w') as fout:
#    flame_lattice.write(fout)
#

"""
# investigate lattice elements
lattice_elements = lattice_layout.elements
element_names1 = [e.name for e in lattice_elements]
print element_names1

element_names2 = [e.name for e in lat]
"""


