# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Lattice application startup script.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import functools

from argparse import ArgumentParser
from tornado.gen import coroutine
from tornado.ioloop import IOLoop

from ...common.tornado.web import Application
from ...latticemodel.service import urls
from ...latticemodel.service import settings


LOGGER = logging.getLogger(__name__)


def main():
    """
    Configuration the application and start the HTTP server.
    """
    parser = ArgumentParser()
    parser.add_argument("-e", dest="env", default="development",
                        help="deployment environment (default: development)")
    parser.add_argument("-p", dest="port", type=int, default=9090,
                        help="application server port (default: 9090)")
    parser.add_argument("--init-db", dest="init_db", action="store_true",
                        help="initialize the application database")
    args = parser.parse_args()

    if not hasattr(settings, args.env):
        LOGGER.error("Deployment environment not found: '%s'", args.env)
        return

    env = getattr(settings, args.env)
    app = Application(urls.urlpatterns, **env)
    LOGGER.info("Application initialized with environment: '%s'", args.env)

    if args.init_db:
        LOGGER.info("Starting database initialization")
        try:
            IOLoop.current().run_sync(functools.partial(init_database, app))
        except:
            LOGGER.exception("Error while initializing the application database")
        LOGGER.info("Completed database initialization")
        return

    app.listen(args.port)
    LOGGER.info("Application listening on port: %s", args.port)

    IOLoop.current().start()


@coroutine
def init_database(application):
    """
    Initialize the database with the required data.
    """
    data = application.data

    particle_types = [
        {"type":"ar36", "name":"Ar-36", "protons":18, "neutrons":18},
        {"type":"kr86", "name":"Kr-86", "protons":36, "neutrons":50},
        {"type":"u238", "name":"U-238", "protons":92, "neutrons":146}
    ]

    LOGGER.info("Inserting particle type data")
    for particle_type in particle_types:
        yield data.insert_particle_type(particle_type)



if __name__ == "__main__":
    main()
else:
    restapi = Application(urls.restpatterns)

