#!/bin/bash

# 
# Push new PV data onto Channelfinder service,
# only valid for current directory.
# 
# Tong Zhang <zhangt@frib.msu.edu>
# 2017-02-13 15:58:02 EST
#
phytool cfutil-update baseline_channels_0.csv --op del
phytool cfutil-update baseline_channels.csv --op add
