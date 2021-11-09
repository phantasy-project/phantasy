#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is created for the CLI operations, could be treated like
the bridge interface between middle layer and high-level physics
applications.

The workflow of the high-level physics operations are mainly defined in
this module, each physics application should be initiated from here,
other potential usages should also be defined here.
"""
import logging
import os
import sys
from functools import reduce

from numpy import intersect1d
from phantasy.library.lattice import CaElement
from phantasy.library.parser import Configuration
from phantasy.library.pv import get_readback
from phantasy.facility.frib import INI_DICT

from .lattice import load_lattice

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams, \
        Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)


class MachinePortal(object):
    """The very first step to control the machine (accelerator system) on
    physics high-level view, create high-level lattice object from segment
    of machine, upon which various operations could be proceeded.

    Parameters
    ----------
    machine : str
        Name of the accelerator machine, typically, is the name of the data
        directory, within which all the related configuration files are
        hosted, could be the path of the configuration folder. The default
        value is ``FRIB``.
    segment : str
        All machine segments are defined in *segments* field in the
        configuration file "phantasy.ini", separated by space, e.g.
        ``segments: LINAC LS1`` defines two segments ``LINAC`` and ``LS1``,
        the ``default_segment`` field in that file is used to define the
        default segment to use. If *segment* parameter is not defined, use
        the one defined by ``default_segment``.

    Keyword Arguments
    -----------------
    prefix : str
        String prefix to all channels, this parameter is crucial to the
        virtual accelerator (VA) modeling, when '--pv-prefix' argument is
        used when starting up the VA rather than the one defined in the
        configuration file (e.g. phantasy.cfg). If this parameter is not
        defined, will use the one defined by 'machine' in 'DEFAULT' section
        of configuration file.
    verbose : int
        If set nonzero, print out verbose message.
    auto_monitor : bool
        If set True, initialize all channels auto subscribe, default is False.

    Note
    ----
    1. Lattice is created from segment of machine.
    2. Directory searching rule for the machine configuration files:
       (searching priority from high to low)

       - Path of user-defined directory;
       - Path of current working directory;
       - Path defined by env: ``PHANTASY_CONFIG_DIR``;
       - Current user's home folder: ``~/.phantasy``;
       - Path of phantasy-machines if installed via pip.

       If the found directory is ``MPATH``, then the naming rule of *machine*:
       ``MPATH`` + machine name, e.g. ``MPATH=/home/user/develop``,
       machine name is ``FRIB``, then *machine* could be defined as:
       ``/home/user/develop/FRIB``, all configuration files of ``FRIB`` should
       be in that directory.

    Examples
    --------
    >>> # Use default configuration
    >>> mp = MachinePortal()
    >>> mp.last_machine_path # where I put FRIB machine
    /home/tong1/work/FRIB/projects/machines/FRIB
    >>> # with machine name, just the same as above
    >>> mp = MachinePortal(machine="FRIB")
    >>> # another machine name
    >>> mp = MachinePortal(machine="FRIB1")
    # FRIB1 is in the current working directory
    >>> os.path.relpath(mp.last_machine_path)
    'FRIB1'
    """

    def __init__(self, machine=None, segment=None, **kws):
        self._machine = "FRIB" if machine is None else machine
        if os.path.isdir(self._machine):
            self._machine = os.path.realpath(self._machine)

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

        # check last_load_success attr
        self.load_lattice(segment=segment, machine=self._machine, **kws)

    @property
    def last_load_success(self):
        """Return True if lattice loaded without error, or False.
        """
        return self._last_load_success

    @property
    def last_machine_name(self):
        """str: Name of last loaded machine."""
        return self._last_mach_name

    @property
    def last_machine_conf(self):
        """Configuration: Last loaded configuration object.

        See Also
        --------
        :class:`~phantasy.library.parser.config.Configuration`
        """
        return self._last_mach_conf

    @property
    def last_machine_path(self):
        """str: Full path of the last loaded *phantasys.ini* file
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
        :class:`~phantasy.library.lattice.element.CaElement`
        """
        return self._last_lattice_conf

    @property
    def work_lattice_name(self):
        """str: Name of working lattice."""
        return self._work_lattice_name

    @property
    def work_lattice_conf(self):
        """list: Configuration of working lattice, composed of CaElements.

        See Also
        --------
        :class:`~phantasy.library.lattice.CaElement`
            Element object for channel access.
        :func:`use_lattice`
            Choose working lattice from loaded lattices.
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

    def load_lattice(self, segment=None, machine=None, **kws):
        """Load machine segment from *phantasy.ini* file.

        Parameters
        ----------
        segment : str
            Segment name.
        machine : str
            Machine name, or path of configuration files.

        Keyword Arguments
        -----------------
        verbose : int
            If set nonzero, print out verbose message.
        re_load : True or False
            If set True, reload segment, ``False`` by default.

        Returns
        -------
        ret : dict
            Configuration of loaded segment of machine, with the keys of
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
        1. If *segment* of *machine* has already been loaded, will not load
           again, just switch working lattice to be the *segment*; keyword
           parameter *re_load* could be set to force reload;
        2. *re_load* could be used if necessary, e.g. the configuration
           file for some segment is changed, etc.

        See Also
        --------
        use_lattice : Choose working lattice from loaded lattices.
        reload_lattice : Reload machine/lattice.
        """
        if machine is None:
            machine = self._machine

        if os.path.isdir(machine):
            machine = os.path.realpath(machine)

        if self._use_cached(segment, machine, re_load=kws.get('re_load', False)):
            mach_name = os.path.basename(machine)
            mach_conf = self._machines.get(mach_name)['conf']
            mach_path = self._machines.get(mach_name)['path']
            lat_name = segment
            lat_conf = self._lattices.get(lat_name)
            retval = {'lat0name': lat_name,
                      'lattices': {lat_name: lat_conf},
                      'machname': mach_name,
                      'machpath': mach_path,
                      'machconf': mach_conf}
            self._last_mach_name = mach_name
            self._last_mach_conf = mach_conf
            self._last_mach_path = mach_path
            self._last_lattice_name = lat_name
            self._last_lattice_conf = lat_conf
            self._work_lattice_name = lat_name
            self._work_lattice_conf = lat_conf
            return retval

        try:
            retval = load_lattice(machine=machine, segment=segment, **kws)

            lat_all = retval['lattices']
            lat_name = retval['lat0name']
            lat_conf = lat_all.get(lat_name)
            mach_name = retval['machname']
            mach_conf = retval['machconf']
            mach_path = retval['machpath']

            self._lattices.update(lat_all)
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
            _LOGGER.error(f"Cannot load machine: {machine} segment: {segment}")
            retval = None
        finally:
            self._last_load_success = retval is not None
        return retval

    def combined_lattice(self):
        """Combine all loaded lattice(s) into one Lattice to return.
        """
        if len(self.lattice_names) <= 1:
            return self.work_lattice_conf
        else:
            return reduce(lambda x,y:x+y, self.lattices.values())

    def print_all_properties(self):
        """Print all properties, for debug only.
        """
        for attr in ['lattice_names', 'machine_names',
                     'last_machine_name',
                     'last_machine_path', 'last_lattice_name',
                     # 'last_lattice_conf',
                     'last_machine_conf']:
            print(f"{attr:<17s} : {getattr(self, attr)}")

    def _use_cached(self, segment, machine, **kws):
        """Test if continue parsing procedure is needed, if machine/segment
        is already parsed, just return value, or do parsing; if *re_load*
        keyword is True, always return False.
        """
        machine = os.path.basename(machine)
        _f_reload = kws.get('re_load')
        if machine in self._machine_names and segment in self._lattice_names:
            if _f_reload:
                _LOGGER.warning(f"Force reload machine: '{machine}', segment: '{segment}'")
                retval = False
            else:
                _LOGGER.warning(f"Use cached results for machine: '{machine}', segment: '{segment}'")
                retval = True
        else:
            if segment is None:
                _LOGGER.warning(f"Load new machine: '{machine}', with default segment")
            else:
                _LOGGER.info(f"Load new machine: '{machine}', segment: '{segment}'")
            retval = False
        return retval

    def reload_lattice(self, segment=None, machine=None, **kws):
        """Reload machine lattice, if parameters *machine* and *segment* are
        not defined, reload last loaded one.

        Parameters
        ----------
        segment : str
            Name of segment of machine.
        machine : str
            Name of machine, or path of configuration files.

        See Also
        --------
        load_lattice : Load machine/lattice from configuration files.
        """
        segment = self._last_lattice_name if segment is None else segment
        machine = self._last_mach_path if machine is None else machine
        return self.load_lattice(machine=machine,
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
            _LOGGER.info(f"Switch working lattice to: {lattice_name}.")
            self._work_lattice_name = lattice_name
            self._work_lattice_conf = self._lattices[lattice_name]
            return self._work_lattice_name
        else:
            _LOGGER.warning("Invalid lattice name, working lattice name unchanged.")
            return self._work_lattice_name

    def get_elements(self, latname=None, name=None, type=None, srange=None,
                     search_all=False,
                     **kws):
        """Get element(s) from working lattice.

        Parameters
        ----------
        latname : str
            Use the (valid) defined lattice name instead of current working
            lattice name, maybe useful to inspect non-working lattices.
        name : str or list[str]
            (List of) Element names or Unix shell style patterns.
        type : str or list[str]
            (List of) Element type/group/family, or Unix shell style patterns.
        srange : tuple
            Start and end points (tuple of float) of elements' longitudinal
            position.
        search_all : bool
            If True, search from all the loaded segments.

        Keyword Arguments
        -----------------
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
        Create MachinePortal instance, e.g. mp
        1. Define *name* with an invalid name:

        >>> mp.get_elements(name='NOEXISTS')
        []

        2. Define *name* with name or name patterns:

        >>> mp.get_elements(name='FS1_BMS:DCV_D2662')
        [FS1_BMS:DCV_D2662 [VCOR] @ sb=153.794690]
        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'], latname='LINAC')
        [LS1_BTS:DCV_D1937 [VCOR] @ sb=81.365954,
         LS1_BTS:DCV_D1964 [VCOR] @ sb=84.013954,
         LS1_BTS:DCV_D1997 [VCOR] @ sb=87.348954,
         LS1_BTS:DCV_D2024 [VCOR] @ sb=90.055166,
         LS1_BTS:DCV_D2061 [VCOR] @ sb=93.710487,
         LS1_BTS:DCV_D2114 [VCOR] @ sb=98.985556,
         FS1_BMS:DCV_D2662 [VCOR] @ sb=153.794690,
         FS1_BMS:DCH_D2662 [HCOR] @ sb=153.794690,
         FS1_BMS:BPM_D2664 [BPM] @ sb=153.963690,
         FS1_BMS:QH_D2666 [QUAD] @ sb=154.144690]

        3. Filter BPMs from the above result:

        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'], type='BPM',
        >>>                 latname='LINAC')
        [FS1_BMS:BPM_D2664 [BPM] @ sb=153.963690]
        >>> # type='BPM' also could be be pattern

        4. Filter hybrid types:

        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'],
        >>>                 type=['BPM', 'QUAD'], latname='LINAC')
        [FS1_BMS:BPM_D2664 [BPM] @ sb=153.963690,
         FS1_BMS:QH_D2666 [QUAD] @ sb=154.144690]

        5. Get subsection from lattice according to s-position range:

        >>> mp.get_elements(srange=(10, 11))
        [LS1_CB01:CAV1_D1229 [CAV] @ sb=10.366596,
         LS1_CB01:BPM_D1231 [BPM] @ sb=10.762191,
         LS1_CB01:SOL1_D1235 [SOL] @ sb=10.894207]

        6. Continue filter with *srange* parameter

        >>> mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'],
        >>>                 type=['BPM', 'QUAD'], srange=(154, 155),
        >>>                 latname='LINAC')
        [FS1_BMS:QH_D2666 [QUAD] @ sb=154.144690]

        Note
        ----
        Select subsection by ``srange`` parameter is realized by new approach,
        other than ``~phantasy.library.Lattice.getLine()``, e.g. the result of
        ``getLine((10,11))`` contains element before the start range: i.e.
        ``LS1_WA03:PM_D1223:PM @ sb=9.929284``, which is beyond the range.

        See Also
        --------
        :func:`get_virtual_elements`
            Get virtual elements.
        :func:`next_elements`
            Get neighborhood of reference element.
        :class:`~phantasy.library.lattice.element.CaElement`
            Element class.
        """
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        elif search_all:
            elems = []
            for _, lat in self._lattices.items():
                elems.extend(
                    lat.get_elements(
                        name=name, type=type, srange=srange, **kws))
            return elems
        else:
            lat = self._work_lattice_conf
        return lat.get_elements(name=name, type=type, srange=srange, **kws)

    def next_elements(self, ref_elem, count=1, **kws):
        """Get elements w.r.t reference element, according to the defined
        confinement, from given lattice name, if not given *latname*, use
        the current working lattice.

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
            Include *ref_elem* in the returned list or not, False by default.

        Returns
        -------
        ret : List
            List of next located elements, ascendingly sorted by position, by
            default, only return one element (for eath *type*) that meets the
            confinement, return more by assgining *range* keyword parameter.

        Examples
        --------
        Create MachinePortal instance, e.g. mp

        1. Select an element as reference element:

        >>> print(all_e)
        [LS1_CA01:CAV1_D1127 [CAV] @ sb=0.207064,
         LS1_CA01:BPM_D1129 [BPM] @ sb=0.511327,
         LS1_CA01:SOL1_D1131 [SOL] @ sb=0.643330,
         LS1_CA01:DCV_D1131 [VCOR] @ sb=0.743330,
         LS1_CA01:DCH_D1131 [HCOR] @ sb=0.743330,
         LS1_CA01:CAV2_D1135 [CAV] @ sb=0.986724,
         LS1_CA01:CAV3_D1143 [CAV] @ sb=1.766370,
         LS1_CA01:BPM_D1144 [BPM] @ sb=2.070634,
         LS1_CA01:SOL2_D1147 [SOL] @ sb=2.202637,
         LS1_CA01:DCV_D1147 [VCOR] @ sb=2.302637,
         LS1_CA01:DCH_D1147 [HCOR] @ sb=2.302637,
         LS1_CA01:CAV4_D1150 [CAV] @ sb=2.546031,
         LS1_WA01:BPM_D1155 [BPM] @ sb=3.109095,
         LS1_CA02:CAV1_D1161 [CAV] @ sb=3.580158,
         LS1_CA02:BPM_D1163 [BPM] @ sb=3.884422,
         LS1_CA02:SOL1_D1165 [SOL] @ sb=4.016425,
         LS1_CA02:DCV_D1165 [VCOR] @ sb=4.116425,
         LS1_CA02:DCH_D1165 [HCOR] @ sb=4.116425,
         LS1_CA02:CAV2_D1169 [CAV] @ sb=4.359819,
         LS1_CA02:CAV3_D1176 [CAV] @ sb=5.139465,
         LS1_CA02:BPM_D1178 [BPM] @ sb=5.443728]
        >>> ref_elem = all_e[5]

        2. Get next element of *ref_elem*:

        >>> mp.next_elements(ref_elem)
        [LS1_CA01:CAV3_D1143 [CAV] @ sb=1.766370]

        3. Get last of the next two element:

        >>> mp.next_elements(ref_elem, count=2)
        [LS1_CA01:BPM_D1144 [BPM] @ sb=2.070634]

        4. Get all of the next two elements:

        >>> mp.next_elements(ref_elem, count=2, range='0::1')
        [LS1_CA01:CAV3_D1143 [CAV] @ sb=1.766370,
         LS1_CA01:BPM_D1144 [BPM] @ sb=2.070634]

        5. Get all of the two elements before *ref_elem*:

        >>> mp.next_elements(ref_elem, count=-2, range='0::1')
        [LS1_CA01:DCV_D1131 [VCOR] @ sb=0.743330,
         LS1_CA01:DCH_D1131 [HCOR] @ sb=0.743330]

        6. Get next two BPM elements after *ref_elem*, including itself:

        >>> mp.next_elements(ref_elem, count=2, type=['BPM'],
        >>>                  ref_include=True, range='0::1')
        [LS1_CA01:CAV2_D1135 [CAV] @ sb=0.986724,
         LS1_CA01:BPM_D1144 [BPM] @ sb=2.070634,
         LS1_WA01:BPM_D1155 [BPM] @ sb=3.109095]

        7. Get with hybrid types:

        >>> mp.next_elements(ref_elem, count=2, type=['BPM', 'CAV'],
        >>>                  range='0::1')
        [LS1_CA01:CAV3_D1143 [CAV] @ sb=1.766370,
         LS1_CA01:BPM_D1144 [BPM] @ sb=2.070634,
         LS1_CA01:CAV4_D1150 [CAV] @ sb=2.546031,
         LS1_WA01:BPM_D1155 [BPM] @ sb=3.109095]
        """
        latname = kws.get('latname')
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf
        return lat.next_elements(ref_elem, count, **kws)

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
        if isinstance(elem, CaElement):
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

    def get_all_types(self, latname=None, virtual=False, **kws):
        """Get names of element types (groups/families) from given lattice.

        Parameters
        ----------
        latname : str
            Name of lattice to be investigated.
        virtual : True or False
            Return virtual group or not, ``False`` by default.

        Returns
        -------
        ret : List(str)
            List of type names.

        See Also
        --------
        lattice_names : Names of all loaded lattices.
        get_all_names : Get all element names from given lattice.
        """
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf
        return lat.get_all_types(virtual, **kws)

    def get_all_names(self, latname=None, virtual=False, **kws):
        """Get names of all elements from  given lattice.

        Parameters
        ----------
        latname : str
            Name of lattice to be investigated.
        virtual : True or False
            Return virtual elements or not, ``False`` by default.

        Returns
        -------
        ret : List(str)
            List of element names.

        See Also
        --------
        lattice_names : Names of all loaded lattices.
        get_all_types : Get all element types from given lattice.
        """
        if latname in self._lattice_names:
            lat = self._lattices.get(latname)
        else:
            lat = self._work_lattice_conf
        return lat.get_all_names(virtual, **kws)

    def inspect_mconf(self, mconf=None, out=None):
        """Inspect given machine configuration.

        Parameters
        ----------
        mconf :
            Machine configuration object, if not given, inspect the last
            loaded machine.
        out :
            Output stream, if not given, only return results, or besides
            returning results, also print into defined stream,
            could be ``stdout``, ``file``(valid file object), or``StringIO``.

        Returns
        -------
        ret : dict or StringIO or None
            Inspection results, retur a dict when *out* is None,
            or StringIO object when *out* is ``sio``, or None;
            keys of dict:

            - ``path`` : (str), phantasy.ini fullpath
            - ``lattices`` : (list), all defined lattices
            - ``machine`` : (str), defined machine name
            - ``config`` : (dict), all configurations

        Examples
        --------
        >>> mconf = mp.inspect_mconf()
        >>> # write inspection results into file
        >>> with open('fileout.dat', 'w') as f:
        >>>     mconf = mp.inspect_mconf(out=f)
        >>> # out could be StringIO or sys.stdout or 'stdout'.

        See Also
        --------
        :class:`~phantasy.library.parser.config.Configuration`
        """
        if mconf is None:
            mconf = self._last_mach_conf

        if isinstance(mconf, Configuration):
            retval = MachinePortal.get_inspect_mconf(mconf)

            try:
                if out == 'stdout':
                    out = sys.stdout

                print('{0:<20s} : {1}'.format('machine config path', retval['path']),
                      file=out, end='\n')
                print('-' * 22, file=out, end='\n')
                print('{0:<20s} : {1}'.format('machine name', retval['machine']),
                      file=out, end='\n')
                print('-' * 22, file=out, end='\n')
                print('{0:<20s} : {1}'.format('All valid lattices', ' '.join(retval['lattices'])),
                      file=out, end='\n')
                d = retval['config']
                for sn in sorted(d):
                    print('-' * 22, file=out, end='\n')
                    print("Section - " + sn, file=out, end='\n')
                    print('-' * 22, file=out, end='\n')
                    for k, v in d[sn].items():
                        print("{0:<20s} : {1}".format(k, v), file=out, end='\n')
            except:
                _LOGGER.warning("Cannot output into stream defined by out.")
            finally:
                return retval
        else:
            _LOGGER.warning("Cannot inspect invalid machine configuration object.")
            return None

    @staticmethod
    def get_inspect_mconf(mconf):
        m_path = mconf.config_path
        m_name = m_path.split(os.sep)[-2]
        m_lats = mconf.getarray('COMMON', 'segments')
        m_dict = {sn: dict(mconf.items(sn)) for sn in mconf.sections()}
        return {'path': m_path, 'lattices': m_lats,
                'machine': m_name, 'config': m_dict}

    @staticmethod
    def get_pv_names(elem, field=None, **kws):
        """Get PV names by given fields for defined elements.

        Parameters
        ----------
        elem :
            (List of) CaElement objects.
        field : str or List(str)
            (List of) Field name of PV, if list of names is defined, only
            names shared by all elements are valid; if not defined, all
            shared fields will be used.

        Keyword Arguments
        -----------------
        handle : str
            Handle of pv, 'readback' (default), 'setpoint' or 'readset'.

        Returns
        -------
        ret : dict
            dict of PV names, with keys of field names.

        Examples
        --------
        1. Get all BPM and PM elements:

        >>> elem = mp.get_elements(type='*PM')

        2. Get all pv names with same field:

        >>> pv1 = mp.get_pv_names(elem) # {'X':[...], 'Y':[...]}

        3. Get define field(s):

        >>> pv2 = mp.get_pv_names(elem, 'X')
        >>> pv2 = mp.get_pv_names(elem, ['X'])

        4. Get all PV names from one elements:

        >>> pv3 = mp.get_pv_names(elem[0])
        >>> # return value example:
        {u'ENG': [u'V_1:LS1_CA01:BPM_D1129:ENG_RD'],
         u'PHA': [u'V_1:LS1_CA01:BPM_D1129:PHA_RD'],
         u'X': [u'V_1:LS1_CA01:BPM_D1129:X_RD'],
         u'Y': [u'V_1:LS1_CA01:BPM_D1129:Y_RD']}

        See Also
        --------
        :func:`get_pv_values`
            Get PV values.
        :func:`~phantasy.library.pv.readback.get_readback`
            Get PV readbacks.
        :class:`~phantasy.library.lattice.element.CaElement`
            Element class.
        """
        if not isinstance(elem, (list, tuple)):
            if not isinstance(elem, CaElement):
                _LOGGER.warning("Invalid CaElement.")
                return None
            elem = elem,
        else:
            if not isinstance(elem[0], CaElement):
                _LOGGER.warning("Invalid CaElements.")
                return None

        all_fields = reduce(intersect1d, [e.fields for e in elem])
        if field is None:
            field = all_fields
        else:
            if not isinstance(field, (list, tuple)):
                field = field,
            field = [f for f in field if f in all_fields]

        handle = kws.get('handle', 'readback')
        return {f: [e.pv(field=f, handle=handle)[0] for e in elem]
                for f in field}

    @staticmethod
    def get_pv_values(elem, field=None, **kws):
        """Get PV readback values by given fields for defined elements.

        Parameters
        ----------
        elem :
            (List of) CaElement objects.
        field : str or List(str)
            (List of) Field name of PV, if list of names is defined, only
            names shared by all elements are valid; if not defined, all
            shared fields will be used.

        Returns
        -------
        ret : dict
            dict of PV readback values, with keys of field names.

        Examples
        --------
        >>> # get all BPM and PM elements
        >>> elem = mp.get_elements(type='*PM')
        >>> # get 'X' and 'Y' pv readback values
        >>> data = mp.get_pv_values(elem, ['X','Y'])
        >>> data.keys()
        ['Y', 'X']

        See Also
        --------
        :func:`get_pv_names`
            Get PV names.
        :func:`~phantasy.library.pv.readback.get_readback`
            Get PV readbacks.
        """
        pv_names = MachinePortal.get_pv_names(elem, field, handle='readback')
        pv_values = get_readback(pv_names)
        return pv_values

    def sync_settings(self, ):
        pass

    def roll_back(self, ):
        pass

    def update_model_settings(self, ):
        pass

    def get_all_segment_names(self):
        """Return all available segment names.
        """
        config = self.machines[self.last_machine_name].get('conf')
        return config.get(INI_DICT['COMMON_SECTION_NAME'],
                          INI_DICT['KEYNAME_SEGMENTS']).split()

    def __repr__(self):
        return 'MachinePortal({!r}, {!r})'.format(
                    self.last_machine_name,
                    self.last_lattice_name)

    def _repr_pretty_(self, p, cycle):
        p.text(str(self))

    def __str__(self):
        if not self.last_load_success:
            return "[{}] MachinePortal cannot be initialized.".format(self._machine)
        all_segments = self.get_all_segment_names()
        wl_name = self.work_lattice_name
        idx = all_segments.index(wl_name)
        all_segments.remove(wl_name)
        all_segments.insert(idx, '*{}'.format(wl_name))
        return "[{mname}] MachinePortal | Valid segment: {msects}".format(
                    mname=self.last_machine_name,
                    msects=', '.join(all_segments))
