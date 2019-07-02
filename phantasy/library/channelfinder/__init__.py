import logging

_LOGGER = logging.getLogger(__name__)

from .database import init_db
from .database import write_db
from .database import CFCDatabase

from .table import read_csv
from .table import write_csv
from .table import write_tb
from .table import CFCTable

from .io import get_data_from_db
from .io import get_data_from_tb
from .io import write_json

__all__ = ['init_db', 'write_db', 'CFCDatabase', 'read_csv',
           'write_csv', 'write_tb', 'CFCTable',
           'get_data_from_db', 'get_data_from_tb', 'write_json',
           ]
try:
    from channelfinder import ChannelFinderClient
    HAS_CFC = True
except ImportError:
    HAS_CFC = False
    _LOGGER.debug("Package 'channelfinder' does not exit, some" \
            " features may not be available.")

if HAS_CFC:
    from .io_cfs import get_data_from_cf
    from .io_cfs import write_cfs
    from .io_cfs import get_all_properties
    from .io_cfs import get_all_tags
    __all__.extend([
        'get_data_from_cf', 'write_cfs',
        'get_all_tags', 'get_all_properties'])
