#!/usr/bin/python

from phantasy import MachinePortal
from phantasy import get_readback

machine = 'FRIB_FLAME'

mp = MachinePortal(machine=machine, segment='LINAC')

elem_BPMs = mp.get_elements(type='BPM')
elem = elem_BPMs[0]

lat = mp.work_lattice_conf

print(lat.get(elem, source='control', field='X'))
lat.run()
res = (lat.get(elem, source='model', mstate=True))
print res['mstate'].last_caviphi0

#print lat.settings[elem.name]

#print elem.family in ['BPM']

"""
import sys
sys.exit(0)

flame_lattice = lat.model_factory.build()

from flame import Machine
from phantasy import MachineStates
from phantasy import ModelFlame

m = Machine(flame_lattice.conf())

ms = MachineStates(machine=m)
fm = ModelFlame()
fm.mstates, fm.machine = ms, m
obs = fm.get_index_by_type(type='bpm')['bpm']
r,s = fm.run(monitor=obs)
for i,res in r:
    #print fm.get_element(index=i)[-1]['properties']['name']
    #print res.x0/1e3, res.y0/1e3
    print getattr(res, 'x0')/1e3
    print getattr(res, 'y0')/1e3
    break
#print elem.name
readings = lat.get(elem, source='control')
#print readings
print readings['X']
print readings['Y']


# 1. Create another dict to host viewers model settings, e.g. viewer_settings
# 2. Additional step for lat.get():
#    2.1: check element type, if is view, get from viewer_settings
# 3. Normally, viewer_settings is readonly
# 4. viewer_settings could be updated only when lat.run() is issued.
#TEST NEEDED
#2017-03-15 18:02:40 PM EDT
"""
