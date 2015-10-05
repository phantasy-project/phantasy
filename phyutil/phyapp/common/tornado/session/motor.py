# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#

"""
Implements user session supported using MongoDB for session persistence.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import logging

from tornado.gen import coroutine
from tornado.gen import Return
from tornado.ioloop import PeriodicCallback

from . import Session
from . import SessionProvider

_LOGGER = logging.getLogger(__name__)


class MotorSession(Session, dict):
    """
    Session implementation stored in MongoDB using Motor driver.
    """
    def __init__(self, *args, **kwargs):
        super(MotorSession, self).__init__(*args, **kwargs)
        self.dirty = False

    def __setitem__(self, name, value):
        super(MotorSession, self).__setitem__(name, value)
        self.dirty = True

    def __delitem__(self, name):
        super(MotorSession, self).__delitem__(name)
        self.dirty = True



class MotorSessionProvider(SessionProvider):
    """
    Session provider implementation that stores user sessions in
    Mongo DB using the Motor driver. Modified sessions are cached
    and periodically flushed to the database.
    """
    def __init__(self, application):
        super(MotorSessionProvider,self).__init__(application)
        self._sessions = {}
        # TODO: Get collection name from application settings
        # TODO: Get flush period from application settings
        self._flusher = PeriodicCallback(self._flush, 5000)
        self._flusher.start()


    @coroutine
    def get(self, handler):
        """
        Get the session from MongoDB request handler.

        :param handler: request handler

        :returns: a Future that resolves to a Session object
        """
        token = self.get_session_token(handler)

        # Check local cache for session
        session = self._sessions.get(token, None)

        if not session:
            # check MongoDB for session
            db = self.application.db
            session = yield db.session.find_one({ "token":token })
            if session:
                session = MotorSession(session)
                self._sessions[token] = session

        if session and not self.validate_session(session, handler):
            token = self.get_session_token(handler, force=True)
            session = None

        if not session:
            # Create a new session
            session = MotorSession(token=token)
            self.prepare_session(session, handler)
            session.dirty = True
            self._sessions[token] = session

        raise Return(session)


    @coroutine
    def _flush(self):
        """
        Persist modified sessions to MongoDB.
        """
        db = self.application.db
        for token, session in self._sessions.iteritems():
            if session.dirty:
                _LOGGER.debug("Flush dirty session with token: %s", token)
                yield db.session.update({ "token":token }, session, upsert=True)
                session.dirty = False

