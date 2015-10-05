# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#

"""
Defines a standard interface to provide application user session support.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import uuid
import logging

from datetime import datetime
from collections import MutableMapping
from tornado.gen import coroutine
from tornado.gen import Return

_LOGGER = logging.getLogger(__name__)


class SessionMixin(object):
    """
    Mixin providing user session support for request handlers.
    """
    def get_current_session_user(self):
        if not hasattr(self, "current_session"):
            _LOGGER.warning("Missing session: prepare_current_session() not called")
            return None

        if not self.current_session.get("authenticated", False):
            return None

        return self.current_session.get("username", None)


    @coroutine
    def prepare_current_session(self):
        self.current_session = yield self.application.sessions.get(self)
        #self.current_session["username"] = None
        #self.current_session["authenticated"] = False
        #self.current_session["last_activity"] = datetime.now()



class Session():
    """
    Specifies the standard class representing the user session.

    The Session object must implement the MutableMapping interface and must
    contain the key 'token' containing the unique string identifier for this
    session.
    """

    def __hash__(self):
        return hash(self["token"])


class SessionProvider(object):
    """
    Specifies the standard SessionProvider interface that provides general
    support for user sessions. The session provider is initialized with
    the current application instance and uses the following settings:

    *session_provider_cookie*: name of session cookie
    """

    _CONFIG_COOKIE = "session_provider_cookie"

    def __init__(self, application):
        super(SessionProvider,self).__init__()
        self.application = application
        settings = application.settings
        self._cookie_name = settings.get(self._CONFIG_COOKIE, "phyutil_session")


    def get(self, handler):
        """
        Find the current user session or create one if not found.

        :param handler: current request handler

        :returns: a Future that must resolve to a Session object
        """
        raise NotImplementedError()


    def get_session_token(self, handler, force=False):
        """
        Get the session token from the request header using the
        configured session cookie name. If the session token
        is not found than created a new session token and set
        the session cookie in the response.

        :param handler: current request handler
        :param force: always create new token

        :returns: string session token
        """
        token = None if force else handler.get_cookie(self._cookie_name)
        if not token:
            token = str(uuid.uuid4())
            handler.set_cookie(self._cookie_name, token)
            _LOGGER.info("Session cookie name: %s, token: %s",
                                        self._cookie_name, token)
        return token


    def prepare_session(self, session, handler):
        """
        Prepare the session with the session validation factors.

        :param session: Session object
        :param handler: request Handler
        """
        headers = handler.request.headers
        session["Remote-IP"] = handler.request.remote_ip
        _LOGGER.debug("Session validation factor: Remote IP: %s",
                                                session["Remote-IP"])
        session["User-Agent"] = headers.get("User-Agent", "")
        _LOGGER.debug("Session validation factor: User-Agent: %s",
                                                session["User-Agent"])
        session["X-Forwarded-From"] = headers.get("X-Forwarded-From", "")
        _LOGGER.debug("Session validation factor: X-Forwarded-From: %s",
                                                session["X-Forwarded-From"])


    def validate_session(self, session, handler):
        """
        Validate the current session with the validation factors.

        :param session: Session object
        :param handler: request handler
        :returns: True if session is valid, otherwise False
        """
        headers = handler.request.headers
        if session["Remote-IP"] != handler.request.remote_ip:
            _LOGGER.warn("Session validation failure: Remote IP: '%s' != '%s'",
                                session["Remote-IP"], handler.request.remote_ip)
            return False
        if session["User-Agent"] != headers.get("User-Agent", ""):
            _LOGGER.warn("Session validation failure: User-Agent: '%s' != '%s'",
                         session["User-Agent"], headers.get("User-Agent", ""))
            return False
        if  session["X-Forwarded-From"] != headers.get("X-Forwarded-From", ""):
            _LOGGER.warn("Session validation failure: User-Agent: '%s' != '%s'",
                         session["X-Forwarded-From"], headers.get("X-Forwarded-From", ""))
            return False
        # success
        return True


class InMemorySession(Session, dict):
    """
    Implement Session object using a simple dictionary.
    """
    def __init__(self, *args, **kwargs):
        super(InMemorySession, self).__init__(*args, **kwargs)


class InMemorySessionProvider(SessionProvider):
    """
    Implement the SessionProvider interface using in-memory dictionary.
    """
    def __init__(self, application):
        super(InMemorySessionProvider, self).__init__(application)
        self._sessions = {}


    @coroutine
    def get(self, handler):
        """
        Get the in-memory session from request handler.

        :param handler: request handler

        :returns: a Future that resolves to a Session object
        """
        token = self.get_session_token(handler)
        session = self._sessions.get(token, None)

        if session and not self.validate_session(session, handler):
                token = self.get_session_token(handler, force=True)
                session = None

        if not session:
            session = InMemorySession(token=token)
            self.prepare_session(session, handler)
            self._sessions[token] = session

        raise Return(session)

