#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Element styles.
"""

from phantasy.library.misc import find_conf
from phantasy.library.parser import Configuration
from phantasy.library.parser.config import NoSectionError

STR_ATTRS = ('fc', 'ec', 'ls')


style_file = find_conf('element_style.ini')
style_conf = Configuration(style_file)


def get_style(etype, attr, style_conf=style_conf):
    if attr in STR_ATTRS:
        try:
            return style_conf.get(etype, attr)
        except NoSectionError:
            return style_conf.get_default(attr)
    else:
        try:
            return style_conf.getfloat(etype, attr)
        except NoSectionError:
            return style_conf.getfloat_default(attr)
