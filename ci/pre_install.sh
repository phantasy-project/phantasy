#!/bin/bash

#
# before_install
#

sudo apt-get update -qq

sudo apt-get install -y -qq \
    libboost-dev libboost-system-dev \
    libboost-thread-dev libboost-filesystem-dev \
    libboost-regex-dev libboost-program-options-dev \
    libboost-test-dev \
    build-essential cmake bison flex cppcheck git libhdf5-dev \
    doxygen python-dev

sudo apt-get install -y -qq python-numpy python-matplotlib \
    python-scipy python-xlrd

sudo apt-get install -y -qq libatlas-dev liblapack-dev gfortran
