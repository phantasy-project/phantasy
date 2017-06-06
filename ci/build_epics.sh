#!/bin/bash

#
# before_install
#

cwd=$(pwd)
wget -q https://www.aps.anl.gov/epics/download/base/baseR3.14.12.6.tar.gz \
    -O /tmp/base.tar.gz
tar xvf /tmp/base.tar.gz -C $HOME
cd $HOME/base-3.14.12.6
make -j2
cd ${cwd}
