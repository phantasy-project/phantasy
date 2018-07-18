# -*- coding: utf-8 -*-

import nose
import os

try:
    basestring
except NameError:
    basestring = str

CWD = os.path.dirname(__file__)


def run(argv=None, **kws):
    argv_list = ['--logging-clear-handlers', '--logging-level=INFO']
    if argv is not None:
        if isinstance(argv, basestring):
            argv = argv,
        argv_list.extend(argv)
        nose.run(argv=list(set(argv_list)), defaultTest=CWD, **kws)
    else:
        nose.run(argv=argv_list, defaultTest=CWD, **kws)
