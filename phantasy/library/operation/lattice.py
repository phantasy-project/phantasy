#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Lattice operations, including: loading
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging
import os

from phantasy.library.parser import find_machine_config
from phantasy.library.parser import Configuration
from phantasy.library.layout import build_layout
from phantasy.library.settings import Settings
from phantasy.library.pv import DataSource
from phantasy.library.misc import simplify_data
from phantasy.library.lattice import merge
from phantasy.library.lattice import CaElement
from phantasy.library.lattice import Lattice

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)

# HLA MARCOs
HLA_TAG_PREFIX = 'phyutil'
HLA_TAG_SYS_PREFIX = HLA_TAG_PREFIX + '.sys'
HLA_VFAMILY = 'HLA:VIRTUAL'

# submachines and default_submachine
KEYNAME_SUBMACHINES = "submachines"
KEYNAME_DEFAULT_SUBMACHINE = "default_submachine"

# root directory for output data
KEYNAME_OUTPUT_DATA_DIR = 'output_dir'
DEFAULT_OUTPUT_DATA_DIR = "~/data"

# scan server address
KEYNAME_SCAN_SVR_URL = 'ss_url'
DEFAULT_SCAN_SVR_URL = None

# simulating code, or model
KEYNAME_MULATION_CODE = 'model'
DEFAULT_SIMULATION_CODE = None

# model data dir, extra resources to support simulation
KEYNAME_MODEL_DATA_DIR = 'model_data_dir'
DEFAULT_MODEL_DATA_DIR = os.path.join(DEFAULT_OUTPUT_DATA_DIR, 'model')

# config file, e.g. phyutil.cfg
KEYNAME_CONFIG_FILE = 'config_file'
DEFAULT_CONFIG_FILE = None

# lattice layout file
KEYNAME_LAYOUT_FILE = 'layout_file'
DEFAULT_LAYOUT_FILE = None

# lattice settings file
KEYNAME_SETTINGS_FILE = 'settings_file'
DEFAULT_SETTINGS_FILE = None

# channel finder server address
KEYNAME_CF_SVR_URL = 'cfs_url'
DEFAULT_CF_SVR_URL = None

# channel finder tag
# tagging rule: phyutil.sys.{LATTICE}, e.g. phyutil.sys.LINAC
KEYNAME_CF_SVR_TAG = 'cfs_tag'
DEFAULT_CF_SVR_TAG =  lambda x: '{0}.{1}'.format(HLA_TAG_SYS_PREFIX, x)

# machine type, loop (1) or not (0)
KEYNAME_MTYPE = 'loop'
DEFAULT_MTYPE = 0

# the properties used for initializing Element are different from those defined
# by cfs or sqlite, re-name property to Element property may needed.
_cf_map = {'elemName' : 'name',
           'elemField': 'field',
           'elemType' : 'family',
           'elemHandle' : 'handle',
           'elemIndex' : 'index',
           'elemPosition' : 'se',
           'elemLength' : 'length',
           ##
           'system' : 'system',
           'devName' : 'devname',
           'elemGroups' : 'groups',
}


