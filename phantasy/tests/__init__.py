# -*- coding: utf-8 -*-

import nose
import os
import shutil
import sys

try:
    basestring
except NameError:
    basestring = str

CWD = os.path.dirname(__file__)
TMP_DIR = "/tmp/phantasy_data"

def main(argv=None, **kws):
    """Run tests for `phantasy` package, accept CLI options when executing
    `run_phantasy` command.

    Parameters
    ----------
    argv : list
        List of options of `nosetests`.
    """
    argv_list = ['--logging-clear-handlers',
                 '--logging-level=INFO',
                 '--nologcapture']
    argv_list.extend(sys.argv[1:])
    if argv is not None:
        if isinstance(argv, basestring):
            argv = argv,
        argv_list.extend(argv)
        nose.run(argv=list(set(argv_list)), defaultTest=CWD, **kws)
    else:
        nose.run(argv=argv_list, defaultTest=CWD, **kws)

    if os.path.isdir(TMP_DIR):
        shutil.rmtree(TMP_DIR)

    return 0
