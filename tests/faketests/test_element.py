#!/usr/bin/env python

"""Test element module.

Tong Zhang <zhangt@frib.msu.edu>
2017-05-19 15:01:53 PM EDT
"""

import os
import json

from phantasy import CaElement


with open('../data/pv_record.json', 'r') as f:
    pv_data = json.load(f)

print(pv_data)

pv_data['pv_props']['group'] = ['group_a', 'group_b']
elem = CaElement(pv_data=pv_data)
assert elem.group == {pv_data['pv_props']['family'], 'group_a', 'group_b'}


