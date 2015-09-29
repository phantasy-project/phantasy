# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#


"""
Common utilities for the Tornado Web framework.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import re


class WriteFileMixin(object):

    @staticmethod
    def clean_filename(filename):
        return re.sub(r'[^\.\-_\(\)\w]', '', filename)

    def write_file(self, file_obj, buf_size=2048):
        while True:
            buf = file_obj.read(buf_size)
            if len(buf) == buf_size:
                self.write(buf)
            else:
                self.finish(buf)
                return