# encoding: UTF-8

"""
Utilities and extensions for the `cothread`_ catools library.

.. cothread: http://controls.diamond.ac.uk/downloads/python/cothread

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from collections import OrderedDict

from cothread import catools

# Export constants from catools module
FORMAT_RAW = catools.FORMAT_RAW
FORMAT_TIME = catools.FORMAT_TIME
FORMAT_CTRL = catools.FORMAT_CTRL


def _to_str(pvs):
    """Ensure argument is a string or list of strings."""
    # The logic follows that from the cothread library.
    # If is it NOT a string then assume it is an iterable.
    if isinstance(pvs, str):
        return str(pvs)
    else:
        return [str(pv) for pv in pvs]


def caput(pvs, values, repeat_value=None, datatype=None,
          wait=True, timeout=5, callback=None, throw=True):
    """
    Convenience function that wraps the cothread.catools.caput()
    function with safe handling of unicode strings in Python 2.X.

    .. note:: The default value of the 'wait' keyword argument
       has been changed from the original cothread function.

    .. note:: The default value of the 'repeat_value' keyword
       argument has been changed from the original cothread
       function. The original cothread function raises an
       exception if the repeat_value argument is given when
       using a single channel. This function permits the
       repeat_value argument to be given with a value of
       None when using a single channel.  When using an
       array of channels, a repeat_value with the value
       of None is the same as the value of False.
    """
    if isinstance(pvs, str):
        if repeat_value is not None:
            raise ValueError("repeat_value must be None for a single channel")
        return catools.caput(_to_str(pvs), values,
                             datatype=datatype, wait=wait,
                             timeout=timeout, callback=callback, throw=throw)
    else:
        if repeat_value is None:
            repeat_value = False
        return catools.caput(_to_str(pvs), values,
                             repeat_value=repeat_value,
                             datatype=datatype, wait=wait,
                             timeout=timeout, callback=callback, throw=throw)


def caget(pvs, timeout=5, datatype=None,
          format=FORMAT_RAW, count=0, throw=True):
    """
    Convenience function that wraps the cothread.catools.caget()
    function with safe handling of unicode strings in Python 2.X.
    """
    # The argument 'format' redefines builtin function
    #   pylint: disable=redefined-builtin
    return catools.caget(_to_str(pvs), timeout=timeout, datatype=datatype,
                         format=format, count=count, throw=throw)


def camonitor(pvs, callback, events=None, datatype=None,
              format=FORMAT_RAW, count=0, all_updates=False,
              notify_disconnect=False, connect_timeout=None):
    """
    Convenience function that wraps the cothread.cotools.camonitor()
    function with safe handling of unicode string in Python 2.X.
    """
    # The argument 'format' redefines builtin function
    #   pylint: disable=redefined-builtin
    return catools.camonitor(_to_str(pvs), callback,
                             events=events, datatype=datatype, format=format,
                             count=count, all_updates=all_updates,
                             notify_disconnect=notify_disconnect,
                             connect_timeout=connect_timeout)


def connect(pvs, cainfo=False, wait=True, timeout=5, throw=True):
    """
    Convenience function that wraps the cothread.catools.connect()
    function with safe handling of unicode strings in Python 2.X.
    """
    # The argument 'cainfo' redefines module function
    #   pylint: disable=redefined-outer-name
    return catools.connect(_to_str(pvs), cainfo=cainfo,
                           wait=wait, timeout=timeout, throw=throw)


def cainfo(pvs, timeout=5, throw=True):
    """
    Convenience function that wraps the cothread.catools.cainfo()
    function with safe handling of unicode string in Python 2.X.
    """
    return catools.cainfo(_to_str(pvs), timeout=timeout, throw=throw)


class CABatch(OrderedDict):
    """
    Utility class for making batch calls to caget, caput, camonitor.

    The CABatch class is an ordered dictionary with the keys being
    channels. The values of the map are different depending on usage.
    """
    def __init__(self, *args, **kwargs):
        super(CABatch, self).__init__(*args, **kwargs)


    def caput(self, repeat_value=False, datatype=None,
              wait=True, timeout=5, callback=None, throw=True):
        """
        Batch caput all channels using the dictionary values.
        """
        pvs = list(self.keys())
        values = list(self.values())
        return caput(pvs, values, repeat_value=repeat_value, datatype=datatype,
                     wait=wait, timeout=timeout, callback=callback, throw=throw)


    def caget(self, timeout=5, datatype=None,
              format=FORMAT_RAW, count=0, throw=True):
        """
        Batch caget all channels and store the returned values.
        """
        # The argument 'format' redefines builtin function
        #   pylint: disable=redefined-builtin
        pvs = list(self.keys())
        values = caget(pvs, timeout=timeout, datatype=datatype,
                       format=format, count=count, throw=throw)
        self.update(zip(pvs, values))
        return values


    def camonitor(self, callback, events=None, datatype=None,
                  format=FORMAT_RAW, count=0, all_updates=False,
                  notify_disconnect=False, connect_timeout=None):
        """
        Batch camonitor all channels and store the returned subscriptions.
        """
        # The argument 'format' redefines builtin function
        #   pylint: disable=redefined-builtin
        pvs = list(self.keys())
        subs = camonitor(pvs, callback, events=events, datatype=datatype,
                         format=format, count=count, all_updates=all_updates,
                         notify_disconnect=notify_disconnect,
                         connect_timeout=connect_timeout)
        self.update(zip(pvs, subs))
        return subs


    def connect(self, cainfo=False, wait=True, timeout=5, throw=True):
        """
        Batch connect all channels.
        """
        # The argument 'cainfo' redefines module function
        #   pylint: disable=redefined-outer-name
        pvs = list(self.keys())
        return connect(pvs, cainfo=cainfo, wait=wait,
                       timeout=timeout, throw=throw)


    def cainfo(self, timeout=5, throw=True):
        """
        Batch cainfo all channels.
        """
        pvs = list(self.keys())
        return connect(pvs, timeout=timeout, throw=throw)


    def close(self):
        """
        Call close method on all values of the dictionary.

        The indented purposed of this is to close subscriptions
        from a previous call to camonitor.
        """
        for value in self.values:
            if hasattr(value, "close"):
                value.close()


    def append(self, pv, value=None):
        """
        Alternate method for adding channels to batch object.
        """
        # Pylint requires argument names to be at least 3 characters
        #   pylint: disable=invalid-name
        self[pv] = value
