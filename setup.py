#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import glob
import versioneer
from fnmatch import fnmatch


def readme():
    with open('README.rst', 'r') as f:
        return f.read()

def read_license():
    with open('LICENSE') as f:
        return f.read()

app_name = "phantasy"
app_description = 'Physics high-level applications and toolkits for accelerator system'
app_long_description = readme() + '\n\n'
app_platform = ["Linux"]
app_author = "Tong Zhang"
app_author_email = "zhangt@frib.msu.edu"
app_license = read_license()
app_url = "https://controls.frib.msu.edu/phantasy/"
app_keywords = "phantasy FRIB HLA high-level python FLAME IMPACT"
installrequires = [
    'numpy',
    'scipy',
    'matplotlib',
    'xlrd',
#    'tornado',
#    'motor==0.4',
#    'jinja2',
#    'humanize',
#    'jsonschema',
#    'cothread',
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

app_scripts = [i for i in glob.glob("scripts/*") if not fnmatch(i, "scripts/softIoc")]

setup(
        name=app_name,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description=app_description,
        author=app_author,
        author_email=app_author_email,
        url = app_url,
        platforms=app_platform,
        license=app_license,
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
