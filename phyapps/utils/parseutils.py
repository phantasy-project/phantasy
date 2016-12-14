#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:author: Tong Zhang <zhangt@frib.msu.edu>
:time: 2016-11-14 17:29:28 PM EST
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from ConfigParser import SafeConfigParser, ConfigParser

import os
import sys
import time


class ConfigFile(object):
    """
    Class to resolve parameters parsing by applying xmlparser approach.
    """
    def __init__(self, infilename='config.xml', *args, **kwargs):
        self.xmlfile = infilename
        self.namelist = {}
        self.parseConfigs()

    def parseConfigs(self):
        pass

    def getConfigs(self):
        return self.namelist
    
    def updateConfigs(self, params_dict, savetofile=None):
        if not savetofile:
            savetofile = self.xmlfile
        for p in self.root.iter('properties'):
            for k in params_dict.keys():
                if p.get(k):
                    p.set(k, params_dict[k])
        self.tree.write(savetofile)

class IniParser(object):
    """ General parameter parser class for ``.ini`` configuration files.

    :param fname: file name of ``.ini`` configuration file
    
    """
    def __init__(self, fname='config.ini', *args, **kws):
        self.inifilename = fname
        self.parser = ConfigParser()
        self.parser.optionxform = str
        self.readConfig()

    def readConfig(self):
        if not os.path.isfile(self.inifilename): 
            self.createTemplate()
            sys.exit(1)
        else:
            self.parser.read(self.inifilename)
    
    def createTemplate(self, fname='sample.ini'):
        """ configuration sample
        """
        dict_sample = dict([
            ('COMMON', {'submachine': 'LINAC LS1', 
                        'default_submachine': 'LINAC',
                        'output_dir': "/tmp/accelerator/data",
                        }), 
            ('LINAC', {'controls_protocol': 'EPICS', 
                       's_begin': '0.0',
                       's_end': '158.094',
                       'loop': '0',
                       'model': 'impact',
                       'cfs_url': 'baseline_channels.sqlite',
                       'cfs_tag': 'phyutil.sys.LINAC',
                       'ss_url': 'http://localhost:4810',
                       'physics_data': 'linac.hdf5',
                       'unit_conversion': 'linac_unitconv.hdf5, UnitConversion',
                       'settings_file': 'baseline_settings.json',
                       'layout_file': 'baseline_layout.csv',
                       'config_file': 'phyutil.cfg',
                       'impact_map': 'ls1_fs1.map',}), 
            ])
        parser_sample = SafeConfigParser()
        for section_name in sorted(dict_sample.keys()):
            parser_sample.add_section(section_name)
            [parser_sample.set(section_name, k, v) for k, v in sorted(dict_sample[section_name].items())]
        with open(fname, 'w') as f:
            ts = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime())
            f.write('# Sample of configuration file\n')
            f.write('# Created time: {}\n'.format(ts))
            parser_sample.write(f)

    def to_dict(self, flat=False):
        """ return configuration as dict format

        :param flat: if True, return flat (k,v) dict, overidden same key,
            the default is False, i.e. return dict with hierarch structure
        """
        if flat:
            return self._make_flat_dict()
        else:
            return self._make_hier_dict()

    def _make_flat_dict(self):
        """
        return dict with key,value pairs
        """
        onedict = {}
        for section_name in self.parser.sections():
            onedict.update({k:v for k, v in self.parser.items(section_name)})
        return onedict

    def _make_hier_dict(self):
        """
        return dict with hierarch structure
        """
        rdict = dict([(sn,{k:v for k,v in self.parser.items(sn)}) for sn in self.parser.sections()])
        return rdict

    def setOneParam(self, section_name, option_name, newvalue):
        self.parser.set(section_name, option_name, newvalue)
    
    def setAllParams(self, newhierdict):
        for section_name in self.parser.sections():
            for k,v in self.parser.items(section_name):
                self.parser.set(section_name, k, newhierdict[section_name][k])

    def dumpDictToConfig(self, newhierdict, configfilename):
        newparser = SafeConfigParser()
        newparser.optionxform = str
        for section_name in sorted(newhierdict.keys()):
            newparser.add_section(section_name)
            [newparser.set(section_name, k, v) for k, v in sorted(newhierdict[section_name].items())]
        newparser.write(open(configfilename, 'w'))

    def saveConfig(self, filetosave=None):
        if filetosave == None:
            filetosave = self.inifilename
        self.parser.write(open(filetosave, 'w'))

def loadtest():
    # test load config from file
    testparser = IniParser('sample.ini')
    testparser.readConfig()
    print(testparser.makeHierDict())

def savetest():
    # test save config to file
    # save parser into new config file

    # get param dict from sample.ini which is parsed by readConfig method
    testparser = IniParser('sample.ini')
    testparser.readConfig()
    raw_dict = testparser.makeHierDict()

    # modify parameters
    raw_dict['01-facility']['name'] = 'XFEL'
    raw_dict['03-undulator']['period_length(m)'] = str(0.04)
    raw_dict['02-electron_beam']['peak_current(A)'] = str(300)
    if not raw_dict.has_key('00-info'):
        raw_dict['00-info'] = {}
    raw_dict['00-info']['time'] = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime())

    # add options
    raw_dict['04-FEL_radiation']['output_power(W)'] = '%.3e' % 1e8

    # save to new config file
    testparser.dumpDictToConfig(raw_dict, 'sxfel.conf')

if __name__ == '__main__':
    #loadtest()
    savetest()
