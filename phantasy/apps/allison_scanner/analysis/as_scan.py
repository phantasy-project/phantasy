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

class ASScan(object):

    def __init__(self,
    pos = [-30, 30, 1], vol = [-500, 500, 20],
    x_or_y = 'y',
    pv_dict = dict(),
    esq_setting = [],
    time = '', number = None):

        self.esq_setting = esq_setting
        self.x_or_y = x_or_y
        self.name = 'FE_LEBT_AS' + self.x_or_y + '_D0739_' + time

        self.PV_dict = pv_dict

        self.pos_start, self.pos_end, self.pos_step = pos
        self.pos_count = np.int( np.ceil((self.pos_end - self.pos_start)/self.pos_step) ) + 1
        self.pos_end = self.pos_start + (self.pos_count-1)*self.pos_step

        self.vol_start, self.vol_end, self.vol_step = vol
        self.vol_count = np.int( np.ceil((self.vol_end - self.vol_start)/self.vol_step) ) + 1
        self.vol_end = self.vol_start + (self.vol_count-1)*self.vol_step

        self.perform_scan()


    def perform_scan(self):
        self.check_fc_bias()

        caput(self.PV_dict['pos_start'], self.pos_start)
        caput(self.PV_dict['pos_end'], self.pos_end)
        caput(self.PV_dict['pos_step'], self.pos_step)

        caput(self.PV_dict['vol_start'], self.vol_start)
        caput(self.PV_dict['vol_end'], self.vol_end)
        caput(self.PV_dict['vol_step'], self.vol_step)

        self.enable()
        self.initiate_scan()
        self.read_data()

    def check_fc_bias(self):

        fc_set_voltage = caget(self.PV_dict['bias_set_voltage'])

        if fc_set_voltage > -199.:
            print('FC bias set voltage is too small, changing set voltage to -200V')
            caput(self.PV_dict['bias_set_voltage'], -200)
            time.sleep(3)
            fc_set_voltage = caget(self.PV_dict['bias_set_voltage'])
            if fc_set_voltage > -199.:
                dummy = raw_input("Unable to set FC bias voltage, press Enter to continue...")
            else:
                print('FC bias set voltage changed to -200V')

        fc_status = caget(self.PV_dict['bias_status'])

        if fc_status == 1:
            print('FC bias is on')
            return
        else:
            caput(self.PV_dict['bias_on'],1)
            print('FC bias is off, turning on FC bias')

        for i in range(20):
            time.sleep(1)
            fc_status = caget(self.PV_dict['bias_status'])

            if fc_status == 1:
                print('FC bias turned on')
                return

        dummy = raw_input("Unable to turn on FC bias, press Enter to continue...")

    def enable(self):
        enable_status = caget(self.PV_dict['enable_status'])

        if enable_status == 1:
            print('Scanner already enabled')
            return
        else:
            caput(self.PV_dict['enable_on'],1)
            print('Scanner not enabled, enabling scanner')

        for i in range(8):
            time.sleep(1)
            fc_status = caget(self.PV_dict['enable_status'])

            if fc_status == 1:
                print('Scanner enabled')
                return

        raise Exception("Unable to enable scanner")

    def initiate_scan(self):

        if caget(self.PV_dict['scan_status']) != 0:
            raise Exception("Scan already running, cannot initiate scan")

        caput(self.PV_dict['scan_start'], 1,wait=False, timeout=10)
        print('Starting scan')

        time.sleep(3)

        if caget(self.PV_dict['scan_status']) == 0:
            raise Exception("Scan does not start")
        else:
            print('Scan started')

        #while caget(self.PV_dict['scan_status']) == 1:
        while caget(self.PV_dict['scan_status']) != 9:
            time.sleep(1)

        time.sleep(5)
        print("Scan completed, scanner returning to default position")

    def read_data(self):
        self.raw_data = np.copy(caget(self.PV_dict['data']))
        np.trim_zeros(self.raw_data)

        if self.x_or_y == 'x':
            self.scan_parameters = np.array([0, self.pos_start, self.pos_end, self.pos_step, self.vol_start, self.vol_end, self.vol_step])
        elif self.x_or_y == 'y':
            self.scan_parameters = np.array([1, self.pos_start, self.pos_end, self.pos_step, self.vol_start, self.vol_end, self.vol_step])
        else:
            raise Exception('x_or_y not defined properly')

        self.output_data = np.append(self.scan_parameters, self.raw_data)

        np.savetxt(self.name + '_RawData.out', self.output_data)
