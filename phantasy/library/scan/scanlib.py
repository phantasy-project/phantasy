'''
This module is built on top of PyScanClient library, which uses a RESTful based web service to perform a scan task.
The scan server host and port could be configured in site configuration file, phyutil.ini. 

The scan server is a RESTful based web service, which was developed at SNS.
Its binary nightly build could be found at:
https://ics-web.sns.ornl.gov/css/nightly/
and source code is managed at github:
https://github.com/ControlSystemStudio/cs-studio/tree/master/applications/plugins/org.csstudio.scan

The PyScanClient source code is managed at github:
https://github.com/PythonScanClient/PyScanClient

Created on Apr 21, 2015

@author: shen
'''

import re
from urlparse import urlparse

from scan.client.scanclient import ScanClient
from scan.commands import Set, Loop, Delay, Log, Comment

from scan.client.logdata import createTable


try:
    # Python 2.X
    basestring
except NameError:
    # Python 3.X
    basestring = str


# TODO inherit ScanClient class
class ScanLib():
    """
    """
    def __init__(self, url=None):
        self.SCAN_SRV_URL = url
        self.scanclient = None

    def updateurl(self, url):
        if url is None or not re.match(r"https?://.*", url, re.I):
            raise RuntimeError("machine is not properly initialized yet. Cannot find valid scan server url.")
        self.SCAN_SRV_URL = url
        self.scanclient =None
        self._connectscanserver()
        
    def scan1d(self, device, start, stop, step, meas_dev, **kwds):
        """ Perform a 1-D alignment scan, it checks the readback within given tolerance, 
        or waits callback completion if readback is `False`, for each setting.
        If original setting is provided, it will restore to this point after scan finished.
        If there is any error, it will try again, then abort.
    
        acceptable kwds key words:
            - title:     job title for a scan, "phyutil 1D Scan" by default
            - orig:      original settings for `device`, default None. 
            - readback:  `False` to not check any readback,
                         `True` to wait for readback from the 'device',
                         or name of specific device to check for readback.
            - tolerance: Tolerance when checking numeric `readback`, 0 by default.
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
    
        :param device:     Device name
        :param start:      Initial value
        :param stop:       Final value
        :param step:       Step size
        :param meas_dev:   Device to measure
         
        :return: a table with column following the device order: device, meas_dev
        :raise:
        
        """
        if not isinstance(device, basestring):
            raise Exception("Expecting device name, got '%s'" % str(device))
        else:
            # Ensure device is NOT unicode object until 
            # it is supported by PyScanClient library.
            device = str(device)
        comments = kwds.get("title", "phyutil 1D Scan")
        orig = kwds.get("orig", None)
        readback = kwds.get("readback", False)
        tolerance = kwds.get("tolerance", 0.0)
        timeout = kwds.get("timeout", 5.0)
        ramping = kwds.get("ramping", False)
        delay = kwds.get("delay", 5.0)
        samples = int(kwds.get("samples", 1))
        compress = kwds.get("compress", None)
        wait = kwds.get('wait', True)
        completion = kwds.get('completion', False)
        errhandler = kwds.get('errhandler', None)
        if compress is not None:
            # TODO add support for multiple samples and compress.lower not in ["average"]:
            raise RuntimeError("Compress algorithm is not support yet.")
    
        scan_cmds = []
    
        # prepare scan comments    
        scan_cmds.append(Comment(comments))
        
        # ramp to start point if needed
        if orig is not None and ramping:
            # slow ramping to the start point for scan
            if orig < start:
                scan_cmds.append(Loop(device, orig, start, abs(step),
                                      [Delay(delay)], completion=completion, 
                                      readback=readback, tolerance=tolerance, 
                                      timeout=timeout, errhandler=errhandler))
            else:
                scan_cmds.append(Loop(device, orig, start, -abs(step),
                                      [Delay(delay)], completion=completion, 
                                      readback=readback, tolerance=tolerance, 
                                      timeout=timeout, errhandler=errhandler))
        
        # confirm start point
        scan_cmds.append(Set(device, start, completion=completion,
                             readback=readback, tolerance=tolerance, 
                             timeout=timeout, errhandler=errhandler))
        
        # real scan
        if samples == 1:
            scan_cmds.append(Loop(device, start, stop, step,
                                  [
                                   Delay(delay),
                                   Log([device] + list(meas_dev))
                                  ],
                                  completion=completion, 
                                  readback=readback, tolerance=tolerance, 
                                  timeout=timeout, errhandler=errhandler))
        else:
            scan_cmds.append(Loop(device, start, stop, step,
                                  [
                                   Loop('loc://i(0)', 1, samples, 1,
                                   [Delay(delay), Log([device] + list(meas_dev))])
                                  ],
                                  completion=completion, 
                                  readback=readback, tolerance=tolerance, 
                                  timeout=timeout, errhandler=errhandler))
        
        # ramp back to original setting
        if  orig is not None and ramping:
            # slow ramping to the start point for scan
            if stop < orig:
                scan_cmds.append(Loop(device, stop, orig, abs(step),
                                      [Delay(delay)], completion=completion, 
                                      readback=readback, tolerance=tolerance,
                                      timeout=timeout, errhandler=errhandler))
            else:
                scan_cmds.append(Loop(device, stop, orig, -abs(step),
                                      [Delay(delay)], completion=completion,
                                      readback=readback, tolerance=tolerance, 
                                      timeout=timeout, errhandler=errhandler))
        
        # confirm original setting
        if orig is not None:
            scan_cmds.append(Set(device, orig, completion=completion,
                                 readback=readback, tolerance=tolerance, 
                                 timeout=timeout, errhandler=errhandler))
    
        if self.scanclient is None:
            self._connectscanserver()
              
        scid =self.scanclient.submit(scan_cmds, name=comments)
        if wait:
            self.scanclient.waitUntilDone(scid)
            
        return scid
    
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

        if not isinstance(device1[0], basestring):
            raise Exception("Expecting device1 name, got '%s'" % str(device1[0]))
        else:
            # Ensure device is NOT unicode object until 
            # it is supported by PyScanClient library.
            device1[0] = str(device1[0])

        if not isinstance(device2[0], basestring):
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
    
    def _connectscanserver(self):
        """Connect to scan server using server information from configuration.
        """
        if self.SCAN_SRV_URL is None or not re.match(r"https?://.*", self.SCAN_SRV_URL, re.I):
            raise RuntimeError("machine is not properly initialized yet. Cannot find valid scan server url.")

        if self.scanclient is None:
            ss_host = urlparse(self.SCAN_SRV_URL)
            if ss_host.port is None:
                self.scanclient = ScanClient(ss_host.hostname)
            else:
                self.scanclient = ScanClient(ss_host.hostname, ss_host.port)
    
    def deletescan(self, scanid):
        """Delete a scan task
        
        :param scanid: scan id number
        """
        if self.scanclient is None:
            self._connectscanserver()
        # clean up this scan task          
        self.scanclient.delete(scanid)
    
    def getscanstatus(self, scanid):
        """Get status of a scan task.
        Detailed status could be fetched by calling:
            - state: like 'Idle', 'Running', 'Paused', 'Finished'
            - name: scan instance name
            - id: scan id
            and
            - isDone(): `True` or `False`
            - percentage(): Percent of work done, 0...100
        
        see :class:`PyScanClient.scan.client.ScanInfo`
        
        :param scanid: scan id number
        :return: ScanInfo object
        """
        if self.scanclient is None:
            self._connectscanserver()
        # clean up this scan task          
        return self.scanclient.scanInfo(scanid)
    
    def abortscan(self, scanid):
        """Abort a scan task
        
        :param scanid: scan id number
        """
        if self.scanclient is None:
            self._connectscanserver()
        self.scanclient.abort(scanid)
    
    def pausescan(self, scanid):
        """Pause a scan task
        
        :param scanid: scan id number
        """
        if self.scanclient is None:
            self._connectscanserver()
        self.scanclient.pause(scanid)
    
    def resumescan(self, scanid):
        """Resume a scan task
        
        :param scanid: scan id number
        """
        if self.scanclient is None:
            self._connectscanserver()
        self.scanclient.resume(scanid)
    
    def getscandata(self, scanid, devicelist, dtype="table"):
        """Get scan results
        
        :param scanid:     scan id number
        :param devicelist: a list of all wished device, which is used for table format
        :param dtype:      returned data format, either "table" or "dict"
        """
    
        if self.scanclient is None:
            self._connectscanserver()
        data = self.scanclient.getData(scanid)
        
        if dtype=="table":
            # Create table
            return createTable(data, *devicelist)
        elif dtype=="dict":
            # return dictionary
            return data
        else:
            raise Exception("Unsupported return data type")
    
    # TODO add method to save scan data into database
    