def load_lattice(facility, segment=None, **kwargs):
    """Load segment lattice from facility.

    Parameters
    ----------
    facility : str
        The exact name of facility/machine.
    segment : str
        Default '*', Unix shell pattern to define lattice/submachine.

    Keyword Arguments
    -----------------
    use_cache : bool
        Use cache or not, ``False`` by default.
    save_cache : bool
        Save cache or not, ``False`` by default.
    verbose : int
        If not 0, show output, 0 by default.
    return_lattices : bool
        Return lattices or not, ``False`` by default.
    return_more : bool
        Return more information, ``False`` by default,
        if set True, return information as a dict.

    Note
    ----
    *facility* can be a path to config dir.
    """
    lat_dict = {}

    use_cache = kwargs.get('use_cache', False)
    save_cache = kwargs.get('save_cache', False)
    verbose = kwargs.get('verbose', 0)
    return_lattices = kwargs.get('return_lattices', False)
    return_more = kwargs.get('return_more', False)

    if use_cache:
        try:
            loadCache(machine)
        except:
            _LOGGER.error('Lattice initialization using cache failed. ' +
                  'Will attempt initialization with other method(s).')
            save_cache = True
        else:
            # Loading from cache was successful.
            return
    
    mconfig, mdir, mname = find_machine_config(facility, verbose=verbose)

    d_common = dict(mconfig.items("COMMON"))
    output_data_dir = d_common.get(KEYNAME_OUTPUT_DATA_DIR,
                                   os.path.expanduser(DEFAULT_OUTPUT_DATA_DIR))
    # the default submachine
    accdefault = d_common.get(KEYNAME_DEFAULT_SUBMACHINE, "")
    if submachine is None:
        submachine = accdefault

    # for all submachines specified in INI and matches the pattern
    msects = [subm for subm in re.findall(r'\w+', d_common.get(KEYNAME_SUBMACHINES, ""))
                if fnmatch.fnmatch(subm, submachine)]

    for msect in msects:
        d_msect = dict(mconfig.items(msect))

        # scan server
        scan_svr_url = d_msect.get(KEYNAME_SCAN_SVR_URL, DEFAULT_SCAN_SVR_URL)

        # model: code
        simulation_code = d_msect.get(KEYNAME_SIMULATION_CODE, DEFAULT_SIMULATION_CODE)
        if simulation_code is not None:
            simulation_code = simulation_code.upper()

        # model: data
        model_data_dir = d_msect.get(KEYNAME_MODEL_DATA_DIR, DEFAULT_MODEL_DATA_DIR)
        if model_data_dir is not None:
            model_data_dir = os.path.expanduser(model_data_dir)

        # config file
        config_file = d_msect.get(KEYNAME_CONFIG_FILE, DEFAULT_CONFIG_FILE)
        if config_file is not None:
            if not os.path.isabs(config_file):
                config_file = os.path.join(mdir, config_file)
            config = Configuration(config_file)
        else:
            raise RuntimeError("Lattice configuration for '%s' not specified" % (msect,))

        # layout file
        layout_file = d_msect.get(KEYNAME_LAYOUT_FILE, DEFAULT_LAYOUT_FILE)
        if layout_file is not None:
            if not os.path.isabs(layout_file):
                layout_file = os.path.join(mdir, layout_file)
            layout = build_layout(layoutPath=layout_file)
        else:
            raise RuntimeError("Layout for '%s' not specified" % (msect,))

        # settings file
        settings_file = d_msect.get(KEYNAME_SETTINGS_FILE, DEFAULT_SETTINGS_FILE)
        if settings_file is not None:
            if not os.path.isabs(settings_file):
                settings_file = os.path.join(mdir, settings_file)
            settings = Settings(settingsPath=settings_file)
        else:
            raise RuntimeError("Settings for '%s' not specified" % (msect,))

        # machine type, linear (non-loop) or ring (loop)
        mtype = int(d_msect.get(KEYNAME_MTYPE, DEFAULT_MTYPE))

        # channel finder service: address
        cf_svr_url = d_msect.get(KEYNAME_CF_SVR_URL, DEFAULT_CF_SVR_URL)
        if cf_svr_url is None:
            raise RuntimeError("No accelerator data source (cfs_url) available")

        # channel finder service: tag
        cf_svr_tag = d_msect.get(KEYNAME_CF_SVR_TAG, DEFAULT_CF_SVR_TAG(msect))
        ds_sql_path = os.path.join(mdir, cf_svr_url)

        if re.match(r"https?://.*", cf_svr_url, re.I):
            # pv data source is cfs
            _LOGGER.info("Using Channel Finder Service '%s' for '%s'" % (cf_svr_url, msect))
            ds = DataSource(source=cf_svr_url)
        elif os.path.isfile(ds_sql_path):
            # pv data source is sqlite
            _LOGGER.info("Using SQlite instead of CFS '%s'" % ds_sql_path)
            ds = DataSource(source=ds_sql_path)
        else:
            _LOGGER.warn("Invalid CFS is defined.")
            raise RuntimeError("Unknown channel finder source '%s'" % cf_svr_url)

        ds.get_data(tag_filter=cf_svr_tag)
        ds.map_property_name(_cf_map)

        # build lattice from PV data
        latname = msect
        pv_data = simplify_data(ds.pvdata)
        tag = cf_svr_tag
        src = ds.source
        lat = create_lattice(latname, pv_data, tag, src, mtype=machinetype,
                             simulation=simulation_code,
                             layout=layout, config=config, settings=settings)
        
