#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is created for the CLI operations, could be treated like
the bridge interface between middle layer and high-level physics
applications.

The workflow of the high-level physics operations are mainly defined in
this module, each physics application should be initiated from here,
other potential usages should also be defined here.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging
import os

import phyutil
from .miscutils import (flatten, get_intersection, 
                        bisect_index, pattern_filter)

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)


class MachinePortal(object):
    """Very first step to control the machine on physics high-level layer.

    Parameters
    ----------
    facility : str
        Name of the accelerator machine, typically, use the fold of the
        facility name to host all the related configuration files, also
        this parameter could be the path of the configuration folder.
    
    segment : str
        all machine segments are defined in *submachines* field in the
        configuration file "phyutil.ini", separated by space, e.g.
        ``submachines: LINAC LS1`` defines two segments ``LINAC`` and ``LS1``,
        the ``default_submachine`` field in that file is used to define the
        default segment to use. If *segment* parameter is not defined, use the
        one defined by ``default_submachine``.

    Keyword Arguments
    -----------------
    verbose : int
        If set nonzero, print out parsing message.

    Note
    ----
    1. ``segment`` is the same meaning as ``lattice`` or ``submachine``.
    2. Directory searching rule for the machine/facility configuration files:
       (list by searching priority)
        - User-defined directory;
        - Environmental variable: ``PHYUTIL_CONFIG_DIR``;
        - Current user's home folder: ``~/.phyutil``;
       If the search directory is ``MPATH``, then the naming rule of *facility*:
       ``MPATH`` + machine name, e.g. ``MPATH=/home/user/develop``, 
       machine name is ``FRIB``, then *facility* could be 
       ``/home/user/develop/FRIB``, all configuration files of ``FRIB`` should
       be in this directory.

    Examples
    --------
    >>> # Use default configuration
    >>> mp = MachinePortal()
    >>> mp.last_machine_path # where I put FRIB machine
    /home/tong1/work/FRIB/projects/machines/FRIB
    >>> # with facility name, just the same as above
    >>> mp = MachinePortal(facility="FRIB")
    >>> # another facility name
    >>> mp = MachinePortal(facility="FRIB1")
    # FRIB1 is in the current working directory
    >>> os.path.relpath(mp.last_machine_path)
    'FRIB1'
    """
    def __init__(self, facility=None, segment=None, **kws):
        self._facility = "FRIB" if facility is None else facility
        if os.path.isdir(self._facility):
            self._facility = os.path.realpath(self._facility)

        self._lattice_names = []
        self._machine_names = []
        self._lattices = {}
        self._machines = {}

        self._last_mach_name = ''
        self._last_mach_conf = None
        self._last_mach_path = ''
        self._last_lattice_name = ''
        self._last_lattice_conf = None
        self._work_lattice_name = ''
        self._work_lattice_conf = None


        self.load_lattice(facility=self._facility, segment=segment, **kws)

    @property
    def last_machine_name(self):
        """str: Name of last loaded machine or facility."""
        return self._last_mach_name

    @property
    def last_machine_conf(self):
        """Configuration: Last loaded configuration object.
        
        See Also
        --------
        :class:`~phyutil.Configuration`
        """
        return self._last_mach_conf

    @property
    def last_machine_path(self):
        """str: Full path of the last loaded *phyutils.ini* file
        """
        return self._last_mach_path

    @property
    def machine_names(self):
        """list: Names of all loaded machines or facilities."""
        return self._machine_names

    @property
    def lattice_names(self):
        """list: Names of all loaded lattices."""
        return self._lattice_names

    @property
    def last_lattice_name(self):
        """str: Name of last loaded lattice."""
        return self._last_lattice_name

    @property
    def last_lattice_conf(self):
        """list: Configuration of last loaded lattice, composed of caElements.
        
        See Also
        --------
        :class:`~phyutil.CaElement`
        """
        return self._last_lattice_conf

    @property
    def work_lattice_name(self):
        """str: Name of working lattice."""
        return self._work_lattice_name

    @property
    def work_lattice_conf(self):
        """list: Configuration of working lattice, composed of caElements.
        
        See Also
        --------
        :class:`~phyutil.CaElement`
        use_lattice : Choose working lattice from loaded lattices.
        """
        return self._work_lattice_conf

    @property
    def lattices(self):
        """dict: All loaded lattices."""
        return self._lattices

    @property
    def machines(self):
        """dict: All loaded machines."""
        return self._machines

    def load_lattice(self, segment=None, facility=None, **kws):
        """Load machine lattice from *phyutil.ini* file.

        Parameters
        ----------
        segment : str
            Segment or lattice or submachine name.
        facility : str
            Facility or machine name, or path of configuration files.

        Keyword Arguments
        -----------------
        verbose : int
            If set nonzero, print out parsing message.
        re_load : True or False
            If set True, reload segment, ``False`` by default.

        Returns
        -------
        ret : dict
            Configuration of loaded segment of facility, with the keys of
            ``lat_name``, ``lat_conf``, ``mach_name``, ``mach_path`` and
            ``mach_conf``.
        
        Examples
        --------
        >>> mp.load_lattice('LS1')
        >>> mp.work_lattice_name # 'LS1'
        >>> mp.load_lattice('LINAC') # does not actually load, use cached
        >>> mp.work_lattice_name # 'LINAC'
        # Note working lattice is changed from 'LS1' to 'LINAC', although
        # not actually loaded the lattice, see use_lattice().
        
        The cached tricky could improve performance, e.g. in ipython:

        >>> %%timeit
        >>> mp.load_lattice('LS1', re_load=True)
        10 loops, best of 3: 180 ms per loop
        >>> %%timeit
        >>> mp.load_lattice('LS1')
        10000 loops, best of 3: 190 µs per loop

        Note
        ----
        1. If *segment* of *facility* has already been loaded, will not load
           again, just switch working lattice to be the *segment*; keyword
           parameter *re_load* could be used to do force reload;
        2. *re_load* could be used if necessary, e.g. the configuration
           file for some segment is changed, etc.

        See Also
        --------
        use_lattice : Choose working lattice from loaded lattices.
        reload_lattice : Reload machine/lattice.
        """
        if facility is None:
            facility = self._facility

        if os.path.isdir(facility):
            facility = os.path.realpath(facility)
        if self._use_cached(segment, facility, re_load=kws.get('re_load', False)):
            mach_name = os.path.basename(facility)
            mach_conf = self._machines.get(mach_name)['conf']
            mach_path = self._machines.get(mach_name)['path']
            lat_name = segment
            lat_conf = self._lattices.get(lat_name)
            retval = {'lat_name': lat_name,
                      'lat_conf': lat_conf,
                      'mach_name': mach_name,
                      'mach_path': mach_path,
                      'mach_conf': mach_conf}
            self._last_mach_name = mach_name
            self._last_mach_conf = mach_conf
            self._last_mach_path = mach_path
            self._last_lattice_name = lat_name
            self._last_lattice_conf = lat_conf
            self._work_lattice_name = lat_name
            self._work_lattice_conf = lat_conf
            return retval

        try:
            retval = phyutil.machine.load(machine=facility, submachine=segment,
                            return_lattices=True, return_more=True, **kws)
            
            lat_name = retval['lat_name']
            lat_conf = retval['lat_conf']
            mach_name = retval['mach_name']
            mach_conf = retval['mach_conf']
            mach_path = retval['mach_path']

            self._lattices.update({lat_name: lat_conf})
            self._machines.update({mach_name: {'conf': mach_conf, 'path': mach_path}})
            self._last_mach_conf = mach_conf
            self._last_mach_path = mach_path
            self._last_mach_name = mach_name
            self._last_lattice_name = lat_name
            self._last_lattice_conf = lat_conf
            self._work_lattice_name = lat_name
            self._work_lattice_conf = lat_conf

            if lat_name is not None and lat_name not in self._lattice_names:
                self._lattice_names.append(lat_name) 

            if mach_name is not None and mach_name not in self._machine_names:
                self._machine_names.append(mach_name) 
        except:
            _LOGGER.error("Cannot load facility: {} segment: {}".format(
                facility, segment))
            retval = None
        return retval
    
    def print_all_properties(self):
        """Print all properties, for debug only.
        """
        for attr in ['lattice_names', 'machine_names', 
                     'last_machine_name',
                     'last_machine_path', 'last_lattice_name',
                     #'last_lattice_conf',
                     'last_machine_conf']:
            print(attr, getattr(self, attr))

    def _use_cached(self, segment, facility, **kws):
        """Test if continue parsing procedure is needed, if facility/segment
        is already parsed, just return value, or do parsing; if *re_load*
        keyword is True, always return False.
        """
        facility = os.path.basename(facility)
        if segment is None:
            segment = 'DEFAULT'
        _f_reload = kws.get('re_load')
        if facility in self._machine_names and segment in self._lattice_names:
            if _f_reload:
                _LOGGER.warn("Force reload facility: {} segment: {}".format(
                              facility, segment))
                retval = False
            else:
                _LOGGER.warn("Use cached results for facility: {} segment: {}".format(
                              facility, segment))
                retval = True
        else:
            _LOGGER.warn("Load new facility: {} segment: {}".format(
                          facility, segment))
            retval = False
        return retval
    
    def reload_lattice(self, segment=None, facility=None, **kws):
        """Reload machine lattice, if parameters *facility* and *segment* are
        not defined, reload last loaded one.

        Parameters
        ----------
        segment : str
            Segment or lattice or submachine name.
        facility : str
            Facility or machine name, or path of configuration files.
        
        See Also
        --------
        load_lattice : Load machine/lattice from configuration files.
        """
        segment = self._last_lattice_name if segment is None else segment
        facility = self._last_mach_path if facility is None else facility
        return self.load_lattice(facility=facility,
                                 segment=segment,
                                 re_load=True)

    def use_lattice(self, lattice_name=None):
        """Choose name of one of the loaded lattices as the working lattice,
        if this method is not evoked, the working lattice is the last loaded
        lattice.

        Parameters
        ----------
        lattice_name : str
            Lattice name.

        Returns
        -------
        ret : str
            Selected working lattice name.

        Note
        ----
        If ``load_lattice()`` or ``reload_lattice()`` is called, the working
        lattice name would be changed to the just loaded one, since,
        usually as the user loading a lattice, most likely he/she would like
        to switch onto that lattice, or explicitly invoking ``use_lattice()``
        again to switch to another one.

        See Also
        --------
        load_lattice : Load machine/lattice from configuration files.
        """
        if lattice_name in self._lattice_names:
            _LOGGER.info("Switch working lattice to: {}.".format(lattice_name))
            self._work_lattice_name = lattice_name
            self._work_lattice_conf = self._lattices[lattice_name]
            return self._work_lattice_name
        else:
            _LOGGER.warn("Invalid lattice name, working lattice name unchanged.")
            return self._work_lattice_name
    
    def get_elements(self, name=None, type=None, srange=None, **kws):
        """Get element(s) from working lattice.

        Parameters
        ----------
        name : str or list[str]
            (List of) Element names or Unix shell style patterns.
        type : str or list[str]
            (List of) Element type/group/family, or Unix shell style patterns.
        srange : tuple
            Start and end points (tuple of float) of elements' longitudinal
            position.

        Keyword Arguments
        -----------------
        latname : str
            Use the (valid) defined lattice name instead of current working
            lattice name, maybe useful to inspect non-working lattices.
        sort_key : str
            Ascendingly sort key of the returned list, ``name`` or ``pos``,
            ``pos`` by default, or other attributes valid for ``CaElement``.

        Returns
        -------
        ret : List
            List of elements (``CaElement``), excluding virtual elements.
            
        Note
        ----
        1. The pattern here used is Unix shell style, slightly different
           from regex, e.g. pattern 'BP' matches 'BPM' in regex, but matches
           nothing in Unix shell style, 'BP*' works;
        2. If more than one positional parameters (*name*, *type*, *srange*)
           are defined, return elements that meet all definitions;
        3. By default, the returned elements are ascendingly sorted according
           to element position values.

        Examples
        --------
        >>> # create MachinePortal instance, e.g. mp
        >>> # 1. define name parameter, invalid names
        >>> mp.get_elements(name='NOEXISTS')
        []
        >>> # 2. names or name patterns
        >>> mp.get_elements(name='FS1_BMS:DCV_D2662')
        [FS1_BMS:DCV_D2662:VCOR @ sb=153.794690]
        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'], latname='LINAC')
        [LS1_BTS:DCV_D1937:VCOR @ sb=81.365954,
         LS1_BTS:DCV_D1964:VCOR @ sb=84.013954,
         LS1_BTS:DCV_D1997:VCOR @ sb=87.348954,
         LS1_BTS:DCV_D2024:VCOR @ sb=90.055166,
         LS1_BTS:DCV_D2061:VCOR @ sb=93.710487,
         LS1_BTS:DCV_D2114:VCOR @ sb=98.985556,
         FS1_BMS:DCV_D2662:VCOR @ sb=153.794690,
         FS1_BMS:DCH_D2662:HCOR @ sb=153.794690,
         FS1_BMS:BPM_D2664:BPM @ sb=153.963690,
         FS1_BMS:QH_D2666:QUAD @ sb=154.144690]
        >>> # filter BPMs for the above result
        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'], type='BPM',
        >>>                 latname='LINAC')
        [FS1_BMS:BPM_D2664:BPM @ sb=153.963690]
        >>> # type='BPM' also could be be pattern
        >>> # filter hybrid types
        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'],
        >>>                 type=['BPM', 'QUAD'], latname='LINAC')
        [FS1_BMS:BPM_D2664:BPM @ sb=153.963690,
         FS1_BMS:QH_D2666:QUAD @ sb=154.144690]
        >>> # get sub-segment from lattice according to pos range
        >>> mp.get_elements(srange=(10, 11))
        [LS1_CB01:CAV1_D1229:CAV @ sb=10.366596,
         LS1_CB01:BPM_D1231:BPM @ sb=10.762191,
         LS1_CB01:SOL1_D1235:SOL @ sb=10.894207]
        >>> # continue filter with srange parameter
        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'],
        >>>                 type=['BPM', 'QUAD'], srange=(154, 155),
        >>>                 latname='LINAC')
        [FS1_BMS:QH_D2666:QUAD @ sb=154.144690]

        Note
        ----
        Select sub-segment by ``srange`` parameter is realized by new approach,
        other than ``phyutil.Lattice.getLine()``, e.g. the result of
        ``getLine((10,11))`` contains element before the start range: i.e.
        ``LS1_WA03:PM_D1223:PM @ sb=9.929284``, which is before the range.

        See Also
        --------
        :class:`phyutil.CaElement` : Element class.
        get_virtual_elements
        next_elements
        """
        latname = kws.get('latname')
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf

        valid_types = self.get_all_types(virtual=False)
        
        # name
        if isinstance(name, (str, unicode)):
            ele_names = lat.getElementList(name)
        elif isinstance(name, (list, tuple)):
            ele_names = flatten(lat.getElementList(n) for n in name)
        else:
            ele_names = []

        # group
        if type is not None:
            if isinstance(type, (str, unicode)):
                type = type, 
            _type_list = flatten(pattern_filter(valid_types, p) for p in type)
            ele_types = flatten(lat.getElementList(t) for t in _type_list)
        else:
            ele_types = []
        
        # srange
        if isinstance(srange, (list, tuple)):
            pos_start, pos_end = srange[0], srange[1]
            # by default elems is sorted, if not, sort it before using.
            elems = lat.getElementList('*', virtual=False)
            s = [e.sb for e in elems]
            index0 = bisect_index(s, pos_start)
            index1 = bisect_index(s, pos_end)
            ele_srange = elems[index0:index1]
        else:
            ele_srange = []

        ret_elems = get_intersection(c1=ele_names, c2=ele_types, c3=ele_srange)

        sk = kws.get('sort_key', 'sb')
        if sk == 'pos':
            sk = 'sb'
        return sorted([e for e in ret_elems if not MachinePortal.is_virtual(e)],
                        key=lambda e: getattr(e, sk))

    def next_elements(self, ref_elem, count=1, **kws):
        """Get elements w.r.t reference element, according to the defined
        confinement, from given lattice name, if not given, use the current
        working lattice.

        Parameters
        ----------
        ref_elem :
            ``CaElement`` object, reference element.

        count : int
            Skip element number after *ref_elem*, negative input means before,
            e.g. ``count=1`` will locate the next one of *ref_elem* in the 
            investigated lattice, if keyword parameter *type* is given, will
            locate the next one element of the defined type; ``count=-1`` will
            locate in the opposite direction.
            
        Keyword Arguments
        -----------------
        type : str or list(str)
            (List of) Element type/group/family, if *type* is a list of more
            than one element types, the *next* parameter will apply on each
            type.
        range : str
            String of format ``start:stop:step``, to slicing the output list,
            e.g. return 50 BPMs after *ref_elem* (``count=50``), but only get
            every two elements, simply by setting ``range=0::2``.
        latname : str
            Name of lattice to be investigated.
        ref_include : True or False
            Include *ref_elem* in the returned list or not.

        Returns
        -------
        ret : List
            List of next located elements, ascendingly sorted by position, by
            default, only return one element (for eath *type*) that meets the
            confinement, return more by assgining *range* keyword parameter.

        Examples
        --------
        >>> # create MachinePortal instance, e.g. mp
        >>> print(all_e)
        [LS1_CA01:CAV1_D1127:CAV @ sb=0.207064,
         LS1_CA01:BPM_D1129:BPM @ sb=0.511327,
         LS1_CA01:SOL1_D1131:SOL @ sb=0.643330,
         LS1_CA01:DCV_D1131:VCOR @ sb=0.743330,
         LS1_CA01:DCH_D1131:HCOR @ sb=0.743330,
         LS1_CA01:CAV2_D1135:CAV @ sb=0.986724,
         LS1_CA01:CAV3_D1143:CAV @ sb=1.766370,
         LS1_CA01:BPM_D1144:BPM @ sb=2.070634,
         LS1_CA01:SOL2_D1147:SOL @ sb=2.202637,
         LS1_CA01:DCV_D1147:VCOR @ sb=2.302637,
         LS1_CA01:DCH_D1147:HCOR @ sb=2.302637,
         LS1_CA01:CAV4_D1150:CAV @ sb=2.546031,
         LS1_WA01:BPM_D1155:BPM @ sb=3.109095,
         LS1_CA02:CAV1_D1161:CAV @ sb=3.580158,
         LS1_CA02:BPM_D1163:BPM @ sb=3.884422,
         LS1_CA02:SOL1_D1165:SOL @ sb=4.016425,
         LS1_CA02:DCV_D1165:VCOR @ sb=4.116425,
         LS1_CA02:DCH_D1165:HCOR @ sb=4.116425,
         LS1_CA02:CAV2_D1169:CAV @ sb=4.359819,
         LS1_CA02:CAV3_D1176:CAV @ sb=5.139465,
         LS1_CA02:BPM_D1178:BPM @ sb=5.443728]
        >>> ref_elem = all_e[5]
        >>> # get next element of ref_elem
        >>> mp.next_elements(ref_elem)
        [LS1_CA01:CAV3_D1143:CAV @ sb=1.766370]
        >>> # next two, get last one
        >>> mp.next_elements(ref_elem, count=2)
        [LS1_CA01:BPM_D1144:BPM @ sb=2.070634]
        >>> # next two, get all
        >>> mp.next_elements(ref_elem, count=2, range='0::1')
        [LS1_CA01:CAV3_D1143:CAV @ sb=1.766370,
         LS1_CA01:BPM_D1144:BPM @ sb=2.070634]
        >>> # get two elements before ref_elem
        >>> mp.next_elements(ref_elem, count=-2, range='0::1')
        [LS1_CA01:DCV_D1131:VCOR @ sb=0.743330,
         LS1_CA01:DCH_D1131:HCOR @ sb=0.743330]
        >>> # get next two BPM elements after ref_elem, result including itself
        >>> mp.next_elements(ref_elem, count=2, type=['BPM'],
        >>>                  ref_include=True, range='0::1')
        [LS1_CA01:CAV2_D1135:CAV @ sb=0.986724,
         LS1_CA01:BPM_D1144:BPM @ sb=2.070634,
         LS1_WA01:BPM_D1155:BPM @ sb=3.109095]
        >>> # hybrid types
        >>> mp.next_elements(ref_elem, count=2, type=['BPM', 'CAV'],
        >>>                  range='0::1')
        [LS1_CA01:CAV3_D1143:CAV @ sb=1.766370,
         LS1_CA01:BPM_D1144:BPM @ sb=2.070634,
         LS1_CA01:CAV4_D1150:CAV @ sb=2.546031,
         LS1_WA01:BPM_D1155:BPM @ sb=3.109095]
        """
        ref_include_flag = kws.get('ref_include', False)
        if not isinstance(ref_elem, phyutil.CaElement):
            _LOGGER.warn("{} is not a valid CaElement.".format(str(ref_elem)))
            if ref_include_flag:
                return [ref_elem]
            else:
                return []

        if count == 0:
            return [ref_elem]

        count_is_positive = True if count > 0 else False
        if count_is_positive:
            eslice = kws.get('range', '-1::1')
        else:
            eslice = kws.get('range', '0:1:1')
        slice_tuple = [int(i) if i != '' else None for i in eslice.split(':')]
        eslice = slice(*slice_tuple)

        latname = kws.get('latname')
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf

        etype = kws.get('type', None)
        
        elem_sorted = sorted([e for e in lat if e.virtual == 0],
                             key=lambda e: e.sb)
        spos_list = [e.sb for e in elem_sorted]
        ref_idx = spos_list.index(ref_elem.sb)
        if count_is_positive:
            eslice0 = slice(ref_idx+1, ref_idx+count+1, 1)
        else:
            eslice0 = slice(ref_idx+count, ref_idx, 1)

        if etype is None:
            ret =  elem_sorted[eslice0][eslice]
        else:
            if isinstance(etype, (str, unicode)):
                etype = etype,
            if count_is_positive:
                ret = flatten([e for e in elem_sorted[ref_idx+1:]
                            if e.family == t][:count]
                                for t in etype)
            else:
                ret = flatten([e for e in elem_sorted[:ref_idx]
                            if e.family == t][count:]
                                for t in etype)
        if ref_include_flag:
            ret.append(ref_elem)
        return sorted(ret, key=lambda e: e.sb)
            
    @staticmethod
    def is_virtual(elem):
        """Test if input element is virtual element.

        Parameters
        ----------
        elem : 
            ``CaElement`` object.
        
        Returns
        -------
        ret : True or False
            True for virtual element, else False.
        """
        if isinstance(elem, phyutil.CaElement):
            t_vir = True if elem.virtual == 1 else False
        else:
            t_vir = False
        return t_vir

    def get_virtual_elements(self, **kws):
        """Get all virtual elements from given lattice.

        Keyword Arguments
        -----------------
        latname : str
            Name of lattice to be investigated.

        Returns
        -------
        ret : List
            List of virtual ``CaElement`` objects.
        """
        latname = kws.get('latname')
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf
        return [e for e in lat.getElementList('*') if e.virtual == 1]

    def get_all_types(self, virtual=False, **kws):
        """Get names of element types (groups/families) from given lattice.

        Parameters
        ----------
        virtual : True or False
            Return virtual group or not, ``False`` by default.

        Keyword Arguments
        -----------------
        latname : str
            Name of lattice to be investigated.

        Returns
        -------
        ret : List(str)
            List of type names.

        See Also
        --------
        lattice_names : Names of all loaded lattices.
        get_all_names : Get all element names from given lattice.
        """
        latname = kws.get('latname')
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf
        all_groups = lat.getGroups()
        if virtual == True:
            return all_groups
        else:
            return [g for g in all_groups if g != 'HLA:VIRTUAL']

    def get_all_names(self, virtual=False, **kws):
        """Get names of all elements from  given lattice.

        Parameters
        ----------
        virtual : True or False
            Return virtual elements or not, ``False`` by default.

        Keyword Arguments
        -----------------
        latname : str
            Name of lattice to be investigated.

        Returns
        -------
        ret : List(str)
            List of element names.

        See Also
        --------
        lattice_names : Names of all loaded lattices.
        get_all_types : Get all element types from given lattice.
        """
        latname = kws.get('latname')
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf
        return [e.name for e in lat.getElementList('*', virtual=virtual)]
