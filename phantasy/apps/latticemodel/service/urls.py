# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tornado.web import RedirectHandler

from .handlers import web
from .handlers import rest

APP_CONTEXT = "/lattice"

def _URL_PATTERN(pattern):
    return APP_CONTEXT + pattern.format(
        particle_type_id="(?P<type_id>\w+)",
        lattice_id=r"(?P<lattice_id>\w{24})",
        lattice_file_id="(?P<file_id>\\w{6})",
        lattice_element_id=r"(?P<element_id>\w{24})",
        lattice_element_order=r"(?P<order>\d+)",
        lattice_type_id="(?P<type_id>\\w+)",
        model_id="(?P<model_id>\\w{24})",
        model_file_id="(?P<file_id>\\w{6})",
        model_element_id="(?P<element_id>\\w{24})",
        model_type_id="(?P<type_id>\\w+)"
    )


urlpatterns = []

webpatterns = [
    (r'/user/login/?',
        web.LatticeLoginHandler, { "template":"latticemodel/login.html" }),

    (r'/user/logout/?',
        web.LatticeLogoutHandler),

    (_URL_PATTERN(r'/?'),
        RedirectHandler, {"url":_URL_PATTERN("/web/lattices/search")}),

    (_URL_PATTERN(r'/web/?'),
        RedirectHandler, {"url":_URL_PATTERN("/web/lattices/search")}),

    (_URL_PATTERN(r'/web/lattices/?'),
        RedirectHandler, {"url":_URL_PATTERN("/web/lattices/search")}),

    (_URL_PATTERN(r'/web/lattices/search'),
        web.LatticeSearchHandler, {}, "lattice_search"),

    (_URL_PATTERN(r'/web/lattices/compare'),
        web.LatticeCompareHandler, {}, "web_lattice_compare"),

    (_URL_PATTERN(r'/web/lattices/names'),
        web.LatticeNamesHandler, {}, "web_lattice_names"),

    (_URL_PATTERN(r'/web/lattices/branches'),
        web.LatticeBranchesHandler, {}, "web_lattice_branches"),

    (_URL_PATTERN(r'/web/lattices/upload/{lattice_type_id}'),
        web.LatticeUploadHandler, {}, "lattice_upload"),

    (_URL_PATTERN(r'/web/lattices/{lattice_id}'),
        web.LatticeDetailsHandler, {}, "lattice_details"),

    (_URL_PATTERN(r'/web/lattices/{lattice_id}/files/download'),
        web.LatticeFilesDownloadHandler, {}, "lattice_files_download"),

    (_URL_PATTERN(r"/web/lattices/{lattice_id}/files/{lattice_file_id}/download"),
        web.LatticeFileDownloadHandler, {}, "lattice_file_download"),

    (_URL_PATTERN(r'/web/models/search'),
        web.ModelSearchHandler, {}, "model_search"),

    (_URL_PATTERN(r'/web/models/compare'),
        web.ModelCompareHandler, {}, "web_model_compare"),

    (_URL_PATTERN(r'/web/models/names'),
        web.ModelNamesHandler, {}, "web_model_names"),

    (_URL_PATTERN(r'/web/models/upload/{model_type_id}'),
        web.ModelUploadHandler, {}, "model_upload"),

    (_URL_PATTERN(r'/web/models/{model_id}'),
        web.ModelDetailsHandler, {}, "model_details"),

    (_URL_PATTERN(r'/web/models/{model_id}/files/download'),
        web.ModelFilesDownloadHandler, {}, "model_files_download"),

    (_URL_PATTERN(r'/web/models/{model_id}/files/{model_file_id}/download'),
        web.ModelFileDownloadHandler, {}, "model_file_download"),

    (_URL_PATTERN(r'/web/models/elements/property/values'),
        web.ModelElementsPropertyValuesHandler, {}, "web_model_elements_property_values")
]
urlpatterns.extend(webpatterns)


restpatterns = [
    (_URL_PATTERN(r"/rest/v1/particles/types"),
        rest.ParticleTypesRestHandler),

    (_URL_PATTERN(r"/rest/v1/particles/types/{particle_type_id}"),
        rest.ParticleTypeRestHandler, {}, "rest_particle_type_by_id"),

    (_URL_PATTERN(r"/rest/v1/lattices"),
        rest.LatticesRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}"),
        rest.LatticeRestHandler, {}, "rest_lattice_by_id"),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_type_id}"),
        rest.LatticeUploadRestHandler, {}, "rest_lattice_upload"),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/files/download"),
        rest.LatticeFilesDownloadRestHander, {}, "rest_lattice_files_download"),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/files/{lattice_file_id}/download"),
        rest.LatticeFileDownloadRestHander, {}, "rest_lattice_file_download_by_id"),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/elements"),
        rest.LatticeElementsByOrderRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/elements/{lattice_element_order}"),
        rest.LatticeElementByOrderRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/models"),
        rest.ModelsByLatticeIdRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/elements/{lattice_element_id}"),
        rest.LatticeElementRestHandler, {}, "rest_lattice_element_by_id"),

    (_URL_PATTERN(r"/rest/v1/lattices/types"),
        rest.LatticeTypesRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/types/{lattice_type_id}"),
        rest.LatticeTypeRestHandler, {}, "rest_lattice_type_by_id"),

    (_URL_PATTERN(r"/rest/v1/models"),
        rest.ModelsRestHandler),

    (_URL_PATTERN(r"/rest/v1/models/{model_id}"),
        rest.ModelRestHandler, {}, "rest_model_by_id"),

    (_URL_PATTERN(r"/rest/v1/models/{model_type_id}"),
        rest.ModelUploadRestHandler, {}, "rest_model_upload"),

    (_URL_PATTERN(r"/rest/v1/models/{model_id}/files/download"),
        rest.ModelFilesDownloadRestHander, {}, "rest_model_files_download"),

    (_URL_PATTERN(r"/rest/v1/models/{model_id}/files/{model_file_id}/download"),
        rest.ModelFileDownloadRestHander, {}, "rest_model_file_download_by_id"),

    (_URL_PATTERN(r"/rest/v1/models/{model_id}/elements"),
        rest.ModelElementsByModelIdRestHandler),

    (_URL_PATTERN(r"/rest/v1/models/elements/{model_element_id}"),
        rest.ModelElementRestHandler, {}, "rest_model_element_by_id"),

    (_URL_PATTERN(r"/rest/v1/models/types"),
        rest.ModelTypesRestHandler),

    (_URL_PATTERN(r"/rest/v1/models/types/{model_type_id}"),
        rest.ModelTypeRestHandler, {}, "rest_model_type_by_id")
]
urlpatterns.extend(restpatterns)
