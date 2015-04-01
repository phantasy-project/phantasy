"""
Machine Structure Initialization
--------------------------------


In ``aphla`` one machine includes several accelerator structure,
e.g. "nsls2v2" is a machine with several submachine or lattice V1LTD, V1LTB,
V2SR.

Submachines are also called lattice in ``aphla``. Each lattice has a list of
elements, magnet or instrument. The submachines/lattices can share elements.
"""

# :author: Lingyun Yang <lyyang@bnl.gov>

from ..phylib.model.element import merge
from ..phylib.model import Lattice
from ..phylib.channelfinder import ChannelFinderAgent
from ..phylib.model.element import CaElement

import os
import time
import glob
import re
from pkg_resources import resource_string, resource_exists, resource_filename
import cPickle as pickle
import ConfigParser
import fnmatch
import logging
import numpy as np

_logger = logging.getLogger(__name__)

HLA_TAG_PREFIX = 'aphla'
HLA_TAG_SYS_PREFIX = HLA_TAG_PREFIX + '.sys'

#
HLA_VFAMILY = 'HLA:VIRTUAL'
HLA_VBPM   = 'HLA:VBPM'
HLA_VHCOR  = 'HLA:VHCOR'
HLA_VVCOR  = 'HLA:VVCOR'
HLA_VCOR   = 'HLA:VCOR'
HLA_VQUAD  = 'HLA:VQUAD'
HLA_VSEXT  = 'HLA:VSEXT'


# HOME = os.environ['HOME'] will NOT work on Windows,
# unless %HOME% is set on Windows, which is not the case by default.
_home_hla = os.path.join(os.path.expanduser('~'), '.aphla')
HLA_CONFIG_DIR = os.environ.get("APHLA_CONFIG_DIR", _home_hla)
HLA_DEBUG      = int(os.environ.get('APHLA_DEBUG', 0))
HLA_ROOT = os.environ.get("APHLA_ROOT", _home_hla)

# the properties used for initializing Element are different than
# ChannelFinderAgent (CFS or SQlite). This needs a re-map.
# convert from CFS property to Element property
_cf_map = {'elemName': 'name',
           'elemField': 'field',
           'devName': 'devname',
           'elemType': 'family',
           'elemGroups': 'groups',
           'elemHandle': 'handle',
           'elemIndex': 'index',
           'elemPosition': 'se',
           'elemLength': 'length',
           'system': 'system'
}


# keep all loaded lattice
_lattice_dict = {}

# the current lattice
_lat = None

def _findMachinePath(machine):
    # if machine is an abs path
    _logger.info("trying abs path '%s'" % machine)
    if os.path.isabs(machine) and os.path.isdir(machine):
        mname = os.path.basename(os.path.realpath(machine))
        return machine, mname
    # try "machine" in APHLA_CONFIG_DIR and ~/.aphla/ (default)
    _logger.info("trying path '%s' '%s'" % (HLA_CONFIG_DIR, machine))
    home_machine = os.path.join(HLA_CONFIG_DIR, machine)
    if os.path.isdir(home_machine):
        mname = os.path.basename(os.path.realpath(machine))
        return home_machine, mname
    # try the package
    pkg_machine = resource_filename(__name__, machine)
    _logger.info("trying system dir '%s'" % pkg_machine)
    if os.path.isdir(pkg_machine):
        mname = os.path.basename(os.path.realpath(pkg_machine))
        return pkg_machine, mname

    _logger.warn("can not find machine dir")
    return None, ""

