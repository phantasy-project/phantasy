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

import json
import logging

from tornado.web import authenticated
from tornado.web import RequestHandler
from tornado.gen import maybe_future
from tornado.gen import coroutine
from tornado.util import ObjectDict

from phantasy.apps.common.tornado.jinja2 import Jinja2Mixin
from phantasy.apps.common.tornado.session import SessionMixin
from phantasy.apps.common.tornado.web import LogoutSessionHandler
from phantasy.apps.common.tornado.web import FormLoginSessionHandler
from phantasy.apps.common.tornado.util import WriteJsonMixin

from . import LatticeSupportMixin
from . import ModelSupportMixin
from . import FileDownloadMixin


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
        self.send_error(status_code, *args, **kwargs)


    def write_error(self, status_code, *args, **kwargs):
        self.set_status(status_code)
        if "reason" not in kwargs and hasattr(self, "_reason"):
            # attribute _reason should be set by set_status()
            kwargs["reason"] = self._reason
        self.render("latticemodel/error.html", *args, **kwargs)



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
    Search for Lattices with the specified properties.
    """
    @coroutine
    def get(self):
        ctx = ObjectDict()
        ctx.search_active = True
        ctx.search = ObjectDict()
        data = self.application.data
        ctx.particle_types = yield data.find_particle_types()
        self.render("latticemodel/lattice_search.html", **ctx)

    @coroutine
    def post(self):
        ctx = ObjectDict()
        ctx.search_active = True
        ctx.search = ObjectDict()
        ctx.search.lattice_type = self.get_argument("lattice_type", None)
        ctx.search.particle_type = self.get_argument("particle_type", None)
        ctx.search.name = self.get_argument("name", None)
        ctx.search.branch = self.get_argument("branch", None)
        ctx.search.version = self.get_argument("version", None)
        ctx.search.properties = self.get_argument("properties", None)
        #ctx.lattice_description = self.get_argument("name", None)
        data = self.application.data
        ctx.lattices = yield data.search_lattices(**ctx.search)
        ctx.particle_types = yield data.find_particle_types()
        self.render("latticemodel/lattice_search.html", **ctx)


class LatticeCompareHandler(BaseLatticeHandler):
    """Compare the two specified Lattices.
    """
    @coroutine
    def post(self):
        data = self.application.data
        lattice_ids = self.get_arguments("lattice")
        if len(lattice_ids) < 2:
            self.send_error(400, message="Must select two lattice for comparison")
            return

        lattice1 = yield data.find_lattice_by_id(lattice_ids[0])
        if not lattice1:
            self.send_error(400, message="Lattice (1) not found: " + lattice_ids[0])
            return
        lattice_elements1 = yield data.find_lattice_elements_by_lattice_id(lattice_ids[0])

        lattice2 = yield data.find_lattice_by_id(lattice_ids[1])
        if not lattice2:
            self.send_error(400, message="Lattice (2) not found: " + lattice_ids[1])
            return
        lattice_elements2 = yield data.find_lattice_elements_by_lattice_id(lattice_ids[1])

        ctx = ObjectDict()
        ctx.lattice = (lattice1, lattice2)

        n1 = len(lattice_elements1)
        n2 = len(lattice_elements2)
        ctx.lattice_elements = []
        for idx in range(max(n1, n2)):
            if idx < n1 and idx < n2:
                ctx.lattice_elements.append((lattice_elements1[idx], lattice_elements2[idx]))
            elif idx < n1:
                ctx.lattice_elements.append((lattice_elements1[idx], None))
            elif idx < n2:
                ctx.lattice_elements.append((None, lattice_elements2[idx]))

        ctx.particle_types = yield data.find_particle_types()
        self.render("latticemodel/lattice_compare.html", **ctx)


class LatticeNamesHandler(BaseLatticeHandler, WriteJsonMixin):
    """Find the names of Lattice matching the specified query.
    """
    @coroutine
    def get(self):
        yield self.post()

    @coroutine
    def post(self):
        query = self.get_argument("query", "")
        data = self.application.data
        names = yield data.find_lattice_names(query)
        self.write_json(names)


class LatticeBranchesHandler(BaseLatticeHandler, WriteJsonMixin):
    """Find the branches of Lattice matching the specified query.
    """
    @coroutine
    def get(self):
        yield self.post()

    @coroutine
    def post(self):
        query = self.get_argument("query", "")
        data = self.application.data
        names = yield data.find_lattice_branches(query)
        self.write_json(names)


class LatticeUploadHandler(BaseLatticeHandler, LatticeSupportMixin):
    """
    Upload lattice files and save to database.

    This class uses the application "lattice_support" settings to delegate requests.
    """
    @authenticated
    @coroutine
    def get(self, type_id):
        lattice_support = self.construct_lattice_support(type_id)
        yield lattice_support.web_form_upload_get()


    @authenticated
    @coroutine
    def post(self, type_id):
        lattice_support = self.construct_lattice_support(type_id)
        yield lattice_support.web_form_upload_post()


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
        yield self.get_lattice_file(lattice_id, file_id)


class LatticeFilesDownloadHandler(BaseLatticeHandler, FileDownloadMixin):
    """
    Download the lattice files in a single archive file (zip).
    """
    @coroutine
    def get(self, lattice_id):
        yield self.get_lattice_files(lattice_id)


class ModelSearchHandler(BaseLatticeHandler):
    """
    Search for a lattice with the specified properties.
    """
    @coroutine
    def get(self):
        ctx = ObjectDict()
        ctx.search_active = True
        ctx.search = ObjectDict()
        self.render("latticemodel/model_search.html", **ctx)

    @coroutine
    def post(self):
        ctx = ObjectDict()
        ctx.search_active = True
        ctx.search = ObjectDict()
        ctx.search.model_type = self.get_argument("model_type", None)
        ctx.search.name = self.get_argument("name", None)
        ctx.search.properties = self.get_argument("properties", None)
        #ctx.model_description = self.get_argument("description", None)
        data = self.application.data
        ctx.models = yield data.search_models(**ctx.search)
        self.render("latticemodel/model_search.html", ctx)


class ModelCompareHandler(BaseLatticeHandler):
    """Compare the two specified Models.
    """
    @coroutine
    def post(self):
        data = self.application.data
        model_ids = self.get_arguments("model")
        if len(model_ids) < 2:
            self.send_error(400, message="Must select two models for comparison")
            return

        model1, model2 = yield [
            data.find_model_by_id(model_ids[0]),
            data.find_model_by_id(model_ids[1])
        ]

        if not model1:
            self.send_error(400, message="Model (1) not found: " + model_ids[0])
            return

        if not model2:
            self.send_error(400, message="Model (2) not found: " + model_ids[1])
            return

        lattice1, lattice2, model_elements1, model_elements2 = yield [
            data.find_lattice_by_id(model1.lattice_id),
            data.find_lattice_by_id(model2.lattice_id),
            data.find_model_elements_by_model_id(model1._id),
            data.find_model_elements_by_model_id(model2._id)
        ]

        ctx = ObjectDict()
        ctx.model = (model1, model2)
        ctx.lattice = (lattice1, lattice2)

        n1 = len(model_elements1)
        n2 = len(model_elements2)
        ctx.model_elements = []
        for idx in range(max(n1, n2)):
            if idx < n1 and idx < n2:
                ctx.model_elements.append((model_elements1[idx], model_elements2[idx]))
            elif idx < n1:
                ctx.model_elements.append((model_elements1[idx], None))
            elif idx < n2:
                ctx.model_elements.append((None, model_elements2[idx]))

        self.render("latticemodel/model_compare.html", **ctx)


class ModelNamesHandler(BaseLatticeHandler, WriteJsonMixin):
    """Find the names of Models matching the specified query.
    """
    @coroutine
    def get(self):
        yield self.post()

    @coroutine
    def post(self):
        query = self.get_argument("query", "")
        data = self.application.data
        names = yield data.find_model_names(query)
        self.write_json(names)


class ModelUploadHandler(BaseLatticeHandler, ModelSupportMixin):
    """
    Upload Model files and save to database.

    This class uses the application "model_support" settings to delegate requests.
    """
    @authenticated
    @coroutine
    def get(self, type_id):
        model_support = self.construct_model_support(type_id)
        yield model_support.web_form_upload_get()


    @authenticated
    @coroutine
    def post(self, type_id):
        model_support = self.construct_model_support(type_id)
        yield model_support.web_form_upload_post()


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
        yield self.get_model_file(model_id, file_id)


class ModelFilesDownloadHandler(BaseLatticeHandler, FileDownloadMixin):
    """
    Download the model files in a single archive file (zip).
    """
    @coroutine
    def get(self, model_id):
        yield self.get_model_files(model_id)


class ModelElementsPropertyValuesHandler(BaseLatticeHandler, WriteJsonMixin):

    @coroutine
    def get(self, model_id, property_name):
        yield self._post()


    @coroutine
    def post(self):
        data = self.application.data
        model_id = self.get_argument("model_id", None)
        if not model_id:
            self.send_error(400)
            return
        name = self.get_argument("name", None)
        if not name:
            self.send_error(400)
            return
        values = yield data.find_model_elements_property_values(model_id, name)
        self.write_json(values)


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

