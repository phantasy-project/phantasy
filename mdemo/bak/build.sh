#!/bin/bash

START_ELEM="LS1_CA01:CAV1_D1127"
END_ELEM="FS1_BMS:IP_D2703"

echo "Generate layout..."
phytool frib-layout --cfg phantasy.cfg \
    --start=${START_ELEM} \
    --end=${END_ELEM} \
    LS1FS1_layout.csv

echo "Generate channels in CSV"
phytool frib-channels LS1FS1_layout.csv \
    LS1FS1_channels.csv \
    --start ${START_ELEM} \
    --end  ${END_ELEM} \
    --tag 'phantasy.LINAC' --machine 'VA'

#echo "Generate channels in SQLite"
#phytool cfutil-export \
#    --from LS1FS1_channels.csv \
#    --to LS1FS1_channels.sqlite

echo "Push channels to ChannelFinder"
phytool cfutil-update LS1FS1_channels.csv --url https://127.0.0.1:8181/ChannelFinder
