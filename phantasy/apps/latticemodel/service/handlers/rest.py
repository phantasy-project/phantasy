# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#
"""
Request handlers for REST API.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import functools

from collections import OrderedDict
from tornado.web import HTTPError
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import maybe_future

from ....common.tornado.auth import AuthBasicMixin
from ....common.tornado.util import WriteJsonMixin


from . import LatticeSupportMixin
from . import ModelSupportMixin
from . import FileDownloadMixin


LOGGER = logging.getLogger(__name__)



def authorized(method):
    """Decorate handler methods with this to require users to be authorized.
    Response status code 401 (Unauthorized) is sent for unauthorized users.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.send_error(401)
            return
        return method(self, *args, **kwargs)
    return wrapper


class BaseRestRequestHandler(RequestHandler, AuthBasicMixin):

    @coroutine
    def prepare(self):
        yield maybe_future(super(BaseRestRequestHandler, self).prepare())
        yield self.prepare_auth_basic_user()


    def get_current_user(self):
        return self.get_auth_basic_user()


    def write_error(self, status_code, **kwargs):
        if status_code == 401:
            self.set_unauthorized_header(**kwargs)
        super(BaseRestRequestHandler,self).write_error(status_code, **kwargs)


    def _particle_type_api(self, particle_type):
        api = OrderedDict()
        api["type"] = particle_type["type"]
        api["links"] = {
            "self":self.reverse_url("rest_particle_type_by_id", api["type"])
        }
        api["name"] = particle_type["name"]
        api["protons"] = particle_type["protons"]
        api["neutrons"] = particle_type["neutrons"]
        return api


    def _lattice_type_api(self, lattice_type):
        api = OrderedDict()
        api["type"] = lattice_type["type"]
        api["links"] = {
            "self":self.reverse_url("rest_lattice_type_by_id", api["type"])
        }
        api["name"] = lattice_type["name"]
        return api


    def _model_type_api(self, model_type):
        api = OrderedDict()
        api["type"] = model_type["type"]
        api["links"] = {
            "self":self.reverse_url("rest_model_type_by_id", api["type"])
        }
        api["name"] = model_type["name"]
        return api


    def _lattice_api(self, lattice):
        api = OrderedDict()
        api["id"] = str(lattice["_id"]) # ObjectId to String
        api["links"] = { "self":self.reverse_url("rest_lattice_by_id", api["id"]) }
        api["name"] = lattice["name"]
        api["description"] = lattice["description"]
        api["status_type"] = lattice["status_type"]
        api["lattice_type"] = lattice["lattice_type"]
        api["particle_type"] = lattice["particle_type"]
        api["created_by"] = lattice["created_by"]
        api["created_date"] = lattice["created_date"].isoformat()
        api["properties"] = [self._lattice_prop_api(p) for p in lattice["properties"]]
        files = []
        for idx, lattice_file in enumerate(lattice["files"]):
            files.append(self._lattice_file_api(lattice_file, api["id"], idx+1))
        api["files"] = files
        return api


    def _lattice_file_api(self, lattice_file, lattice_id, file_id):
        api = OrderedDict()
        api["links"] = {
            #"self":self.reverse_url("rest_lattice_file_by_id", "", ""),
            "enclosure":self.reverse_url("rest_lattice_file_download_by_id", lattice_id, file_id)
        }
        api["name"] = lattice_file["name"]
        api["filename"] = lattice_file["filename"]
        return api


    def _lattice_prop_api(self, lattice_prop):
        api = OrderedDict()
        api["name"] = lattice_prop["name"]
        api["value"] = lattice_prop["value"]
        if "units" in lattice_prop:
            api["unit"] = lattice_prop["units"]
        return api


    def _lattice_elem_api(self, lattice_elem):
        api = OrderedDict()
        api["id"] = str(lattice_elem["_id"])
        api["links"] = {
            "self":self.reverse_url("rest_lattice_element_by_id", api["id"])
        }
        api["type"] = lattice_elem["type"]
        api["lattice_id"] = str(lattice_elem["lattice_id"])
        api["order"] = lattice_elem["order"]
        api["name"] = lattice_elem["name"]
        api["length"] = lattice_elem["length"]
        api["position"] = lattice_elem["position"]
        properties = []
        for p in lattice_elem["properties"]:
            properties.append(self._lattice_elem_prop_api(p))
        api["properties"] = properties
        return api


    def _lattice_elem_prop_api(self, lattice_elem_prop):
        api = OrderedDict()
        api["name"] = lattice_elem_prop["name"]
        api["value"] = lattice_elem_prop["value"]
        if "units" in lattice_elem_prop:
            api["unit"] = lattice_elem_prop["units"]
        return api


    def _model_api(self, model):
        api = OrderedDict()
        api["id"] = str(model["_id"])
        api["links"] = {
            "self":self.reverse_url("rest_model_by_id", api["id"])
        }
        api["lattice_id"] = str(model["lattice_id"])
        api["name"] = model["name"]
        api["description"] = model["description"]
        api["created_by"] = model["created_by"]
        api["created_date"] = model["created_date"].isoformat()
        properties = []
        for p in model["properties"]:
            properties.append(self._model_prop_api(p))
        api["properties"] = properties
        files = []
        for idx, model_file in enumerate(model["files"]):
            files.append(self._model_file_api(model_file, api["id"], str(idx+1)))
        api["files"] = files
        return api


    def _model_file_api(self, model_file, model_id, file_id):
        api = OrderedDict()
        api["links"] = {
            "enclosure":self.reverse_url("rest_model_file_download_by_id", model_id, file_id)
        }
        api["name"] = model_file["name"]
        api["filename"] = model_file["filename"]
        return api


    def _model_prop_api(self, model_prop):
        api = OrderedDict()
        api["name"] = model_prop["name"]
        api["value"] = model_prop["value"]
        if "units" in model_prop:
            api["unit"] = model_prop["units"]
        return api


    def _model_elem_api(self, model_elem):
        api = OrderedDict()
        api["id"] = str(model_elem["_id"])
        api["links"] = {
            "self":self.reverse_url("rest_model_element_by_id", api["id"])
        }
        api["model_id"] = str(model_elem["model_id"])
        api["lattice_element_id"] = str(model_elem["lattice_element_id"])
        properties = []
        for p in model_elem["properties"]:
            properties.append(self._model_elem_prop_api(p))
        api["properties"] = properties
        return api


    def _model_elem_prop_api(self, model_elem_prop):
        api = OrderedDict()
        api["name"] = model_elem_prop["name"]
        api["value"] = model_elem_prop["value"]
        if "units" in model_elem_prop:
            api["unit"] = model_elem_prop["units"]
        return api


class ParticleTypesRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self):
        """Retrieve list of Particle Types.

        **Example response**:

        .. sourcecode:: json

            HTTP/1.1 200 OK
            Content-Type: text/json

            [
              {
                "type": "ar36",
                "links": {
                  "self": "/lattice/rest/v1/particle/types/ar36"
                },
                "name": "Ar-36",
                "protons": 18.0,
                "neutrons": 18.0
              },
              ...
            ]

        :status 200: Particle Types found
        """
        data = self.application.data
        particle_types = yield data.find_particle_types()
        self.write_json([self._particle_type_api(pt) for pt in particle_types])


class ParticleTypeRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, type_id):
        """Retrieve Particle Type by ID

        **Example response**:

        .. sourcecode:: json

            HTTP/1.1 200 OK
            Content-Type: text/json

            [
              {
                "type": "ar36",
                "links": {
                  "self": "/lattice/rest/v1/particle/types/ar36"
                },
                "name": "Ar-36",
                "protons": 18.0,
                "neutrons": 18.0
              },
              ...
            ]

        :param type_id: Particle Type ID
        :status 200: Particle Type found
        :status 404: Particle Type not found
        """
        data = self.application.data
        particle_type = yield data.find_particle_type_by_id(type_id)
        if not particle_type:
            raise HTTPError(404)
        self.write_json(self._particle_type_api(particle_type))


class LatticeTypesRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self):
        """Retrieve list of Lattice Types.

        **Example response**:

        .. sourcecode:: json

            HTTP/1.1 200 OK
            Content-Type: text/json

            [
              {
                "type": "impactz",
                "links": {
                  "self": "/lattice/rest/v1/lattices/types/impactz"
                },
                "name": "IMPACT"
              },
              ...
            ]

        :status 200: Lattice Types found
        """
        data = self.application.data
        lattice_types = yield data.find_lattice_types()
        self.write_json([self._lattice_type_api(lt) for lt in lattice_types])


class LatticeTypeRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, type_id):
        """Retrieve Lattice Type by ID.

        **Example response**:

        .. sourcecode:: json

            HTTP/1.1 200 OK
            Content-Type: text/json

            {
              "type": "impactz",
              "links": {
                "self": "/lattice/rest/v1/lattices/types/impactz"
              },
              "name": "IMPACT"
            }

        :param type_id: Lattice Type ID
        :status 200: Lattice Type found
        :status 404: Lattice Type not found
        """
        data = self.application.data
        lattice_type = yield data.find_lattice_type_by_id(type_id)
        self.write_json(self._lattice_type_api(lattice_type))


class LatticesRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self):
        """Retrieve list of Lattice objects.

        **Example response**:

        .. sourcecode:: json

            HTTP/1.1 200 OK
            Content-Type: text/json

            [
              {
                "id": "55e7542bfad7b66cf2598b4a",
                "links": {
                  "self": "/lattice/rest/v1/lattices/55e7542bfad7b66cf2598b4a"
                },
                "name": "Test",
                "description": "This is a description",
                "status_type": "development",
                "lattice_type": "impactz",
                "particle_type": "kr86",
                "created_by": "physuser",
                "created_date": "2015-09-02T15:55:23.852000",
                "properties": [
                  {
                    "name": "RefParticleMass",
                    "value": 931494320.0
                  },
                  ...
                ]
                "files": [
                  {
                    "links": {
                      "enclosure": "/lattice/rest/v1/lattices/55e7542bfad7b66cf2598b4a/files/1/download"
                    },
                   "name": "LatticeFile",
                   "filename": "test.in"
                  },
                  ...
                ]
              }
              ...
            ]

        :status 200: Lattices found
        """
        data = self.application.data
        lattices = yield data.find_lattices()
        self.write_json([self._lattice_api(l) for l in lattices])


class LatticeRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, lattice_id):
        """Retrieve Lattice object by identifier.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
              "id": "55e7542bfad7b66cf2598b4a",
              "links": {
                "self": "/lattice/rest/v1/lattices/55e7542bfad7b66cf2598b4a"
              },
              "name": "Test",
              "description": "This is a description",
              "status_type": "development",
              "lattice_type": "impactz",
              "particle_type": "kr86",
              "created_by": "physuser",
              "created_date": "2015-09-02T15:55:23.852000",
              "properties": [
                {
                  "name": "RefParticleMass",
                  "value": 931494320.0
                },
                ...
              ]
              "files": [
                {
                  "links": {
                   "enclosure": "/lattice/rest/v1/lattices/55e7542bfad7b66cf2598b4a/files/1/download"
                  },
                  "name": "LatticeFile",
                  "filename": "test.in"
                },
                ...
              ]
            }

        :param lattice_id: Lattice ID
        :status 200: Lattice found
        :status 404: Lattice not found
        """
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)
        if not lattice:
            raise HTTPError(404)
        self.write_json(self._lattice_api(lattice))


class LatticeUploadRestHandler(BaseRestRequestHandler, WriteJsonMixin, LatticeSupportMixin):
    @authorized
    @coroutine
    def post(self, type_id):
        """Create a new Lattice by submitting form data.

        Content type MUST be 'multipart/form-data'

        Content of the form is dictated by the Lattice type being submitted.

        For Lattice type 'impactz' the follow parameters are supported:
        *name*: new lattice name
        *branch*: new lattice branch
        *version*: new lattice version (ignored if autoversion is specified)
        *autoversion*: (optional) automatically select version of new lattice
        *particle_type*: particle type associated with new lattice
        *description*: new lattice description
        *lattice_file*: raw IMPACT lattice file (ie test.in)
        *data_file*: data files referenced by the lattice (multiple allowed)

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
              "links":{
                  "replies":"/lattice/rest/v1/lattices/5618320efad7b6600d1f2ecc"
              }
            }

        :param type_id: Lattice Type ID
        :status 201: Lattice created
        :status 401: Unauthorized
        :status 404: Lattice Type not supported
        """
        lattice_support = self.construct_lattice_support(type_id)
        yield lattice_support.rest_form_upload_post()


class LatticeFilesDownloadRestHander(BaseRestRequestHandler, FileDownloadMixin):
    @coroutine
    def get(self, lattice_id):
        """
        Retrieve the an archive file containing all files of the Lattice specifed.

        :param lattice_id: Lattice ID
        :status 200: Lattice file found
        :status 404: Lattice file not found
        """
        yield self.get_lattice_files(lattice_id)


