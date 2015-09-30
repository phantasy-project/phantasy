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

import json
import logging
import os.path

from collections import OrderedDict
from tornado.web import HTTPError
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import maybe_future
from tornado.escape import url_escape

from ....common.tornado.util import WriteFileMixin


LOGGER = logging.getLogger(__name__)


class BaseRestRequestHandler(RequestHandler):


    @coroutine
    def prepare(self):
        yield maybe_future(super(BaseRestRequestHandler,self).prepare())
        # TODO: process basic authorization


    def write_error(self, status_code, **kwargs):
        self.write_json({ "error":status_code })


    def write_json(self, obj, content_type="application/json"):
        indent = None
        if self.settings.get("debug", False):
            indent = 2    # pretty
        else:
            indent = None # compact
        self.set_header("Content-Type", content_type)
        json.dump(obj, self, indent=indent)


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


class LatticesRestHandler(BaseRestRequestHandler):
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


class LatticeRestHandler(BaseRestRequestHandler):
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


class LatticeFileDownloadRestHander(BaseRestRequestHandler, WriteFileMixin):
    @coroutine
    def get(self, lattice_id, file_id):
        """
        Retrieve the file content of the Lattice File specifed.
        
        :param lattice_id: Lattice ID
        :param file_id: Lattice file ID
        :status 200: Lattice file found
        :status 404: Lattice file not found
        """
        data = self.application.data
        lattice = yield data.find_lattice_by_id(lattice_id)

        if not lattice or "files" not in lattice:
            raise HTTPError(404)

        lattice_file_id = int(file_id)
        if lattice_file_id < 1 or lattice_file_id > len(lattice.files):
            raise HTTPError(404)

        lattice_file = lattice.files[lattice_file_id-1]

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            LOGGER.error("Setting 'attachment_path' does not specify a directory")
            raise HTTPError(500)

        location = os.path.join(file_root, lattice_file.location)
        try:
            data_file = open(location, 'r')
        except:
            LOGGER.exception("Error opening lattice file at location: %s", location)
            raise HTTPError(500)

        with data_file:
            filename = self.clean_filename(lattice_file.filename)
            self.set_header("Content-Type", "application/octet-stream")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                self.write_file(data_file)
            except:
                LOGGER.exception("Error writing lattice file to response: %s", filename)
                raise HTTPError(500)


class LatticeElementsByOrderRestHandler(BaseRestRequestHandler):
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



class LatticeElementByOrderRestHandler(BaseRestRequestHandler):
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


class LatticeElementRestHandler(BaseRestRequestHandler):
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


class ModelsRestHandler(BaseRestRequestHandler):
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


class ModelRestHandler(BaseRestRequestHandler):
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


class ModelFileDownloadRestHander(BaseRestRequestHandler, WriteFileMixin):
    @coroutine
    def get(self, model_id, file_id):
        """
        Retrieve the file content of the Model File specifed.

        :param model_id: Lattice ID
        :param file_id: Lattice file ID
        :status 200: Lattice file found
        :status 404: Lattice file not found
        """
        data = self.application.data
        model = yield data.find_model_by_id(model_id)

        if not model or "files" not in model:
            raise HTTPError(404)

        model_file_id = int(file_id)
        if model_file_id < 1 or model_file_id > len(model.files):
            raise HTTPError(404)

        model_file = model.files[model_file_id-1]

        file_root = self.settings.get("attachment_path", "")
        if not os.path.isdir(file_root):
            LOGGER.error("Setting 'attachment_path' does not specify a directory")
            raise HTTPError(500)

        location = os.path.join(file_root, model_file.location)
        try:
            data_file = open(location, 'r')
        except:
            LOGGER.exception("Error opening lattice file at location: %s", location)
            raise HTTPError(500)

        with data_file:
            filename = self.clean_filename(model_file.filename)
            self.set_header("Content-Type", "application/octet-stream")
            self.set_header("Content-Disposition",
                            "attachment;filename=" + url_escape(filename))
            try:
                self.write_file(data_file)
            except:
                LOGGER.exception("Error writing lattice file to response: %s", filename)
                raise HTTPError(500)


class ModelElementsByModelIdRestHandler(BaseRestRequestHandler):
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


class ModelElementRestHandler(BaseRestRequestHandler):
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
