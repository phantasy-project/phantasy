#!/bin/bash

#
# install
# 

cwd=$(pwd)
cd $HOME
git clone -b latest https://github.com/archman/FLAME.git
cd FLAME/deb
sudo dpkg -i *.deb
cd ${cwd}

#export PYTHONPATH=/usr/lib/python2.7/dist-packages/:${PYTHONPATH}