class LatticeFileDownloadRestHander(BaseRestRequestHandler, FileDownloadMixin):
    @coroutine
    def get(self, lattice_id, file_id):
        """
        Retrieve the file content of the Lattice File specifed.

        :param lattice_id: Lattice ID
        :param file_id: Lattice file ID
        :status 200: Lattice file found
        :status 404: Lattice file not found
        """
        yield self.get_lattice_file(lattice_id, file_id)


class LatticeElementsByOrderRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, lattice_id):
        """Retrieve Lattice Elements by Lattice ID.

        **Example response**:

        .. sourcecode:: json

            HTTP/1.1 200 OK
            Content-Type: text/json
            [
              {
                "id": "55e7542bfad7b66cf2598b4e",
                "links": {
                  "self": "/lattice/rest/v1/lattices/elements/55e7542bfad7b66cf2598b4e"
                },
                "type": "VALVE",
                "lattice_id": "55e7542bfad7b66cf2598b4a",
                "name": "DRIFT",
                "length": 0.072,
                "position": 0.07200000000000273,
                "properties": []
              },
              {
                "id": "55e7542bfad7b66cf2598b50",
                "links": {
                  "self": "/lattice/rest/v1/lattices/elements/55e7542bfad7b66cf2598b50"
                },
                "type": "CAV",
                "lattice_id": "55e7542bfad7b66cf2598b4a",
                "name": "LS1_CA01:CAV1_D1127",
                "length": 0.24,
                "position": 0.44706350000001294,
                "properties": [
                  {
                    "name": "AMP",
                    "value": 0.64
                  },
                  {
                    "name": "PHA",
                    "value": -6.524
                  }
                ]
              },
              ...
            ]

        :param lattice_id: Lattice ID
        :status 200: Lattice Elements found
        """
        data = self.application.data
        elements = yield data.find_lattice_elements_by_lattice_id(lattice_id)
        self.write_json([self._lattice_elem_api(e) for e in elements])



class LatticeElementByOrderRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, lattice_id, order):
        """Retrieve Lattice Element by Lattice ID and element order.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
              "id": "55e7542bfad7b66cf2598b50",
              "links": {
                "self": "/lattice/rest/v1/lattices/elements/55e7542bfad7b66cf2598b50"
              },
              "type": "CAV",
              "lattice_id": "55e7542bfad7b66cf2598b4a",
              "order": 3,
              "name": "LS1_CA01:CAV1_D1127",
              "length": 0.24,
              "position": 0.44706350000001294,
              "properties": [
                {
                  "name": "AMP",
                  "value": 0.64
                },
                {
                  "name": "PHA",
                  "value": -6.524
                },
                ...
              ]
            }

        :param lattice_id: Lattice ID
        :param order: Lattice Element order
        :status 200: Lattice Element found
        :status 404: Lattice Element not found
        """
        data = self.application.data
        element = yield data.find_lattice_element_by_order(lattice_id, int(order))
        if not element:
            raise HTTPError(404)
        self.write_json(self._lattice_elem_api(element))


class LatticeElementRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, element_id):
        """Retrieve Lattice Element by ID.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
              "id": "55e7542bfad7b66cf2598b50",
              "links": {
                "self": "/lattice/rest/v1/lattices/elements/55e7542bfad7b66cf2598b50"
              },
              "type": "CAV",
              "lattice_id": "55e7542bfad7b66cf2598b4a",
              "order": 3,
              "name": "LS1_CA01:CAV1_D1127",
              "length": 0.24,
              "position": 0.44706350000001294,
              "properties": [
                {
                  "name": "AMP",
                  "value": 0.64
                },
                {
                  "name": "PHA",
                  "value": -6.524
                },
                ...
              ]
            }

        :param element_id: Lattice Element ID
        :status 200: Lattice Element found
        :status 404: Lattice Element not found
        """
        data = self.application.data
        element = yield data.find_lattice_element_by_id(element_id)
        if not element:
            raise HTTPError(404)
        self.write_json(self._lattice_elem_api(element))


class ModelsByLatticeIdRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, lattice_id):
        """Retrive list of Models for given Lattice ID.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            [
              {
                "id": "55ef4db0fad7b6267302fb4d",
                "links": {
                  "self": "/lattice/rest/v1/models/55ef4db0fad7b6267302fb4d"
                },
                "lattice_id": "55eefbf0fad7b60a68e74754",
                "name": "Test Model",
                "description": "",
                "created_by": "physuser",
                "created_date": "2015-09-08T17:05:52.052000",
                "properties": [
                  ...
                ],
                "files": [
                  ...
                ]
              },
              {
                "id": "55ef4ed3fad7b62d1990bd3d",
                "links": {
                  "self": "/lattice/rest/v1/models/55ef4ed3fad7b62d1990bd3d"
                },
                "lattice_id": "55eefbf0fad7b60a68e74754",
                "name": "Test Model",
                "description": "",
                "created_by": "physuser",
                "created_date": "2015-09-08T17:10:43.317000",
                "properties": [
                  ...
                ],
                "files": [
                  ...
                ]
              },
              ...
            ]

        :param lattice_id: Lattice ID
        :status 200: Models found
        :status 404: Lattice not found
        """
        data = self.application.data
        models = yield data.find_models_by_lattice_id(lattice_id)
        if not models:
            raise HTTPError(404)
        self.write_json([self._model_api(m) for m in models])


class ModelsRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self):
        """Retrieve list of Model objects.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            [
              {
                "id": "55ef4db0fad7b6267302fb4d",
                "links": {
                  "self": "/lattice/rest/v1/models/55ef4db0fad7b6267302fb4d"
                },
                "lattice_id": "55eefbf0fad7b60a68e74754",
                "name": "Test Model",
                "description": "",
                "created_by": "physuser",
                "created_date": "2015-09-08T17:05:52.052000",
                "properties": [
                  ...
                ],
                "files": [
                  ...
                ]
              },
              {
                "id": "55ef4ed3fad7b62d1990bd3d",
                "links": {
                  "self": "/lattice/rest/v1/models/55ef4ed3fad7b62d1990bd3d"
                },
                "lattice_id": "55eefbf0fad7b60a68e74754",
                "name": "Test Model",
                "description": "",
                "created_by": "physuser",
                "created_date": "2015-09-08T17:10:43.317000",
                "properties": [
                  ...
                ],
                "files": [
                  ...
                ]
              },
              ...
            ]

        :status 200: Models found
        """
        data = self.application.data
        models = yield data.find_models()
        self.write_json([self._model_api(m) for m in models])


class ModelRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, model_id):
        """Retrieve Model object by ID.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
              "id": "55ef4db0fad7b6267302fb4d",
              "links": {
                "self": "/lattice/rest/v1/models/55ef4db0fad7b6267302fb4d"
              },
              "lattice_id": "55eefbf0fad7b60a68e74754",
              "name": "Test Model",
              "description": "",
              "created_by": "physuser",
              "created_date": "2015-09-08T17:05:52.052000",
              "properties": [
                {
                  "name":"Property1",
                  "value":1.0,
                  "unit":"mm"
                }
                ...
              ],
              "files": [
                {
                  "links": {
                    "enclosure": "/lattice/rest/v1/models/55ef4db0fad7b6267302fb4d/files/1/download"
                  },
                  "name": "ModelData",
                  "filename": "model.map"
                },
                ...
              ]
            }

        :param model_id: Model ID
        :status 200: Model found
        :status 404: Model not found
        """
        data = self.application.data
        model = yield data.find_model_by_id(model_id)
        if not model:
            raise HTTPError(404)
        self.write_json(self._model_api(model))


class ModelUploadRestHandler(BaseRestRequestHandler, WriteJsonMixin, ModelSupportMixin):
    @authorized
    @coroutine
    def post(self, type_id):
        """Create a new Model by submitting form data.

        Content type MUST be 'multipart/form-data'

        Content of the form is dictated by the Model type being submitted.

        For Model type 'impactz' the follow parameters are supported:
        *name*: new lattice name
        *lattice_id*: lattice ID
        *description*: new model description
        *model_fort18*: IMPACT output file fort.18
        *model_fort24*: IMPACT output file fort.19
        *model_fort25*: IMPACT output file fort.24
        *model_fort26*: IMPACT output file fort.26
        *model_map*: IMPACT output map file model.map

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
              "links":{
                  "replies":"/lattice/rest/v1/models/561d449dfad7b65083879d0d"
              }
            }

        :param type_id: Model Type ID
        :status 201: Model created
        :status 401: Unauthorized
        :status 404: Model Type not supported
        """
        model_support = self.construct_model_support(type_id)
        yield model_support.rest_form_upload_post()


