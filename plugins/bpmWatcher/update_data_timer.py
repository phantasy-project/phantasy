#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Update BPM waveform PVs.
"""

import cothread
from cothread.catools import camonitor, caput, caget
import pandas as pd
import numpy as np

df0 = pd.read_csv('bpm_pvdata.csv')
n_bpm = 151

pos_arr_pv = "PHY:BPM_ALL:SPOS_RD"
pos1_arr_pv = "PHY:BPM_ALL:SPOS1_RD"
name_arr_pv = "PHY:BPM_ALL:NAME_RD"
# RD
x_arr_pv = "PHY:BPM_ALL:XPOS_RD"
y_arr_pv = "PHY:BPM_ALL:YPOS_RD"
pha_arr_pv = "PHY:BPM_ALL:PHASE_RD"
mag_arr_pv = "PHY:BPM_ALL:MAG_RD"
# diff or ratio
dx_arr_pv = "PHY:BPM_ALL:XPOS_DRDREF"
dy_arr_pv = "PHY:BPM_ALL:YPOS_DRDREF"
dpha_arr_pv = "PHY:BPM_ALL:PHASE_DRDREF"
rmag_arr_pv = "PHY:BPM_ALL:MAG_RATIO"

# max tolerance range for monitoring, +/- x[y]pos limits
xpos_limit_pv = "PHY:BPM_ALL:XPOS_LMT"
xpos_h_arr_pv = "PHY:BPM_ALL:XPOS_HIGH_RD"
xpos_l_arr_pv = "PHY:BPM_ALL:XPOS_LOW_RD"
ypos_limit_pv = "PHY:BPM_ALL:YPOS_LMT"
ypos_h_arr_pv = "PHY:BPM_ALL:YPOS_HIGH_RD"
ypos_l_arr_pv = "PHY:BPM_ALL:YPOS_LOW_RD"
# phase
pha_limit_pv = "PHY:BPM_ALL:PHASE_LMT"
pha_h_arr_pv = "PHY:BPM_ALL:PHASE_HIGH_RD"
pha_l_arr_pv = "PHY:BPM_ALL:PHASE_LOW_RD"
# mag
mag_limit_pv = "PHY:BPM_ALL:MAG_LMT"
mag_h_arr_pv = "PHY:BPM_ALL:MAG_HIGH_RD"
mag_l_arr_pv = "PHY:BPM_ALL:MAG_LOW_RD"

"""
def cb_x(value, index):
    x_arr[index] = value
    cothread.Spawn(lambda:caput(x_arr_pv, x_arr)).Wait()

def cb_y(value, index):
    y_arr[index] = value
    cothread.Spawn(lambda:caput(y_arr_pv, y_arr)).Wait()

def cb_pha(value, index):
    pha_arr[index] = value
    cothread.Spawn(lambda:caput(pha_arr_pv, pha_arr)).Wait()

def cb_mag(value, index):
    mag_arr[index] = value
    cothread.Spawn(lambda:caput(mag_arr_pv, mag_arr)).Wait()
"""

df = df0.iloc[:n_bpm,:n_bpm]

# single RD
x_pvs = df.pv_x.to_list()
y_pvs = df.pv_y.to_list()
pha_pvs = df.pv_pha.to_list()
mag_pvs = df.pv_mag.to_list()

# signle diff or ratio
dx_pvs = df.pv_dx_ref.to_list()
dy_pvs = df.pv_dy_ref.to_list()
dpha_pvs = df.pv_dpha_ref.to_list()
rmag_pvs = df.pv_mag_ratio.to_list()


# initial X, Y, PHA, MAG array PVs
x_arr = caget(x_pvs)
y_arr = caget(y_pvs)
pha_arr = caget(pha_pvs)
mag_arr = caget(mag_pvs)

dx_arr = caget(dx_pvs)
dy_arr = caget(dy_pvs)
dpha_arr = caget(dpha_pvs)
rmag_arr = caget(rmag_pvs)

# set static array data
spos = df.s.to_list()
spos1 = [i for i in spos]
names = df.pv_x.apply(lambda i: i[:-9]).to_list()
cothread.Spawn(lambda:caput(pos_arr_pv, spos)).Wait()
cothread.Spawn(lambda:caput(pos1_arr_pv, spos1)).Wait()
cothread.Spawn(lambda:caput(name_arr_pv, names)).Wait()

"""
# monitor X, Y, PHA and MAG
mm_x = camonitor(x_pvs, cb_x)
mm_y = camonitor(y_pvs, cb_y)
mm_pha = camonitor(pha_pvs, cb_pha)
mm_mag = camonitor(mag_pvs, cb_mag)
"""

rate = 5
x_timer = cothread.Timer(1.0 / rate, lambda: caput(x_arr_pv, caget(x_pvs)), True)
y_timer = cothread.Timer(1.0 / rate, lambda: caput(y_arr_pv, caget(y_pvs)), True)
pha_timer = cothread.Timer(1.0 / rate, lambda: caput(pha_arr_pv, caget(pha_pvs)), True)
mag_timer = cothread.Timer(1.0 / rate, lambda: caput(mag_arr_pv, caget(mag_pvs)), True)

dx_timer = cothread.Timer(1.0 / rate, lambda: caput(dx_arr_pv, caget(dx_pvs)), True)
dy_timer = cothread.Timer(1.0 / rate, lambda: caput(dy_arr_pv, caget(dy_pvs)), True)
dpha_timer = cothread.Timer(1.0 / rate, lambda: caput(dpha_arr_pv, caget(dpha_pvs)), True)
rmag_timer = cothread.Timer(1.0 / rate, lambda: caput(rmag_arr_pv, caget(rmag_pvs)), True)

# cothread.Sleep(5)
# .close to close a monitor
# .cancel to cancel a timer

def update_xtolm(value):
    # XPOS
    caput(xpos_h_arr_pv, [value] * n_bpm)
    caput(xpos_l_arr_pv, [-value] * n_bpm)

def update_ytolm(value):
    # YPOS
    caput(ypos_h_arr_pv, [value] * n_bpm)
    caput(ypos_l_arr_pv, [-value] * n_bpm)

def update_ptolm(value):
    # PHASE
    caput(pha_h_arr_pv, [value] * n_bpm)
    caput(pha_l_arr_pv, [-value] * n_bpm)

def update_mtolm(value):
    # MAG ratio
    caput(mag_h_arr_pv, [value] * n_bpm)
    caput(mag_l_arr_pv, [-0] * n_bpm)

camonitor(xpos_limit_pv, update_xtolm)
camonitor(ypos_limit_pv, update_ytolm)
camonitor(pha_limit_pv, update_ptolm)
camonitor(mag_limit_pv, update_mtolm)

#
cothread.WaitForQuit()
