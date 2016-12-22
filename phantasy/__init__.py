from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import logging

from .apps import lmapp
from .tools import phytool


# configure the root logger
logging.basicConfig(format="%(levelname)s: %(asctime)s: %(name)s: %(message)s")

