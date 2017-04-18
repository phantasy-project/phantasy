#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create high-level lattice object from machine configuration files.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
import re
import numpy as np
import shelve
import tempfile
import time
from fnmatch import fnmatch
from math import log10
from collections import OrderedDict
from datetime import datetime

from .element import AbstractElement
from .element import CaElement
from .impact import LatticeFactory as ImpactLatticeFactory
from .impact import run_lattice as run_impact_lattice
from .flame import FlameLatticeFactory
from phantasy.library.layout import Layout
from phantasy.library.parser import Configuration
from phantasy.library.settings import Settings
from phantasy.library.settings import build_flame_settings
from phantasy.library.pv import caget
from phantasy.library.pv import caput
from phantasy.library.misc import parse_dt
from phantasy.library.model import MachineStates
from phantasy.library.model import ModelFlame
from phantasy.library.layout import CavityElement
from flame import Machine


_LOGGER = logging.getLogger(__name__)

class Lattice(object):
    """Machine high-level lattice object, all elements inside this lattice
    has a unique name.
    
    Parameters
    ----------
    name : str
        Lattice name.

    Keyword Arguments
    -----------------
    s_begin : float
        Start position along beam trajectory, [m].
    s_end : float
        End position along beam trajectory, [m].
    mname : str
        Name of loaded machine, from which lattice itself is loaded.
    mpath : str
        Path name of machine configurations.
    mconf : obj
        Machine configuration object.
    mtype : int
        Machine type, 0 for linear (default), 1 for a ring.
    source : str
        Source of PV data, URL of channel finder service, file name of SQLite
        database or csv spreadsheet.
    length : float
        Total length of lattice, if 'mtype' is 1, refers to circumference.
    model : str
        Model type (case insensitive), or code name for simulation, 'FLAME'
        or 'IMPACT', the former is the default one.
    data_dir: str
        Path of directory to host data generated from model, including input
        lattice files, output files and other related files, if not defined,
        random folder will be created in system temporary directory,
        e.g.'/tmp/model_hGe1sq'.
    config :
        Lattice configuration object.
    layout :
        Lattice layout object.
    settings :
        Lattice settings object.
    model_factory :
        Lattice factory object for online model.
    trace : str
        If 'on', history of PV set actions could be traced back, or ('off')
        set action cannot be reverted, by default, trace feature is on.
    

    - *tune* [nux, nuy], mainly for circular machine
    - *chromaticity* [cx, cy] mainly for circular machine
    - *ormdata* orbit response matrix data

    Note
    ----
    :class:`~phantasy.library.operation.create_lattice` method could be used
    set up lattice created by this class by provided information like: PV data,
    lattice layout, configuration and settings, etc.

    See Also
    --------
    :class:`~phantasy.library.operation.create_lattice`
    """
    # ignore those "element" when construct the lattice object
    def __init__(self, name, **kws):
        self.name = name
        self.source = kws.get('source', None)
        self.s_begin = kws.get('s_begin', None)
        self.s_end = kws.get('s_end', None)
        self.mname = kws.get('mname', None)
        self.mpath = kws.get('mpath', None)
        self.mconf = kws.get('mconf', None)
        self.mtype = kws.get('mtype', None)
        self.length = kws.get('length', None)
        self.model = kws.get('model', None)
        self.data_dir = kws.get('data_dir', None)
        self.layout = kws.get('layout', None)
        self.config = kws.get('config', None)
        self.settings = kws.get('settings', None)
        self.model_factory = kws.get('model_factory', None)

        self._viewer_settings = OrderedDict()
        self._trace_history = None
        self.trace = kws.get('trace', None)


        ## clean up the following parameters
        self._twiss = None
        # group name and its element
        self._group = {}
        # guaranteed in the order of s.
        self._elements = []
        # data set
        self.mode = ''
        self.tune = [None, None]
        self.chromaticity = [None, None]
        self.ormdata = None
        self.isring = bool(self.mtype)
        self.Ek = None
        self.arpvs = None
        self.latticemodelmap = None

    @property
    def trace(self):
        """str: Keep/revert history feature flag for PV set actions."""
        return self._trace

    @trace.setter
    def trace(self, trace):
        if trace is None or trace == 'on':
            self._trace = 'on'
            if self._trace_history is None:
                self._trace_history = []
        else:
            self._trace = 'off'
            if self._trace_history is not None:
                self._trace_history = None

    @property
    def config(self):
        """Obj: Lattice configuration object."""
        return self._config

    @config.setter
    def config(self, config):
        if config is not None and isinstance(config, Configuration):
            self._config = config
        else:
            self._config = self._get_default_config()

    @property
    def layout(self):
        """Obj: Accelerator layout object."""
        return self._layout
    
    @layout.setter
    def layout(self, layout):
        if layout is not None and isinstance(layout, Layout):
            self._layout = layout
        else:
            self._layout = self._get_default_layout()

    @property
    def settings(self):
        """Obj: Lattice settings object."""
        return self._settings

    @settings.setter
    def settings(self, settings):
        if settings is not None and isinstance(settings, Settings):
            self._settings = settings
        else:
            self._settings = self._get_default_settings()

    @property
    def model_factory(self):
        """Obj: Lattice factory of defined model type."""
        return self._model_factory

    @model_factory.setter
    def model_factory(self, mf):
        if mf is None:
            self._model_factory = self._set_model_factory()
        elif self.model == "FLAME" and isinstance(mf, FlameLatticeFactory):
            self._model_factory = mf
        elif self.model == "IMPACT" and isinstance(mf, ImpactLatticeFactory):
            self._model_factory = mf
        else:
            raise TypeError("Wrong input model factory.")
            
    @property
    def s_begin(self):
        """float: Start position along beam trajectory, [m]."""
        return self._s_begin

    @s_begin.setter
    def s_begin(self, s):
        if s is None:
            self._s_begin = 0.0
        else:
            self._s_begin= s

    @property
    def s_end(self):
        """float: End position along beam trajectory, [m]."""
        return self._s_end

    @s_end.setter
    def s_end(self, s):
        if s is None:
            self._s_end = sys.float_info.max
        else:
            self._s_end = s 

    @property
    def mname(self):
        """str: Name of loaded machine, from which lattice itself is loaded."""
        return self._mname

    @mname.setter
    def mname(self, name):
        if name is None:
            self._mname = ''
        else:
            self._mname = name

    @property
    def mpath(self):
        """str: Path name of machine configurations."""
        return self._mpath

    @mpath.setter
    def mpath(self, path):
        if path is None:
            self._mpath = ''
        else:
            self._mpath = path
    
    @property
    def mconf(self):
        """Obj: Machine configuration object."""
        return self._mconf

    @mconf.setter
    def mconf(self, config):
        if isinstance(config, Configuration):
            self._mconf = config
        else:
            self._mconf = None

    @property
    def mtype(self):
        """int: Machine type, linear (0) or circular (1)."""
        return self._mtype
    
    @mtype.setter
    def mtype(self, i):
        if i is None:
            self._mtype = 0
        else:
            self._mtype = i

    @property
    def source(self):
        """str: Source of PV data."""
        return self._source
    
    @source.setter
    def source(self, src):
        if src is None:
            self._source = None
        else:
            self._source = src

    @property
    def length(self):
        """Total length of lattice, if 'mtype' is 1, refers to circumference."""
        return self._length

    @length.setter
    def length(self, s):
        if s is None:
            self._length = 0.0
        else:
            self._length = s

    @property
    def model(self):
        """str: Simulation code name to simulate online model type."""
        return self._model
    
    @model.setter
    def model(self, code):
        if code is None:
            self._model = "FLAME"
        else:
            self._model = code.upper()

    @property
    def data_dir(self):
        """str: Path of directory to host data generated from model."""
        return self._data_dir

    @data_dir.setter
    def data_dir(self, path):
        if path is None:
            systmp = '/tmp'
            self._data_dir = tempfile.mkdtemp(prefix='model_', dir=systmp)
        else:
            self._data_dir = path

    def _get_default_config(self):
        if self.mconf.has_option(self.name, "config_file"):
            configfile = self.mconf.getabspath(self.name, "config_file")
            config = Configuration(configfile)
        else:
            config = None
        return config

    def _get_default_settings(self):
        if self.mconf.has_option(self.name, "settings_file"):
            settingfile = self.mconf.getabspath(self.name, "settings_file")
            settings = Settings(settingfile)
        else:
            settings = None
        return settings

    def _get_default_layout(self):
        if self.mconf.has_option(self.name, "layout_file"):
            layoutfile = self.mconf.getabspath(self.name, "layout_file")
            layout = build_layout(layoutfile)
        else:
            layout = None
        return layout
    
    def _set_model_factory(self):
        if self.model == "IMPACT":
            mf = ImpactLatticeFactory(self.layout, config=self.config, settings=self.settings)
        elif self.model == "FLAME":
            mf = FlameLatticeFactory(self.layout, config=self.config, settings=self.settings)
        else:
            raise RuntimeError("Lattice: Model '{}' not supported".format(self.model))
        return mf

    def set(self, elem, value, field=None, **kws):
        """Set the value of a lattice element field, if element only has one
        field, parameter *field* is optional, or *field* must be specified.
        
        Parameters
        ----------
        elem : str or CaElement object 
            Element name string or CaElement object.
        value :
            Value of the field, type should be valid w.r.t *field*.
        field : str
            Field name (case insensitive) of element to be assigned, optional
            if element has only one field, *value* will be assigned to.

        Keyword Arguments
        -----------------
        source : str
            Three options available: 'all', 'control' and 'model', by default
            'all', i.e. update both 'control' and 'model' environment.

        Returns
        -------
        ret :
            None if failed, or 0.
        """
        elems = self.getElementList(elem)
        if len(elems) != 1:
            raise RuntimeError("Lattice: Multiple elements found with the specified name.")
        _elem = elems[0]

        all_fields = _elem.fields()
        
        if len(all_fields) > 1:
            if field is None:
                print("Please specify field from [{}]".format(','.join(all_fields)))
                return None
            elif field not in all_fields:
                print("Wrong field.")
                return None
        elif len(all_fields) == 1:
            field = all_fields[0]
        else:
            print("Element has not defined field.")
            return None
        
        source = kws.get('source', 'all')
        if source == 'all':
            self._set_control_field(_elem, field, value)
            self._set_model_field(_elem, field, value)
        elif source == 'control':
            self._set_control_field(_elem, field, value)
        elif source == 'model':
            self._set_model_field(_elem, field, value)
        else:
            raise RuntimeError("Invalid source.")

        return 0

    def _set_control_field(self, elem, field, value):
        """Set value to element field onto control environment.
        """
        pv = elem.pv(field=field, handle='setpoint')[0]
        value0 = caget(pv)
        if elem.family == "CAV" and field == 'PHA':
            value = _normalize_phase(value)
        caput(pv, value)
        self._log_trace('control', element=elem.name, 
                field=field, value0=value0, value=value, pv=pv)

    def _set_model_field(self, elem, field, value):
        """Set value to element field.
        """
        if isinstance(elem, CaElement):
            elem_name = elem.name
        else:
            elem_name = elem
        if elem_name not in self.settings:
            _LOGGER.warn("Element:{} to set not found in lattice model.".format(elem_name))
        elif field not in self.settings[elem_name]:
            _LOGGER.warn("Field: {} to set not found in element: {}.".format(field, elem_name))
        else:
            value0 = self.settings[elem_name][field]
            self.settings[elem_name][field] = value
            self.model_factory.settings[elem_name][field] = value
            _LOGGER.debug("Updated field: {0:s} of element: {1:s} with value: {2:f}".format(field, elem_name, value))
        self._log_trace('model', element=elem_name, field=field, value=value, value0=value0)

    def _log_trace(self, type, **kws):
        """Add set log entry into trace history.

        Parameters
        ----------
        type : str
            Set type according to environment source, 'control' or 'model'.
        timestamp
        element
        field
        pv
        value
        value0
        """
        if self._trace == 'on':
            name = kws.get('element')
            field = kws.get('field')
            value = kws.get('value')
            value0 = kws.get('value0')
            if type == 'control':
                pv = kws.get('pv')
                log_entry = OrderedDict((
                            ('timestamp', time.time()),
                            ('type', type),
                            ('element', name),
                            ('field', field),
                            ('value0', value0),
                            ('value', value),
                            ('pv', pv)))
            elif type == 'model':
                log_entry = OrderedDict((
                            ('timestamp', time.time()),
                            ('type', type),
                            ('element', name),
                            ('field', field),
                            ('value0', value0),
                            ('value', value)))

            self._trace_history.append(log_entry)
        else:
            pass

    def get(self, elem, field=None, **kws):
        """Get the value of a lattice element field.

        Parameters
        ----------
        elem : str or CaElement object
            Element name string or CaElement object.
        field : str
            Field name (case insensitive) of element, if not defined, all
            field names will be selected.

        Keyword Arguments
        -----------------
        source : str
            Two options available: 'control' and 'model', by default 'control'
            i.e. only get from 'control' environment.
        mstate : bool
            If True, return MachineStates instance, False by default, only
            valid for viewer elements and ``source='model'``.

        Note
        ----
        If ``source`` is defined as ``'model'``, settings will be retrieved
        from model environment, there are two categories: one is devices that
        accept new values settings, e.g. corrector, cavity, etc., the other is
        devices that only can show readings, e.g. BPM, PM, etc. (so-called
        *viewer elements*). For *viewer elements*, ``MachineStates`` could be
        got after ``run()``, for flame model.

        Returns
        -------
        ret : dict 
            Field value, {field: value}.
        """
        elems = self.getElementList(elem)
        if len(elems) != 1:
            raise RuntimeError("Lattice: Multiple elements found with the specified name.")
        _elem = elems[0]
        all_fields = _elem.fields()
        if field is None:
            field = all_fields
        elif field not in all_fields:
            print("Wrong field.")
            return None

        source = kws.get('source', 'control')

        if source == 'control':
            retval = self._get_control_field(_elem, field)
        elif source == 'model':
            mstate_flag = kws.get('mstate', False)
            retval = self._get_model_field(_elem, field, mstate=mstate_flag)
        else:
            raise RuntimeError("Invalid source.")

        return retval

    def _get_control_field(self, elem, field):
        """Get field value(s) from element, source is control environment.
        """
        if not isinstance(field, (list, tuple)):
            field = field,
        pv = {f:elem.pv(field=f, handle='readback') for f in field}
        return {k:caget(v)[0] for k,v in pv.iteritems()}

    def _get_model_field(self, elem, field, **kws):
        """Get field value(s) from elment.

        Keyword Arguments
        -----------------
        mstate : bool
            If True, return MachineStates instance, False by default.
        """
        if not isinstance(field, (list, tuple)):
            field = field,
        elem_name = elem.name
        if self._is_viewer(elem):
            _settings = self._viewer_settings
        else:
            _settings = self.settings
        retval = {k:v for k,v in _settings[elem_name].items() if k in field}
        if kws.get('mstate', False) and self._is_viewer(elem):
            retval['mstate'] = self._viewer_settings[elem_name]['mstate']
        return retval

    def trace_history(self, rtype='human', **kws):
        """Inspect trace history of Lattice set actions, return data type with
        human friendly or raw format.

        Parameters
        ----------
        rtype : str
            'human' or 'raw', default option 'human' will return formated
            human readable strings, could be printed out to streams;
            'raw' will return history entries meeting filters defined by
            keyword arguments.

        Note
        ----
        Data structure of every traced log entry:

        +---------------+--------------------------------------+
        |  key name     |   value example                      |
        +---------------+--------------------------------------+
        | *timestamp*   | ``1485275869``                       |
        +---------------+--------------------------------------+
        | *type*        | ``control``                          |  
        +---------------+--------------------------------------+
        | *element*     | ``LS1_CA01:CAV1_D1127``              |
        +---------------+--------------------------------------+
        | *field*       | ``PHA``                              |
        +---------------+--------------------------------------+
        | *value*       | ``30``                               |
        +---------------+--------------------------------------+
        | *value0*      | ``325``                              |
        +---------------+--------------------------------------+
        | *pv*          | ``V_1:LS1_CA01:CAV1_D1127:PHA_CSET`` |
        +---------------+--------------------------------------+

        Keyword Arguments
        -----------------
        element : str
            Unix shell pattern of element name.
        pv : str
            Unix shell pattern of element pv name, only valid for 'control'
            type entry.
        field : str
            Unix shell pattern of element field name.
        type : str
            Log entry type: 'control' or 'model', could be Unix shell pattern.
        value : number or list of numbers
            From which, lower and upper limit values will be extracted.
        """
        if self._trace_history is None:
            return None

        _history = self._filter_trace(self._trace_history, **kws)

        if rtype == 'human':
            retval = []
            for log_entry in _history:
                type = log_entry['type']
                time = log_entry['timestamp']
                value = log_entry['value']
                value0 = log_entry['value0']
                if type == 'control':
                    pv = log_entry['pv']
                    log_str = "{time} [{type:^7s}] set {pv:<34s} with {value:>16.6e} which was {value0:>16.6e}".format(
                            time=datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'),
                            type=type, pv=pv, value=value, value0=value0)
                elif type == 'model':
                    name = log_entry['element']
                    field = log_entry['field']
                    log_str = "{time} [{type:^7s}] set {name:<34s} with {value:>16.6e} which was {value0:>16.6e}".format(
                            time=datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'),
                            type=type, name="{0}:{1}".format(name,field), value=value, value0=value0)
                retval.append(log_str)
                print(log_str)
            return "\n".join(retval)
        else:
            return _history

    @staticmethod
    def _filter_trace(data, **kws):
        """Apply filters on trace history data, return list of valid entries.
        """
        # filters
        elem_name = kws.get('element', '*')
        pv_name = kws.get('pv', None)
        entry_type = kws.get('type', '*')
        field_name = kws.get('field', '*')
        value = kws.get('value', None)
        if value is not None:
            if isinstance(value, (int, float, long)):
                value = [value]
            elif not isinstance(value, (list, tuple)):
                raise RuntimeError("Invalid value argument.")
                return []
            val_min, val_max = min(value), max(value)
        else:
            val_min, val_max = -1e10, 1e10

        retval = []
        for d in data:
            _elem_name = d.get('element')
            _pv_name = d.get('pv', None)
            _entry_type = d.get('type')
            _field_name = d.get('field')
            _value = d.get('value')
            if Lattice._fnmatch(_pv_name, pv_name) and fnmatch(_elem_name, elem_name) \
                and fnmatch(_entry_type, entry_type) \
                and fnmatch(_field_name, field_name) \
                and val_min <= _value <= val_max:
                    retval.append(d)
        
        return retval

    @staticmethod
    def _fnmatch(name, pattern):
        if pattern == None: # pv pattern is not defined
            return True
        else: # pv pattern is defined
            if name is None:
                return False
            else:
                return fnmatch(name, pattern)

    def roll_back(self, setting=None, type=None, retroaction=None):
        """Roll back PV setpoint by providing *setting* or log entries from
        trace history, which indicating high-level lattice object to proceed
        some set action to roll it back into previous states.

        Parameters
        ----------
        setting : dict of list of dict
            Element setting, could be trace_history entry, if not defined,
            use the last entry with the type of 'control'
        type : str
            Type of environment to roll back, 'control' or 'model', 'control'
            by default.
        retroaction : time
            Timestamp of the trace history, dating back to *retroaction*,
            machine state should roll back to be.

        Note
        ----
        Possible input of *setting* parameter:
        - (Default) Last trace history entry.
        - Trace history entry or list of entries;

        Note
        ----
        About *retroaction* parameter, following input types will be supported:
        - Absolute timestamp indicated by a float number, i.e. time in seconds
          since Epoch: entries with logging timestamp newer (bigger) than
          *retroaction* will be rolled back;
        - Relative timestamp w.r.t. current time available units: *years*,
          *months*, *weeks*, *days*, *hours*, *minutes*, *seconds*,
          *microseconds*, and some unit alias: *year*, *month*, *week*, *day*,
          *hour*, *minute*, *second*, *microsecond*, *mins*, *secs*, *msecs*,
          *min*, *sec*, *msec*, could be linked by string 'and' or ',',
          ended with 'ago', e.g. '5 mins ago', '1 hour and 30 mins ago'.
        
        Warning
        -------
        If valid *retroaction* parameter is defined, *setting* will be
        disregarded.

        See Also
        --------
        trace_history : Log history of set actions.
        """
        type = 'control' if type is None else type
        _history = self.trace_history(rtype='raw', type=type)
        if setting is None:
            if _history != []:
                setting = _history[-1]

        if retroaction is not None:
            setting = self._get_retroactive_trace_history(_history, retroaction)
        
        if not isinstance(setting, (list, tuple)):
            setting = setting,

        for entry in setting:
            _elem_name = entry.get('element')
            _entry_type = entry.get('type')
            _field_name = entry.get('field')
            _value = entry.get('value0')
            _pv_name = entry.get('pv', None)
            if _pv_name is None:
                self._set_model_field(_elem_name, _field_name, _value)
            else:
                _value0 = caget(_pv_name)
                caput(_pv_name, _value)
                self._log_trace('control', element=_elem_name, field=_field_name,
                                value=_value, value0=_value0, pv=_pv_name)

    def _get_retroactive_trace_history(self, trace_history_data, retroaction):
        data = trace_history_data
        if isinstance(retroaction, (float, int, long)):
            # absolute time
            retval = [_entry for _entry in data if _entry['timestamp'] >= retroaction]
        else:
            # relative time
            retro_datetime = parse_dt(retroaction, datetime.now(), epoch=True)
            retval = [_entry for _entry in data if _entry['timestamp'] >= retro_datetime]
        return retval

    def update_model_settings(self, model_lattice, **kws):
        """Update model lattice settings with external lattice file, prefer
        keyword argument *sdict* or *sjson* if anyone is defined.

        Parameters
        ----------
        model_lattice : path
            External model lattice file.
        
        Keyword Arguments
        -----------------
        sdict : dict
            Dict of model lattice settings.
        sjson : path
            JSON file of model lattice settings.
        """
        sdict = kws.get('sdict', None)
        sjson = kws.get('sjson', None)
        if isinstance(sdict, dict):
            settings = sdict
        elif sjson is not None:
            with open(sjson, 'r') as fp:
                settings = json.load(fp)
        else:
            # read settings from lattice file
            if self.model == 'FLAME':
                settings = build_flame_settings(model_lattice)
            elif self.model == 'IMPACT':
                raise NotImplementedError

        # apply settings
        for e_name, e_setting in settings.iteritems():
            if e_name in self.settings:
                for field,value in e_setting.iteritems():
                        self._set_model_field(e_name, field, value)
                        _LOGGER.debug("Update model: {e}:{f} to be {v}.".format(e=e_name, f=field, v=value))
            else:
                _LOGGER.debug('Model settings does not have field: {e}:{f}.'.format(e=e_name, f=field))

    def sync_settings(self, data_source=None):
        """Synchronize lattice settings between model and control environment.

        Parameters
        ----------
        data_source : str
            Data source of synchronization, if 'model' is defined, will update 
            data of control environment with data from 'model'; if 'control'
            is defined, model data will be synchronized; *data_source* is
            'control' by default.
        """
        data_source = 'control' if data_source is None else data_source
        
        if data_source == 'control':
            _LOGGER.info("Sync settings from 'control' to 'model'.")
            model_settings = self.settings
            for elem in self.getElementList('*'):
                if elem.name in model_settings:
                    if not self._skip_elements(elem.name):
                        for field,value in self.get(elem=elem, source='control').iteritems():
                            if field in model_settings[elem.name]:
                                self._set_model_field(elem, field, value)
                                # model_settings[elem.name][field] = value
                                # _LOGGER.debug("Update model: {e}:{f} to be {v}.".format(e=elem.name, f=field, v=value))
                            else:
                                _LOGGER.debug('Model settings does not have field: {e}:{f}.'.format(e=elem.name, f=field))
                else:
                    _LOGGER.debug('Model settings does not have element: {e}.'.format(e=elem.name))
        elif data_source == 'model':
            _LOGGER.info("Sync settings from 'model' to 'control'.")
            for e_name, e_setting in self.settings.iteritems():
                elem = self.getElementList(e_name)
                if elem == []:
                    _LOGGER.debug('Control settings does not have element {0}.'.format(e_name))
                    continue
                for field,value in e_setting.iteritems():
                    if not self._skip_elements(elem[0].name):
                        if field in elem[0].fields():
                            self._set_control_field(elem[0], field, value)

    def _skip_elements(self, name):
        """Presently, element should skip: SEXT
        """
        SKIP_TYPES = ['SEXT']
        elements = self.model_factory._accel.elements
        for e in elements:
            if e.name == name:
                return e.ETYPE in SKIP_TYPES

    def run(self):
        """Run mchine with defined model, e.g. 'FLAME' or 'IMPACT',
        update model settings, but not control settings.
        
        Returns
        -------
        ret : tuple
            tuple of (path, model), path of the model data directory and model
            object.
        """
        if self.model == "IMPACT":
            lat = self._latticeFactory.build()
            config = self._latticeFactory.config
            work_dir = run_impact_lattice(lat, config=config, work_dir=self.data_dir)
            if self.latticemodelmap is None:
                self.createLatticeModelMap(os.path.join(work_dir, "model.map"))
            return work_dir, None
        elif self.model == "FLAME":
            lat = self.model_factory.build()
            _, latpath = tempfile.mkstemp(prefix='model_', suffix='.lat', dir=self.data_dir)
            with open(latpath, 'w') as f:
                lat.write(f)
            fm = self._flame_model(latconf=lat.conf())
            return latpath, fm
        else:
            raise RuntimeError("Lattice: Simulation code '{}' not supported".format(self.model))
    
    def _flame_model(self, **kws):
        """Create a new flame model
        """
        latconf = kws.get('latconf', None)
        latfile = kws.get('latfile', None)
        
        if latconf is not None:
            m = Machine(latconf)
        elif latfile is not None:
            m = Machine(open(latfile, 'r'))
        ms = MachineStates(machine=m)
        fm = ModelFlame()
        fm.mstates, fm.machine = ms, m
        obs = fm.get_index_by_type(type='bpm')['bpm']
        r,s = fm.run(monitor=obs)
        self._update_viewer_settings(fm, r)
        return fm
    
    def _update_viewer_settings(self, fm, r):
        """Initially, all viewer settings are {}, after ``run()``,
        new key-values will be added into.
        
        field : model environment
        key   : flame model
        +---------+----------+-----------+
        |  Family | field    |  key      |
        +---------+----------+-----------+
        |  BPM    |   X [m]  |  x0 [mm]  |
        |  BPM    |   Y [m]  |  y0 [mm]  |
        +---------+----------+-----------+

        """
        for i,res in r:
            elem_name = fm.get_element(index=i)[0]['properties']['name']
            readings = {field:getattr(res, k)[0]*1e-3 for field,k in zip(['X','Y'], ['x0','y0'])}
            readings['mstate'] = res
            self._viewer_settings[elem_name] = readings
    
    def _is_viewer(self, elem):
        """Test if elem is viewer, e.g. BPM, PM, ...
        """
        return elem.family in ['BPM']

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._elements[key]
        elif isinstance(key, str) or isinstance(key, unicode):
            return self._find_exact_element(name=key)
        else:
            return None

    def _find_exact_element(self, name):
        """Exact matching of element name, None if not.
        """
        if isinstance(name, AbstractElement):
            return name
        for e in self._elements:
            if str(e.name) == str(name):
                return e
        return None

    def _find_element_s(self, s, eps=1e-9, loc='left'):
        """Given s location, find an element at this location, mostly return
        the element index mostly near s, by left/right approaching.

        If this is drift space, find the element at 'left' or 'right' of the
        given point.
        """
        if not loc in ['left', 'right']:
            raise ValueError('loc must be in ["left", "right"]')

        # normalize s into [0, C]
        sn = s
        if s > self.length: sn = s - self.length
        if s < 0: sn = s + self.length

        if sn < 0 or sn > self.length:
            raise ValueError("s= %f out of boundary ([%f, %f])"
                             % (s, -self.length, self.length))
        ileft, eleft = -1, self.length
        iright, eright = -1, self.length
        for i,e in enumerate(self._elements):
            if e.virtual > 0: continue
            # assuming elements is in order
            if abs(e.sb-s) <= eleft:
                ileft, eleft = i, abs(e.sb-s)
            if abs(e.se-s) <= eright:
                iright, eright = i, abs(e.se-s)
        if loc == 'left':
            return ileft
        elif loc == 'right':
            return iright

    def createLatticeModelMap(self, mapfile):
        """Create a mapping between lattice layout and model output from a file
        
        :param mapfile: file name which has mapping information.
        
        """
        mapping = np.loadtxt(mapfile, dtype=str)
        if self.latticemodelmap is not None:
            self.latticemodelmap.clear()
        else:
            self.latticemodelmap={}
        for idx, mp in enumerate(mapping):
            if mp[0] == "NONE":
                continue
            if mp[0] not in self.latticemodelmap:
                self.latticemodelmap[mp[0]] = {}
            if mp[1] not in self.latticemodelmap[mp[0]]:
                self.latticemodelmap[mp[0]][mp[1]] = []
            self.latticemodelmap[mp[0]][mp[1]].append(idx)

    def hasElement(self, name):
        """has the named element"""
        if self._find_exact_element(name):
            return True
        else:
            return False

    def insertElement(self, elem, i=None, groups=None):
        """Insert an element at index *i* or append it.

        Parameters
        ------------
        elem : 
            CaElement object. 
        i : int
            Index to insert, append if None.
        groups : 
            Group names the element belongs to.

        See Also
        --------
        appendElement
        :class:`~phantasy.library.lattice.CaElement`
        """
        if i is not None:
            self._elements.insert(i, elem)
        else:
            if len(self._elements) == 0:
                self._elements.append(elem)
            else:
                k = 0
                for e in self._elements:
                    if e.sb < elem.sb: 
                        k += 1
                        continue
                if k == len(self._elements):
                    self._elements.append(elem)
                else:
                    self._elements.insert(k, elem)
        if groups is not None:
            for g in groups:
                if self._group.has_key(g):
                    self._group[g].append(elem)
                else:
                    self._group[g] = [elem]

    def getOverlapped(self):
        ret = []
        i = 0
        while i < len(self._elements):
            # for each element, searching the elements behind it
            j = i + 1
            ov = []
            while j < len(self._elements):
                if self._elements[j].sb < self._elements[i].se:
                    ov.append(self._elements[j].name)
                elif self._elements[j].sb >= self._elements[i].se:
                    break
                j = j + 1
            if ov:
                ret.append([self._elements[i].name] + ov)
            i = i + 1
        if ret:
            return ret
        else: return None

    def appendElement(self, elem):
        """append a new element to lattice. 

        callers are responsible for avoiding duplicate elements (call
        hasElement before).

        seealso :func:`insertElement`
        """
        self._elements.append(elem)

    def size(self):
        """total number of elements."""
        return len(self._elements)

    def remove(self, elemname):
        """remove the element, return None if not find the element."""
        for i,e in enumerate(self._elements):
            if e.name != elemname:
                continue
            return self._elements.pop(i)
        return None

    def save(self, fname, dbmode='c'):
        """save the lattice into binary data, using writing *dbmode*.

        see also Python Standard Lib `shelve`
        """
        f = shelve.open(fname, dbmode)
        pref = "lat.%s." % self.mode
        f[pref+'group']   = self._group
        f[pref+'elements'] = self._elements
        f[pref+'mode']    = self.mode
        f[pref+"source"]  = self.source
        f[pref+'tune']    = self.tune
        f[pref+'chromaticity'] = self.chromaticity
        f.close()

    def load(self, fname):
        """load the lattice from binary data

        In the db file, all lattice has a key with prefix 'lat.mode.'. If the
        given mode is empty string, then use 'lat.'
        
        seealso Python Standard Lib `shelve`
        """
        f = shelve.open(fname, 'r')
        pref = "lat."
        self._group  = f[pref+'group']
        self._elements  = f[pref+'elements']
        self.mode     = f[pref+'mode']
        self.source   = f[pref+"source"]
        self.tune     = f[pref+'tune']
        self.chromaticity = f[pref+'chromaticity']
        if self._elements:
            self.length = self._elements[-1].se
        f.close()

    def mergeGroups(self, parent, children):
        """merge child group(s) into a parent group

        the new parent group is replaced by this new merge of children
        groups. no duplicate element will appears in merged *parent* group
        
        Examples
        ---------
        >>> mergeGroups('BPM', ['BPMX', 'BPMY'])
        >>> mergeGroups('TRIM', ['TRIMX', 'TRIMY'])
        >>> mergeGroups('BPM', ['BPM', 'UBPM'])

        """
        if isinstance(children, str):
            chlist = [children]
        elif hasattr(children, '__iter__'):
            chlist = children[:]
        else:
            raise ValueError("children can be string or list of string")

        #if not self._group.has_key(parent):
        pl = []

        for child in chlist:
            if not self._group.has_key(child):
                _LOGGER.warn("WARNING: no %s group found" % child)
                continue
            for elem in self._group[child]:
                if elem in pl: continue
                pl.append(elem)
        self._group[parent] = pl
            
    def sortElements(self, namelist=None):
        """sort the element list to the order of *s*

        use sorted() for a list of element object.

        The group needs to be rebuild, since *getElementList* relies on a 
        sorted group dict.
        """
        if namelist is None:
            self._elements = sorted(self._elements)
            self.buildGroups()
            return
        
        ret = []
        for e in self._elements:
            if e.name in ret:
                continue
            if e.name in namelist:
                ret.append(e.name)

        #
        if len(ret) < len(namelist):
            raise ValueError("Some elements are missing in the results")
        elif len(ret) > len(namelist):
            raise ValueError("something wrong on sorting element list")
 
        return ret[:]

    def getLocations(self, elemsname):
        """
        if elems is a string(element name), do exact match and return
        single number.  if elems is a list do exact match on each of them,
        return a list. None if the element in this list is not found.

        .. warning::
        
          If there are duplicate elements in *elems*, only first
          appearance has location returned.

        :Example:

          >>> getLocations(['BPM1', 'BPM1', 'BPM1']) #doctest: +SKIP
          [0.1, None, None]

        """

        if isinstance(elemsname, str):
            e = self._find_exact_element(elemsname)
            return e.sb
        elif isinstance(elemsname, list):
            ret = [None] * len(elemsname)
            for elem in self._elements:
                if elem.name in elemsname:
                    idx = elemsname.index(elem.name)
                    ret[idx] = elem.s
            return ret
        else:
            raise ValueError("not recognized type of *elems*")

    def getLocationRange(self):
        s0, s1 = 0.0, 1.0
        for elem in self._elements:
            if elem.virtual:
                continue
            if isinstance(elem.sb, (int, float)): 
                s0 = elem.sb
                break
        for i in range(1, 1+len(self._elements)):
            elem = self._elements[-i]
            if elem.virtual:
                continue
            if isinstance(elem.se, (int, float)) and elem.se > s0:
                s1 = elem.se
                break
        return s0, s1

    def getLine(self, srange, eps = 1e-9):
        """
        get a list of element within range=(s0, s1).

        if s0 > s1, the range is equiv to (s0, s1+C), where C is the
        lattice length.

        *eps* is the resolution.

        relying on the fact that element.s is the beginning of element.
        """
        s0, s1 = srange[0], srange[1]

        i0 = self._find_element_s(s0, loc='right')
        i1 = self._find_element_s(s1, loc='left')

        if i0 == None or i1 == None:
            return None
        elif i0 == i1:
            return self._elements[i0]
        elif i0 < i1:
            ret = self._elements[i0:i1+1]
        else:
            ret = self._elements[i0:]
            ret.extend(self._elements[:i1+1])
        return ret

    def getElementList(self, group, **kwargs):
        """Get a list of element objects.

        Parameters
        ----------
        group : str, list.
            Element name, pattern or name list.
            when it is str, searching for elements of defined group name;
            if not found, searching for a group with name *group*.
            At last treat it as a pattern to match the element names.
            When the input *group* is a list, each string in this list will
            be treated as exact string instead of pattern.

        virtual : bool. optional(True). Including virtual element or not.

        Returns
        --------
        elemlst : a list of element objects.

        Examples
        ----------
        >>> getElementList('BPM')
        >>> getElementList('PL*')
        >>> getElementList('C02')
        >>> getElementList(['BPM1', 'BPM2'])

        """

        virtual = kwargs.get('virtual', True)
        # do exact element name match first
        elem = self._find_exact_element(group)
        if elem is not None: 
            return [elem]

        # do exact group name match
        if group in self._group.keys():
            return self._group[group][:]

        if isinstance(group, str) or isinstance(group, unicode):
            # do pattern match on element name
            ret, names = [], []
            for e in self._elements:
                if e.name in names:
                    continue
                if not virtual and e.virtual:
                    continue
                if fnmatch(e.name, group):
                    ret.append(e)
                    names.append(e.name)
            return ret
        elif isinstance(group, list):
            # exact one-by-one match, None if not found
            return [self._find_exact_element(e) for e in group]
            
    def _matchElementCgs(self, elem, **kwargs):
        """check properties of an element
        
        - *cell*
        - *girder*
        - *symmetry*
        """

        cell = kwargs.get("cell", None)
        
        if isinstance(cell, str) and elem.cell != cell:
            return False
        elif hasattr(cell, "__iter__") and not elem.cell in cell:
            return False

        girder = kwargs.get("girder", None)
        
        if isinstance(girder, str) and elem.girder != girder:
            return False
        elif hasattr(girder, "__iter__") and not elem.girder in girder:
            return False

        symmetry = kwargs.get("symmetry", None)
        
        if isinstance(symmetry, str) and elem.symmetry != symmetry:
            return False
        elif hasattr(symmetry, "__iter__") and not elem.symmetry in symmetry:
            return False

        return True

    def _getElementsCgs(self, group = '*', **kwargs):
        """
        call signature::
        
          getElementsCgs(group)

        Get a list of elements from cell, girder and sequence

        - *cell*
        - *girder*
        - *symmetry*

        :Example:

            >>> getElementsCgs('BPMX', cell=['C20'], girder=['G2'])

        When given a general group name, check the following:

        - element name
        - element family
        - existing *group*: 'BPM', 'BPMX', 'BPMY', 'A', 'C02', 'G4'

            - cell
            - girder
            - symmetry
        """

        # return empty set if not specified the group
        if not group: return None
        
        elem = []
        for e in self._elements:
            # skip for duplicate
            if e.name in elem: continue

            if not self._matchElementCgs(e, **kwargs):
                continue
            
            if e.name in self._group.get(group, []):
                elem.append(e.name)
            elif fnmatch(e.name, group):
                elem.append(e.name)
            else:
                pass
                
            #if cell and not e.cell in cell: continue
            #if girder and not e.girder in girder: continue
            #if symmetry and not e.symmetry in symmetry: continue
        
        return elem

    def _illegalGroupName(self, group):
        # found character not in [a-zA-Z0-9_]
        if not group: return True
        elif re.search(r'[^\w:]+', group):
            #raise ValueError("Group name must be in [a-zA-Z0-9_]+")
            return True
        else: return False

    def buildGroups(self):
        """
        clear the old groups, fill with new data by collecting group name
        that each element belongs to.

        - the elements must be in s order
        """
        # cleanr everything
        self._group = {}
        for e in self._elements:
            for g in e.group:
                if self._illegalGroupName(g):
                    continue
                #self.addGroupMember(g, e.name, newgroup=True)
                lst = self._group.setdefault(g, [])
                lst.append(e)

    def addGroup(self, group):
        """
        create a new group

        :Example:
        
            >>> addGroup(group)
          
        Input *group* is a combination of alphabetic and numeric
        characters and underscores. i.e. "[a-zA-Z0-9\_]"

        raise ValueError if the name is illegal or the group already exists.
        """
        if self._illegalGroupName(group):
            raise ValueError('illegal group name %s' % group)

        if not self._group.has_key(group):
            self._group[group] = []
        else:
            raise ValueError('group %s exists' % group)

    def removeGroup(self, group):
        """
        remove a group only when it is empty
        """
        if self._illegalGroupName(group):
            return
        if not self._group.has_key(group):
            raise ValueError("Group %s does not exist" % group)
        if len(self._group[group]) > 0:
            raise ValueError("Group %s is not empty" % group)
        # remove it!
        self._group.pop(group)

    def addGroupMember(self, group, member, newgroup=False):
        """
        add a member to group

        if newgroup == False, the group must exist before.
        """

        elem = self._find_exact_element(member)
        if not elem:
            raise ValueError("element %s is not defined" % member)

        if self.hasGroup(group):
            if elem in self._group[group]:
                return
            elem.group.add(group)
            for i,e in enumerate(self._group[group]):
                if e.sb < elem.sb:
                    continue
                self._group[group].insert(i, elem)
                break
            else:
                self._group[group].append(elem)
        elif newgroup:
            self._group[group] = [elem]
            elem.group.add(group)
        else:
            raise ValueError("Group %s does not exist."
                             "use newgroup=True to add it" % group)

    def hasGroup(self, group):
        """
        check if group exists or not.
        """
        return self._group.has_key(group)

    def removeGroupMember(self, group, member):
        """
        remove a member from group
        """
        if not self.hasGroup(group):
            raise ValueError("Group %s does not exist" % group)
        if member in self._group[group]:
            self._group[group].remove(member)
        else:
            raise ValueError("%s not in group %s" % (member, group))

    def getGroups(self, element=None):
        """
        return a list of groups this element belongs to

        :Example:

            >>> getGroups() # list all groups, including the empty groups
            >>> getGroups('*') # all groups, not including empty ones
            >>> getGroups('Q?')
          
        The input string is wildcard matched against each element.
        """
        if element is None:
            return self._group.keys()

        ret = []
        for k, elems in self._group.items():
            for e in elems:
                if fnmatch(e.name, element):
                    ret.append(k)
                    break
        return ret

    def getGroupMembers(self, groups, op, **kwargs):
        """
        return members in a list of groups. 

        can take a union or intersections of members in each group

        - *groups* can be a list of exact group name, pattern or both.
        - op = ['union' | 'intersection']

        :Example:
        
            >>> getGroupMembers(['C0[2-3]', 'BPM'], op = 'intersection')

        Note: an element pattern, e.g. "p*g1c23a" is not a pattern of `groups`
        """
        if not groups:
            return None
        ret = {}

        if groups in self._group.keys():
            return self._group[groups]

        for g in groups:
            ret[g] = []
            imatched = 0
            for k, elems in self._group.items():
                if fnmatch(k, g): 
                    imatched += 1
                    ret[g].extend([e.name for e in elems])


        r = set(ret[groups[0]])
        if op.lower() == 'union':
            for g, v in ret.items():
                r = r.union(set(v))
        elif op.lower() == 'intersection':
            for g, v in ret.items():
                r = r.intersection(set(v))
        else:
            raise ValueError("%s not defined" % op)
        
        return self.getElementList(self.sortElements(r))

    def getNeighbors(self, elemname, groups, n, elemself=True):
        """
        Assuming self._elements is in s order

        the element matched with input 'element' string should be unique
        and exact.

        If the input *element* name is also in one of the *groups*, no
        duplicate the result.
        
        For a linear machine, it will fill `None` is there is no enough elements in upstream or in downstream. 

        :Example:

            >>> getNeighbors('P4', 'BPM', 2)
            ['P2', 'P3', 'P4', 'P5', 'P6']
            >>> getNeighbors('Q3', 'BPM', 2)
            ['P2', 'P3', 'Q3', 'P4', 'P5']
            >>> getNeighbors('Q3', ["BPM", "SEXT"], 2)
        """

        e0 = self._find_exact_element(elemname)
        if not e0:
            raise ValueError("element %s does not exist" % elemname)

        el = []
        if isinstance(groups, (str, unicode)):
            el = self.getElementList(groups, virtual=0)
        elif isinstance(groups, (list, tuple)):
            el = self.getGroupMembers(groups, op="union")

        if not el:
            raise ValueError("elements/group %s does not exist" % groups)
        if e0 in el:
            el.remove(e0)

        i0 = len(el)
        for i, e in enumerate(el):
            if e.sb < e0.sb: 
                continue
            i0 = i
            break
        ret = [e0] if elemself else []
        for i in range(n):
            _, r = divmod(i0 - i - 1, len(el))
            if self.isring or el[r].sb < e0.sb:
                # insert into the front no matter what for a ring  
                # or when the position is smaller than that of current element for a linear machine
                ret.insert(0, el[r])
            else:
                ret.insert(0, None)
            _, r = divmod(i0 + i, len(el))
            if self.isring or el[r].sb > e0.sb:
                # append into the list no matter what for a ring  
                # or when the position is larger than that of current element for a linear machine
                ret.append(el[r])
            else:
                ret.append(None)
        return ret
        
    def getClosest(self, elemname, groups):
        """
        Assuming self._elements is in s order

        the element matched with input 'element' string should be unique
        and exact.

        :Example:

            >>> getClosest('P4', 'BPM')
            >>> getClosest('Q3', 'BPM')
            >>> getClosest('Q3', ["QUAD", "SEXT"])

        The result can not be virtual element.
        """

        e0 = self._find_exact_element(elemname)
        if not e0:
            raise ValueError("element %s does not exist" % elemname)

        el = []
        if isinstance(groups, (str, unicode)):
            el = self.getElementList(groups, virtual=0)
        elif isinstance(groups, (list, tuple)):
            el = self.getGroupMembers(groups, op="union")

        if not el: raise ValueError("elements/group %s does not exist" % groups)

        idx, ds = 0, el[-1].sb
        for i,e in enumerate(el):
            if e == e0: continue
            if isinstance(e.sb, (list, tuple)):
                ds0 = abs(e.sb[0] - e0.sb)
            else:
                ds0 = abs(e.sb - e0.sb)
            if ds0 > ds: continue
            idx = i
            ds = ds0

        return el[idx]
        
    def __repr__(self):
        s0 = '#name of segment: {}'.format(self.name)
        s1 = '#{0:<6s}{1:^20s} {2:<10s} {3:<10s} {4:<10s}'.format(
                'index', 'name', 'family', 'position', 'length'
                )
        ret = [s0, s1]

        ml_name, ml_family = 0, 0
        for e in self._elements:
            if len(e.name) > ml_name: ml_name = len(e.name)
            if e.family and len(e.family) > ml_family:
                ml_family = len(e.family)

        idx = 1
        if len(self._elements) >= 10:
            idx = int(1.0+log10(len(self._elements)))
        fmt = "{idx:<6d} {name:<20s} {family:<10s} {pos:<10.4f} {len:<10.4f}" 
        for i, e in enumerate(self._elements):
            if e.virtual: continue
            ret.append(fmt.format(idx=i, name=e.name, family=e.family, 
                                  pos=e.sb, len=e.length))            
        return '\n'.join(ret)


def _normalize_phase(x):
    while x >= 360.0:
        x -= 360.0
    while x < 0.0:
        x += 360.0
    return x

