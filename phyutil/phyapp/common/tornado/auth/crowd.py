# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#

"""
Implements authentication support using the Atlassian Crowd service RESTful API.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import logging

from tornado.gen import coroutine
from tornado.gen import Return
from tornado.httputil import HTTPHeaders
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import url_escape
from tornado.escape import json_decode
from tornado.escape import json_encode
from . import AuthProvider
from . import AuthUser

_LOGGER = logging.getLogger(__name__)


class CrowdAuthProvider(AuthProvider):
    """
    AuthProvider implemention support Atlassian Crowd server using REST API.

    The following application settings are used to configure this provider:
    *crowd_auth_provider_url*: root URL of the Crowd API server
    *crowd_auth_provider_username*: username to authenticate with Crowd API
    *crowd_auth_provider_password*: password to authenticate with Crowd API
    """

    _CROWD_AUTH_URL = "/rest/usermanagement/1/authentication"

    _CONFIG_CROWD_URL = "auth_provider_crowd_url"

    _CONFIG_CROWD_USERNAME = "auth_provider_crowd_username"

    _CONFIG_CROWD_PASSWORD = "auth_provider_crowd_password"

    def __init__(self, application):
        super(CrowdAuthProvider,self).__init__(application)
        settings = self.application.settings

        if self._CONFIG_CROWD_URL in settings:
            self._crowd_url = settings.get(self._CONFIG_CROWD_URL)
        else:
            raise RuntimeError("Settings '"+ self._CONFIG_CROWD_URL + "' not found")

        if self._CONFIG_CROWD_USERNAME in settings:
            self._crowd_username = settings.get(self._CONFIG_CROWD_USERNAME)
        else:
            raise RuntimeError("Settings '"+ self._CONFIG_CROWD_USERNAME +"' not found")

        if self._CONFIG_CROWD_PASSWORD in settings:
            self._crowd_password = settings.get(self._CONFIG_CROWD_PASSWORD)
        else:
            raise RuntimeError("Settings '"+ self._CONFIG_CROWD_PASSWORD +"' not found")

        self._crowd_headers = HTTPHeaders({
            "Accept":"application/json",
            "Content-Type":"application/json"
        })

        self._client = AsyncHTTPClient()


    @coroutine
    def authenticate(self, username, password):
        """
        Authenticate user with using the Crowd service API.

        :returns: a Future that must a resolve to None or a valid AuthUser object.
        """
        auth_url = self._crowd_url
        auth_url += self._CROWD_AUTH_URL
        auth_url +=  "?username="
        auth_url += url_escape(username)

        auth_body = { "value":password }

        request = HTTPRequest(auth_url,
            method="POST",
            auth_mode="basic",
            auth_username=self._crowd_username,
            auth_password=self._crowd_password,
            headers=self._crowd_headers,
            body=json_encode(auth_body)
        )

        fetch_time = time.clock()
        try:
            response = yield self._client.fetch(request)
        except HTTPError as e:
            if e.code == 400:
                # Expected status code from the Crowd API
                # for unsuccessful user authentication.
                body = json_decode(e.response.body)
                _LOGGER.warn("Authentication failure for username: %s: %s",
                                                username, body["message"])
                return
            # Re-raise execption
            raise

        fetch_time = (time.clock() - fetch_time) * 1000
        if fetch_time > 100:
            _LOGGER.warn("Authentication request success: %sms", fetch_time)
        else:
            _LOGGER.info("Authentication request success: %sms", fetch_time)

        if "Set-Cookie" in response.headers:
            if "Cookie" in self._crowd_headers:
                del self._crowd_headers["Cookie"]
            for cookie in response.headers.get_list("Set-Cookie"):
                self._crowd_headers.add("Cookie", cookie)

        body = json_decode(response.body)

        if "name" not in body:
            _LOGGER.warn("Missing 'name' attribute in Crowd response")
            return

        user = AuthUser()
        user.username = body["name"]
        raise Return(user)

