import os
import time
import numpy as np

from phantasy import MachinePortal
from phantasy.library.pv import get_readback

import matplotlib.pyplot as plt


## Define machine configurations
machine_repo = "/home/tong1/work/FRIB/projects/machines"
machine = os.path.join(machine_repo, "FRIB_FLAME")

## Initialize high-level machine
mp = MachinePortal(machine=machine, segment="LINAC")
lat = mp.work_lattice_conf

## Get data from modeled high-level lattice
elem_BPM = mp.get_elements(type='BPM')
pv_bpm_x = mp.get_pv_names(elem_BPM,'X')['X']
orbit0 = get_readback(pv_bpm_x)
#plt.plot(orbit0,'r-')

## Control machine with model-based approach, e.g. correct orbit

# Introduce a kick on the first horizontal corrector (h-corrector)
hcor0 = mp.get_elements(type='HCOR')[0]

# Check settings for both 'model' or 'control'
lat.get(hcor0, _source='model')
lat.get(hcor0, _source='control')

# Apply kicker to distort trajectory
lat.set(hcor0, value=0.001, field='ANG')
time.sleep(10)

# Check settings after set() action
print(lat.get(hcor0, _source='control'))
print(lat.get(hcor0, _source='model'))

orbit1 = get_readback(pv_bpm_x)

# Generate lattice file for modeling code
# ...
# latfile2 is generated after certain procedure

latfile2 = 'model_oc.lat'

# Update settings to model
lat.update_model_settings(latfile2)

# Synchronize settings from model to control
lat.sync_settings(data_source='model') 

# Check setting action log:
print(lat.trace_history(), file=open('log.dat', 'w'))
