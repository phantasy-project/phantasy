# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

import os.path

from ...common.tornado.web import InMemoryAuthProvider
from ...common.tornado.web import MotorSessionProvider
from ...common.tornado.web import motor_connection_factory
from .support.impact import ImpactLatticeSupport
from .support.impact import ImpactModelSupport
from .data import MotorDataProvider

production = {}

production["template_path"] = os.path.join(os.path.dirname(__file__), "templates")

production["static_path"] = os.path.join(os.path.dirname(__file__), "static")

production["login_url"] = "/user/login"
production["login_template"] = "lattice/login.html"
production["login_success_url"] = "/lattice/web/lattice/search"

production["logout_url"] = "/user/logout"
production["logout_success_url"] = "/lattice/web/lattice/search"

production["cookie_secret"] = "123456789"

production["data_provider_factory"] = MotorDataProvider



production["lattice_support"] = [
                    ("impactz", "IMPACT", ImpactLatticeSupport)
                ]

production["model_support"] = [
                    ("impactz", "IMPACT", ImpactModelSupport)
                ]

development = dict(production)

development["attachment_path"] = os.path.join(os.path.dirname(__file__), "attachments")

# print base64.b64encode(os.urandom(50)).decode('ascii')
production["cookie_secret"] = "012345678901234567890123456789012345678901234567890123456789"

development["users"] = {
    "username":"password"
}

development["auth_provider_factory"] = InMemoryAuthProvider
development["auth_provider_users"] = { "physuser":"E=mc^2" }

#development["session_provider_factory"] = common.web.InMemorySessionProvider
development["session_provider_factory"] = MotorSessionProvider

development["db_connection_factory"] = motor_connection_factory
development["db_connection_database"] = "lattice"

#development["db_conn_class"] = common.web

#development["db_conn_url"] = 
#development["db_conn_username"] =
#development["db_conn_password"] =

development["debug"] = True

