#!/usr/bin/env bash

#
# install
#
pip install ./python/scipy-0.19.0-cp27-cp27mu-manylinux1_x86_64.whl
python -c "import scipy;print(scipy.__version__)"
