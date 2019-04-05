import numpy as np

class ASGridFRIB(object):

    def __init__(self, perform_scan = False, data_file = '', live_data = [], time = ''):

        self.perform_scan = perform_scan
        self.live_data = live_data
        self.data_file = data_file
        self.load_data()
        self.generate_grids()

        if perform_scan:
            self.name = 'FE_LEBT_AS' + self.x_or_y + '_D0739_' + time
        else:
            self.name = 'FE_LEBT_AS' + self.x_or_y + '_D0739_' + data_file[18:33]

    def load_data(self):

        if self.perform_scan:
            self.input_data = self.live_data
        else:
            self.input_data = np.loadtxt(self.data_file)

        if np.sum( np.isnan(self.input_data) ) != 0:
            self.input_data = np.nan_to_num(self.input_data)
            print('NaN values detected')

        if self.input_data[0] == 0:
            self.x_or_y = 'x'
        elif self.input_data[0] == 1:
            self.x_or_y = 'y'
        else:
            raise Exception('Scanner direction not appropriately defined')

        self.pos_start, self.pos_end, self.pos_step = self.input_data[1:4]
        self.vol_start, self.vol_end, self.vol_step = self.input_data[4:7]

        if (self.pos_end - self.pos_start)%self.pos_step != 0:
            raise Exception('Pos step not a factor of scan range')
        else:
            self.pos_count = np.int((self.pos_end - self.pos_start)/self.pos_step) + 1

        if (self.vol_end - self.vol_start)%self.vol_step != 0:
            raise Exception('Vol step not a factor of scan range')
        else:
            self.vol_count = np.int((self.vol_end - self.vol_start)/self.vol_step) + 1

        self.raw_data = self.input_data[7:]

    def generate_grids(self):

        self.x_array = np.linspace(self.pos_start, self.pos_end, self.pos_count)
        self.v_array = np.linspace(self.vol_end, self.vol_start, self.vol_count)

        self.X_grid, self.V_grid = np.meshgrid(self.x_array,self.v_array)
        self.I_grid = self.raw_data.reshape(self.vol_count, self.pos_count)
