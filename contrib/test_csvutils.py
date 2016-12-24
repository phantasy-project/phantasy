#!/usr/bin/env python

"""
test csv_utils
"""

import csv
#from phyutil.phylib.common import csv_utils
import csvutils

csvfile = 'channels.csv'

#csv_utils.read_csv(csvfile)
csvdata = list(csv.reader(open(csvfile)))
csvutils._read_csv_1(csvdata)

