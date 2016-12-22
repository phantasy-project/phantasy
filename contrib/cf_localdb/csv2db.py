#!/usr/bin/env python
# -*- coding: utf-8 -*-


from phantasy.library.misc import read_csv
from phantasy.library.channelfinder import create_cf_localdb
from phantasy.library.channelfinder import import_cf_localdata


csvfile = 'impact_va.csv'
csvdata = read_csv(csvfile)
headstr = csvdata[0][2]
create_cf_localdb(dbname='impact_va.sqlite', overwrite=True,
                  colheads=headstr)

print(headstr)
print(csvdata)

#import_cf_localdata(csvdata, 'impact_va.sqlite', overwrite=True)


