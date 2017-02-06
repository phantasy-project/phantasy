#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Facility for Rare Isotope Beams
#

from setuptools import setup, find_packages
import glob
import versioneer


def readme():
    with open('README.rst', 'r') as f:
        return f.read()

app_name = "phantasy"
app_description = 'Physics High-level Applications aNd Toolkits for Accelerator SYstem'
app_long_description = readme() + '\n\n'
app_platform = ["Linux"]
app_author = "Tong Zhang"
app_author_email = "zhangt@frib.msu.edu"
app_license = "FRIB"
app_url = "STASH"
app_keywords = "FRIB HLA high-level python FLAME IMPACT"
installrequires = [
    'numpy',
    'scipy',
    'matplotlib',
    'xlrd',
    'tornado',
    'motor==0.4',
    'jinja2',
    'humanize',
    'jsonschema',
]
extrasrequire = {
    "LMS": [
        'tornado',
        'humanize',
        'motor==0.4',
        'jinja2',
        'jsonschema',
    ]
}

app_scripts = [i for i in glob.glob("bin/*") if i != "bin/softIoc"]

setup(
        name=app_name,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description=app_description,
        author=app_author,
        author_email=app_author_email,
        #url = app_url,
        platforms=app_platform,
        #license=app_license,
        keywords=app_keywords,
        scripts=app_scripts,
        packages=find_packages(exclude=['utest', 'demo', 'example']),
        classifiers=[
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules', 
            'Topic :: Scientific/Engineering :: Physics'],
        tests_require=['nose'],
        test_suite='nose.collector',
        install_requires=installrequires,
        extras_require=extrasrequire, 
)