def load(machine, submachine = "*", **kwargs):
    """
    load submachine lattices in machine.

    Parameters
    -----------
    machine: str. the exact name of machine
    submachine: str. default '*'. pattern of sub machines
    use_cache: bool. default False. use cache
    save_cache: bool. default False, save cache

    This machine can be a path to config dir.
    """

    global _lattice_dict, _lat

    lat_dict, lat0 = {}, None

    use_cache = kwargs.get('use_cache', False)
    save_cache = kwargs.get('save_cache', False)
    verbose = kwargs.get('verbose', 0)
    return_lattices = kwargs.get("return_lattices", False)

    if use_cache:
        try:
            loadCache(machine)
        except:
            _logger.error('Lattice initialization using cache failed. ' +
                  'Will attempt initialization with other method(s).')
            save_cache = True
        else:
            # Loading from cache was successful.
            return

    #importlib.import_module(machine, 'machines')
    machdir, machname = _findMachinePath(machine)
    if verbose:
        print "loading machine data '%s: %s'" % (machname, machdir)

    if machdir is None:
        msg = "can not find machine data directory for '%s'" % machine
        _logger.error(msg)
        raise RuntimeError(msg)

    _logger.info("importing '%s' from '%s'" % (machine, machdir))

    cfg = ConfigParser.ConfigParser()
    try:
        cfg.readfp(open(os.path.join(machdir, "aphla.ini"), 'r'))
        _logger.info("using config file: 'aphla.ini'")
    except:
        raise RuntimeError("can not open '%s' to read configurations" % (
                os.path.join(machdir, "aphla.ini")))

    d = dict(cfg.items("COMMON"))
    # set proper output directory in the order of env > aphla.ini > $HOME
    HLA_OUTPUT_DIR = os.environ.get("HLA_DATA_DIR",
                                    d.get("output_dir",
                                          os.path.expanduser('~')))
    # the default submachine
    accdefault = d.get("default_submachine", "")

    # print(cfg.sections())
    # for all submachines specified in INI and matches the pattern
    msects = [subm for subm in re.findall(r'\w+', d.get("submachines", ""))
             if fnmatch.fnmatch(subm, submachine)]
    # print(msect)
    for msect in msects:
        d = dict(cfg.items(msect))
        accstruct = d.get("cfs_url", None)
        if accstruct is None:
            raise RuntimeError("No accelerator data source (cfs_url) available "
                               "for '%s'" % msect)
        #print cfa.rows[:3]
        acctag = d.get("cfs_tag", "aphla.sys.%s" % msect)
        cfa = ChannelFinderAgent()
        accsqlite = os.path.join(machdir, accstruct)
        if re.match(r"https?://.*", accstruct, re.I):
            _logger.info("using CFS '%s' for '%s'" % (accstruct, msect))
            #cfa.downloadCfs(accstruct, property=[('elemName', '*'),
            #                                     ('iocName', '*')],
            #                tagName=acctag)
            cfa.downloadCfs(accstruct, property=[('elemName', '*'),], tagName=acctag)
        elif os.path.isfile(accsqlite):
            _logger.info("using SQlite '%s'" % accsqlite)
            cfa.loadSqlite(accsqlite)
        else:
            _logger.warn("NOT CFS '%s'" % accstruct)
            _logger.warn("NOT SQlite '%s'" % accsqlite)
            raise RuntimeError("Unknown accelerator data source '%s'" % accstruct)

        cfa.splitPropertyValue('elemGroups')
        cfa.splitChainedElement('elemName')
        for k,v in _cf_map.iteritems(): cfa.renameProperty(k, v)

        #print "New CFA:", cfa.rows

        lat = createLattice(msect, cfa.rows, acctag, cfa.source)
        lat.sb = float(d.get("s_begin", 0.0))
        lat.se = float(d.get("s_end", 0.0))
        lat.loop = bool(d.get("loop", True))
        lat.machine = machname
        lat.machdir = machdir
        if d.get("archive_pvs", None):
            lat.arpvs = os.path.join(machdir, d["archive_pvs"])
        lat.OUTPUT_DIR = d.get("output_dir",
                               os.path.join(HLA_OUTPUT_DIR, msect))

        # unit conversion & physics data to be added later
        # uconvfile = d.get("unit_conversion", None)
        # if uconvfile is not None:
        #     _logger.info("loading unit conversion '%s'" % uconvfile)
        #     loadUnitConversion(lat, machdir, uconvfile.split(", "))
        #
        # physics_data = d.get("physics_data", None)
        # if physics_data is not None:
        #     _logger.info("loading physics data '%s'" % physics_data)
        #     phy_fname = os.path.join(machdir, physics_data)
        #     lat.ormdata = OrmData(phy_fname, "OrbitResponseMatrix")
        #     lat._twiss = TwissData(phy_fname)
        #     lat._twiss.load(phy_fname, group="Twiss")
        #     setGoldenLattice(lat, phy_fname, "Golden")

        vex = lambda k: re.findall(r"\w+", d.get(k, ""))
        vfams = { HLA_VBPM:  ('BPM',  vex("virtual_bpm_exclude")),
                  HLA_VHCOR: ('HCOR', vex("virtual_hcor_exclude")),
                  HLA_VVCOR: ('VCOR', vex("virtual_vcor_exclude")),
                  HLA_VCOR:  ('COR',  vex("virtual_cor_exclude")),
                  HLA_VQUAD: ('QUAD', vex("virtual_quad_exclude")),
                  HLA_VSEXT: ('SEXT', vex("virtual_sext_exclude")),
        }
        createVirtualElements(lat, vfams)
        lat_dict[msect] = lat
        if verbose:
            nelems = len(lat.getElementList('*'))
            if msect == accdefault:
                print "%s (*): %d elements" % (msect, nelems)
            else:
                print "%s: %d elements" % (msect, nelems)
            print "  BPM: %d, COR: %d, QUAD: %d, SEXT: %d" % (
                len(lat.getElementList('BPM')), len(lat.getElementList('COR')),
                len(lat.getElementList('QUAD')),
                len(lat.getElementList('SEXT')))

    # set the default submachine, if no, use the first one
    lat0 = lat_dict.get(accdefault, None)
    if lat0 is None and len(lat_dict) > 0:
        _logger.warn("default submachine not defined, "
                      "use the first available one '%s'" % k)
        lat0 = lat_dict[sorted(lat_dict.keys())[0]]

    if lat0 is None:
        raise RuntimeError("NO accelerator structures available")

    _lat = lat0
    _lattice_dict.update(lat_dict)
    if save_cache:
        selected_lattice_name = [k for (k,v) in _lattice_dict.iteritems()
                                 if _lat == v][0]
        saveCache(machine, _lattice_dict, selected_lattice_name)

    #if verbose:
    #    print "Default lattice:", lat0.name

    if return_lattices:
        return lat0, lat_dict

