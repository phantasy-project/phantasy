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

import uuid
import logging
import threading
import collections
import tornado.web
import tornado.escape
import jinja2
import motor

from datetime import datetime
from bson.objectid import ObjectId
from tornado.web import Finish
from tornado.web import HTTPError
from tornado.gen import Return
from tornado.gen import coroutine
from tornado.gen import maybe_future
from tornado.ioloop import PeriodicCallback

_LOGGER = logging.getLogger("tornado.general")


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


class Jinja2RequestHandler(tornado.web.RequestHandler):
    """
    A RequestHandler that uses Jinja2 template engine.
    """

    _jinja2_env_lock = threading.Lock()
    _jinja2_environment = None


    @property
    def template_namespace(self):
        """The template namespace for this request

        This is a cached version from `get_template_namespace`
        with additional items added by `prepare_template_namespace`.
        """
        if not hasattr(self, "_template_namespace"):
            self._template_namespace = self.get_template_namespace()
        return self._template_namespace


    def get_template_namespace(self):
        """
        Default variables and functions for Jinja template local context
        """
        return dict(
            handler = self,
            request = self.request,
            current_user = self.current_user,
            static_url = self.static_url,
            reverse_url = self.reverse_url
        )


    @coroutine
    def prepare_template_namespace(self):
        """Asynchronous preparation of the template namespace.

        Intended to be overwritten by extending classes.
        """
        pass


    def render_string(self, template_name, *args, **kwargs):
        """
        Render the template with the the specified name and return
        the result as a string.

        Note that this method handles arguments differently from
        the original. Positional arguments are added to the template
        namespace and must be dictionary-like objects (ie anything
        supported by the dict.update() method.
        """
        namespace = self.template_namespace
        for arg in args:
            namespace.update(arg)
        namespace.update(kwargs)
        env = self.get_jinja2_environment()
        template = env.get_template(template_name)
        return template.render(namespace)


    def render(self, template_name, *args, **kwargs):
        """
        Render the template with the specified name of finish request.

        Note that this methid handles arguments differently from the
        original. Positional arguments are added to the template
        namespace and must be dictionary-like objects (ie anything
        supported by the dict.update() method.
        """
        html = self.render_string(template_name, *args, **kwargs)
        self.finish(html)


    def get_jinja2_environment(self):
        """
        Construct and return the singleton instance of the Jinja2 environment.
        """
        with Jinja2RequestHandler._jinja2_env_lock:
            if Jinja2RequestHandler._jinja2_environment is None:
                template_path = self.application.settings.get("template_path", ".")
                template_reload = self.application.settings.get("debug", False)
                template_loader = jinja2.FileSystemLoader(template_path)
                template_extensions = [ 'jinja2.ext.do', 'jinja2.ext.with_' ]
                env = jinja2.Environment(loader=template_loader,
                                         auto_reload=template_reload,
                                         extensions=template_extensions)
                env.globals["datetime"] = datetime
                env.filters["jsonencode"] = tornado.escape.json_encode
                env.filters["squeeze"] = tornado.escape.squeeze
                env.filters["linkify"] = tornado.escape.linkify
                Jinja2RequestHandler._jinja2_environment = env
                _LOGGER.info("Create jinja2 environment")
            else:
                env = Jinja2RequestHandler._jinja2_environment
        return env


