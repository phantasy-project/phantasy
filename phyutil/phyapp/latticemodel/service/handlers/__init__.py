# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Web application request handlers for Lattice Model Service.
"""


from tornado.web import HTTPError


class LatticeSupportMixin(object):
    def construct_lattice_support(self, lattice_type):
        """
        Construct a Lattice support class for the given lattice type.
        """
        self.require_setting("lattice_support")
        for support in self.settings["lattice_support"]:
            if lattice_type == support[0]:
                return support[2](support[0], support[1], self)
        raise HTTPError(404)

