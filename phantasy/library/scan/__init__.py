import logging

_LOGGER = logging.getLogger(__name__)


try:
    import scan
    HAS_SCAN = True
except ImportError:
    HAS_SCAN = False
    _LOGGER.warning("Package 'scanclient' does not exit, some" \
            " features may not be available.")

if HAS_SCAN:
    from .baseclient import BaseScanClient
    from .client1 import ScanClient1D
    from .datautil import ScanDataFactory

    __all__ = ['BaseScanClient', 'ScanClient1D', 'ScanDataFactory']
