#!/usr/bin/python

""" test channel finder interface
"""

from phantasy.library.channelfinder import CFCDatabase
from channelfinder import ChannelFinderClient as CFCWebserver

db = 'config/FRIB1/baseline_channels.sqlite'
url = 'https://127.0.0.1:8181/ChannelFinder'

cfc1 = CFCDatabase(db)
cfc2 = CFCWebserver(url)

print(cfc1.getAllTags())
print(cfc2.getAllTags())
print(cfc1.getAllProperties())
print(cfc2.getAllProperties())

