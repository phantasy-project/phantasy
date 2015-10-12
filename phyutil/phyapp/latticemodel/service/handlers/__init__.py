# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Web application request handlers for Lattice Model Service.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging

from tempfile import TemporaryFile
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from tornado.gen import coroutine
from tornado.escape import url_escape

from phyutil.phyapp.common.tornado.util import WriteFileMixin


_LOGGER = logging.getLogger(__name__)


class LatticeSupportMixin(object):
    def construct_lattice_support(self, lattice_type):
        """
        Construct a Lattice support class for the given lattice type.
        """
        self.require_setting("lattice_support")
        for support in self.settings["lattice_support"]:
            if lattice_type == support[0]:
                return support[2](support[0], support[1], self)
        self.send_error(404)
        return



class LatticeFileDownloadMixin(WriteFileMixin):
    """Mixin implementing Lattice file download.
    """
    @coroutine
    def get_lattice_file(self, lattice_id, file_id):
        """Retrieve the specified Lattice file.

        :param lattice_id: Lattice ID
        :param file_id: Lattice File ID
        """
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)

        if not lattice or "files" not in lattice:
            self.send_error(404)
            return

        for lattice_file in lattice.files:
            if lattice_file.id == file_id:
                break
        else:
            self.send_error(404)
            return

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            _LOGGER.error("Setting 'attachment_path' does not specify a directory")
            self.send_error(500)
            return

        location = os.path.join(file_root, lattice_file.location)
        try:
            data_file = open(location, 'r')
        except:
            _LOGGER.exception("Error opening lattice file at location: %s", location)
            self.send_error(500)
            return

        with data_file:
            filename = self.clean_filename(lattice_file.filename)
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                print(self._headers)
                self.write_file(data_file, content_type="application/octet-stream")
            except:
                _LOGGER.exception("Error writing lattice file to response: %s", filename)
                self.send_error(500)
                return


    @coroutine
    def get_lattice_files(self, lattice_id):
        """Retrieve the specified Lattice files and create file archive.

        :param lattice_id: Lattice ID
        """
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)

        if not lattice or "files" not in lattice:
            self.send_error(404)
            return

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            _LOGGER.error("Setting 'attachment_path' does not specify a directory")
            self.send_error(500)
            return

        filenames = set()
        def unique_filename(filename):
            filename = self.clean_filename(filename)
            if filename in filenames:
                name, ext = os.path.splitext(filename)
                for idx in range(100):
                    filename = "{}({}).{}".format(name, idx, ext)
                    if filename not in filenames:
                        break
            filenames.add(filename)
            return filename

        try:
            archive_temp = TemporaryFile()
        except:
            _LOGGER.exception("Error opening temporary file")
            self.send_error(500)
            return

        with archive_temp:
            try:
                archive_file = ZipFile(archive_temp, 'w', ZIP_DEFLATED)
            except:
                _LOGGER.exception("Error opening archive file")
                self.send_error(500)
                return

            with archive_file:
                for lattice_file in lattice.files:
                    filename = unique_filename(lattice_file.filename)
                    location = os.path.join(file_root, lattice_file.location)
                    try:
                        archive_file.write(location, filename)
                    except:
                        _LOGGER.exception("Error writing to archive file from location: %s", location)
                        self.send_error(500)
                        return

            filename = self.clean_filename(lattice.name + ".zip")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                archive_temp.seek(0)
                self.write_file(archive_temp, content_type="application/zip")
            except:
                _LOGGER.exception("Error writing temporary file to response: %s", filename)
                self.send_error(500)
                return

