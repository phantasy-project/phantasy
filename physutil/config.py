# encoding: UTF-8

"""
Utilities for handling configuration file.
"""

from __future__ import print_function

import os.path, json

from collections import OrderedDict


class Configuration(OrderedDict):

    @classmethod
    def read(cls, confpath):

        if not os.path.isfile(confpath)
            raise Exception("Config: file not found: {}".format(confpath))

        with open(confpath, "r") as conffile:
            return json.load(conffile, object_pairs_hook=cls))


class BaseFactory(object):

	def __init__(self):
		pass
