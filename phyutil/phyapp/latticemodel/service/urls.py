# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tornado.web import RedirectHandler
from .handlers import web


urlpatterns = [
    (r'/user/login/?', web.LatticeLoginHandler),

    (r'/user/logout/?', web.LatticeLogoutHandler),

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

    #(r'/lattice/web/model/upload', handlers.LatticeUploadHandler, {}, "model_upload"),
    #(r'/lattice/rest/v1/lattice/files', handlers.LatticeFilesHandler)
    #(r'/lattice/rest/v1/lattice/([0-9a-f]{24})/attachments')
]

