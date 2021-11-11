#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''One-dimensional scan client.
'''

import logging
import numpy as np
import scan

from .baseclient import BaseScanClient
from .datautil import ScanDataFactory

_LOGGER = logging.getLogger(__name__)


class ScanClient1D(BaseScanClient):
    """Scan task for scanning one device.

    Parameters
    ----------
    url : str
        URL of scan server, e.g. http://127.0.0.1:4810.

    Keyword Arguments
    -----------------
    name
    port
    host
    n_sample
    delay
    timeout
    tolerance
    scan_start
    scan_stop
    scan_step
    scan_num, prefer over scan_step.
    TODO: correct scan_num
    scan_range: prefer overall

    pv_scan_cnt: PV name of scan counter
    """

    def __init__(self, url=None, **kws):
        BaseScanClient.__init__(self, url=url, **kws)
        self._post_init(**kws)

    def _post_init(self, **kws):
        self.name = kws.get('name', None)
        self.host = kws.get('host', None)
        self.port = kws.get('port', None)
        self.n_sample = kws.get('n_sample', None)

        self.delay = kws.get('delay', None)
        self.timeout = kws.get('timeout', None)
        self.tolerance = kws.get('tolerance', None)
        self.scan_start = kws.get('scan_start', None)
        self.scan_stop = kws.get('scan_stop', None)
        self.scan_step = kws.get('scan_step', None)
        self.scan_num = kws.get('scan_num', None)

        self.PV_SCAN_CNT = str('loc://i(0)') if kws.get('pv_scan_cnt', None) is None else kws.get('pv_scan_cnt')
        self._scan_cmds = []
        self._scan_id = None
        self._pre_scan_cmds = None
        self._post_scan_cmds = None

    @property
    def pre_scan(self):
        """list: List of operations defined before scan routine."""
        return self._pre_scan_cmds

    @pre_scan.setter
    def pre_scan(self, cmds):
        self._pre_scan_cmds = cmds

    @property
    def post_scan(self):
        """list: List of operations defined after scan routine."""
        return self._post_scan_cmds

    @post_scan.setter
    def post_scan(self, cmds):
        self._post_scan_cmds = cmds

    @property
    def device_set(self):
        """str: Device name to be scanned, usually PV name of setpoint handle."""
        return self._device_set

    @device_set.setter
    def device_set(self, dev):
        self._device_set = dev

    @property
    def device_read(self):
        """str or bool: Device name to be scanned, usually PV name of readback
        handle. If True is assigned, value will be the same as *device_set*; if
        False is assigned, value will be False, which means the readback of
        *device_set* will not be checked when scan routine is processing; for
        other valid readback PV name, readback of *device_set* will be checked.
        """
        return self._device_read

    @device_read.setter
    def device_read(self, dev):
        if dev is False:
            self._device_read = False
        elif dev is True:
            self._device_read = True
        else:
            # check dev is readable()
            self._device_read = dev

    @property
    def log_devices(self):
        """list[str]: Interested device names to be read and logged when scan
        routine is processing, *device_read* is alway included in this list.
        """
        return self._log_devices

    @log_devices.setter
    def log_devices(self, dev):
        self._log_devices = dev

    @property
    def delay(self):
        """float: Delay time after every *device_set* updating, [sec],
        5.0 by default."""
        return self._delay

    @delay.setter
    def delay(self, t):
        if t is None:
            self._delay = 5.0
        elif isinstance(t, (int, float)):
            self._delay = float(t)
        else:
            raise TypeError("Input should be a float number.")

    @property
    def timeout(self):
        """float: Timeout for waiting device readback or completion, [sec],
        5.0 by default."""
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        if t is None:
            self._timeout = 5.0
        elif isinstance(t, (int, float)):
            self._timeout = float(t)
        else:
            raise TypeError("Input should be a float number.")

    @property
    def tolerance(self):
        """float: Numerical difference allowed between device set value and
        readback, 0.0 by default."""
        return self._tolerance

    @tolerance.setter
    def tolerance(self, t):
        if t is None:
            self._tolerance = 0.0
        elif isinstance(t, (int, float)):
            self._tolerance = float(t)
        else:
            raise TypeError("Input should be a float number.")

    @property
    def scan_start(self):
        """float: Initial value of *device_set*, 0.0 by default."""
        return self._scan_start

    @scan_start.setter
    def scan_start(self, x):
        if x is None:
            self._scan_start = 0.0
        elif isinstance(x, (int, float)):
            self._scan_start = float(x)
        else:
            raise TypeError("Input should be a float number.")
        try:
            self._setup_scan_params()
        except:
            pass

    @property
    def scan_stop(self):
        """float: Final value of *device_set*, 1.0 by default."""
        return self._scan_stop

    @scan_stop.setter
    def scan_stop(self, x):
        if x is None:
            self._scan_stop = 1.0
        elif isinstance(x, (int, float)):
            self._scan_stop = float(x)
        else:
            raise TypeError("Input should be a float number.")
        try:
            self._setup_scan_params()
        except:
            pass

    @property
    def scan_step(self):
        """float: Step size of *device_set*, 0.1 by default."""
        return self._scan_step

    @scan_step.setter
    def scan_step(self, x):
        if x is None:
            self._scan_step = 0.1
        elif isinstance(x, (int, float)):
            self._scan_step = float(x)
        else:
            raise TypeError("Input should be a float number.")
        self._scan_num = 1 + int((self._scan_stop - self._scan_start) / self._scan_step)
        _range_tmp = self._scan_start \
                     + self._scan_step * np.arange(0, self._scan_num)
        self._scan_range = _range_tmp[np.where(_range_tmp <= self._scan_stop)]
        self._scan_num = len(self._scan_range)

    @property
    def scan_num(self):
        """int: Total number of varied *device_set* value, 10 by defaut."""
        return self._scan_num

    @scan_num.setter
    def scan_num(self, n):
        if n is None:
            self._scan_num = 10
        elif isinstance(n, (int, float)):
            self._scan_num = int(n)
        else:
            raise TypeError("Input should be an integer.")
        try:
            self._setup_scan_params()
        except:
            pass

    @property
    def scan_range(self):
        """Array: Range of values for scan device, if non-equidistant array is
        assigned, *scan_step* is insignificant."""
        return self._scan_range

    @scan_range.setter
    def scan_range(self, arr):
        if isinstance(arr, (np.ndarray, list, tuple)):
            self._scan_range = np.array(arr)
        # if non-equidistant:
        # pass
        self._scan_start = self._scan_range.min()
        self._scan_stop = self._scan_range.max()
        self.scan_num = len(self._scan_range)

    @property
    def scan_commands(self):
        """list: List of scan commands."""
        return self._scan_cmds

    @scan_commands.setter
    def scan_commands(self, cmds):
        if isinstance(cmds, list):
            self._scan_cmds = cmds
        else:
            raise TypeError("Input should be a list.")

    @property
    def scan_id(self):
        """int: Scan task id number, generated after submit_scan()."""
        if self._scan_id is not None:
            return self._scan_id
        else:
            raise RuntimeError("Scan id is not assigned, invoke submit_scan() to generate.")

    def _setup_scan_params(self):
        self._scan_step = (self._scan_stop - self._scan_start) / (self._scan_num - 1)
        _range_tmp = self._scan_start \
                     + self._scan_step * np.arange(0, self._scan_num)
        self._scan_range = _range_tmp[np.where(_range_tmp <= self._scan_stop)]
        self._scan_num = len(self._scan_range)

    def build_scan(self, **kws):
        """Build scan commands.

        Keyword Arguments
        -----------------
        completion: True or False
        errhandler: None

        Returns
        -------
        ret : list
            List of scan commands.
        """
        completion = kws.get('completion', False)
        errhandler = kws.get('errhandler', None)

        cmds = list()
        pre_scan_cmds = self.pre_scan
        post_scan_cmds = self.post_scan

        # PRE SCAN
        if pre_scan_cmds is not None:
            [cmds.append(cmd) for cmd in pre_scan_cmds]

        # MAIN SCAN ROUTINES
        set_start_cmd = scan.Set(self.device_set, self.scan_start,
                                 completion=completion, readback=self.device_read,
                                 tolerance=self.tolerance, timeout=self.timeout,
                                 errhandler=errhandler)
        cmds.append(set_start_cmd)

        if self._n_sample == 1:
            scan_cmd = scan.Loop(
                self.device_set,
                self.scan_start, self.scan_stop, self.scan_step,
                body=[
                    scan.Delay(self.delay),
                    scan.Log(self.log_devices),
                ],
                completion=completion,
                readback=self.device_read,
                tolerance=self.tolerance,
                timeout=self.timeout,
                errhandler=errhandler,
            )
        else:  # n_sample > 1
            scan_cmd = scan.Loop(
                self.device_set,
                self.scan_start, self.scan_stop, self.scan_step,
                body=[
                    scan.Loop(
                        self.PV_SCAN_CNT, 1, self._n_sample, 1,
                        body=[
                            scan.Delay(self.delay),
                            scan.Log(self.log_devices + [self.PV_SCAN_CNT]),
                        ]
                    )
                ],
                completion=completion,
                readback=self.device_read,
                tolerance=self.tolerance,
                timeout=self.timeout,
                errhandler=errhandler,
            )
        cmds.append(scan_cmd)

        # POST SCAN
        if post_scan_cmds is not None:
            [cmds.append(cmd) for cmd in post_scan_cmds]

        self.scan_commands = cmds
        return cmds

    def submit_scan(self, wait=False):
        """Submit scan task to server, if *wait* if True, wait until scan task
        is done.

        Returns
        -------
        ret : int
            Id number of scan task.
        """
        scan_id = self.submit(self.scan_commands, name=self.name)
        self._scan_id = scan_id
        if wait:
            self.waitUntilDone(scan_id)
        return scan_id

    def simulate_scan(self):
        """Simulate scan routine, for reviewing scan task setup only.
        """
        sim = self.simulate(self.scan_commands)
        return sim.get('simulation')

    def get_data(self, scan_id=None, n=None):
        """Get scan result data.

        Parameters
        ----------
        scan_id : int
            ID of scan task, if not defined, try to get from current instance.
        n : int
            Counter of DAQ for every *device_set* updating, if not defined,
            try to get from current instance.

        Returns
        -------
        ret :
            ScanDataFactory object.
        """
        scan_id = scan_id if scan_id is not None else self.scan_id
        n = n if n is not None else self.n_sample
        data = self.getData(scan_id)
        return ScanDataFactory(data, n)

    def __repr__(self):
        try:
            retval = str(self.scanInfo(self.scan_id))
        except:
            retval = "{0} at {1}".format(
                'ScanClient1D',
                self.url
            )
        return retval

    def state(self):
        return self.scanInfo(self.scan_id).state
