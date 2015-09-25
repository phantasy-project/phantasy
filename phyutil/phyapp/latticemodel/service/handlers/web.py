# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Request handlers for web application.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import json
import os.path
import logging

from tempfile import TemporaryFile
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from tornado.web import authenticated, RequestHandler
from tornado.gen import maybe_future
from tornado.web import HTTPError
from tornado.gen import coroutine
from tornado.util import ObjectDict
from tornado.escape import url_escape
from bson import ObjectId

from ....common.tornado.jinja2 import Jinja2Mixin
from ....common.tornado.session import SessionMixin
from ....common.tornado.web import LogoutSessionHandler
from ....common.tornado.web import FormLoginSessionHandler


LOGGER = logging.getLogger(__name__)


class BaseLatticeHandler(RequestHandler, SessionMixin, Jinja2Mixin):
    """
    Base request handler for the lattice application.
    """

    @coroutine
    def prepare(self):
        yield maybe_future(super(BaseLatticeHandler,self).prepare())
        yield self.prepare_current_session()
        self.template_namespace = self.get_jinja2_namespace()
        self.template_namespace.login_url = self.settings.get("login_url")
        self.template_namespace.logout_url = self.settings.get("logout_url")
        data = self.application.data
        namespace = yield dict(
            lattice_types=data.find_lattice_types(),
            model_types=data.find_model_types()
        )
        self.template_namespace.update(namespace)


    def get_current_user(self):
        return self.get_current_session_user()


    def get_template_namespace(self):
        return self.template_namespace


    def render(self, template_name, *args, **kwargs):
        self.render_jinja2(template_name, *args, **kwargs)


    def render_string(self, template_name, *args, **kwargs):
        return self.render_jinja2_string(template_name, *args, **kwargs)


    def render_error(self, status_code, *args, **kwargs):
        self.set_status(status_code)
        if "reason" not in kwargs and hasattr(self, "_reason"):
            # attribute _reason should be set by set_status()
            kwargs["reason"] = self._reason
        self.render("latticemodel/error.html", *args, **kwargs)


class FileDownloadMixin(object):

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



class LatticeLoginHandler(FormLoginSessionHandler, Jinja2Mixin):
    """
    Extends the common UsernamePasswordLoginHandler with the BaseLatticeHandler.
    """

    @coroutine
    def prepare(self):
        yield maybe_future(super(LatticeLoginHandler,self).prepare())
        self.template_namespace = self.get_jinja2_namespace()


    def get_template_namespace(self):
        return self.template_namespace


    def render_string(self, template_name, *args, **kwargs):
        return self.render_jinja2_string(template_name, *args, **kwargs)

    def render(self, template_name, *args, **kwargs):
        self.render_jinja2(template_name, *args, **kwargs)


class LatticeLogoutHandler(LogoutSessionHandler):
    """
    Extends the common SessionLogoutHandler with the BaseLatticeHandler.
    """
    pass


class LatticeSearchHandler(BaseLatticeHandler):
    """
    Search for a lattice with the specified properties.
    """
    @coroutine
    def get(self):
        ctx = ObjectDict()
        ctx.search_active = True
        data = self.application.data
        ctx.particle_types = yield data.find_particle_types()
        self.render("latticemodel/lattice_search.html", **ctx)

    @coroutine
    def post(self):
        ctx = ObjectDict()
        ctx.search_active = True
        ctx.lattice_type = self.get_argument("lattice_type", None)
        ctx.particle_type = self.get_argument("particle_type", None)
        ctx.lattice_name = self.get_argument("name", None)
        ctx.lattice_description = self.get_argument("name", None)

        data = self.application.data
        ctx.lattices = yield data.search_lattices(**ctx)
        ctx.particle_types = yield data.find_particle_types()

        self.render("latticemodel/lattice_search.html", **ctx)


class LatticeUploadHandler(BaseLatticeHandler):
    """
    Upload lattice files and save to database.
    
    This class uses the application "lattice_support" settings to delegate requests.
    """
    @authenticated
    @coroutine
    def get(self):
        lattice_type = self.get_argument("type")
        lattice_support = self._construct_support(lattice_type)
        yield lattice_support.get_upload()


    @authenticated
    @coroutine
    def post(self):
        lattice_type = self.get_argument("type")
        lattice_support = self._construct_support(lattice_type)
        yield lattice_support.post_upload()


    def _construct_support(self, type_):
        """
        Construct a Lattice support class from the given lattice support tuple.
        """
        self.require_setting("lattice_support")
        for support in self.settings["lattice_support"]:
            if type_ == support[0]:
                return support[2](support[0], support[1], self)
        raise HTTPError(404)


