#!/bin/bash

#
# build ES index for channel finder service
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-02 14:35:11 PM EST
#

cfs_dir="/etc/channelfinder"
bash "${cfs_dir}/mapping_definitions.sh"

