#!/bin/bash

#
# install
#

cwd=$(pwd)
cd ${HOME}
git clone https://github.com/archman/PyScanClient.git
#export PYTHONPATH=${HOME}/PyScanClient:${PYTHONPATH}
#python -c "import scan"
cd ${cwd}
