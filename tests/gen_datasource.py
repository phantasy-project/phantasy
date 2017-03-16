#!/usr/bin/env python


"""generate data for test_datasource.py

Tong Zhang <zhangt@frib.msu.edu>
2017-01-04 17:42:33 EST
"""

import pickle

from phantasy.library.pv import DataSource


def dump_data(data, file):
    """Dump data to file.
    """
    with open(file, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def load_data(file):
    """Load data from file.
    """
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data

db = './config/FRIB_TEST/baseline_channels_bak.sqlite'
url = 'https://127.0.0.1:8181/ChannelFinder'

ds1 = DataSource(source=db)
#ds2 = DataSource(source=url)

# get_data()
data1 = ds1.get_data()
file1 = 'data/cfd_data_1.pkl'
dump_data(data1, file1)

data2 = ds1.get_data(tag_filter='phyutil.sub.CB09', prop_filter='elem*')
file2 = 'data/cfd_data_2.pkl'
dump_data(data2, file2)

data3 = ds1.get_data(prop_filter=['elem*', ('elemHandle', 'setpoint')])
file3 = 'data/cfd_data_3.pkl'
dump_data(data3, file3)
