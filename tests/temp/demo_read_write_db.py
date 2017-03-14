#!/usr/bin/python

"""demo of database:
    1: read data from SQLite or CFS
    2: write data to SQLite to serve as a local CFS by CFCDatabase class
"""

from phantasy.library.channelfinder import get_data_from_db
from phantasy.library.channelfinder import get_data_from_cf
from phantasy.library.channelfinder import write_db
from phantasy.library.channelfinder import init_db

# read data from database
db = '../../contrib/FRIB_FLAME/baseline_channels.sqlite'
data = get_data_from_db(db_name=db)

# read data from cfs
url = 'https://127.0.0.1:8181/ChannelFinder'
data = get_data_from_cf(url=url)

# write data
new_db = 'new_db.sqlite'
init_db(new_db, overwrite=True, extra_cols=['pvStatus'])
write_db(data=data, db_name=new_db)
