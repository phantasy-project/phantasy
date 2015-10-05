# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#


"""
Common components for building web application based on the Tornado framework.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import logging
import collections
import tornado.web

from datetime import datetime
from tornado.web import Finish
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import maybe_future
from tornado.auth import OpenIdMixin

from .session import SessionMixin


_LOGGER = logging.getLogger(__name__)



class Application(tornado.web.Application):
    """
    A common base application that adds support for configuration of the
    database connection, session provider and authentication provider.

    The following settings are supported by this application:

    *db_connection_factory*: Callable that returns a database connection
    *auth_provider_factory*: Callable that returns the an authentication provider
    *session_provider_factor*: Callable that returns the a session provider
    *data_provider_factory*: Callabble that returns a data provider
    """
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        if "debug" in self.settings:
            if self.settings["debug"]:
                logging.getLogger().setLevel(logging.DEBUG)

        self.db = None
        if "db_connection_factory" in self.settings:
            db_conn_factory = self.settings["db_connection_factory"]
            if isinstance(db_conn_factory, collections.Callable):
                self.db = db_conn_factory(self)
            else:
                raise RuntimeError("Application: Setting 'db_connection_factory'"
                                    " value must be callable")

        self.auth = None
        if "auth_provider_factory" in self.settings:
            auth_provider_factory = self.settings["auth_provider_factory"]
            if isinstance(auth_provider_factory, collections.Callable):
                self.auth = auth_provider_factory(self)
            else:
                raise RuntimeError("Application: Setting 'auth_provider_factory'"
                                    " value must be callable")

        self.sessions = None
        if "session_provider_factory" in self.settings:
            session_provider_factory = self.settings["session_provider_factory"]
            if isinstance(session_provider_factory, collections.Callable):
                self.sessions = session_provider_factory(self)
            else:
                raise RuntimeError("Application: Setting 'session_provider_factory'"
                                    " value must be callable")

        self.data = None
        if "data_provider_factory" in self.settings:
            data_provider_factory = self.settings["data_provider_factory"]
            if isinstance(data_provider_factory, collections.Callable):
                self.data = data_provider_factory(self)
            else:
                raise RuntimeError("Application: Setting 'data_provider_factory'"
                                    " value must be callable")


class OpenIdAuthSessionHandler(RequestHandler, SessionMixin, OpenIdMixin):
    """
    Open ID authentication handler.

    *NEEDS TESTING*

    This handler uses the following application settings:
    *login_success_url*: Redirect to this URL on successful login
    *openid_endpoint*: Location of the OpenID endpoint
    """

    _CONFIG_SUCCESS_URL = "login_success_url"

    _CONFIG_OPENID_ENDPOINT = "auth_openid_endpoint"

    def initialize(self, **kwargs):
        self._OPENID_ENDPOINT = "https://crowd.nscl.msu.edu/openidserver/op"

        settings = self.application.settings
        if self._CONFIG_SUCCESS_URL in settings:
            self._success_url = settings.get(self._CONFIG_SUCCESS_URL)
        else:
            raise RuntimeError("Required setting '"+ self._CONFIG_SUCCESS_URL +"' not found")

        if self._CONFIG_OPENID_ENDPOINT in settings:
            self._OPENID_ENDPOINT = settings.get(self._CONFIG_OPENID_ENDPOINT)
        else:
            raise RuntimeError("Required setting '"+ self._CONFIG_OPENID_ENDPOINT +"' not found")


    @coroutine
    def get(self):
        user = yield self.get_authenticated_user()
        if not user:
            yield self.authenticate_redirect()

        self.current_session["username"] = user["username"]
        self.current_session["authenticated"] = True
        self.current_session["last_authenticated"] = datetime.now()

        next_url = self.get_argument("next", None)
        if next_url:
            self.redirect(next_url)
        else:
            self.redirect(self._success_url)
        raise Finish()


class FormLoginSessionHandler(RequestHandler, SessionMixin):
    """
    Form login handler that delegates to the configured authentication provider.

    This handles must be initialized with the following:
    *template*: name of login page template

    This handler uses the following application settings:
    *login_success_url*: Redirect to this URL on successful login
    """

    _CONFIG_SUCCESS_URL = "login_success_url"

    def initialize(self, **kwargs):
        if "template" in kwargs:
            self._login_template = kwargs.get("template")
        else:
            raise RuntimeError("Arugment 'template' not found")

        settings = self.application.settings
        if self._CONFIG_SUCCESS_URL in settings:
            self._success_url = settings.get(self._CONFIG_SUCCESS_URL)
        else:
            raise RuntimeError("Settings '"+ self._CONFIG_SUCCESS_URL +"' not found")


    @coroutine
    def prepare(self):
        yield maybe_future(super(FormLoginSessionHandler,self).prepare())
        yield self.prepare_current_session()


    def get_current_user(self):
        return self.get_current_session_user()


    def get(self):
        """
        If current user is not authenticated, then render the login template,
        otherwise redirect to application.
        """
        if self.current_user:
            self._redirect_next()
        self._render_login()


    @coroutine
    def post(self):
        """
        Attempt authentication based on submitted 'username' and 'password'
        paramters. If successful then redirect to application, otherwise
        render the login template with error message.
        """
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        auth = self.application.auth
        user = yield auth.authenticate(username, password)
        if not user:
            self._render_login(username=username, message="Username or password incorrect")
            return

        self.current_session["username"] = username
        self.current_session["authenticated"] = True
        self.current_session["last_authenticated"] = datetime.now()

        self._redirect_next()


    def _render_login(self, *args, **kwargs):
        if kwargs.get("message", None):
            self.set_status(401)
        self.render(self._login_template, **kwargs)


    def _redirect_next(self):
        """
        Send redirect based on 'next' paramenter or configured success URL.
        """
        next_url = self.get_argument("next", None)
        if next_url:
            self.redirect(next_url)
        else:
            self.redirect(self._success_url)


class LogoutSessionHandler(RequestHandler, SessionMixin):
    """
    Simple login handler that invalids the current session.

    This handler uses the following application settings:
    *logout_success_url*: Redirect to this URL on successful logout
    """

    _CONFIG_SUCCESS_URL = "logout_success_url"

    def initialize(self, **kwargs):
        settings = self.application.settings
        if self._CONFIG_SUCCESS_URL in settings:
            self._success_url = settings.get(self._CONFIG_SUCCESS_URL)
        else:
            raise RuntimeError("Settings '"+ self._CONFIG_SUCCESS_URL +"' not found")

    @coroutine
    def prepare(self):
        yield maybe_future(super(LogoutSessionHandler,self).prepare())
        yield self.prepare_current_session()


    def get(self):
        self._logout()


    def post(self):
        self._logout()


    def _logout(self):
        self.current_session["authenticated"] = False
        self.redirect(self._success_url)

