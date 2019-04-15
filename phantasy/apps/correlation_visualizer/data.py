# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
from copy import deepcopy

from .data_templates import SHEET_TEMPLATES

try:
    basestring
except NameError:
    basestring = str


class ScanDataModel(object):
    """Standardize the scan output data.

    Parameters
    ----------
    data : array
        Numpy array with the shape of `(t, h, w)`, e.g.
        `t` is iteration number, `h` is shot number, `w` is scan dimension.
    """

    def __init__(self, data=None):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, z):
        """Every time data is updated, the shape, std array and mean array
        will be updated.
        """
        self._data = z
        self.t, self.h, self.w = self.shape
        self._std = self._data.std(axis=1)
        self._avg = self._data.mean(axis=1)

    @property
    def shape(self):
        return self._data.shape

    def get_xerr(self, **kws):
        ind = kws.get('ind', 0)  # x index
        skws = {k: v for k, v in kws.items() if k != 'ind'}
        if skws == {}:
            return self._std[:, ind]
        else:
            return self._data.std(axis=1, **skws)[:, ind]

    def get_yerr(self, **kws):
        ind = kws.get('ind', 1)  # y index
        skws = {k: v for k, v in kws.items() if k != 'ind'}
        if skws == {}:
            return self._std[:, ind]
        else:
            return self._data.std(axis=1, **skws)[:, ind]

    def get_xavg(self, **kws):
        ind = kws.get('ind', 0)  # x index
        return self._avg[:, ind]

    def get_yavg(self, **kws):
        ind = kws.get('ind', 1)  # y index
        return self._avg[:, ind]

    def get_avg(self):
        """Return array of averages, shape of (t, w).
        """
        return self._avg

    def get_err(self):
        """Return array of standard errors, shape of (t, w).
        """
        return self._std


class DataSheetBase(OrderedDict):
    def __init__(self, path=None, template=None):
        super(DataSheetBase, self).__init__()
        if template is not None:
            self.load_template(template)
        if isinstance(path, basestring):
            with open(path, "r") as fp:
                self.read(fp)

    def read(self, fp):
        """How to read the data sheet from file-like stream defined by *fp*.
        """
        raise NotImplementedError

    def write(self, path=None):
        """How to write the data sheet to file defined by *path*.
        """
        raise NotImplementedError

    def __deepcopy__(self, memo):
        s = DataSheetBase()
        s.update(deepcopy(list(self.items()), memo))
        return s

    def load_template(self, template):
        """Load template dict.

        Parameters
        ----------
        template : str
            Name of sheet template, all valid names could be returned from
            :method:`~DataSheetBase.template_names()`.
        """
        temp_sheet_dict = SHEET_TEMPLATES[template]
        self.update(temp_sheet_dict)

    @staticmethod
    def template_names():
        """Return list of all valid sheet template names.
        """
        return list(SHEET_TEMPLATES.keys())


class JSONDataSheet(DataSheetBase):
    """Save/Open JSON formated data sheet.
    """

    def __init__(self, path=None, template='Quad Scan'):
        super(JSONDataSheet, self).__init__(path)

        # load 'Quad Scan' template
        # self.load_template('Quad Scan')

    def read(self, fp):
        self.update(json.load(fp, object_pairs_hook=OrderedDict))

    def write(self, path):
        with open(path, 'w') as fp:
            json.dump(self, fp, indent=2, sort_keys=False)
