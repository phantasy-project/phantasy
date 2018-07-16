#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
from fnmatch import fnmatch
from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()

def read_license():
    with open('LICENSE') as f:
        return f.read()


app_version="0.9.7"
app_name = "phantasy"
app_description = 'Physics high-level applications and toolkit for ' \
        'accelerator system'
app_long_description = readme() + '\n\n'
app_platform = ["Linux"]
app_author = "Tong Zhang"
app_author_email = "zhangt@frib.msu.edu"
app_license = read_license()
app_url = "https://archman.github.io/phantasy/"
app_keywords = "phantasy FRIB HLA high-level python FLAME IMPACT"
app_install_requires = [
    'numpy',
    'matplotlib',
    'xlrd',
    'lmfit==0.8.0',
    'scipy==0.14.0',
    'cothread',
    'pyepics',
]
app_extras_require = {
    'test': ['nose', 'nose-exclude', 'coverage'],
}

app_scripts = [i for i in glob.glob("scripts/*") if not fnmatch(i, "scripts/softIoc")]

def get_all_dirs(des_root, src_root):
    ret = []
    for r,d,f in os.walk(src_root):
        ret.append(
                (os.path.join(des_root, r), [os.path.join(r, fi) for fi in f])
        )
    return ret

setup(
    name=app_name,
    version=app_version,
    description=app_description,
    long_description=app_long_description,
    author=app_author,
    author_email=app_author_email,
    url=app_url,
    platforms=app_platform,
    license=app_license,
    keywords=app_keywords,
    scripts=app_scripts,
    packages=find_packages(),
    data_files = get_all_dirs('/etc/phantasy/config', 'demo_mconfig'),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules', 
        'Topic :: Scientific/Engineering :: Physics'],
    tests_require=['nose'],
    test_suite='nose.collector',
    install_requires=app_install_requires,
    extras_require=app_extras_require,
)
