#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''General Python client for SCAN service, built on top of PyScanClient
library, which uses a RESTful web service to manage and proceed scan jobs.

The scan server host and port could be configured in configuration file, e.g.:
phantasy.ini. 

The scan server was developed at SNS, its nightly built binary could be found
at: https://ics-web.sns.ornl.gov/css/nightly/ and source code is managed on
github: https://github.com/ControlSystemStudio/cs-studio/tree/master/applications/scan/scan-plugins/org.csstudio.scan.server

The PyScanClient source code is managed at github:
https://github.com/PythonScanClient/PyScanClient
'''

import re
from urllib.parse import urlparse

import scan

from scan.client.scanclient import ScanClient
from scan.commands import Set, Loop, Delay, Log, Comment

from scan.client.logdata import createTable

import logging

_LOGGER = logging.getLogger(__name__)


class BaseScanClient(scan.ScanClient):
    __NAME_ID = 1

    def __init__(self, url=None, **kws):
        self._url = None
        if url is None:
            self.url = 'http://localhost:4810'
            host, port = 'localhost', 4810
        else:
            self.url = url
            _, host, port = [s.strip('/') for s in re.split('[:]', self.url)]
        self._host, self._port = host, port
        scan.ScanClient.__init__(self, host=host, port=port)
        self._post_init(**kws)

    @property
    def url(self):
        """str: URL of scan server, e.g. http://127.0.0.1:4810."""
        return self._url

    @property
    def host(self):
        """str: Scan server address, e.g. 127.0.0.1."""
        return self._host

    @host.setter
    def host(self, host):
        if host is None or host == self.host:
            pass
        else:
            self._host = host
            scan.ScanClient.__init__(self, host=self.host, port=self.port)

    @property
    def port(self):
        """int: Scan server port, e.g. 4810."""
        return self._port

    @port.setter
    def port(self, port):
        if port is None or port == self.port:
            pass
        else:
            self._port = port
            scan.ScanClient.__init__(self, host=self.host, port=self.port)

    @url.setter
    def url(self, url):
        if url is not None and url == self.url:
            pass
        else:
            urlp = urlparse(url)
            if urlp.scheme in ['http', 'https']:
                self._url = urlp.geturl()
                _, host, port = [s.strip('/') for s in re.split('[:]', self._url)]
                self._host, self._port = host, port
                scan.ScanClient.__init__(self, host=self.host, port=self.port)
            else:
                raise TypeError("Invalid URL.")

    @property
    def name(self):
        """str: Name of the scan task, 'Scan-###' by default, '###' is an
        auto-incremental integer, ranging from 001-999."""
        return self._name

    @name.setter
    def name(self, name):
        if name is None:
            self._name = "Scan-{0:03d}".format(BaseScanClient.__NAME_ID)
            BaseScanClient.__NAME_ID += 1
        else:
            self._name = name

    @property
    def n_sample(self):
        """int: Counter of DAQ for every *device_set* updating, 1 by default.
        """
        return self._n_sample

    @n_sample.setter
    def n_sample(self, n):
        if n is None:
            self._n_sample = 1
        elif isinstance(n, (int, float)):
            self._n_sample = int(n)
        else:
            raise TypeError("Input should be an integer.")

    def _post_init(self, **kws):
        pass
        # self.name = kws.get('name', None)
        # self.host = kws.get('host', None)
        # self.port = kws.get('port', None)
        # self.n_sample = kws.get('n_sample', None)

    def __repr__(self):
        pass

    def saveData(self):
        """Save data
        """
        pass

    def scan2d(self, device1, device2, meas_dev, **kwds):
        """ Perform a 2-D alignment scan, it checks the readback within given tolerance, 
        or waits callback completion if readback is `False`, for each setting.
        If original setting is provided, it will restore to this point after scan finished.
        If there is any error, it will try again, then abort.
    
        acceptable kwds key words:
            - title:     job title for a scan, "phyutil 1D Scan" by default
            - orig1:     original settings for `device`, default None. 
            - readback1: `False` to not check any readback,
                         `True` to wait for readback from the 'device',
                         or name of specific device to check for readback.
            - tolerance1:Tolerance when checking numeric `readback`, 0 by default.
            - orig2:     original settings for `device`, default None. 
            - readback2: `False` to not check any readback,
                         `True` to wait for readback from the 'device',
                         or name of specific device to check for readback.
            - tolerance2:Tolerance when checking numeric `readback`, 0 by default.
            - timeout:   Timeout in seconds, used for `completion` and `readback` check, 5.0 by default.
            - ramping:   ramping `device` to start at beginning, and ramp back to original after finish. 
                         If orig is not given, then ignore since not know where to go.
                         False by default.
                         `False` to directly jump to start for the 'device',
                         `True`  to ramp to start with same step for the 'device',
            - delay:     delay in seconds, 5.0 by default.
            - wait:      whether wait until done, `True` by default
            - samples:   how many point taken for each measurement device, 1 by default
            - compress:  how to compress data if multiple samples are taken, None by default.
                         Has to be:
                         `None`: no compress, and keep all data as it is;
                         `average`: take an average. 
    
        :param device1:    first dimension information with format [Device name, start, stop, step]
        :param device2:    second dimension information with format [Device name, start, stop, step]
        :param meas_dev:   Device to measure
         
        :return: a table with column following the device order: device, meas_dev
        :raise:
        
        """
        if not isinstance(device1, (list, tuple)) or len(device1) != 4 or \
                not isinstance(device2, (list, tuple)) or len(device2) != 4:
            raise RuntimeError("Scan parameters are not sufficient.")

        if not isinstance(device1[0], str):
            raise Exception("Expecting device1 name, got '%s'" % str(device1[0]))
        else:
            # Ensure device is NOT unicode object until 
            # it is supported by PyScanClient library.
            device1[0] = str(device1[0])

        if not isinstance(device2[0], str):
            raise Exception("Expecting device2 name, got '%s'" % str(device2[0]))
        else:
            # Ensure device is NOT unicode object until 
            # it is supported by PyScanClient library.
            device2[0] = str(device2[0])

        comments = kwds.get("title", "phyutil 2D Scan")
        orig1 = kwds.get("orig1", None)
        readback1 = kwds.get("readback1", False)
        tolerance1 = kwds.get("tolerance1", 0.0)
        orig2 = kwds.get("orig2", None)
        readback2 = kwds.get("readback2", False)
        tolerance2 = kwds.get("tolerance2", 0.0)
        timeout = kwds.get("timeout", 5.0)
        ramping = kwds.get("ramping", False)
        delay = kwds.get("delay", 5.0)
        samples = int(kwds.get("samples", 1))
        wait = kwds.get('wait', True)
        compress = kwds.get("compress", None)
        completion = kwds.get("completion", False)
        errhandler = kwds.get('errhandler', None)
        if compress is not None:
            # TODO add support to compress multiple samples and compress.lower not in ["average"]:
            raise RuntimeError("Compress algorithm is not support yet.")

        scan_cmds = []

        # prepare scan comments    
        scan_cmds.append(Comment(comments))

        # ramp to start point if needed
        if orig1 is not None and ramping:
            # slow ramping to the start point for scan
            if orig1 < device1[1]:
                scan_cmds.append(Loop(device1[0], orig1, device1[1],
                                      abs(device1[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback1, tolerance=tolerance1,
                                      timeout=timeout, errhandler=errhandler))
            else:
                scan_cmds.append(Loop(device1[0], orig1, device1[1],
                                      -abs(device1[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback1, tolerance=tolerance1,
                                      timeout=timeout, errhandler=errhandler))
        # ramp to start point if needed
        if orig2 is not None and ramping:
            # slow ramping to the start point for scan
            if orig2 < device2[1]:
                scan_cmds.append(Loop(device2[0], orig2, device2[1],
                                      abs(device2[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback2, tolerance=tolerance2,
                                      timeout=timeout, errhandler=errhandler))
            else:
                scan_cmds.append(Loop(device2[0], orig2, device2[1],
                                      -abs(device2[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback2, tolerance=tolerance2,
                                      timeout=timeout, errhandler=errhandler))

        # confirm start point
        scan_cmds.append(Set(device1[0], device1[1], completion=completion,
                             readback=readback1, tolerance=tolerance1,
                             timeout=timeout, errhandler=errhandler))
        scan_cmds.append(Set(device2[0], device2[1], completion=completion,
                             readback=readback2, tolerance=tolerance2,
                             timeout=timeout, errhandler=errhandler))

        # real scan
        if samples == 1:
            scan_cmds.append(Loop(device1[0], device1[1], device1[2], device1[3],
                                  [Loop(device2[0], device2[1], device2[2], device2[3],
                                        [Delay(delay),
                                         Log([device1[0], device2[0]] + list(meas_dev))
                                         ],
                                        completion=completion,
                                        readback=readback2, tolerance=tolerance2,
                                        ),
                                   ],
                                  completion=completion,
                                  readback=readback1, tolerance=tolerance1,
                                  timeout=timeout, errhandler=errhandler))
        else:
            scan_cmds.append(Loop(device1[0], device1[1], device1[2], device1[3],
                                  [Loop(device2[0], device2[1], device2[2], device2[3],
                                        [Loop('loc://i(0)', 1, samples, 1,
                                              [Delay(delay), Log([device1[0], device2[0]] + list(meas_dev))])
                                         ],
                                        completion=completion,
                                        readback=readback2, tolerance=tolerance2,
                                        ),
                                   ],
                                  completion=completion,
                                  readback=readback1, tolerance=tolerance1,
                                  timeout=timeout, errhandler=errhandler))

        # ramp back to original setting
        if orig1 is not None and ramping:
            # slow ramping to the start point for scan
            if device1[2] < orig1:
                scan_cmds.append(Loop(device1[0], device1[2], orig1,
                                      abs(device1[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback1, tolerance=tolerance1,
                                      timeout=timeout, errhandler=errhandler))
            else:
                scan_cmds.append(Loop(device1[0], device1[2], orig1,
                                      -abs(device1[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback1, tolerance=tolerance1,
                                      timeout=timeout, errhandler=errhandler))

        # ramp back to original setting
        if orig2 is not None and ramping:
            # slow ramping to the start point for scan
            if device2[2] < orig2:
                scan_cmds.append(Loop(device2[0], device2[2], orig2,
                                      abs(device2[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback2, tolerance=tolerance2,
                                      timeout=timeout, errhandler=errhandler))
            else:
                scan_cmds.append(Loop(device2[0], device2[2], orig2,
                                      -abs(device2[3]), [Delay(delay)],
                                      completion=completion,
                                      readback=readback2, tolerance=tolerance2,
                                      timeout=timeout, errhandler=errhandler))
        # confirm original setting
        if orig1 is not None:
            scan_cmds.append(Set(device1[0], orig1, completion=completion,
                                 readback=readback1, tolerance=tolerance1,
                                 timeout=timeout, errhandler=errhandler))
        if orig2 is not None:
            scan_cmds.append(Set(device2[0], orig2, completion=completion,
                                 readback=readback2, tolerance=tolerance2,
                                 timeout=timeout, errhandler=errhandler))

        if self.scanclient is None:
            self._connectscanserver()

        scid = self.scanclient.submit(scan_cmds, name=comments)
        if wait:
            self.scanclient.waitUntilDone(scid)

        return scid
