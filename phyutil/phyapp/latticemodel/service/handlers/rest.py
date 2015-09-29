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
        if lattice_file_id >= len(lattice.files):
            raise HTTPError(404)

        lattice_file = lattice.files[lattice_file_id]

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
                }
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
                }
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


