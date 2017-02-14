#!/bin/bash

#
# start virtual accelerator
#
# 2016-09-22 15:32:08 PM EDT
# 

if [ $# -eq 0 ]
then
    echo "Usage: `basename $0` va_engine"
    echo " va_engine: engine to be used to simulate virtual accelerator"
    echo "            'flame' or 'impact', case sensitive"
    echo "            if not defined, use 'flame' by default."
fi

va_engine=${1:-"flame"}

if [ "x${va_engine}" != "xflame" ] && [ "x${va_engine}" != "ximpact" ]
then
    echo "wrong engine input, use 'flame' or 'impact'"
    exit 1
fi

phytool ${va_engine}-vastart -v --mach="FRIB_FLAME"
