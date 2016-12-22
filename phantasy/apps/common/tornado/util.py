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
import json


class WriteFileMixin(object):
    """Mixin providing support for sending file-like object in response.
    """
    @staticmethod
    def clean_filename(filename):
        return re.sub(r'[^\.\-_\(\)\w]', '', filename)

    def write_file(self, file_obj, content_type="application/octet-stream", buf_size=2048):
        """Write the provided file-like object to the response.

        HTTP response is finished on completion of this method.

        :param file_obj: file-like object to be written
        :param content_type: optional content type of response (default: application/octet-stream)
        :param buf_size: optional buffer size used for reading file object
        """
        if content_type:
            self.set_header("Content-Type", content_type)
        while True:
            buf = file_obj.read(buf_size)
            if len(buf) == buf_size:
                self.write(buf)
            else:
                self.finish(buf)
                return


class WriteJsonMixin(object):
    """Mixin providing support for sending JSON encoded response.
    """
    def write_json(self, obj, content_type="application/json"):
        """Write the provided object to the response in JSON format.

        HTTP Response is finished on completion of this method.

        :param obj: data structure to be written as JSON
        :param content_type: optional content type of reponse (default: application/json)
        """
        if self.settings.get("debug", False):
            indent = 2    # pretty
        else:
            indent = None # compact
        if content_type:
            self.set_header("Content-Type", content_type)
        json.dump(obj, self, indent=indent)
        self.finish()
