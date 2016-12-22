# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#

"""
Provide support for Jinja2 <http://jinja.pocoo.org> template engine.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import datetime
import threading
import jinja2
import humanize

from tornado.escape import json_encode
from tornado.escape import squeeze
from tornado.escape import linkify
from tornado.util import ObjectDict

_LOGGER = logging.getLogger(__name__)


class Jinja2Mixin(object):
    """
    Mixin to add support for Jinj2 templates to request handler.
    """

    _jinja2_env_lock = threading.Lock()
    _jinja2_environment = None


    def get_jinja2_namespace(self):
        """
        Default variables and functions for Jinja template local context
        """
        return ObjectDict(
            handler = self,
            request = self.request,
            current_user = self.current_user,
            static_url = self.static_url,
            reverse_url = self.reverse_url
        )


    def render_jinja2_string(self, template_name, *args, **kwargs):
        """
        Render the template with the the specified name and return
        the result as a string.

        Note that this method handles arguments differently from
        the original. Positional arguments are added to the template
        namespace and must be dictionary-like objects (ie anything
        supported by the dict.update() method.
        """
        namespace = self.get_template_namespace()
        for arg in args:
            namespace.update(arg)
        namespace.update(kwargs)
        env = self.get_jinja2_environment()
        template = env.get_template(template_name)
        return template.render(namespace)


    def render_jinja2(self, template_name, *args, **kwargs):
        self.finish(self.render_jinja2_string(template_name, *args, **kwargs))


    def get_jinja2_environment(self):
        """
        Construct and return the singleton instance of the Jinja2 environment.
        """
        with Jinja2Mixin._jinja2_env_lock:
            if Jinja2Mixin._jinja2_environment is None:
                template_path = self.application.settings.get("template_path", ".")
                template_reload = self.application.settings.get("debug", False)
                template_loader = jinja2.FileSystemLoader(template_path)
                template_extensions = [ 'jinja2.ext.do', 'jinja2.ext.with_' ]
                env = jinja2.Environment(loader=template_loader,
                                         auto_reload=template_reload,
                                         extensions=template_extensions)
                env.globals["datetime"] = datetime
                env.filters["jsonencode"] = json_encode
                env.filters["squeeze"] = squeeze
                env.filters["linkify"] = linkify
                env.filters["humanize.filesize"] = _humanize_filesize
                Jinja2Mixin._jinja2_environment = env
                _LOGGER.info("Create jinja2 environment")
            else:
                env = Jinja2Mixin._jinja2_environment
        return env


def _humanize_filesize(value, *args, **kwargs):
    if isinstance(value, jinja2.Undefined):
        return value
    return humanize.naturalsize(value, *args, **kwargs)

