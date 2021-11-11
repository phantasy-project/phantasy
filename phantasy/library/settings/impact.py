# encoding: UTF-8

"""Library for reading device settings from IMPACT input file (test.in)."""

import logging
import os
from collections import OrderedDict

from phantasy.library.layout import BCMElement
from phantasy.library.layout import BLElement
from phantasy.library.layout import BLMElement
from phantasy.library.layout import BPMElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import CavityElement
from phantasy.library.layout import CorElement
from phantasy.library.layout import DriftElement
from phantasy.library.layout import PMElement
from phantasy.library.layout import PortElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import SeqElement
from phantasy.library.layout import SextElement
from phantasy.library.layout import SolCorElement
from phantasy.library.layout import StripElement
from phantasy.library.layout import ValveElement

from .common import Settings

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

_LOGGER = logging.getLogger(__name__)


def build_settings(accel, latpath, start=None, end=None):
	"""Convenience method for initialize SettingsFactory and generate settings.

	   :param accel: accelerator design description element
	   :param latpath: path to lattice file (test.in)
	   :param start: name of accelerator element to start processing
	   :param end: name of accelerator element to end processing
	"""
	settings_factory = SettingsFactory(accel, latpath)

	if start is not None:
		settings_factory.start = start

	if end is not None:
		settings_factory.end = end

	return settings_factory.build()


