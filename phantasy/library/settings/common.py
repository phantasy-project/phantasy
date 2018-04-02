#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from copy import deepcopy
from collections import OrderedDict

try:
	basestring
except:
	basestring = str


class Settings(OrderedDict):
	"""Settings is a simple extention of :class:`OrderedDict` with
	the addition of some utility functions for use within the library.
	"""
	def __init__(self, settingsPath=None):
		super(Settings, self).__init__()
		# if settingsPath is not None:
		if isinstance(settingsPath, basestring):
			with open(settingsPath, "rb") as fp:
				self.readfp(fp)

	def readfp(self, fp):
		"""Read settings from file-like object in JSON format.

		Parameters
		----------
		fp :
			File-like object to read settings.
		"""
		self.update(json.load(fp, object_pairs_hook=OrderedDict))

	def __deepcopy__(self, memo):
		"""Due to the custom class initializer the default deepcopy
		implementation is broken. Override it to make it work again.
		"""
		s = Settings()
		s.update(deepcopy(self.items(), memo))
		return s
