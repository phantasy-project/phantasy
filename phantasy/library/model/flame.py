#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains classes/functions to serve as utils for the
potential requirment of modeling accelerator with FLAME code.

As of 0.7.6, package: flame_utils has been applied to provide these features.
"""

import logging
import sys

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2018, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)

try:
    from flame_utils import BeamState
    from flame_utils import ModelFlame
    from flame_utils import collect_data
    from flame_utils import configure
    from flame_utils import convert_results
    from flame_utils import generate_latfile
    from flame_utils import get_all_names
    from flame_utils import get_all_types
    from flame_utils import get_element
    from flame_utils import get_index_by_name
    from flame_utils import get_index_by_type
    from flame_utils import get_names_by_pattern
    from flame_utils import inspect_lattice
    from flame_utils import propagate
except ImportError:
    _LOGGER.error(
        "Cannot find package: flame_utils, install debian package: python-flame-utils or python3-flame-utils")
    sys.exit(1)
