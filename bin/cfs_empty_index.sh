#!/bin/bash

#
# empty ES index for channel finder service
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2016-12-02 14:37:40 PM EST
#

curl -XDELETE 'http://localhost:9200/channelfinder'
curl -XDELETE 'http://localhost:9200/tags'
curl -XDELETE 'http://localhost:9200/properties'
