#!/bin/bash

#
# build ES index for channel finder service
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-02 14:35:11 PM EST
#

cfs_dir="/home/tong1/work/FRIB/projects/CFS/ChannelFinderService/channelfinder"
bash "${cfs_dir}/src/main/resources/mapping_definitions.sh"

