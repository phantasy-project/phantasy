#!/bin/bash

#
# Generate lattice layout file from configuration files,
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-22 13:24:53 PM EST
#
mach="../FRIB_FLAME"
xlf_file=${mach}/"T30102-CM-000155-R001_20150227.xlsx"
cfg_file=${mach}/"phyutil.cfg"

#phytool frib-layout --xlf ${xlf_file} --cfg ${cfg_file} test.layout.csv
phytool frib-layout --cfg ${cfg_file} test_layout.csv
