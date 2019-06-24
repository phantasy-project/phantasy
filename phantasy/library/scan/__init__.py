import logging

_LOGGER = logging.getLogger(__name__)


try:
    import scan
except ImportError:
    HAS_SCAN = False
    _LOGGER.debug("Package 'scanclient' does not exit, some" \
            " features may not be available.")
else:
    HAS_SCAN = True

if HAS_SCAN:
    from .baseclient import BaseScanClient
    from .client1 import ScanClient1D
    from .datautil import ScanDataFactory

    __all__ = ['BaseScanClient', 'ScanClient1D', 'ScanDataFactory']
