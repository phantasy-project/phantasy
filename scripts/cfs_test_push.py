#!/usr/bin/env python

""" simple test to talk to CFS

Tong Zhang <zhangt@frib.msu.edu>
2016-10-28 10:25:41 AM EDT
"""

import sys
import csv
import os

import channelfinder as cf

def push_data(csv_filename):
    csv_dir = "/home/tong1/work/FRIB/projects/CFS/cf_test/"
    csv_file = os.path.join(csv_dir, csv_filename)

    cfs_url = "https://127.0.0.1:8181/ChannelFinder"
    client = cf.ChannelFinderClient(BaseURL=cfs_url) 

    csv_info = parse_channels(csv_file)
    tags = csv_info['tags']
    properties = csv_info['properties']
    channels = csv_info['channels']
    
    try:
        client.set(properties=properties)
    except:
        pass
    try:
        client.set(tags=tags)
    except:
        pass

    try:
        client.set(channels=channels)
    except:
        pass

    #for ch in channels:
    #    client.update(channel=ch)

    #new_channel1 = {
    #                'name'  : 'test_channel_1', 
    #                'owner' : 'tong',
    #                'properties': [
    #                    {'name':'p1', 'value':'v1'},
    #                    {'name':'p2', 'value':'v2'},
    #                ],
    #               }
    #client.set(properties)
    #client.update(channel=new_channel1)

def parse_channels(fname, ftype='csv'):
    """ generate list of channel dict from file

    :param fname: file name
    :param ftype: file type, 'csv' by default
    :return: dict, keys: 'tags', 'properties', 'channels'
    """
    try:
        f = open(fname, 'r')
    except:
        print('Cannot open %s' % fname)
        sys.exit(1)

    freader = csv.reader(f, delimiter=',')
    property_names = freader.next()
    property_list = [{'name':n, 'owner':'tong'} for n in property_names]
    property_list.pop(0)
    #client.set(properties=property_list)

    tagnames = set() 
    channels = []
    for line in freader:
        p = dict(zip(property_names, line))
        tmp_tagnames = list(set(line) - set(p.values()))

        new_ch = {'name':p.pop('PV'), 'owner':'tong'}
        new_ch['properties'] = [{'name':k, 'value':v} for k,v in p.items()]

        tmp_tags = [{'name':t, 'owner':'tong'} for t in tmp_tagnames]
        new_ch['tags'] = tmp_tags
        tagnames.update(set(tmp_tagnames))

        channels.append(new_ch)
    
    tags = [{'name':t, 'owner':'tong'} for t in tagnames]

    return {'tags': tags, 'properties': property_list, 'channels': channels}
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        f1 = 'test1.csv'
        push_data(f1)
    else:
        f2 = 'baseline_channels.csv'
        push_data(f2)
