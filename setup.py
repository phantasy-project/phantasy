#!/usr/bin/env python
# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

MAJOR = 0
MINOR = 2
PATCH = 0
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, PATCH)

from setuptools import setup, find_packages
setup(
    name='physutil',
    version=VERSION,
    description='FRIB Python based physics application toolkit',
    author='Guobao Shen, Dylan Maxwell',
    author_email='shen@frib.msu.edu, maxwelld@frib.msu.edu',
    maintainer = "Guobao Shen",
    maintainer_email = "shen@frib.msu.edu",
    url = 'https"//git.nscl.msu.edu/physapps/physutil.git',
    packages= find_packages(exclude=['utest', 'demo', 'example']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires = [
        # PyPI
        'numpy>=1.8',
        'scipy>=0.14',
        'xlrd>=0.9',
        'tornado>=4.2',
        'jinja2>=2.7',
        'motor>=0.4',
        'functools32>=3.2',
        'jsonschema>=2.5',
        'matplotlib>=1.4.2',
        # Custom
        'channelfinder>=2.0',
        'PyScanClient>=0.9.5',
        'cothread>=2.13'
    ],
    dependency_links=[
        'git+https://github.com/ChannelFinder/pyCFClient.git',
        'git+https://github.com/PythonScanClient/PyScanClient.git',
        'git+http://controls.diamond.ac.uk/downloads/python/cothread/cothread.git@v2-13'
    ]
)
