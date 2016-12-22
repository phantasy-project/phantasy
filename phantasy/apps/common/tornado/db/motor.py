# encoding: UTF-8
#
# Copyright (c) 2015, Facility for Rare Isotope Beams
#
#

"""
Defines a connection factory for MongoDB server using the Motor driver.

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import motor


_CONFIG_URL = "db_connection_url"

_CONFIG_DB = "db_connection_database"


def MotorConnectionFactory(application):
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
