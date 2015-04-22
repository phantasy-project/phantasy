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

from ... import machine as machines

def scan1d(device, start, stop, step, meas_dev, **kwds):
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
        - cleanup:   clean up this scan after finish, False by default
                     `False` to leave the scan on the server,
                     `True`  to delete the scan from the server.
        - delay:     delay in seconds, 5.0 by default.
        - samples:   how many point taken for each measurement device, 1 by default

    :param device:     Device name
    :param start:      Initial value
    :param stop:       Final value
    :param step:       Step size
    :param meas_dev:   Device to measure
     
    :return: a table with column following the device order: device, meas_dev
    :raise:
    
    """
    if machines.SCAN_SRV_URL is None or not re.match(r"https?://.*", machines.SCAN_SRV_URL, re.I):
        raise RuntimeError("machine is not properly initialized yet. Cannot find valid scan server url.")
    
    comments = kwds.get("title", "phyutil 1D Scan")
    orig = kwds.get("orig", None)
    readback = kwds.get("readback", False)
    tolerance = kwds.get("tolerance", 0.0)
    timeout = kwds.get("timeout", 5.0)
    ramping = kwds.get("ramping", False)
    cleanup = kwds.get("cleanup", False)
    delay = kwds.get("delay", 5.0)
    samples = int(kwds.get("samples", 1))
    compress = kwds.get("compress", "average")
    completion = True
    if readback:
        completion = False

    scan_cmds = []

    # prepare scan comments    
    scan_cmds.append(Comment(comments))
    
    # ramp to start point if needed
    if orig is not None and ramping:
        # slow ramping to the start point for scan
        if orig < start:
            scan_cmds.append(Loop(device, orig, start, abs(step), [Delay(delay)], completion=completion, 
                                  readback=readback, tolerance=tolerance, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
        else:
            scan_cmds.append(Loop(device, orig, start, -abs(step), [Delay(delay)], completion=completion, 
                                  readback=readback, tolerance=tolerance, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # confirm start point
    scan_cmds.append(Set(device, start, completion=completion, readback=readback, tolerance=tolerance, 
                         timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # real scan
    if samples == 1:
        scan_cmds.append(Loop(device, start, stop, step,
                              [
                               Delay(delay),
                               Log([device] + list(meas_dev))
                               ], 
                              completion=completion, 
                              readback=readback, tolerance=tolerance, 
                              timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    else:
        scan_cmds.append(Loop(device, start, stop, step,
                              [Loop('loc://i(0)', 1, samples, 1, 
                                    [Delay(delay), Log([device] + list(meas_dev))])
                               ],
                              completion=completion, 
                              readback=False, 
                              timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # ramp back to original setting
    if  orig is not None and ramping:
        # slow ramping to the start point for scan
        if stop < orig:
            scan_cmds.append(Loop(device, stop, orig, abs(step), [Delay(delay)], completion=completion, 
                                  readback=readback, tolerance=tolerance,
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
        else:
            scan_cmds.append(Loop(device, stop, orig, -abs(step), [Delay(delay)], completion=completion,
                                  readback=readback, tolerance=tolerance, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # confirm original setting
    scan_cmds.append(Set(device, orig, completion=completion, readback=readback, tolerance=tolerance, 
                         timeout=timeout, errhandler='OnErrorRetryThenAbort'))

    ss_host = urlparse(machines.SCAN_SRV_URL)
    if ss_host.port is None:
        client = ScanClient(ss_host.hostname)
    else:
        client = ScanClient(ss_host.hostname, ss_host.port)
          
    scid = client.submit(scan_cmds, name=comments)
    client.waitUntilDone(scid)
    data = client.getData(scid)
    
    # Create table
    if isinstance(meas_dev, (list, tuple)):
        table = createTable(data, device, *meas_dev)
    else:
        table = createTable(data, device, meas_dev)
    
    if cleanup:
        # clean up this scan task
        client.delete(scid)
    
    return table

def scan2d(device1, device2, meas_dev, **kwds):
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
        - cleanup:   clean up this scan after finish, False by default
                     `False` to leave the scan on the server,
                     `True`  to delete the scan from the server.
        - delay:     delay in seconds, 5.0 by default.
        - samples:   how many point taken for each measurement device, 1 by default

    :param device1:    first dimension information with format [Device name, start, stop, step]
    :param device2:    second dimension information with format [Device name, start, stop, step]
    :param meas_dev:   Device to measure
     
    :return: a table with column following the device order: device, meas_dev
    :raise:
    
    """
    if machines.SCAN_SRV_URL is None or not re.match(r"https?://.*", machines.SCAN_SRV_URL, re.I):
        raise RuntimeError("machine is not properly initialized yet. Cannot find valid scan server url.")
    if not isinstance(device1, (list, tuple)) or len(device1) != 4 or \
        not isinstance(device2, (list, tuple)) or len(device2) != 4:
        raise RuntimeError("Scan parameters are not sufficient.")
    
    comments = kwds.get("title", "phyutil 2D Scan")
    orig1 = kwds.get("orig1", None)
    readback1 = kwds.get("readback1", False)
    tolerance1 = kwds.get("tolerance1", 0.0)
    orig2 = kwds.get("orig2", None)
    readback2 = kwds.get("readback2", False)
    tolerance2 = kwds.get("tolerance2", 0.0)
    timeout = kwds.get("timeout", 5.0)
    ramping = kwds.get("ramping", False)
    cleanup = kwds.get("cleanup", False)
    delay = kwds.get("delay", 5.0)
    samples = int(kwds.get("samples", 1))
    compress = kwds.get("compress", "average")
    completion1 = True
    completion2 = True
    if readback1:
        completion1 = False
    if readback2:
        completion2 = False

    scan_cmds = []

    # prepare scan comments    
    scan_cmds.append(Comment(comments))
    
    # ramp to start point if needed
    if orig1 is not None and ramping:
        # slow ramping to the start point for scan
        if orig1 < device1[1]:
            scan_cmds.append(Loop(device1[0], orig1, device1[1], abs(device1[3]), [Delay(delay)], 
                                  completion=completion1, 
                                  readback=readback1, tolerance=tolerance1, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
        else:
            scan_cmds.append(Loop(device1[0], orig1, device1[1], -abs(device1[3]), [Delay(delay)],
                                  completion=completion1, 
                                  readback=readback1, tolerance=tolerance1, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    # ramp to start point if needed
    if orig2 is not None and ramping:
        # slow ramping to the start point for scan
        if orig2 < device2[1]:
            scan_cmds.append(Loop(device2[0], orig2, device2[1], abs(device2[3]), [Delay(delay)], 
                                  completion=completion2, 
                                  readback=readback2, tolerance=tolerance2, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
        else:
            scan_cmds.append(Loop(device2[0], orig2, device2[1], -abs(device2[3]), [Delay(delay)],
                                  completion=completion2, 
                                  readback=readback2, tolerance=tolerance2, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # confirm start point
    scan_cmds.append(Set(device1[0], device1[1], completion=completion1, readback=readback1, tolerance=tolerance1, 
                         timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    scan_cmds.append(Set(device2[0], device2[1], completion=completion2, readback=readback2, tolerance=tolerance2, 
                         timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # real scan
    if samples == 1:
        scan_cmds.append(Loop(device1[0], device1[1], device1[2], device1[3],
                              [Loop(device2[0], device2[1], device2[2], device2[3], 
                                    [Delay(delay),
                                     Log([device1[0], device2[0]] + list(meas_dev))
                                     ],
                                    completion=completion2, 
                                    readback=readback2, tolerance=tolerance2,
                                    ),
                               ], 
                              completion=completion1, 
                              readback=readback1, tolerance=tolerance1, 
                              timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    else:
        scan_cmds.append(Loop(device1[0], device1[1], device1[2], device1[3],
                              [Loop(device2[0], device2[1], device2[2], device2[3], 
                                    [Loop('loc://i(0)', 1, samples, 1, 
                                          [Delay(delay), Log([device1[0], device2[0]] + list(meas_dev))])
                                     ],
                                    completion=completion2, 
                                    readback=readback2, tolerance=tolerance2,
                                    ),
                               ], 
                              completion=completion1, 
                              readback=readback1, tolerance=tolerance1, 
                              timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # ramp back to original setting
    if orig1 is not None and ramping:
        # slow ramping to the start point for scan
        if device1[2] < orig1:
            scan_cmds.append(Loop(device1[0], device1[2], orig1, abs(device1[3]), [Delay(delay)], 
                                  completion=completion1, 
                                  readback=readback1, tolerance=tolerance1, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
        else:
            scan_cmds.append(Loop(device1[0], device1[2], orig1, -abs(device1[3]), [Delay(delay)],
                                  completion=completion1, 
                                  readback=readback1, tolerance=tolerance1, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    
    # ramp back to original setting
    if orig2 is not None and ramping:
        # slow ramping to the start point for scan
        if device2[2] < orig2:
            scan_cmds.append(Loop(device2[0], device2[2], orig2, abs(device2[3]), [Delay(delay)], 
                                  completion=completion2, 
                                  readback=readback2, tolerance=tolerance2, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))
        else:
            scan_cmds.append(Loop(device2[0], device2[2], orig2, -abs(device2[3]), [Delay(delay)],
                                  completion=completion2, 
                                  readback=readback2, tolerance=tolerance2, 
                                  timeout=timeout, errhandler='OnErrorRetryThenAbort'))    
    # confirm original setting
    scan_cmds.append(Set(device1[0], orig1, completion=completion1, readback=readback1, tolerance=tolerance1, 
                         timeout=timeout, errhandler='OnErrorRetryThenAbort'))
    scan_cmds.append(Set(device2[0], orig2, completion=completion2, readback=readback2, tolerance=tolerance2, 
                         timeout=timeout, errhandler='OnErrorRetryThenAbort'))

    ss_host = urlparse(machines.SCAN_SRV_URL)
    if ss_host.port is None:
        client = ScanClient(ss_host.hostname)
    else:
        client = ScanClient(ss_host.hostname, ss_host.port)
          
    scid = client.submit(scan_cmds, name=comments)
    client.waitUntilDone(scid)
    data = client.getData(scid)
    
    # Create table
    if isinstance(meas_dev, (list, tuple)):
        table = createTable(data, device1[0], device2[0], *meas_dev)
    else:
        table = createTable(data, device1[0], device2[0], meas_dev)
    
    if cleanup:
        # clean up this scan task
        client.delete(scid)
    
    return table