class SettingsFactory(object):
	"""SettingsFactory is a factory class to build a settings dictionary from
	   and IMPACT lattice file (test.in) based on an Accelerator Design Description

	   :param accel: accelerator design description element
	   :param latpath: path to lattice file (test.in)
	"""

	def __init__(self, accel, latpath):
		self.accel = accel
		self.latpath = latpath
		self.start = None
		self.end = None

	@property
	def accel(self):
		return self._accel

	@accel.setter
	def accel(self, accel):
		if not isinstance(accel, SeqElement):
			raise TypeError("AccelFactory: 'accel' property much be type SeqElement")
		self._accel = accel

	@property
	def latpath(self):
		return self._latpath

	@latpath.setter
	def latpath(self, latpath):
		if not isinstance(latpath, str):
			raise TypeError("AccelFactory: 'latpath' property much be type string")
		self._latpath = latpath

	@property
	def start(self):
		return self._start

	@start.setter
	def start(self, start):
		if (start is not None) and not isinstance(start, str):
			raise TypeError("AccelFactory: 'start' property much be type string or None")
		self._start = start

	@property
	def end(self):
		return self._end

	@end.setter
	def end(self, end):
		if (end is not None) and not isinstance(end, str):
			raise TypeError("AccelFactory: 'end' property much be type string or None")
		self._end = end

	def build(self):
		"""Generate the settings dictionary from the IMPACT lattice file.
		"""
		if not os.path.isfile(self._latpath):
			raise RuntimeError("SettingsFactory: IMPACT lattice file not found: {}".format(self._latpath))

		with open(self._latpath, "r") as fp:
			lattice_elements = list(_LatticeIterator(fp.readlines(), skip=11))
			lattice_elements.reverse()

		settings = Settings()

		for elem in self._accel.iter(self.start, self.end):

			if isinstance(elem, CavityElement):

				(latidx, latelm) = lattice_elements.pop()

				if latelm[3] not in ["103", "110"]:
					raise RuntimeError(
						"SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx + 1,
																							  latelm))

				if not self._isclose(float(latelm[0]), elem.length):
					raise RuntimeError(
						"SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name,
																									latidx + 1,
																									latelm[0],
																									elem.length))

				_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx + 1, latelm)

				settings[elem.name] = OrderedDict()
				settings[elem.name][elem.fields.phase] = float(latelm[6])
				settings[elem.name][elem.fields.amplitude] = float(latelm[4])
				settings[elem.name][elem.fields.frequency] = float(latelm[5])

			elif isinstance(elem, SolCorElement):
				# Solenoid elements are normally split into a number of steps, add these steps to get the total length.
				hkick = None
				vkick = None
				length = 0.0
				while (length < elem.length) and not self._isclose(length, elem.length):
					(latidx, latelm) = lattice_elements.pop()

					if latelm[3] == "3":
						length += float(latelm[0])

					elif latelm[3] == "-21":
						if hkick is None:
							hkick = float(latelm[6])
						else:
							hkick += float(latelm[6])

						if vkick is None:
							vkick = float(latelm[8])
						else:
							vkick += float(latelm[8])

					else:
						raise RuntimeError(
							"SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx + 1,
																								  latelm))

					_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx + 1, latelm)

				if not self._isclose(length, elem.length):
					raise RuntimeError(
						"SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name,
																									latidx + 1,
																									latelm[0],
																									elem.length))

				settings[elem.name] = OrderedDict()
				settings[elem.name][elem.fields.field] = float(latelm[4])

				if hkick is not None:
					settings[elem.h.name] = OrderedDict([(elem.h.fields.angle, hkick)])
				else:
					_LOGGER.warning("SettingsFactory: %s: Missing horizontal kick setting, assuming 0.0", elem.name)
					settings[elem.h.name] = OrderedDict([(elem.h.fields.angle, 0.0)])

				if vkick is not None:
					settings[elem.v.name] = OrderedDict([(elem.v.fields.angle, vkick)])
				else:
					_LOGGER.warning("SettingsFactory: %s: Missing vertical kick setting, assuming 0.0", elem.name)
					settings[elem.v.name] = OrderedDict([(elem.v.fields.angle, 0.0)])

			elif isinstance(elem, CorElement):
				hkick = None
				vkick = None
				count = 0
				while True:
					(latidx, latelm) = lattice_elements.pop()

					if latelm[3] == "-21":
						count += 1

						if hkick is None:
							hkick = float(latelm[6])
						else:
							hkick += float(latelm[6])

						if vkick is None:
							vkick = float(latelm[8])
						else:
							vkick += float(latelm[8])

					elif count > 0:
						lattice_elements.append((latidx, latelm))
						break

					else:
						raise RuntimeError(
							"SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx + 1,
																								  latelm))

					_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx + 1, latelm)

				# Do not check the element length. Element -21 typically has length 0.0 with drift before and after the element.
				# if not self._isclose(float(latelm[0]), elem.length):
				#    raise RuntimeError("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))

				if hkick is not None:
					settings[elem.h.name] = OrderedDict([(elem.h.fields.angle, hkick)])
				else:
					_LOGGER.warning("SettingsFactory: %s: Missing horizontal kick setting, assuming 0.0", elem.name)
					settings[elem.h.name] = OrderedDict([(elem.h.fields.angle, 0.0)])

				if vkick is not None:
					settings[elem.v.name] = OrderedDict([(elem.v.fields.angle, vkick)])
				else:
					_LOGGER.warning("SettingsFactory: %s: Missing vertical kick setting, assuming 0.0", elem.name)
					settings[elem.v.name] = OrderedDict([(elem.v.fields.angle, 0.0)])

			elif isinstance(elem, BendElement):
				field = 0.0
				angle = 0.0
				length = 0.0
				entrAngle = None
				exitAngle = None
				while (length < elem.length) and not self._isclose(length, elem.length):
					(latidx, latelm) = lattice_elements.pop()

					if latelm[3] in ["4"]:
						# Field is not divided by the number of segments,
						# therefore it is not required to sum the field.
						field = float(latelm[5])
						angle += float(latelm[4])
						length += float(latelm[0])
						# get entrance angle from first element only
						if entrAngle is None:
							entrAngle = float(latelm[8])
					else:
						raise RuntimeError(
							"SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx + 1,
																								  latelm))

					_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx + 1, latelm)

				# get exit angle from last element only
				exitAngle = float(latelm[9])

				if not self._isclose(length, elem.length):
					raise RuntimeError(
						"SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name,
																									latidx + 1, length,
																									elem.length))

				settings[elem.name] = OrderedDict()
				settings[elem.name][elem.fields.field] = field
				settings[elem.name][elem.fields.angle] = angle
				settings[elem.name][elem.fields.entrAngle] = entrAngle
				settings[elem.name][elem.fields.exitAngle] = exitAngle

			elif isinstance(elem, QuadElement):
				(latidx, latelm) = lattice_elements.pop()

				if latelm[3] not in ["1", "5"]:
					raise Exception(
						"SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx + 1,
																							  latelm))

				_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx + 1, latelm)

				if not self._isclose(float(latelm[0]), elem.length):
					raise Exception(
						"SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name,
																									latidx + 1,
																									latelm[0],
																									elem.length))

				# Both element type 1 and 5 have the quad field strength at index 4. No special logic required!
				settings[elem.name] = OrderedDict([(elem.fields.gradient, float(latelm[4]))])

			elif isinstance(elem, SextElement):
				# (latidx, latelm) = next(lattice_element)
				#
				# if latelm[3] not in [ "5" ]:
				#    raise Exception("SettingsFactory: {} at line {}: unexpected element found: {}".format(elem.name, latidx+1, latelm))
				#
				# _LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx+1, latelm)
				#
				# if not self._isclose(float(latelm[0]), elem.length):
				#    raise Exception("SettingsFactory: {} at line {}: unexpected element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))
				#
				_LOGGER.warning(
					"SettingsFactory: Sextapole magnet element support not implemented. Assume field setting 0.0 T/m^2.")

				settings[elem.name] = OrderedDict([(elem.fields.field, 0.0)])

			elif isinstance(elem, StripElement):
				(latidx, latelm) = lattice_elements.pop()

				if latelm[3] != "-11":
					raise Exception(
						"SettingsFactory: {} at line {}: unexpecting element found: {}".format(elem.name, latidx + 1,
																							   latelm))

				_LOGGER.info("SettingsFactory: %s at line %s: %s", elem.name, latidx + 1, latelm)

				# Do not check element length. Element -11 typically has length 0.0, with drift before and after element.
				# if not self._isclose(float(latelm[0]), elem.length):
				#    raise Exception("SettingsFactory: {} at line {}: unexpecting element length: {} ({})".format(elem.name, latidx+1, latelm[0], elem.length))

			elif isinstance(elem, (BLMElement, BCMElement, BPMElement, BLElement, PMElement)):
				pass  # ignore diagnostic elements

			elif isinstance(elem, (DriftElement, ValveElement, PortElement)):
				pass  # ignore passive elements

			else:
				raise Exception("SettingsFactory: unsupported accel element: {}".format(elem))

		return settings

	@staticmethod
	def _isclose(a, b, rtol=1e-5, atol=1e-8):
		# Implementation adopted from NumPy 'isclose()'
		# including the default values for rtol and atol.
		return abs(a - b) <= (atol + rtol * abs(b))


class _LatticeIterator(object):
	def __init__(self, seq, skip=0):
		self._idx = -1
		self._iter = iter(seq)
		self._skip = skip

	def __iter__(self):
		return self

	def next(self):
		while self._skip > 0:
			line = self._iter.next()
			self._idx += 1
			if line.startswith("!"):
				continue
			self._skip -= 1

		while True:
			line = self._iter.next().strip()
			self._idx += 1
			if len(line) == 0:
				continue
			if line.startswith("!"):
				continue
			elm = line.split()
			if float(elm[3]) in [0, -13, -28]:
				_LOGGER.debug("SettingsFactory: Skipping line %s: %s", self._idx + 1, elm)
				continue
			return self._idx, elm