#         if IMPACT_ELEMENT_MAP is not None:
#             lat.createLatticeModelMap(IMPACT_ELEMENT_MAP)

        lat.sb = float(d_msect.get("s_begin", 0.0))
        lat.se = float(d_msect.get("s_end", 0.0))
        lat.loop = bool(d_msect.get("loop", True))
        lat.machine = machname
        lat.machdir = machdir
        if d_msect.get("archive_pvs", None):
            lat.arpvs = os.path.join(machdir, d_msect["archive_pvs"])
        lat.OUTPUT_DIR = tempfile.mkdtemp("_phyutil_output")
        _LOGGER.info("Temp output directory: {}".format(lat.OUTPUT_DIR))
        _temp_dirs.append(lat.OUTPUT_DIR);

        # TODO add unit conversion information later
        # unit conversion & physics data to be added later
        # uconvfile = d_msect.get("unit_conversion", None)
        # if uconvfile is not None:
        #     _logger.info("loading unit conversion '%s'" % uconvfile)
        #     loadUnitConversion(lat, machdir, uconvfile.split(", "))
        #
        # physics_data = d_msect.get("physics_data", None)
        # if physics_data is not None:
        #     _logger.info("loading physics data '%s'" % physics_data)
        #     phy_fname = os.path.join(machdir, physics_data)
        #     lat.ormdata = OrmData(phy_fname, "OrbitResponseMatrix")
        #     lat._twiss = TwissData(phy_fname)
        #     lat._twiss.load(phy_fname, group="Twiss")
        #     setGoldenLattice(lat, phy_fname, "Golden")

        vex = lambda k: re.findall(r"\w+", d_msect.get(k, ""))
        vfams = { HLA_VBPM:  ('BPM',  vex("virtual_bpm_exclude")),
                  HLA_VPM:   ('PM',   vex("virtual_pm_exclude")),
                  HLA_VHCOR: ('HCOR', vex("virtual_hcor_exclude")),
                  HLA_VVCOR: ('VCOR', vex("virtual_vcor_exclude")),
                  HLA_VCOR:  ('COR',  vex("virtual_cor_exclude")),
                  HLA_VBEND: ('BEND', vex("virtual_bend_exclude")),
                  HLA_VQUAD: ('QUAD', vex("virtual_quad_exclude")),
                  HLA_VSEXT: ('SEXT', vex("virtual_sext_exclude")),
                  HLA_VSOL:  ('SOL',  vex("virtual_sol_exclude")),
                  HLA_VSOL:  ('CAV',  vex("virtual_cav_exclude")),
        }
        
        createVirtualElements(lat, vfams)
        lat_dict[msect] = lat
        if verbose:
            nelems = len([e for e in lat.getElementList('*') if e.virtual == 0])
            if msect == accdefault:
                print("%s (*): %d elements" % (msect, nelems))
            else:
                print("%s: %d elements" % (msect, nelems))
            print("  BPM: %d, PM: %s, HCOR: %d, VCOR: %d, BEND: %d, QUAD: %d, SEXT: %d, SOL: %d, CAV: %d" % (
                len(lat.getElementList('BPM')), 
                len(lat.getElementList('PM')), 
                len(lat.getElementList('HCOR')),
                len(lat.getElementList('VCOR')),
                len(lat.getElementList('BEND')),
                len(lat.getElementList('QUAD')),
                len(lat.getElementList('SEXT')),
                len(lat.getElementList('SOL')),
                len(lat.getElementList('CAV')))
                )
    
    # set the default submachine, if no, use the first one
    lat0 = lat_dict.get(accdefault, None)
    if lat0 is None and len(lat_dict) > 0:
        machineavailable = sorted(lat_dict.keys())[0]
        _LOGGER.warn("Use '%s' instead of default submachine '%s'" % (machineavailable, accdefault))
        lat0 = lat_dict[machineavailable]

    if lat0 is None:
        raise RuntimeError("NO accelerator structures available")

    _lat = lat0
    _lattice_dict.update(lat_dict)
    if save_cache:
        selected_lattice_name = [k for (k,v) in _lattice_dict.iteritems()
                                 if _lat == v][0]
        saveCache(machine, _lattice_dict, selected_lattice_name)

    if return_lattices:
        if return_more:
            return {'lat_name': lat_dict.keys()[0],
                    'lat_conf': lat_dict.values()[0],
                    'mach_name': machname,
                    'mach_path': machdir,
                    'mach_conf': _machine_config}
        else:
            return lat0, lat_dict


