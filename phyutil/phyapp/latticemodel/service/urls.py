# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tornado.web import RedirectHandler

from ...common.tornado.web import OpenIdAuthSessionHandler

from .handlers import web
from .handlers import rest

APP_CONTEXT = "/lattice"

def _URL_PATTERN(pattern):
    return APP_CONTEXT + pattern.format(
        lattice_id=r"(?P<lattice_id>\w{24})",
        lattice_file_id=r"(?P<file_id>\d+)",
        lattice_element_id=r"(?P<element_id>\w{24})",
        lattice_element_order=r"(?P<order>\d+)"
    )


urlpatterns = []

webpatterns = [
    (r'/user/login/?',
        web.LatticeLoginHandler, { "template":"latticemodel/login.html" }),

    (r'/user/logout/?',
        web.LatticeLogoutHandler),

    (r'/user/auth/?',
        OpenIdAuthSessionHandler),

    (r'/lattice/?',
        RedirectHandler, {"url":"/lattice/web/lattice/search"}),

    (r'/lattice/web/?',
        RedirectHandler, {"url":"/lattice/web/lattice/search"}),

    (r'/lattice/web/lattice/?',
        RedirectHandler, {"url":"/lattice/web/lattice/search"}),

    (r'/lattice/web/lattice/search',
        web.LatticeSearchHandler, {}, "lattice_search"),

    (r'/lattice/web/lattice/upload',
        web.LatticeUploadHandler, {}, "lattice_upload"),

    (r'/lattice/web/lattice/([0-9a-f]{24})',
        web.LatticeDetailsHandler, {}, "lattice_details"),

    (r'/lattice/web/lattice/([0-9a-f]{24})/files',
        web.LatticeArchiveDownloadHandler, {}, "lattice_archive_download"),

    (r'/lattice/web/lattice/([0-9a-f]{24})/file/([0-9a-f]{24})',
        web.LatticeFileDownloadHandler, {}, "lattice_file_download"),

    (r'/lattice/web/model/search',
        web.ModelSearchHandler, {}, "model_search"),

    (r'/lattice/web/model/upload',
        web.ModelUploadHandler, {}, "model_upload"),

    (r'/lattice/web/model/([0-9a-f]{24})',
        web.ModelDetailsHandler, {}, "model_details"),

    (r'/lattice/web/model/([0-9a-f]{24})/files',
        web.ModelArchiveDownloadHandler, {}, "model_archive_download"),

    (r'/lattice/web/model/([0-9a-f]{24})/file/([0-9a-f]{24})',
        web.ModelFileDownloadHandler, {}, "model_file_download"),

    (r'/lattice/web/model/([0-9a-f]{24})/element/property/(.*)', 
        web.ModelElementPropertyValuesHandler, {}, "model_element_property_values")
]
urlpatterns.extend(webpatterns)


restpatterns = [
    (_URL_PATTERN(r"/rest/v1/lattices/?"),
        rest.LatticesRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}"),
        rest.LatticeRestHandler, {}, "rest_lattice_by_id"),

    #(_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/files"),
    #    rest.LatticeFilesRestHandler),

    #(_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/files/{lattice_file_id}"),
    #    rest.LatticeFileRestHandler, {}, "rest_lattice_file_by_id"),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/files/{lattice_file_id}/download"),
        rest.LatticeFileDownloadRestHander, {}, "rest_lattice_file_download_by_id"),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/elements"),
        rest.LatticeElementsByOrderRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/{lattice_id}/elements/{lattice_element_order}"),
        rest.LatticeElementByOrderRestHandler),

    (_URL_PATTERN(r"/rest/v1/lattices/elements/{lattice_element_id}"),
        rest.LatticeElementRestHandler, {}, "rest_lattice_element_by_id"),

    # POST /lattice/rest/v1/lattices
    # /lattice/rest/v1/lattice/{lattice_id}
    # /lattice/rest/v1/lattice/{lattice_id}/files
    # /lattice/rest/v1/lattice/{lattice_id}/elements
    # /lattice/rest/v1/lattice/{lattice_id}/elements/{order}
    # /lattice/rest/v1/lattice/{lattice_id}/models
    # /lattice/rest/v1/lattice/files/{file_id}
    # /lattice/rest/v1/lattice/elements/{element_id}
    # /lattice/rest/v1/model/{lattice_id}/files
    # /lattice/rest/v1/model/{lattice_id}/elements
    # /lattice/rest/v1/model/files
    # /lattice/rest/v1/model/elements/
]
urlpatterns.extend(restpatterns)