def loadfast(machine, submachine = "*"):
    """
    :author: Yoshtieru Hidaka <yhidaka@bnl.gov>
    """

    machine_folderpath = os.path.join(HLA_CONFIG_DIR, machine)

    check_filename_ext_list = [
        '*.sqlite', '*.py', '*.ini', '*.hdf5',]
    check_filepaths = sum(
        [glob.glob(os.path.join(machine_folderpath, pattern))
         for pattern in check_filename_ext_list], [])

    current_timestamp = time.time()

    mod_timestamps = [os.path.getmtime(fp) for fp in check_filepaths]

    cache_filepath = os.path.join(_home_hla, machine+'_lattices.cpkl')

    if os.path.exists(cache_filepath):
        cache_file_timestamp = os.path.getmtime(cache_filepath)

        # If the cache file is more than 24 hours old, force cache update.
        if (current_timestamp - cache_file_timestamp) >= 24.0*60.0*60.0:
            update_cache = True
            print ('* The lattice cache file for the machine "{0}" is more than '
                   '24 hours old.').format(machine)

        # If any of the aphla database files have a timestamp later
        # than that of the cache file, force cache update
        elif np.any(np.array(mod_timestamps) - cache_file_timestamp > 0.0):
            update_cache = True
            print ('* Some of the database files related to the machine "{0}" '
                   'are newer than the lattice cache file.').format(machine)

        else:
            update_cache = False
    else:
        print ('* The lattice cache file for the machine "{0}" does not '
               'exist.').format(machine)
        update_cache = True

    if update_cache:
        print ('* Auto-updating the lattice cache file for the '
               'machine "{0}"...').format(machine)
        load(machine, use_cache=False, save_cache=True)
        print '* Finished updating the cache file.'
    else:
        load(machine, use_cache=True, save_cache=False)

    try:
        use(submachine)
    except:
        pass

