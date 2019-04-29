import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import matplotlib.patches as patches
import matplotlib.colors as colors
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import time

from phantasy import caget, caput

# Physical constants and conversion factors using Warp syntax
echarge = 1.602177e-19      # electronic charge [C]
clight  = 299792458.        # speed of light [m/s]
amu     = 1.660538921e-27   # amu [kg]
jperev  = echarge           # Joules per eV [J/eV]

beta_c = 0.0050758810792083794

class ASReset(object):

    def __init__(self,
    pv_dict = dict()):

        self.PV_dict = pv_dict

        self.reset()

    def reset(self):

        if caget(self.PV_dict['pos_default']) - caget(self.PV_dict['pos_readback']) <= 1.:
            print('Scanner returned to default position')
        else:
            print('Scanner still returning to default position')
            while caget(self.PV_dict['pos_default']) - caget(self.PV_dict['pos_readback']) > 1.:
                time.sleep(1)
            print('Scanner returned to default position')

        time.sleep(5)

        caput(self.PV_dict['interlock_reset'], 1)
        print('Resetting device')

        time.sleep(2)

        if caget(self.PV_dict['interlock_status'])== 1:
            dummy = raw_input("Scanner still interlocked, press Enter to continue...")
            return
        else:
            print('Scanner interlock reset')