class SessionRequestHandler(tornado.web.RequestHandler):
    """
    A common base request handler implemention supporting authentication and sessions.

    .. warning:: This class is designed to be used with the extended Application.
    """
    def __init__(self, *args, **kwargs):
        super(SessionRequestHandler, self).__init__(*args, **kwargs)
        self.current_session = None


    def get_current_user(self):
        if self.current_session is None:
            _LOGGER.warning("Missing session: prepare_current_session() not called")
            return None

        if "authenticated" not in self.current_session:
            _LOGGER.warning("Missing session property: 'authenticated'")
            return None

        if not self.current_session["authenticated"]:
            return None

        if "username" not in self.current_session:
            _LOGGER.warning("Missing session property: 'username'")
            return None

        return self.current_session["username"]


    @coroutine
    def prepare_current_session(self):
        if "session_cookie" in self.settings:
            name = self.settings["session_cookie"]
        else:
            name = "phyutil_session"

        value = self.get_secure_cookie(name)
        if value is not None:
            session = yield self.application.sessions.find(value)
            if session is not None:
                session["last_activity"] = datetime.now()
                self.current_session = session
                return

        session = yield self.application.sessions.create()
        session["username"] = None
        session["authenticated"] = False
        session["last_activity"] = datetime.now()
        self.set_secure_cookie(name, session.id)
        self.current_session = session
        return



class CommonRequestHandler(SessionRequestHandler, Jinja2RequestHandler):
    """
    Common request handler using Jinja2 templates and session support.
    """
    @coroutine
    def prepare(self):
        yield maybe_future(super(CommonRequestHandler, self).prepare())
        yield self.prepare_current_session()
        yield self.prepare_template_namespace()


    def get_current_user(self):
        return SessionRequestHandler.get_current_user(self)


    def get_template_namespace(self):
        return Jinja2RequestHandler.get_template_namespace(self)


    def render_string(self, template_name, *args, **kwargs):
        return Jinja2RequestHandler.render_string(self, template_name, *args, **kwargs)


    def render(self, template_name, *args, **kwargs):
        return Jinja2RequestHandler.render(self, template_name, *args, **kwargs)



class UsernamePasswordLoginHandler(CommonRequestHandler):
    """
    Simple login handler that delegates to the configured authentication provider.
    
    This handler defines the following application settings:
    
    *login_template*: Name of templates for login page 
    *login_success_url*: Redirect to this URL on successful login
    """
    def get(self):
        if "authenticated" in self.current_session:
            if self.current_session["authenticated"]:
                next_url = self.get_argument("next", None)
                if next_url:
                    self.redirect(next_url)
                else:
                    self.require_setting("login_success_url")
                    self.redirect(self.settings["login_success_url"])
                return

        self.require_setting("login_template")
        self.render(self.settings["login_template"])


    @coroutine
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        authenticated = yield self.application.auth.authenticate(username, password)
        if not authenticated:
            self.set_status(401)
            self.render(self.settings["login_template"], username=username,
                            message="Username or password incorrect")
            raise Finish()

        self.current_session["username"] = username
        self.current_session["authenticated"] = True
        self.current_session["last_authenticated"] = datetime.now()

        next_url = self.get_argument("next", None)
        if next_url is not None:
            self.redirect(next_url)
        else:
            self.require_setting("login_success_url")
            self.redirect(self.settings["login_success_url"])
        raise Finish()


class SessionLogoutHandler(CommonRequestHandler):
    """
    Simple login handler that invalids the current session.
    
    This handler defines the following application settings:
     
    *logout_success_url*: Redirect to this URL on successful logout
    """
    def get(self):
        self._do_logout()

    def post(self):
        self._do_logout()

    def _do_logout(self):
        self.current_session["authenticated"] = False
        self.require_setting("logout_success_url", "")
        self.redirect(self.settings["logout_success_url"])


class TemplateHandler(CommonRequestHandler):

    def initialize(self, **kwargs):
        super(TemplateHandler, self).initialize(**kwargs)
        if "name" in kwargs: 
            self._name = kwargs["name"]
        else:
            self._name = None

    def get(self):
        if self._name is not None:
            self.render(self._name)
        else:
            raise HTTPError(404)


#
# Database Connection
#

def motor_connection_factory(application):
    """
    Initialize connection with Mongodb using Motor driver.
    """
    if "db_connection_url" in application.settings:
        db_conn_url = application.settings["db_connection_url"]
    else:
        db_conn_url = None

    if "db_connection_database" in application.settings:
        db_conn_database = application.settings["db_connection_database"]
    else:
        raise RuntimeError("Database name not specified in 'db_connection_database' setting")

    if db_conn_url is None:
        client = motor.MotorClient()
    else:
        client = motor.MotorClient(db_conn_url)

    return client[db_conn_database]


