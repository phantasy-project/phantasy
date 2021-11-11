#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Lattice operations, including:
    1. loading lattice
    2. creating lattice
"""

import logging
import os
import re
import time
from fnmatch import fnmatch

from phantasy.facility.frib import INI_DICT
from phantasy.library.lattice import CaElement
from phantasy.library.lattice import Lattice
from phantasy.library.misc import simplify_data
from phantasy.library.misc import create_tempdir
from phantasy.library.parser import find_machine_config
from phantasy.library.parser import read_polarity
from phantasy.library.parser import read_alignment_data
from phantasy.library.pv import DataSource
#from phantasy.library.layout import build_layout
from phantasy.library.parser import Configuration
#from phantasy.library.settings import Settings
from unicorn.utils import UnicornData


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams, "\
                "Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)

DEFAULT_MODEL_DATA_DIR = 'model_data'


def load_lattice(machine, segment=None, **kws):
    """Load segment lattice(s) from machine.

    Parameters
    ----------
    machine : str
        The exact name of machine.
    segment : str
        Unix shell pattern to define segment of machine, if not defined,
        will use default segment defined in configuration file.

    Keyword Arguments
    -----------------
    use_cache : bool
        Use cache or not, ``False`` by default.
    save_cache : bool
        Save cache or not, ``False`` by default.
    verbose : int
        If not 0, show output, 0 by default.
    sort : True or False
        Sort lattice with s-position or not, default is False.
    prefix : str
        String prefix to all channels, this parameter is crucial to the
        virtual accelerator (VA) modeling, when '--pv-prefix' argument is
        used when starting up the VA rather than the one defined in the
        configuration file (e.g. phantasy.cfg). If this parameter is not
        defined, will use the one defined by 'machine' in 'DEFAULT' section
        of configuration file.
    auto_monitor : bool
        If set True, initialize all channels auto subscribe, default is False.

    Returns
    -------
    ret : dict
        Keys or returned dict:
        - lat0name: name of lattice, default_segment or first sorted key;
        - lattices: dict of loaded lattice(s);
        - machname: name of the machine;
        - machpath: full path of machine;
        - machconf: loaded machine configuration object.

    Note
    ----
    *machine* can be a path to config dir.
    """
    lat_dict = {}

    use_cache = kws.get('use_cache', False)
    save_cache = kws.get('save_cache', False)
    verbose = kws.get('verbose', 0)
    sort_flag = kws.get('sort', False)
    pv_prefix = kws.get('prefix', None)
    auto_monitor = kws.get('auto_monitor', False)

    # if use_cache:
    #    try:
    #        loadCache(machine)
    #    except:
    #        _LOGGER.error('Lattice initialization using cache failed. ' +
    #              'Will attempt initialization with other method(s).')
    #        save_cache = True
    #    else:
    #        # Loading from cache was successful.
    #        return

    mconfig, mdir, mname = find_machine_config(machine, verbose=verbose,
                                               filename=INI_DICT['INI_NAME'])

    d_common = dict(mconfig.items(INI_DICT['COMMON_SECTION_NAME']))
    root_data_dir = d_common.get(INI_DICT['KEYNAME_ROOT_DATA_DIR'],
                                 INI_DICT['DEFAULT_ROOT_DATA_DIR'])
    # create root_data_dir/today(fmt. YYYY-MM-DD)
    today_dir_name = os.path.expanduser(os.path.join(
        root_data_dir, time.strftime("%Y%m%d", time.localtime())))
    if not os.path.exists(today_dir_name):
        os.makedirs(today_dir_name)
    work_dir = today_dir_name

    # default segment and all segments defined in phantasy.ini file
    default_segment = d_common.get(INI_DICT['KEYNAME_DEFAULT_SEGMENT'],
                                   INI_DICT['DEFAULT_DEFAULT_SEGMENT'])
    all_segments = d_common.get(INI_DICT['KEYNAME_SEGMENTS'],
                                INI_DICT['DEFAULT_SEGMENTS'])
    if segment is None:
        segment = default_segment

    _LOGGER.info("Loading segment: '{}'".format(segment))

    # filter out valid segment(s) from 'segment' string or pattern.
    msects = [s for s in re.findall(r'\w+', all_segments)
              if fnmatch(s, segment)]

    for msect in msects:
        d_msect = dict(mconfig.items(msect))

        # scan server
        scan_svr_url = d_msect.get(INI_DICT['KEYNAME_SCAN_SVR_URL'],
                                   INI_DICT['DEFAULT_SCAN_SVR_URL'])

        # model: code
        simulation_code = d_msect.get(INI_DICT['KEYNAME_SIMULATION_CODE'],
                                      INI_DICT['DEFAULT_SIMULATION_CODE'])
        if simulation_code is not None:
            simulation_code = simulation_code.upper()

        # model: data
        model_data_dir = d_msect.get(INI_DICT['KEYNAME_MODEL_DATA_DIR'],
                                     DEFAULT_MODEL_DATA_DIR)
        if model_data_dir is not None:
            model_data_dir = os.path.expanduser(
                os.path.join(work_dir, model_data_dir))

        # config file
        config_file = d_msect.get(INI_DICT['KEYNAME_CONFIG_FILE'],
                                  INI_DICT['DEFAULT_CONFIG_FILE'])
        if config_file is not None:
            if not os.path.isabs(config_file):
                config_file = os.path.join(mdir, config_file)
            config = Configuration(config_file)
        else:
            raise RuntimeError("Lattice configuration for '%s' not specified" %
                               (msect,))

        # # layout file
        # layout_file = d_msect.get(INI_DICT['KEYNAME_LAYOUT_FILE'],
        #                          INI_DICT['DEFAULT_LAYOUT_FILE'])
        # if layout_file is not None:
        #    if not os.path.isabs(layout_file):
        #        layout_file = os.path.join(mdir, layout_file)
        #    layout = build_layout(layoutPath=layout_file)
        # else:
        #    raise RuntimeError("Layout for '%s' not specified" % (msect,))

        # # settings file
        # settings_file = d_msect.get(INI_DICT['KEYNAME_SETTINGS_FILE'],
        #                             INI_DICT['DEFAULT_SETTINGS_FILE'])
        # if settings_file is not None:
        #     if not os.path.isabs(settings_file):
        #         settings_file = os.path.join(mdir, settings_file)
        #     settings = Settings(settingsPath=settings_file)
        # else:
        #     raise RuntimeError("Settings for '%s' not specified" % (msect,))

        # unicorn_file
        udata_file = d_msect.get('unicorn_file', None)
        if udata_file is not None:
            if not os.path.isabs(udata_file):
                udata_file = os.path.join(mdir, udata_file)
            udata = {}
            for f in UnicornData(udata_file).functions:
                _d = udata.setdefault(f.ename, {})
                _d[(f.from_field, f.to_field)] = f.code
            _LOGGER.info("UNICORN policy will be loaded from {}.".format(
                os.path.abspath(udata_file)))
        else:
            udata = None  # no unicorn data provided
            _LOGGER.warning("Default UNICORN policy will be applied.")

        # misalignment_file
        alignment_data_file = d_msect.get('alignment_file', None)
        if alignment_data_file is not None:
            if not os.path.isabs(alignment_data_file):
                alignment_data_file = os.path.join(mdir, alignment_data_file)
            alignment_data = read_alignment_data(alignment_data_file)
            _LOGGER.info("Read alignment data from {}.".format(
                os.path.abspath(alignment_data_file)))
        else:
            alignment_data = None
            _LOGGER.warning("No aligment data is read.")

        # polarity_file
        pdata_file = d_msect.get('polarity_file', None)
        if pdata_file is not None:
            if not os.path.isabs(pdata_file):
                pdata_file = os.path.join(mdir, pdata_file)
            pdata = read_polarity(pdata_file)
            _LOGGER.info("Device polarity data is loaded from {}.".format(
                os.path.abspath(pdata_file)))
        else:
            pdata = None
            _LOGGER.warning("Default device polarity will be applied.")

        # machine type, linear (non-loop) or ring (loop)
        mtype = int(d_msect.get(INI_DICT['KEYNAME_MTYPE'],
                                INI_DICT['DEFAULT_MTYPE']))

        # channel finder service: address
        cf_svr_url = d_msect.get(INI_DICT['KEYNAME_CF_SVR_URL'],
                                 INI_DICT['DEFAULT_CF_SVR_URL'])
        if cf_svr_url is None:
            raise RuntimeError(
                "No accelerator data source (cfs_url) available")
        ds_sql_path = os.path.join(mdir, cf_svr_url)

        # channel finder service: tag, and property names
        cf_svr_tag0 = d_msect.get(INI_DICT['KEYNAME_CF_SVR_TAG'],
                                  INI_DICT['DEFAULT_CF_SVR_TAG'](msect))
        cf_svr_prop0 = d_msect.get(INI_DICT['KEYNAME_CF_SVR_PROP'],
                                  INI_DICT['DEFAULT_CF_SVR_PROP'])
        cf_svr_tag = [s.strip() for s in cf_svr_tag0.split(',')]
        cf_svr_prop = [s.strip() for s in cf_svr_prop0.split(',')]

        if re.match(r"https?://.*", cf_svr_url, re.I):
            # pv data source is cfs
            _LOGGER.info("Loading PV data from CFS: '%s' for '%s'" %
                         (cf_svr_url, msect))
            ds = DataSource(source=cf_svr_url)
        elif os.path.isfile(ds_sql_path):
            # pv data source is sqlite/csv file
            _LOGGER.info("Loading PV data from CSV/SQLite: {}".format(
                os.path.abspath(ds_sql_path)))
            ds = DataSource(source=ds_sql_path)
        else:
            _LOGGER.warning("Invalid PV data source is defined.")
            raise RuntimeError("Unknown PV data source '%s'" %
                               cf_svr_url)

        ds.get_data(tag_filter=cf_svr_tag, prop_filter=cf_svr_prop)
        ds.map_property_name(INI_DICT['CF_NAMEMAP'])

        # model data temp directory
        if not os.path.exists(model_data_dir):
            os.makedirs(model_data_dir)
        data_dir = create_tempdir(prefix="data_", dir=model_data_dir)
        _LOGGER.info("Model data directory: {}".format(data_dir))

        # build lattice from PV data
        latname = msect
        pv_data = simplify_data(ds.pvdata)
        tag = cf_svr_tag
        src = ds.source
        lat = create_lattice(latname,
                             pv_data,
                             tag,
                             source=src,
                             mtype=mtype,
                             mname=mname,
                             mpath=mdir,
                             mconf=mconfig,
                             model=simulation_code,
                             #layout=layout,
                             config=config,
                             #settings=settings,
                             udata=udata,
                             pdata=pdata,
                             alignment_data=alignment_data,
                             data_dir=data_dir,
                             sort=sort_flag,
                             prefix=pv_prefix,
                             auto_monitor=auto_monitor)

        #         if IMPACT_ELEMENT_MAP is not None:
        #             lat.createLatticeModelMap(IMPACT_ELEMENT_MAP)

        lat.loop = bool(d_msect.get(INI_DICT['KEYNAME_MTYPE'],
                                    INI_DICT['DEFAULT_MTYPE']))

        lat_dict[msect] = lat
        # if show more informaion
        if verbose:
            n_elems = len(
                [e for e in lat._get_element_list('*') if e.virtual == 0])
            if msect == default_segment:
                print("%s (*): %d elements" % (msect, n_elems))
            else:
                print("%s: %d elements" % (msect, n_elems))
            print(
                "  BPM: %d, PM: %s, HCOR: %d, VCOR: %d, BEND: %d, QUAD: %d, SEXT: %d, SOL: %d, CAV: %d"
                % (len(lat._get_element_list('BPM')),
                   len(lat._get_element_list('PM')),
                   len(lat._get_element_list('HCOR')),
                   len(lat._get_element_list('VCOR')),
                   len(lat._get_element_list('BEND')),
                   len(lat._get_element_list('QUAD')),
                   len(lat._get_element_list('SEXT')),
                   len(lat._get_element_list('SOL')),
                   len(lat._get_element_list('CAV'))))

    if default_segment in lat_dict:
        lat0name = default_segment
    else:
        lat0name = sorted(lat_dict.keys())[0]

    return {'lat0name': lat0name,
            'lattices': lat_dict,
            'machname': mname,
            'machpath': mdir,
            'machconf': mconfig}


def create_lattice(latname, pv_data, tag, **kws):
    """Create high-level lattice object from PV data source.

    Parameters
    -----------
    latname : str
        Name of segment of machine, e.g. 'LINAC', 'LS1'.
    pv_data : list
        List of PV data, for each PV data, should be of list as:
        ``string of PV name, dict of properties, list of tags``.
    tag : str
        Only select PV data according to defined tag. e.g.
        `phantasy.sys.LS1`.

    Keyword Arguments
    -----------------
    source : str
        Source of PV data, URL of channel finder service, file name of SQLite
        database or csv spreadsheet.
    mtype : int
        Machine type, 0 for linear (default), 1 for a ring.
    model : str
        Model code, 'FLAME' or 'IMPACT', 'FLAME' by default.
    udata : dict
        Scaling law functions, ename as the keys (1st level), (from_field, to_field) as 2nd level
        keys, function object as the values, i.e. {ename: {(f1, f2): fn1, ...}, ...}
    pdata : dict
        Device polarity, key-value pairs of device polarity.
    alignment_data : DataFrame
        Dataframe for alignment info, indexed by element name.
    data_dir: str
        Path of directory to host data generated from model, including input
        lattice files, output files and other related files, if not defined,
        random folder will be created in system temporary directory,
        e.g.'/tmp/model_hGe1sq'.
    #layout :
    #    Lattice layout object.
    config :
        Lattice configuration object.
    settings :
        Lattice settings object.
    sort : True or False
        Sort lattice with s-position or not, default is False.
    prefix : str
        String prefix to all channels, this parameter is crucial to the
        virtual accelerator (VA) modeling, when '--pv-prefix' argument is
        used when starting up the VA rather than the one defined in the
        configuration file (e.g. phantasy.cfg). If this parameter is not
        defined, will use the one defined by 'machine' in 'DEFAULT' section
        of configuration file.
    auto_monitor : bool
        If set True, initialize all channels auto subscribe, default is False.

    Returns
    ---------
    lat :
        High-level lattice object.

    Note
    ----
    Usually, *src* could be obtained from *source* attribute of ``DataSource``
    instance, which can handle general PV data source type, including: channel
    finder service, SQLite database, CSV file, etc.

    See Also
    --------
    :class:`~phantasy.library.lattice.lattice.Lattice`
        High-level lattice.
    :class:`~phantasy.library.pv.datasource.DataSource`
        Unified data source class for PVs.
    """
    udata = kws.get('udata', None)
    pdata = kws.get('pdata', None)
    alignment_data = kws.get('alignment_data', None)
    data_source = kws.get('source', None)
    prefix = kws.get('prefix', None)
    auto_monitor = kws.get('auto_monitor', False)

    config = kws.get('config', None)
    if config is not None:
        pv_prefix = config.get_default('machine')
    if prefix is not None:
        pv_prefix = prefix

    if data_source is None:
        _LOGGER.warning("PV data source type should be explicitly defined.")

    _LOGGER.debug("Creating lattice '{0}' from '{1}'.".format(latname, data_source))
    _LOGGER.info("Found {0:d} PVs in '{1}'.".format(len(pv_data), latname))

    if isinstance(tag, str):
        tag = tag,

    # create a new lattice
    lat = Lattice(latname, **kws)
    # set up lattice
    for pv_name, pv_props, pv_tags in pv_data:
        _LOGGER.debug("Processing {0}.".format(pv_name))

        # skip if property is None
        if pv_props is None:
            continue

        # skip if tag does not match
        if pv_name and not set(tag).issubset(set(pv_tags)):
            _LOGGER.debug("{0} is not tagged as {1}.".format(pv_name, tag))
            continue

        # element name is mandatory ('elemName' -> 'name')
        if 'name' not in pv_props:
            continue
        name = pv_props.get('name')

        # begin and end s position
        if 'se' in pv_props:
            pv_props['sb'] = float(pv_props['se']) \
                    - float(pv_props.get('length', 0.0))

        elem = lat._find_exact_element(name=name)
        if elem is None:
            try:
                elem = CaElement(**pv_props, auto_monitor=auto_monitor)
            except:
                _LOGGER.error(
                    "Error: creating element '{0}' with '{1}'.".format(
                        name, pv_props))
                raise RuntimeError("Creating element ERROR.")
            _LOGGER.debug("Created new element: '{0}'".format(name))
            lat.insert(elem, trust=True)
            _LOGGER.debug("Inserted {}".format(elem.name))
        else:
            _LOGGER.debug(
                "Element '{0}' exists, only update properties.".format(name))

        # update element
        if pv_name:
            # add prefix
            pv_name_prefixed = prefix_pv(pv_name, pv_prefix)
            # add 'u_policy' as keyword argument
            # this policy should created from unicorn_policy
            # new u_policy: {(f1, f2): fn1, ...} or None
            if udata is None:
                u_policy = {}
            else:
                u_policy = udata.get(elem.name, {})
            # polarity info
            polarity = get_polarity(elem.name, pdata)

            # alignment info
            alignment_series = get_alignment_series(elem.name, alignment_data)

            elem.process_pv(pv_name_prefixed, pv_props, pv_tags,
                            u_policy=u_policy, polarity=polarity,
                            alignment_series=alignment_series,
                            auto_monitor=auto_monitor)

    # update group
    lat.update_groups()

    # init design settings for all elements
    lat.load_settings(stype='design')

    # sort lattice or not
    if kws.get('sort', False):
        lat.sort(inplace=True)

    # lattice length
    lat.s_begin, lat.s_end, lat.length = lat.get_layout_length()

    # link layout elements to lattice elements
    lat.refresh_with_layout_info()

    _LOGGER.info("'{0:s}' has {1:d} elements".format(lat.name, lat.size()))
    return lat


def prefix_pv(pv, prefix):
    """Prefix *pv* with *prefix:* if *prefix* is not empty and None.
    """
    if pv.startswith('_#_'):
        return pv[3:]

    m = re.match("(.*:)?(.*):(.*):(.*)", pv)
    if m is None:
        chanprefix = prefix
    elif m.group(1) is None:
        chanprefix = prefix
    else:
        chanprefix = ''

    if chanprefix != '':
        return '{}:{}'.format(chanprefix, pv)
    else:
        return pv


def get_polarity(ename, pdata=None):
    """Get device polarity from *pdata*.
    """
    if pdata is None:
        return 1
    else:
        return pdata.get(ename, 1)


def get_alignment_series(ename, alignment_data=None):
    """Get a Series of alignment data from *alignment_data*.
    """
    if alignment_data is None:
        return None
    else:
        try:
            r = alignment_data.loc[ename]
        except KeyError:
            r = None
        finally:
            return r
