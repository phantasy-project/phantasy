#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration to the workflow of high-level controls.

Tong Zhang <zhangt@frib.msu.edu>
2016-12-14 13:57:55 PM EST
"""
import os
import matplotlib.pyplot as plt

from phyapps import flowutils

## Explicit initialization
# mpath = os.path.join('.', 'FRIB_example')
# segment_name = 'LINAC' # default
# mp = flowutils.MachinePortal(facility=mpath)
# print(mp.last_machine_name) # FRIB_example

## Initial with no input: 
mp = flowutils.MachinePortal()
print(mp.last_machine_name) # FRIB

## Inspect loaded machine
mp.inspect_mconf(out='stdout')

## get elements
elem = mp.get_elements(type='*PM')
pos = [e.sb for e in elem]

## get data
pv1_names = mp.get_pv_names(elem, ['X', 'Y'])
pv1_values = mp.get_pv_values(elem, ['X','Y'])

## plot data
plt.plot(pos, pv1_values['X'], 'r-', label='X')
plt.plot(pos, pv1_values['Y'], 'b-', label='Y')
plt.legend()
plt.show()