class LatticeDetailsHandler(BaseLatticeHandler):
    """
    Render the detailed view of the lattice with the specified lattice ID
    """
    @coroutine
    def get(self, lattice_id):
        ctx = ObjectDict()
        data = self.application.data
        (ctx.lattice_types, ctx.particle_types,
            ctx.lattice, ctx.lattice_elements, ctx.models) = yield [
                data.find_lattice_types(),
                data.find_particle_types(),
                data.find_lattice_by_id(lattice_id),
                data.find_lattice_elements_by_lattice_id(lattice_id),
                data.find_models_by_lattice_id(lattice_id)
        ]

        if not ctx.lattice:
            self.render_error(404)
            return

        self.render("latticemodel/lattice_details.html", ctx)


class LatticeFileDownloadHandler(BaseLatticeHandler, FileDownloadMixin):
    """
    Download the lattice file specified by the given lattice ID and file ID.
    """
    @coroutine
    def get(self, lattice_id, file_id):
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)

        if not lattice or "files" not in lattice:
            self.render_error(404)
            return

        lattice_file_id = ObjectId(file_id)
        for lattice_file in lattice.files:
            if lattice_file._id == lattice_file_id:
                break
        else:
            self.render_error(404)
            return

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            LOGGER.error("Setting 'attachment_path' does not specify a directory")
            self.render_error(500)
            return

        location = os.path.join(file_root, lattice_file.location)
        try:
            data_file = open(location, 'r')
        except:
            LOGGER.exception("Error opening lattice file at location: %s", location)
            self.render_error(500)
            return

        with data_file:
            filename = self.clean_filename(lattice_file.filename)
            self.set_header("Content-Type", "application/octet-stream")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                self.write_file(data_file)
            except:
                LOGGER.exception("Error writing lattice file to response: %s", filename)
                self.set_status(500)
                return


class LatticeArchiveDownloadHandler(BaseLatticeHandler, FileDownloadMixin):
    """
    Download the lattice files in a single archive file (zip).
    """
    @coroutine
    def get(self, lattice_id):
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)

        if not lattice or "files" not in lattice:
            self.render_error(404)
            return

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            LOGGER.error("Setting 'attachment_path' does not specify a directory")
            self.render_error(500)
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
            LOGGER.exception("Error opening temporary file")
            self.render_error(500)
            return

        with archive_temp:
            try:
                archive_file = ZipFile(archive_temp, 'w', ZIP_DEFLATED)
            except:
                LOGGER.exception("Error opening archive file")
                self.render_error(500)
                return

            with archive_file:
                for lattice_file in lattice.files:
                    filename = unique_filename(lattice_file.filename)
                    location = os.path.join(file_root, lattice_file.location)
                    try:
                        archive_file.write(location, filename)
                    except:
                        LOGGER.exception("Error writing to archive file from location: %s", location)
                        self.render_error(500)
                        return

            filename = self.clean_filename(lattice.name + ".zip")
            self.set_header("Content-Type", "application/zip")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                archive_temp.seek(0)
                self.write_file(archive_temp)
            except:
                LOGGER.exception("Error writing temporary file to response: %s", filename)
                self.set_status(500)
                return


class ModelSearchHandler(BaseLatticeHandler):
    """
    Search for a lattice with the specified properties.
    """
    @coroutine
    def get(self):
        ctx = ObjectDict()
        ctx.search_active = True
        data = self.application.data
        #ctx.particle_types = yield data.find_particle_types()
        self.render("latticemodel/model_search.html", **ctx)

    @coroutine
    def post(self):
        ctx = ObjectDict()
        ctx.search_active = True
        #ctx.lattice_type = self.get_argument("lattice_type", None)
        #ctx.particle_type = self.get_argument("particle_type", None)
        ctx.model_name = self.get_argument("name", None)
        ctx.model_description = self.get_argument("description", None)
 
        data = self.application.data
        ctx.models = yield data.search_models(**ctx)
        #ctx.particle_types = yield data.find_particle_types()
 
        self.render("latticemodel/model_search.html", ctx)