def loadCache(machine_name):
    """
    load the cached machine

    :author: Yoshtieru Hidaka <yhidaka@bnl.gov>
    """
    global _lat, _lattice_dict

    cache_folderpath = _home_hla
    cache_filepath = os.path.join(cache_folderpath,
                                  machine_name+'_lattices.cpkl')

    print 'Loading cached lattice from {0:s}...'.format(cache_filepath)

    with open(cache_filepath,'rb') as f:
        selected_lattice_name = pickle.load(f)
        _lattice_dict = pickle.load(f)

    print 'Finished loading cached lattice.'

    _lat = _lattice_dict[selected_lattice_name]


def saveCache(machine_name, lattice_dict, selected_lattice_name):
    """
    save machine as cache

    :author: Yoshtieru Hidaka <yhidaka@bnl.gov>
    """

    cache_folderpath = _home_hla
    if not os.path.exists(cache_folderpath):
        os.mkdir(cache_folderpath)
    cache_filepath = os.path.join(cache_folderpath,
                                  machine_name+'_lattices.cpkl')
    with open(cache_filepath,'wb') as f:
        pickle.dump(selected_lattice_name,f,2)
        pickle.dump(lattice_dict,f,2)

def saveChannelFinderDb(dst, url = None):
    """save the channel finder as a local DB

    Parameters
    -----------
    url : str. channel finder URL, default use environment *APHLA_CFS_URL*
    dst : str. destination db filename.
    """
    cfa = ChannelFinderAgent()
    if url is None: url = os.environ.get('APHLA_CFS_URL', None)
    if url is None:
        raise RuntimeError("no URL defined for downloading")
    cfa.downloadCfs(url, property=[
                ('hostName', '*'), ('iocName', '*')], tagName='aphla.sys.*')
    cfa.exportSqlite(dst)


def createVirtualElements(vlat, vfams):
    """create common merged virtual element"""
    # virutal elements
    # a virtual bpm. its field is a "merge" of all bpms.
    iv = -100
    vpar = { 'virtual': 1, 'name': None, 'family': HLA_VFAMILY,
             'index': None }
    for vfam,famr in vfams.items():
        _logger.debug("creating virtual element {0} {1}".format(vfam, famr))
        # a virtual element. its field is a "merge" of all elems.
        fam, exfam = famr
        velem = [e for e in vlat.getElementList(fam) if e.name not in exfam]
        vpar.update({'name': vfam, 'index': iv})
        if velem:
            allvelem = merge(velem, **vpar)
            vlat.insertElement(allvelem, groups=[HLA_VFAMILY])
            allvelem.virtual = 1

        iv = iv - 100

