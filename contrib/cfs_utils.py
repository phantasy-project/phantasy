#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Demos for channel finder serivce utils.

Tong Zhang <zhangt@frib.msu.edu>
2017-01-09 16:14:51 EST
"""

from phantasy.library.pv import DataSource
from phantasy.library.channelfinder import write_db
from phantasy.library.channelfinder import write_tb
from phantasy.library.channelfinder import write_json
from phantasy.library.channelfinder import write_cfs

# CFS -> SQLite
url = 'https://127.0.0.1:8181/ChannelFinder'

ds = DataSource()
ds.source = url
data = ds.get_data()
new_db1 = 'new_db1.sqlite'
write_db(data, new_db1, overwrite=True)

# CSV -> SQLite
csvfile = 'FRIB_FLAME/baseline_channels.csv'

ds = DataSource()
ds.source = csvfile
data = ds.get_data()
new_db2 = 'new_db2.sqlite'
write_db(data, new_db2, overwrite=True)

# SQLite -> SQLite
ds = DataSource()
ds.source = new_db2
data = ds.get_data()
new_db3 = 'new_db3.sqlite'
write_db(data, new_db3, overwrite=True)

# CFS -> CSV
url = 'https://127.0.0.1:8181/ChannelFinder'

ds = DataSource()
ds.source = url
data = ds.get_data()
new_csv1 = 'new_db1.csv'
write_tb(data, new_csv1, overwrite=True)


# SQLite -> CSV
ds = DataSource()
ds.source = new_db2
data = ds.get_data()
new_csv2 = 'new_db2.csv'
write_tb(data, new_csv2, overwrite=True)

# CSV -> CSV
ds = DataSource()
ds.source = new_csv2
data = ds.get_data()
new_csv3 = 'new_db3.csv'
write_tb(data, new_csv3, overwrite=True)

# CSV -> JSON
ds = DataSource()
ds.source = new_csv2
data = ds.get_data()
write_json(data, 'new_db.json', overwrite=True)

# CSV -> CFS
ds = DataSource()
ds.source = new_csv2
data = ds.get_data()
write_cfs(data, url, force=True)

# SQLite -> CFS
# CFS -> CFS
