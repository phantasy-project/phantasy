#!/bin/bash

#
# install
#

cwd=$(pwd)
cd ${HOME}
git clone https://github.com/archman/pyCFClient.git
export PYTHONPATH=${HOME}/pyCFClient:${PYTHONPATH}
python -c "import channelfinder"
cd ${cwd}

