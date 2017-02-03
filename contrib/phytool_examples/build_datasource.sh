#!/bin/bash

#
# Build machine datasource from layout
# 
# Tong Zhang <zhangt@frib.msu.edu>
# 2017-02-03 12:13:58 EST
#
#

CSVLAYOUT='baseline_layout.csv'
CSVCHANNELS='baseline_channels.csv'
SQLCHANNELS='baseline_channels.sqlite'
CFSURL="https://127.0.0.1:8181/ChannelFinder"

PREFIXMACH='VA'
TAGS='phyutil.sys.LINAC'

phytool frib-channels ${CSVLAYOUT} ${CSVCHANNELS} --machine ${PREFIXMACH} --tag ${TAGS}
phytool cfutil-export --from ${CSVCHANNELS} --to ${SQLCHANNELS}
phytool cfutil-export --from ${CSVCHANNELS} --to ${CFSURL}