class ModelFileDownloadRestHander(BaseRestRequestHandler, FileDownloadMixin):
    @coroutine
    def get(self, model_id, file_id):
        """
        Retrieve the file content of the Model File specifed.

        :param model_id: Lattice ID
        :param file_id: Lattice file ID
        :status 200: Lattice file found
        :status 404: Lattice file not found
        """
        yield self.get_model_file(model_id, file_id)


class ModelFilesDownloadRestHander(BaseRestRequestHandler, FileDownloadMixin):
    @coroutine
    def get(self, model_id):
        """
        Retrieve the an archive file containing all files of the Model specifed.

        :param model_id: Model ID
        :status 200: Model file found
        :status 404: Model file not found
        """
        yield self.get_model_files(model_id)


class ModelElementsByModelIdRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, model_id):
        """Retrieve Model Elements by Model ID.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            [
              {
                "id": "55f342ccfad7b61a9f72b0b5",
                "links": {
                  "self": "/lattice/rest/v1/models/elements/55f342ccfad7b61a9f72b0b5"
                },
                "model_id": "55f342cbfad7b61a9f72afa9",
                "lattice_element_id": "55eefbf0fad7b60a68e7475d",
                "properties": [
                  ...
                ]
              },
              {
                "id": "55f342ccfad7b61a9f72b0b6",
                "links": {
                  "self": "/lattice/rest/v1/models/elements/55f342ccfad7b61a9f72b0b6"
                },
                "model_id": "55f342cbfad7b61a9f72afa9",
                "lattice_element_id": "55eefbf0fad7b60a68e7475e",
                "properties": [
                  ...
                ]
              },
              {
                "id": "55f342ccfad7b61a9f72b0aa",
                "links": {
                  "self": "/lattice/rest/v1/models/elements/55f342ccfad7b61a9f72b0aa"
                },
                "model_id": "55f342cbfad7b61a9f72afa9",
                "lattice_element_id": "55eefbf0fad7b60a68e7475f",
                "properties": [
                  ...
                ]
              },
              ...
            ]

        :param model_id: Model ID
        :status 200: Models found.
        """
        data = self.application.data
        elements = yield data.find_model_elements_by_model_id(model_id)
        self.write_json([self._model_elem_api(e) for e in elements])


class ModelElementRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, element_id):
        """Retrieve Model Element by ID.

         **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
              "id": "55f342ccfad7b61a9f72b0b5",
              "links": {
                "self": "/lattice/rest/v1/model/elements/55f342ccfad7b61a9f72b0b5"
              },
              "model_id": "55f342cbfad7b61a9f72afa9",
              "lattice_element_id": "55eefbf0fad7b60a68e7475d",
              "properties": [
                {
                  "name": "BeamCenterX",
                  "value": 2.6565e-05,
                  "unit":"mm"
                },
                {
                  "name": "BeamCenterY",
                  "value": 4.62876e-05,
                  "unit":"mm"
                },
                ...
              ]
            }

        :param element_id: Model Element ID
        :status 200: Model Element found
        :status 404: Model Element not found
        """
        data = self.application.data
        element = yield data.find_model_element_by_id(element_id)
        if not element:
            raise HTTPError(404)
        self.write_json(self._model_elem_api(element))


class ModelTypesRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self):
        """Retrieve list of Model Types.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            [
              {
                "type": "impactz",
                "links": {
                  "self": "/lattice/rest/v1/models/types/impactz"
                },
                "name": "IMPACT"
              },
              ...
            ]

        :status 200: Model Types found
        """
        data = self.application.data
        model_types = yield data.find_model_types()
        self.write_json([self._model_type_api(mt) for mt in model_types])


class ModelTypeRestHandler(BaseRestRequestHandler, WriteJsonMixin):
    @coroutine
    def get(self, type_id):
        """Retrieve Model Type by ID.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
              "type": "impactz",
              "links": {
                "self": "/lattice/rest/v1/models/types/impactz"
              },
              "name": "IMPACT"
            }

        :param type_id: Model Type ID
        :status 200: Model Type found
        :status 404: Model Type not found
        """
        data = self.application.data
        model_type = yield data.find_model_type_by_id(type_id)
        if not model_type:
            raise HTTPError(404)
        self.write_json(self._model_type_api(model_type))


