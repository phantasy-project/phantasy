#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This module contains classes/functions to serve as utils for the 
potential requirment of modeling with FLAME code

.. moduleauthor:: Tong Zhang <zhangt@frib.msu.edu>

:date: 2016-11-11 11:04:53 AM EST
"""

from __future__ import print_function

from flame import Machine
from numpy import ndarray


def generate_latfile(machine, latfile='out.lat'):
    """ Generate lattice file for the usage of FLAME code

    :param machine: flame machine object
    :param latfile: file name for generated lattice file, 'out.lat' by default
    :return: None if failed to generate lattice file, or the out file name

    :Example:

    >>> from flame import Machine
    >>> latfile = 'test.lat'
    >>> m = Machine(open(latfile))
    >>> outfile1 = generate_latfile(m, 'out1.lat')
    >>> m.reconfigure(80, {'theta_x': 0.1})
    >>> outfile2 = generate_latfile(m, 'out2.lat')
    >>> 
    """
    m = machine
    try:
        mconf = m.conf()
        mks = mconf.keys()
    except:
        print("Failed to load FLAME machine object.")
        return None

    try:
        mconf_ks = mconf.keys()
        [mconf_ks.remove(i) for i in ['elements', 'name'] if i in mconf_ks]

        #
        lines = []
        for k in mconf_ks:
            v = mconf[k]
            if isinstance(v, ndarray):
                v = v.tolist()
            if isinstance(v, str):
                v = '"{0}"'.format(v)
            line = '{k} = {v};'.format(k=k, v=v)
            lines.append(line)

        mconfe = mconf['elements']

        # element configuration
        elem_num = len(mconfe)
        elem_name_list = []
        for i in range(0, elem_num):
            elem_i = m.conf(i)
            ename, etype = elem_i['name'], elem_i['type']
            if ename in elem_name_list:
                continue
            elem_name_list.append(ename)
            ki = elem_i.keys()
            elem_k = set(ki).difference(mks)
            if etype == 'stripper':
                elem_k.add('IonChargeStates')
                elem_k.add('NCharge')
            p = []
            for k, v in elem_i.items():
                if k in elem_k and k not in ['name', 'type']:
                    if isinstance(v, ndarray):
                        v = v.tolist()
                    if isinstance(v, str):
                        v = '"{0}"'.format(v)
                    p.append('{k} = {v}'.format(k=k, v=v))
            pline = ', '.join(p)

            line = '{n}: {t}, {p}'.format(n=ename, t=etype, p=pline)

            line = line.strip(', ') + ';'
            lines.append(line)

        dline = '(' + ', '.join(([e['name'] for e in mconfe])) + ')'

        blname = mconf['name']
        lines.append('{0}: LINE = {1};'.format(blname, dline))
        lines.append('USE: {0};'.format(blname))
    except:
        print("Failed to generate lattice file.")
        return None

    try:
        fout = open(latfile, 'w')
        fout.writelines('\n'.join(lines))
        fout.close()
    except:
        print("Failed to write to %s" % (latfile))
        return None

    return latfile
