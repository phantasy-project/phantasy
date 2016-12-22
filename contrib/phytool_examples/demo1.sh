#!/bin/bash

#
# Generate FLAME lattice file from configuration files,
# based on the generated lattice file, following tasks is done:
#
#   show orbit
#   correct orbit
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-22 12:23:47 PM EST
#
#echo $PHYUTIL_CONFIG_DIR
#/home/tong1/work/FRIB/projects/machines

#ls $PHYUTIL_CONFIG_DIR
#docs  examples  FRIB  FRIB_ERROR  FRIB_FLAME  README.md

# generate lattice
phytool flame-lattice --mach="FRIB_FLAME" test.lat

# plot or correct orbit
plot_orbit test.lat --output test.png
correct_orbit test.lat --iternum 10 --output test_oc.lat
correct_orbit test.lat --iternum 10 --pseudo_all --output test_oc_all.lat
plot_orbit test_oc.lat --output test_oc.png
plot_orbit test_oc_all.lat --output test_oc_all.png
