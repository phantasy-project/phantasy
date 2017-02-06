"""[TODO]
Machine Structure Initialization
--------------------------------

In ``phyutil`` one machine includes several accelerator structure, e.g.:
* "nsls2v2" is a machine with several submachine or lattice: V1LTD, V1LTB, V2SR.
* "FRIB" is a machine, with several submachine or lattice: LINAC, LS1, LS2, etc.

Submachines are also called lattice in ``phyutil``. Each lattice has a list of
elements, magnet or instrument. The submachines/lattices can share elements.

All these definitions are parsed from confguration file named: "phyutil.ini",
whose root directory is defined as a machine or facility.

:author: Lingyun Yang <lyyang@bnl.gov>, Guobao Shen <shen@frib.msu.edu>

recently modified by: Tong Zhang <zhangt@frib.msu.edu>
"""

import os
import time
import glob
import re
import urlparse
from pkg_resources import resource_exists, resource_filename #@UnresolvedImport #pylint: disable=E0611 
import cPickle as pickle
import ConfigParser
import fnmatch
import logging
import numpy as np
import tempfile
import shutil
import atexit

from phantasy.library.layout import build_layout
from phantasy.library.parser import Configuration
from phantasy.library.settings import Settings
from phantasy.library.chanfinder import ChannelFinderAgent

_logger = logging.getLogger(__name__)

HLA_TAG_PREFIX = 'phyutil'
HLA_TAG_SYS_PREFIX = HLA_TAG_PREFIX + '.sys'

#
HLA_VFAMILY = 'HLA:VIRTUAL'
HLA_VBPM   = 'HLA:VBPM'
HLA_VPM    = 'HLA:VPM'
HLA_VHCOR  = 'HLA:VHCOR'
HLA_VVCOR  = 'HLA:VVCOR'
HLA_VCOR   = 'HLA:VCOR'
HLA_VQUAD  = 'HLA:VQUAD'
HLA_VSEXT  = 'HLA:VSEXT'
HLA_VSOL   = 'HLA:VSOL'
HLA_VCAV   = 'HLA:VCAV'
HLA_VBEND  = "HLA:VBEND"

SCAN_SRV_URL = None
SIMULATION_CODE = None
MODELDATA_DIR = None



_machine_config = None


# keep all loaded lattice
_lattice_dict = {}

# the current lattice
_lat = None


_temp_dirs = []

def _rm_temp_dirs():
    for temp_dir in _temp_dirs:
        shutil.rmtree(temp_dir)

atexit.register(_rm_temp_dirs)



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

        # If any of the phyutil database files have a timestamp later
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
    """Load the cached machine.

    Parameters
    ----------
    machine_name : str
        Machine name.

    Note
    ----
    This function was initially written by Yoshtieru Hidaka <yhidaka@bnl.gov>
    """
    global _lat, _lattice_dict

    cache_folderpath = _home_hla
    cache_filepath = os.path.join(cache_folderpath,
                                  machine_name + '_lattices.cpkl')

    print('Loading cached lattice from {0:s}...'.format(cache_filepath))

    with open(cache_filepath,'rb') as f:
        selected_lattice_name = pickle.load(f)
        _lattice_dict = pickle.load(f)

    print('Finished loading cached lattice.')

    _lat = _lattice_dict[selected_lattice_name]


def saveCache(machine_name, lattice_dict, selected_lattice_name):
    """Save machine as cache.

    Parameters
    ----------
    machine_name : str
        Machine name.
    lattice_dict : dict
    selected_lattice_name : dict
        
    Note
    ----
    This function was initially written by Yoshtieru Hidaka <yhidaka@bnl.gov>
    """
    cache_folderpath = _home_hla
    if not os.path.exists(cache_folderpath):
        os.mkdir(cache_folderpath)
    cache_filepath = os.path.join(cache_folderpath,
                                  machine_name + '_lattices.cpkl')
    with open(cache_filepath, 'wb') as f:
        pickle.dump(selected_lattice_name, f, 2)
        pickle.dump(lattice_dict, f, 2)


def saveChannelFinderDb(dst, url = None):
    """save the channel finder as a local DB

    Parameters
    -----------
    url : str. channel finder URL, default use environment *PHYUTIL_CFS_URL*
    dst : str. destination db filename.
    """
    cfa = ChannelFinderAgent()
    if url is None: url = os.environ.get('PHYUTIL_CFS_URL', None)
    if url is None:
        raise RuntimeError("no URL defined for downloading")
    cfa.downloadCfs(url, property=[
                ('hostName', '*'), ('iocName', '*')], tagName='phyutil.sys.*')
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
    - channel finder in ${PHYUTIL_CFS_URL} with tags `phyutil.sys.submachine`
    - `machine.csv` with phyutil package.
    - `machine.sqlite` with phyutil package.

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
    HLA_CFS_URL = os.environ.get('PHYUTIL_CFS_URL', None)

    if os.path.exists(homesrc + '.csv'):
        msg = "Creating lattice from '%s.csv'" % homesrc
        _logger.info(msg)
        cfa.importCsv(homesrc + '.csv')
    elif os.path.exists(homesrc + '.sqlite'):
        msg = "Creating lattice from '%s.sqlite'" % homesrc
        _logger.info(msg)
        cfa.importSqlite(homesrc + '.sqlite')
    elif os.environ.get('PHYUTIL_CFS_URL', None):
        msg = "Creating lattice from channel finder '%s'" % HLA_CFS_URL
        _logger.info(msg)
        #cfa.downloadCfs(HLA_CFS_URL, property=[
        #        ('hostName', '*'), ('iocName', '*')], tagName='phyutil.sys.*')
        cfa.downloadCfs(HLA_CFS_URL, tagName='phyutil.sys.*')
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

    a :class:`~phyutil.lattice.Lattice` object with given name. return the
    current lattice by default.

    .. seealso:: :func:`~phyutil.machines.lattices`
    """
    if lat is None:  return _lat

    global _lattice_dict
    return _lattice_dict.get(lat, None)

def get_all_lattices():
    """Get all loaded lattices.

    Returns
    -------
    ret : dict
        Lattice name as the key and lattice configuration as value.
    """
    return _lattice_dict


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
    from pkg_resources import resource_listdir, resource_isdir  #@UnresolvedImport #pylint: disable=E0611
    return [d for d in resource_listdir(__name__, ".")
            if resource_isdir(__name__, d)]
