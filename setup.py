#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()

def read_license():
    with open('LICENSE') as f:
        return f.read()


_version="2.0.0"
_name = "phantasy"
_description = 'Physics high-level applications and toolkit for accelerator system'
_long_description = readme() + '\n\n'
_platform = ["Linux"]
_author = "Tong Zhang"
_author_email = "zhangt@frib.msu.edu"
_license = read_license()
_url = "https://archman.github.io/phantasy/"
_keywords = "phantasy FRIB HLA high-level python FLAME IMPACT"
_install_requires = [
    'numpy',
    'matplotlib',
    'xlrd',
    'lmfit',
    'scipy',
    'cothread',
    'pyepics',
]
_extras_require = {
    'test': ['pytest', 'pytest-cov'],
}

def get_all_dirs(des_root, src_root):
    ret = []
    for r,d,f in os.walk(src_root):
        ret.append(
                (os.path.join(des_root, r), [os.path.join(r, fi) for fi in f])
        )
    return ret

def set_entry_points():
    r = {}
    r['console_scripts'] = [
        'phytool=phantasy.tools.phytool:main',
        'plot_orbit=phantasy.tools.plot_orbit:main',
        'correct_orbit=phantasy.tools.correct_orbit:main',
        'test_phantasy=phantasy.tests:main',
    ]
    return r

setup(
    name=_name,
    version=_version,
    description=_description,
    long_description=_long_description,
    author=_author,
    author_email=_author_email,
    url=_url,
    platforms=_platform,
    license=_license,
    keywords=_keywords,
    packages=find_packages(),
    include_package_data=True,
    data_files=get_all_dirs('/etc/phantasy/config', 'demo_mconfig'),
    entry_points=set_entry_points(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Physics'],
    # tests_require=['nose'],
    # test_suite='nose.collector',
    install_requires=_install_requires,
    extras_require=_extras_require,
)
