#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests.adapters import HTTPAdapter
import requests
from epics import PV
from io import BytesIO


class DataSource(object):
    """Data interface for image.

    Parameters
    ----------
    url : str
        PV name of waveform record type, or web url for image data.
    protocol : str
        Currently, only support CA or HTTP.
    """

    def __init__(self, url, protocol="CA"):
        self._url = url
        self._protocol = protocol
        self._ds = self.init_source(url, protocol)

    def init_source(self, url, protocol):
        # initialize data source, e.g. create PV or connection
        if protocol == "CA":
            ds = PV(url)
        elif protocol == "HTTP":
            ds = requests.Session()
            ds.mount(url, CameraAdapter(max_retries=3))
        return ds

    def get(self):
        if self._protocol == "CA":
            return self._fetch_data_from_ca()
        elif self._protocol == "HTTP":
            return self._fetch_data_from_http()

    def _fetch_data_from_ca(self):
        return self._ds.get()

    def _fetch_data_from_http(self):
        content = self._ds.get(self._url).content
        return BytesIO(content)


class CameraAdapter(HTTPAdapter):
    def __init__(self, **kws):
        super(self.__class__, self).__init__(**kws)


if __name__ == "__main__":
    # ds = DataSource("EMS:ArrayData")
    # print(ds.get())

    ds = DataSource("http://diag-cam.ftc:8000/MJPG.jpg", protocol='HTTP')
    data = ds.get()

    import matplotlib.pyplot as plt
    from PIL import Image
    img = Image.open(data)
    plt.imshow(img)
    plt.show()