def create_lattice(latname, pv_data, tag, src='channelfinder',
                   vbpm=True, vcor=True, **kwargs):
    """Create a lattice from PV data source.

    Parameters
    -----------
    latname : str
        Lattice/segment/submachine name, e.g. 'LINAC', 'LS1'.
    pv_data : list
        List of PV data, for each PV data, should be of list as: 
        ``string of PV name, dict of properties, list of tags``.
    tag : str
        Only select PV data according to defined tag. e.g. `phyutil.sys.LS1`.
    src : str
        Source of PV data, could be CFS url or sqlite file name,

    Keyword Arguments
    -----------------
    mtype : int
        Machine type, 0 for linear (default), 1 for a ring.

    Returns
    ---------
    lat : 
        Lattice object.

    See Also
    --------
    :class:`~phantasy.library.lattice.Lattice`
    :class:`~phantasy.library.pv.DataSource`
    """
    _LOGGER.debug("Creating lattice {0} from {1}".format(latname, src))
    _LOGGER.info("Found {0:d} PVs in {1}".format(len(pv_data), latname))
    
    # parameters
    mtype = kwargs.get('mtype', 0)
    
    # create a new lattice
    lat = Lattice(latname, source=src, mtype=mtype, **kwargs)
    for pv_name, pv_props, pv_tags in pv_data:
        _LOGGER.debug("Processing {0}".format(pv_name))

        # skip if property is None
        if pv_props is None: 
            continue

        # skip if tag does not match
        if pv_name and tag not in pv_tags:
            _LOGGER.debug("{0} is not tagged as {1}".format(pv_name, tag))
            continue
        
        # element name is mandatory ('elemName' -> 'name')
        if 'name' not in pv_props:
            continue
        name = pv_props.get('name')

        # begin and end s position
        if 'se' in pv_props:
            pv_props['sb'] = float(pv_props['se']) - float(pv_props.get('length', 0))

        # add element only if the element does not exist
        elem = lat._find_exact_element(name=name)
        if elem is None:
            try:
                elem = CaElement(**pv_props)
                gl = [g.strip() for g in pv_props.get('groups', [])]
                elem.group.update(gl)
            except:
                _LOGGER.error("Error: creating element '{0}' with '{1}'".format(name, pv_props))
                raise

            _LOGGER.debug("Created new element: '{0}'".format(name))
            lat.insertElement(elem)
        else:
            _LOGGER.debug("Using existed element '{0}'".format(name))

        # mark element virtual (1) or not (0, default)
        if HLA_VFAMILY in pv_props.get('group', []): 
            elem.virtual = 1

        handle = pv_props.get('handle', '').lower()
        ## legacy code, present code will not be 'get' or 'put'
        if handle == 'get': 
            pv_props['handle'] = 'readback'
        elif handle == 'put': 
            pv_props['handle'] = 'setpoint'

        # update elment attributes
        if pv_name: 
            elem.updatePvRecord(pv_name, pv_props, pv_tags)

    # group info is a redundant info, needs rebuild based on each element
    lat.buildGroups()

    # !IMPORTANT! since Channel finder has no order, but lat class has
    lat.sortElements()
    lat.circumference = lat[-1].se if lat.size() > 0 else 0.0

    _LOGGER.debug("Mode {0}".format(lat.mode))
    _LOGGER.info("'{0:s}' has {1:d} elements".format(lat.name, lat.size()))
    for g in sorted(lat._group.keys()):
        _LOGGER.debug("Lattice '%s' group %s(%d)" % (
                lat.name, g, len(lat._group[g])))

    return lat

