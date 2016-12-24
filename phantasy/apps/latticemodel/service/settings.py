# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path

from phantasy.apps.common.tornado.auth import InMemoryAuthProvider
from phantasy.apps.common.tornado.auth.crowd import CrowdAuthProvider
#from phantasy.apps.common.tornado.session import InMemorySessionProvider
from phantasy.apps.common.tornado.session.motor import MotorSessionProvider
from phantasy.apps.common.tornado.db.motor import MotorConnectionFactory
from .support.impact import ImpactLatticeSupport
from .support.impact import ImpactModelSupport
from .data import MotorDataProvider


production = {}

production["template_path"] = os.path.join(os.path.dirname(__file__), "templates")

production["static_path"] = os.path.join(os.path.dirname(__file__), "static")

production["login_url"] = "/user/login"
production["login_success_url"] = "/lattice/web/lattices/search"

production["logout_url"] = "/user/logout"
production["logout_success_url"] = "/lattice/web/lattices/search"

production["auth_provider_factory"] = CrowdAuthProvider
production["auth_provider_crowd_url"] = "http://example.com/crowd"
production["auth_provider_crowd_username"] = "username"
production["auth_provider_crowd_password"] = "password"

production["auth_basic_realm"] = "latticemodel"

production["db_connection_factory"] = MotorConnectionFactory
production["db_connection_database"] = "lattice"

production["data_provider_factory"] = MotorDataProvider

production["session_provider_factory"] = MotorSessionProvider
production["session_provider_cookie"] = "lms_session"
production["session_provider_secret"] = "012345678901234567890123456789012345678901234567890123456789"


production["lattice_support"] = [
    ("impactz", "IMPACT", ImpactLatticeSupport)
]

production["model_support"] = [
    ("impactz", "IMPACT", ImpactModelSupport)
]

development = dict(production)

development["attachment_path"] = os.path.join(os.path.dirname(__file__), "attachments")

development["auth_provider_factory"] = InMemoryAuthProvider
development["auth_provider_users"] = { "physuser":"E=mc^2" }

#development["session_provider_factory"] = InMemorySessionProvider

development["debug"] = True