class ModelUploadHandler(BaseLatticeHandler):
    """
    Upload lattice files and save to database.
    
    This class uses the application "lattice_support" settings to delegate requests.
    """
    @authenticated
    @coroutine
    def get(self):
        lattice_type = self.get_argument("type")
        lattice_support = self._construct_support(lattice_type)
        yield lattice_support.get_upload()


    @authenticated
    @coroutine
    def post(self):
        lattice_type = self.get_argument("type")
        lattice_support = self._construct_support(lattice_type)
        yield lattice_support.post_upload()


    def _construct_support(self, type_):
        """
        Construct a Lattice support class from the given lattice support tuple.
        """
        self.require_setting("model_support")
        for support in self.settings["model_support"]:
            if type_ == support[0]:
                return support[2](support[0], support[1], self)
        raise HTTPError(404)


class ModelDetailsHandler(BaseLatticeHandler):
    
    @coroutine
    def get(self, model_id):
        ctx = ObjectDict()
        data = self.application.data
        ctx.model, ctx.model_elements = yield [
            data.find_model_by_id(model_id),
            data.find_model_elements_by_model_id(model_id)
        ]
        #data.find_lattice_elements_by_lattice_id(lattice_id)
        if not ctx.model:
            self.render_error(404)
            return

        ctx.lattice, lattice_elements = yield [
            data.find_lattice_by_id(ctx.model.lattice_id),
            data.find_lattice_elements_by_lattice_id(ctx.model.lattice_id)
        ]

        ctx.lattice_elements = {}
        for lattice_element in lattice_elements:
            ctx.lattice_elements[lattice_element._id] = lattice_element

        self.render("latticemodel/model_details.html", ctx)


class ModelFileDownloadHandler(BaseLatticeHandler, FileDownloadMixin):
    """
    Download the model file specified by model ID and file ID.
    """
    @coroutine
    def get(self, model_id, file_id):
        data = self.application.data
        model = yield data.find_model_by_id(model_id)

        if not model or "files" not in model:
            self.render_error(404)
            return

        model_file_id = ObjectId(file_id)
        for model_file in model.files:
            if model_file._id == model_file_id:
                break
        else:
            self.render_error(404)
            return

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            LOGGER.error("Setting 'attachment_path' does not specify a directory")
            self.render_error(500)
            return

        location = os.path.join(file_root, model_file.location)
        try:
            data_file = open(location, 'r')
        except:
            LOGGER.exception("Error opening model file at location: %s", location)
            self.render_error(500)
            return

        with data_file:
            filename = self.clean_filename(model_file.filename)
            self.set_header("Content-Type", "application/octet-stream")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                self.write_file(data_file)
            except:
                LOGGER.exception("Error writing model file to response: %s", filename)
                self.set_status(500)
                return


class ModelArchiveDownloadHandler(BaseLatticeHandler, FileDownloadMixin):
    """
    Download the model files in a single archive file (zip).
    """
    @coroutine
    def get(self, model_id):
        data = self.application.data
        model = yield data.find_model_by_id(model_id)

        if not model or "files" not in model:
            self.render_error(404)
            return

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            LOGGER.error("Setting 'attachment_path' does not specify a directory")
            self.render_error(500)
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
            LOGGER.exception("Error opening temporary file")
            self.render_error(500)
            return

        with archive_temp:
            try:
                archive_file = ZipFile(archive_temp, 'w', ZIP_DEFLATED)
            except:
                LOGGER.exception("Error opening archive file")
                self.render_error(500)
                return

            with archive_file:
                for model_file in model.files:
                    filename = unique_filename(model_file.filename)
                    location = os.path.join(file_root, model_file.location)
                    try:
                        archive_file.write(location, filename)
                    except:
                        LOGGER.exception("Error writing to archive file from location: %s", location)
                        self.render_error(500)
                        return

            filename = self.clean_filename(model.name + ".zip")
            self.set_header("Content-Type", "application/zip")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                archive_temp.seek(0)
                self.write_file(archive_temp)
            except:
                LOGGER.exception("Error writing temporary file to response: %s", filename)
                self.set_status(500)
                return


class ModelElementPropertyValuesHandler(BaseLatticeHandler):

    @coroutine
    def get(self, model_id, property_name):
        data = self.application.data
        result = yield data.find_model_elements_property_values(model_id, property_name)
        self.set_header("Content-Type", "application/json")
        json.dump(result, self)
        self.finish()


class RestLatticeHandler(BaseLatticeHandler):
    """
    """
    @coroutine
    def get(self, lattice_id):
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)
        for key in lattice.keys():
            if key.endswith("_id"):
                lattice[key] = str(lattice[key])
            elif key.endswith("_date"):
                lattice[key] = str(lattice[key])
        self.set_header("Content-Type", "application/json")
        json.dump(lattice, self)