def findCfaConfig(srcname, machine, submachines):
    """
    find the appropriate config for ChannelFinderAgent

    initialize the virtual accelerator 'V2SR', 'V1LTD1', 'V1LTD2', 'V1LTB' from

    - `${HLA_ROOT}/machine.csv`
    - `${HLA_ROOT}/machine.sqlite`
    - channel finder in ${APHLA_CFS_URL} with tags `aphla.sys.submachine`
    - `machine.csv` with aphla package.
    - `machine.sqlite` with aphla package.

    Examples
    ---------
    >>> findCfaConfig("/data/nsls2v2.sqlite", "nsls2", "*")

    """

    cfa = ChannelFinderAgent()

    # if source is an explicit file name
    if os.path.exists(srcname):
        msg = "Creating lattice from explicit source '%s'" % srcname
        if srcname.endswith('.csv'):
            cfa.importCsv(srcname)
        elif srcname.endswith(".sqlite"):
            cfa.importSqlite(srcname)
        else:
            raise RuntimeError("Unknown explicit source '%s'" % srcname)
        return cfa

    # if only filename provided, searching known directories in order.
    # matching HLA_ROOT -> CF -> Package
    homesrc = os.path.join(HLA_ROOT, srcname)
    HLA_CFS_URL = os.environ.get('APHLA_CFS_URL', None)

    if os.path.exists(homesrc + '.csv'):
        msg = "Creating lattice from '%s.csv'" % homesrc
        _logger.info(msg)
        cfa.importCsv(homesrc + '.csv')
    elif os.path.exists(homesrc + '.sqlite'):
        msg = "Creating lattice from '%s.sqlite'" % homesrc
        _logger.info(msg)
        cfa.importSqlite(homesrc + '.sqlite')
    elif os.environ.get('APHLA_CFS_URL', None):
        msg = "Creating lattice from channel finder '%s'" % HLA_CFS_URL
        _logger.info(msg)
        #cfa.downloadCfs(HLA_CFS_URL, property=[
        #        ('hostName', '*'), ('iocName', '*')], tagName='aphla.sys.*')
        cfa.downloadCfs(HLA_CFS_URL, tagName='aphla.sys.*')
    elif resource_exists(__name__, os.path.join(machine, srcname + '.csv')):
        name = resource_filename(__name__, os.path.join(machine,
                                                        srcname + '.csv'))
        #src_pkg_csv = conf.filename(cfs_filename)
        msg = "Creating lattice from '%s'" % name
        _logger.info(msg)
        cfa.importCsv(name)
    elif resource_exists(__name__, os.path.join(machine, srcname + '.sqlite')):
        name = resource_filename(__name__, os.path.join(machine,
                                                        srcname + '.sqlite'))
        msg = "Creating lattice from '%s'" % name
        _logger.info(msg)
        cfa.importSqlite(name)
        #for k,v in _db_map.iteritems(): cfa.renameProperty(k, v)
    else:
        _logger.error("Lattice data are available for machine '%s'" % machine)
        raise RuntimeError("Failed at loading data file '%s' from '%s'" % (
            machine, srcname))

    return cfa

