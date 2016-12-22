# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#

"""
Defines a standard interface to provide application authentication support.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import logging

from tornado.util import ObjectDict
from tornado.gen import coroutine
from tornado.concurrent import Future
from tornado.ioloop import IOLoop
from tornado.web import HTTPError


_LOGGER = logging.getLogger(__name__)


class AuthBasicMixin(object):
    """
    Mixin providing support for HTTP Basic authentication.
    """
    def get_auth_basic_user(self):
        """Get the user authorized by HTTP basic authentication.
        """
        if not hasattr(self, "_auth_basic_user"):
            _LOGGER.warning("Missing _auth_basic_user: prepare_auth_basic_user() not called")
            return None
        return self._auth_basic_user


    @coroutine
    def prepare_auth_basic_user(self):
        """
        Authenticate user with credentials retrieved from the HTTP Basic
        authentication header using the configured authentication provider.
        """
        self._auth_basic_user = None
        headers = self.request.headers
        if "Authorization" not in headers:
            return
        authorization = headers["Authorization"]
        if not authorization.startswith("Basic "):
            return
        token = base64.decodestring(authorization[6:])
        credentials = token.split(":", 2)
        if len(credentials) < 2:
            return
        auth = self.application.auth
        user = yield auth.authenticate(*credentials)
        if user is None:
            return
        self._auth_basic_user = credentials[0]


    def set_unauthorized_header(self, realm=None):
        """
        Set the 'WWW-Authenticate' header with type 'Basic' using
        the specified realm, or the realm from the 'auth_basic_realm'
        application settings.

        :param realm: optional basic authentication realm
        """
        if not realm:
            realm = self.settings.get("auth_basic_realm", "")
        self.set_header("WWW-Authenticate", "Basic realm=\"{}\"".format(realm))


class AuthUser(object):
    """
    Specifies a standard object representing the authenticated user.
    This object is required to contain a 'username' attribute that
    must contain a unique string identifier of the user represented
    by this object.
    """
    def __str__(self):
        return self.username

    def __hash__(self):
        return hash(self.username)


class AuthProvider(object):
    """
    Specifies the standard AuthProvider interface that provides general
    support for application wide authentication logic using a variety
    of implementations.
    """
    def __init__(self, application):
        """
        The AuthProvider interface is initialized with the current application.
        """
        self.application = application


    def authenticate(self):
        """
        Override this method to provide implementation authentication for

        :returns: a Future that must a resolve to None or a valid AuthUser object
        """
        raise NotImplementedError()


class InMemoryAuthProvider(AuthProvider):
    """
    Implementation of AuthProvider interface using an in-memory user store.

    The following application settings are used to configure this provider:

    *auth_provider_users*: Dictionary with username keys and password values.
    """

    _CONFIG_USERS = "auth_provider_users"

    def __init__(self, application):
        super(InMemoryAuthProvider,self).__init__(application)
        settings = self.application.settings
        if self._CONFIG_USERS in self.application.settings:
            self._users = dict(settings.get("auth_provider_users"))
        else:
            raise RuntimeError("Settings '"+self._CONFIG_USERS+"' not found")


    @coroutine
    def authenticate(self, username, password):
        """
        Authenticate user with in-memory user store.

        :returns: a Future that must a resolve to None or a valid AuthUser object
        """
        if username not in self._users:
            return None

        if password != self._users[username]:
            return None

        user = AuthUser()
        user.username = username
        return user