#
# User Session Management
#

class BaseSessionProvider(object):
    """
    Define the "SessionProvider" interface.
    """
    def create(self):
        raise NotImplementedError()

    def find(self, sid):
        raise NotImplementedError()


class BaseSession(dict):
    """
    Define the Session interface.
    """
    def __init__(self, sid, *args, **kwargs):
        super(BaseSession, self).__init__(*args, **kwargs)
        self._id = sid

    @property
    def id(self):
        return self._id


class InMemorySessionProvider(BaseSessionProvider):
    """
    Implement SessionProvider interface using simple dictionary.
    """
    def __init__(self, application):
        super(InMemorySessionProvider, self).__init__()
        self._sessions = {}

    @tornado.gen.coroutine
    def create(self):
        session = InMemorySession(str(uuid.uuid4()))
        self._sessions[session.id] = session
        return session

    @tornado.gen.coroutine
    def find(self, sid):
        if sid in self._sessions:
            return self._sessions[sid]
        else:
            return None


class InMemorySession(BaseSession):
    """
    Implement Session interface using a simple dictionary.
    """
    def __init__(self, sid):
        super(InMemorySession, self).__init__(sid)


class MotorSessionProvider(BaseSessionProvider):
    """
    Session provider implementation that stores user sessions in
    Mongo DB using the Motor driver. Modified sessions are cached
    and periodically flushed to the database.
    """
    def __init__(self, application):
        self._sessions = {}
        self._application = application
        # TODO: Get flush period from application settings.
        self._flusher = PeriodicCallback(self._flush, 5000)
        self._flusher.start()


    @tornado.gen.coroutine
    def create(self):
        """
        Create a new session by inserting an empty document
        into the database then returning a Session object.
        """
        result = yield self._application.db.sessions.insert({})
        session = MotorSession({"_id":result})
        self._sessions[session.id] = session
        raise Return(session)


    @tornado.gen.coroutine
    def find(self, sid):
        _LOGGER.debug("Find session with id: %s", sid)
        if sid in self._sessions:
            raise Return(self._sessions[sid])
        db = self._application.db
        result = yield db.sessions.find_one({"_id":ObjectId(sid)})
        session = MotorSession(result)
        self._sessions[session.id] = session
        raise Return(session)


    @tornado.gen.coroutine
    def _flush(self):
        db = self._application.db
        for session in self._sessions.values():
            if session.dirty:
                _LOGGER.debug("Flush dirty session with id: %s", session.id)
                yield db.sessions.update({ "_id":ObjectId(session.id)}, dict(session))
                session.dirty = False


class MotorSession(BaseSession):
    """
    Session implementation stored in Mongo DB using Motor driver.
    """
    def __init__(self, values):
        if "_id" not in values:
            raise ValueError("Session must be initialized with value '_id'")
        super(MotorSession, self).__init__(str(values["_id"]), values)
        del self["_id"]
        self.dirty = False

    def __setitem__(self, name, value):
        super(MotorSession, self).__setitem__(name, value)
        self.dirty = True

    def __delitem__(self, name):
        super(MotorSession, self).__delitem__(name)
        self.dirty = True


#
# User Authentication
#

class BaseAuthProvider(object):
    """
    Define the AuthProvider interface. 
    """
    def authenticate(self):
        raise NotImplementedError()


class InMemoryAuthProvider(BaseAuthProvider):
    
    def __init__(self, application):
        self._users = {}
        if "auth_provider_users" in application.settings:
            self._users.update(application.settings["auth_provider_users"])

    @tornado.gen.coroutine
    def authenticate(self, username, password):
        if username in self._users:
            return (self._users[username] == password)
        else:
            return False

