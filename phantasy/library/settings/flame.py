# encoding: UTF-8

"""Library for reading device settings from FLAME imput file (test.lat)."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import os
import logging
from collections import OrderedDict

from flame import GLPSParser

from .common import Settings
from phantasy.library.layout import CavityElement
from phantasy.library.layout import SolElement
from phantasy.library.layout import BendElement
from phantasy.library.layout import HCorElement
from phantasy.library.layout import VCorElement
from phantasy.library.layout import QuadElement
from phantasy.library.layout import EQuadElement
from phantasy.library.layout import EBendElement


def build_settings(latpath, start=None, end=None):
    """Convenience method to initialize SettingsFactory and generate settings
    from lattice file.

    Parameters
    ----------
    latpath :
        Path to lattice file.
    start : str
        Name of accelerator element to start processing.
    end : str
        Name of accelerator element to end processing.
    """
    settings_factory = SettingsFactory(latpath)

    if start is None:
        settings_factory.start = start

    if end is None:
        settings_factory.end = end

    return settings_factory.build()


class SettingsFactory(object):
    """SettingsFactory is a factory class to build a settings dictionary from
    a FLAME lattice file (test.lat).

    Parameters
    ----------
    latpath :
        Path to lattice file (test.lat)
    """

    def __init__(self, latpath=None):
        #self.accel = accel
        self._latpath = latpath
        self._start = None
        self._end = None

    @property
    def latpath(self):
        return self._latpath

    @latpath.setter
    def latpath(self, latpath):
        if not isinstance(latpath, basestring):
            raise TypeError("AccelFactory: 'latpath' property much be type string")
        self._latpath = latpath


    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if (start is not None) and not isinstance(start, basestring):
            raise TypeError("AccelFactory: 'start' property much be type string or None")
        self._start = start


    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if (end is not None) and not isinstance(end, basestring):
            raise TypeError("AccelFactory: 'end' property much be type string or None")
        self._end = end


    def build(self):
        """Generate the settings dictionary from the FLAME lattice file.
        """
        if not os.path.isfile(self._latpath):
            raise RuntimeError("SettingsFactory: FLAME lattice file not found: {}".format(self._latpath))

        with open(self._latpath, "r") as fp:
            conf = OrderedDict(GLPSParser().parse(fp))

        settings = Settings()

        if 'elements' not in conf:
            return settings

        def parseName(cname):
            # Too FRIB specific!
            parts = re.split("[_:]", cname)
            name = parts[0] + "_" + parts[1] + ":" + parts[2] + "_" + parts[3]
            return name.upper()

        for celem in conf['elements']:
            elem = OrderedDict(celem)
            ftype = elem['type'].lower()

            if ftype in [ 'source', 'drift', 'marker' ]:
                continue

            elif ftype in [ 'bpm', 'stripper' ]:
                name = parseName(elem['name'])
                settings[name] = OrderedDict()

            elif ftype == "rfcavity":
                name = parseName(elem['name'])
                cav = CavityElement(0, 0, 0, name)
                fields = OrderedDict()
                fields[cav.fields.phase] = elem['phi']
                fields[cav.fields.amplitude] = elem['scl_fac']
                fields[cav.fields.frequency] = elem['f']
                settings[name] = fields

            elif ftype == "solenoid":
                name = parseName(elem['name'])
                sol = SolElement(0, 0, 0, name)
                fields = OrderedDict()
                fields[sol.fields.field] = elem['B']
                settings[name] = fields

            elif ftype == "orbtrim":
                name = parseName(elem['name'])
                fields = OrderedDict()
                if 'theta_x' in elem:
                    cor = HCorElement(0, 0, 0, name)
                    fields[cor.fields.angle] = elem['theta_x']
                elif 'theta_y' in elem:
                    cor = VCorElement(0, 0, 0, name)
                    fields[cor.fields.angle] = elem['theta_y']
                else:
                    cor = HCorElement(0, 0, 0, name)
                    fields[cor.fields.angle] = 0.0
                settings[name] = fields

            elif ftype == "sbend":
                name = parseName(elem['name'])
                bend = BendElement(0, 0, 0, name)
                if name not in settings:
                    fields = OrderedDict()
                    fields[bend.fields.field] = elem['bg']
                    fields[bend.fields.angle] = elem['phi']
                    fields[bend.fields.entrAngle] = elem['phi1']
                    fields[bend.fields.exitAngle] = elem['phi2']
                    settings[name] = fields
                else:
                    settings[name][bend.fields.angle] += elem['phi']
                    if elem['phi2'] != 0.0:
                        if settings[name][bend.fields.exitAngle] == 0.0:
                            settings[name][bend.fields.exitAngle] = elem['phi2']
                        else:
                            raise RuntimeError("Bend element exit angle already defined")

            elif ftype == "quadrupole":
                name = parseName(elem['name'])
                sol = QuadElement(0, 0, 0, name)
                fields = OrderedDict()  
                fields[sol.fields.gradient] = elem['B2']
                settings[name] = fields

            elif ftype == "equad":
                name = parseName(elem['name'])
                equad = EQuadElement(0, 0, 0, name)
                fields = OrderedDict()
                fields[equad.fields.gradient] = elem['V']
                settings[name] = fields

            elif ftype == "edipole":
                name = parseName(elem['name'])
                ebend = EBendElement(0, 0, 0, name)
                fields = OrderedDict()
                fields[ebend.fields.field] = elem['beta']
                settings[name] = fields

            else:
                raise RuntimeError("Flame element type not supported: " + elem['type'])

        return settings
