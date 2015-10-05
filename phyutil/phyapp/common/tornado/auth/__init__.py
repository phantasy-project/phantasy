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

from tornado.util import ObjectDict
from tornado.gen import coroutine
from tornado.concurrent import Future
from tornado.ioloop import IOLoop


class AuthUser():
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