def createLattice(latname, pvrec, systag, src = 'channelfinder',
                  vbpm = True, vcor = True):
    """
    create a lattice from channel finder data

    Parameters
    -----------
    name: lattice name, e.g. 'SR', 'LTD'
    pvrec: list of pv records `(pv, property dict, list of tags)`
    systag: process records which has this systag. e.g. `aphla.sys.SR`
    src: source URL or filename of this lattice

    Returns
    ---------
    lat : the :class:`~aphla.lattice.Lattice` type.
    """

    _logger.debug("creating '%s':%s" % (latname, src))
    _logger.info("%d pvs found in '%s'" % (len(pvrec), latname))
    # a new lattice
    lat = Lattice(latname, src)
    for rec in pvrec:
        _logger.debug("processing {0}".format(rec))
        # skip if there's no properties.
        if rec[1] is None: continue
        if rec[0] and systag not in rec[2]:
            _logger.debug("%s is not tagged '%s'" % (rec[0], systag))
            continue
        #if rec[1].get("system", "") != latname: continue
        if 'name' not in rec[1]: continue
        #print "PASSED"
        prpt = rec[1]
        #if "hostName" not in prpt:
        #    _logger.warn("no 'hostName' for {0}".format(rec))
        #if "iocName" not in prpt:
        #    _logger.warn("no 'iocName' for {0}".format(rec))

        if 'se' in prpt:
            prpt['sb'] = float(prpt['se']) - float(prpt.get('length', 0))
        name = prpt.get('name', None)

        #_logger.debug("{0} {1} {2}".format(rec[0], rec[1], rec[2]))

        # find if the element exists.
        elem = lat._find_exact_element(name=name)
        if elem is None:
            try:
                elem = CaElement(**prpt)
                gl = [g.strip() for g in prpt.get('groups', [])]
                elem.group.update(gl)
            except:
                _logger.error("Error: creating element '{0}' with '{1}'".format(name, prpt))
                raise

            _logger.debug("created new element: '%s'" % name)
            #print "inserting:", elem
            #lat.appendElement(elem)
            lat.insertElement(elem)
        else:
            _logger.debug("using existed element %s" % (name,))
        #
        if HLA_VFAMILY in prpt.get('group', []): elem.virtual = 1

        handle = prpt.get('handle', '').lower()
        if handle == 'get': prpt['handle'] = 'readback'
        elif handle == 'put': prpt['handle'] = 'setpoint'

        pv = rec[0]
        if pv: elem.updatePvRecord(pv, prpt, rec[2])

    # group info is a redundant info, needs rebuild based on each element
    lat.buildGroups()
    # !IMPORTANT! since Channel finder has no order, but lat class has
    lat.sortElements()
    lat.circumference = lat[-1].se if lat.size() > 0 else 0.0

    _logger.debug("mode {0}".format(lat.mode))
    _logger.info("'%s' has %d elements" % (lat.name, lat.size()))
    for g in sorted(lat._group.keys()):
        _logger.debug("lattice '%s' group %s(%d)" % (
                lat.name, g, len(lat._group[g])))

    return lat


def setGoldenLattice(lat, h5fname, grp = "Golden"):
    import h5py
    f = h5py.File(h5fname, 'r')
    if grp not in f:
        _logger.warn("no '%s' in '%s'. Ignore" % (grp, h5fname))
        return
    g = f[grp]
    for elem in lat.getElementList(g.keys()):
        g1 = g[elem.name]
        for fld in g1.keys():
            ds = g1[fld]
            elem.setGolden(fld, ds, unitsys=ds.attrs.get("unitsys", None))
    # the waveform ... ignored now


def use(lattice):
    """
    switch to a lattice

    use :func:`~hla.machines.lattices` to get a dict of lattices and its mode
    name
    """
    global _lat, _lattice_dict
    if isinstance(lattice, Lattice):
        _lat = lattice
    elif lattice in _lattice_dict:
        _lat = _lattice_dict[lattice]
    else:
        raise ValueError("no lattice %s was defined" % lattice)

def getOutputDir(lat = None):
    """
    return the output data dir of lat. None if lat does not exist.

    lat = None will use the default current lattice.
    """

    if lat is None:
        return _lat.OUTPUT_DIR
    elif lat in _lattice_dict:
        _lattice_dict[lat].OUTPUT_DIR
    else:
        raise RuntimeError("no output_dir defined for lattice '%s'" % lat)

def getLattice(lat = None):
    """
    return the lattice with given name, if None returns the current lattice.

    a :class:`~aphla.lattice.Lattice` object with given name. return the
    current lattice by default.

    .. seealso:: :func:`~aphla.machines.lattices`
    """
    if lat is None:  return _lat

    global _lattice_dict
    return _lattice_dict.get(lat, None)

def lattices():
    """
    get a list of available lattices

    Examples
    --------
    >>> lattices()
      [ 'LTB', 'LTB-txt', 'SR', 'SR-txt']
    >>> use('LTB-txt')

    """
    return _lattice_dict.keys()


def machines():
    """all available machines"""
    from pkg_resources import resource_listdir, resource_isdir
    return [d for d in resource_listdir(__name__, ".")
            if resource_isdir(__name__, d)]

