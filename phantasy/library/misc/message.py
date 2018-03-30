# -*- coding: utf-8 -*-

import logging


def disable_warnings(level=logging.CRITICAL):
    """Disable all logging messages for *level* and below.
    
    Parameters
    ----------
    level : int
        Severity level, could be an integer, e.g. NOTSET(0), DEBUG(10),
        INFO(20), WARNING(30), ERROR(40), CRITICAL(50).
    
    Examples
    --------
    >>> from phantasy import disable_warnings
    >>> # disable all logging message
    >>> disable_warnings(50)
    >>> # show level higher than warning
    >>> disable_warnings(20)
    >>> # show level higher than info
    >>> disable_warnings(10)
    """
    logging.disable(level)


def set_loglevel(level='info'):
    LEVELS = {
        "notset": logging.NOTSET,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }
    logging.getLogger('phantasy').setLevel(LEVELS.get(level))

