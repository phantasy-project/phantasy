# -*- coding: utf-8 -*-

"""Field mapping.
"""
import toml

from phantasy.library.misc import find_conf


fm_file = find_conf('element_fields.toml')
fm_conf = toml.load(fm_file)


def get_field_map(etype, field=None):
    if field is not None:
        return fm_conf.get(etype).get(field)
    else:
        return fm_conf.get(etype)
