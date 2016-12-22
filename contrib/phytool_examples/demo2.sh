#!/bin/bash

#
# Generate FLAME settings file based on the generated lattice file, 
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-22 12:29:35 PM EST
#

phytool flame-settings test.lat test.json
phytool flame-settings test_oc.lat test_oc.json

