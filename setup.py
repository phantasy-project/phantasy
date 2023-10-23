#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools


def readme():
    with open('README.md', 'r') as f:
        return f.read()


_version = "2.2.7"
_name = "phantasy"
_description = 'Physics high-level applications and toolkit for accelerator system'
_long_description = readme() + '\n\n'
_platform = ["Linux"]
_author = "Tong Zhang"
_author_email = "zhangt@frib.msu.edu"
_license = "BSD"
_url = "https://phantasy-project.github.io/phantasy/"
_keywords = "PHANTASY FRIB HLA high-level Python FLAME Virtual Model"
_install_requires = [
    'epicscorelibs',
    'importlib_metadata',
    # 'phantasy-machines',
    'xlrd>=1.1,<2.0',
    'matplotlib>=3.1.2,<4.0',
    'lmfit>=1.0.0,<2.0',
    'cothread>=2.16,<3.0',
    'pyepics>=3.4.2,<4.0',
    'flame-code>=1.8.6,<2.0',
    'flame-utils>=0.4.1,<1.0',
    'requests>=2.24.0,<3.0',
    'pandas>=1.1.4,<2.0',
    'toml>=0.10.1,<1.0',
    'python-unicorn>=0.4.4,<1.0',
    'flame-data',
    'epics-appimage',
    'openpyxl',
]
_extras_require = {
    'test': ['pytest', 'pytest-cov'],
    'doc': ['sphinx_rtd_theme', 'nbsphinx', 'dateutils', 'ipython'],
}


def get_all_dirs(des_root, src_root):
    ret = []
    for r, d, f in os.walk(src_root):
        ret.append((os.path.join(des_root,
                                 r), [os.path.join(r, fi) for fi in f]))
    return ret


def set_entry_points():
    r = {}
    r['console_scripts'] = [
        'phytool=phantasy.tools.phytool:main',
        'plot_orbit=phantasy.tools.plot_orbit:main',
        'correct_orbit=phantasy.tools.correct_orbit:main',
        'test_phantasy=phantasy.tests:main',
        'ensure_set=phantasy.tools.ensure_set:run',
        'fetch_data=phantasy.tools.fetch_data:run',
    ]
    return r


setuptools.setup(
    name=_name,
    version=_version,
    description=_description,
    long_description=_long_description,
    long_description_content_type='text/markdown',
    author=_author,
    author_email=_author_email,
    url=_url,
    platforms=_platform,
    license=_license,
    keywords=_keywords,
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=get_all_dirs('/etc/phantasy/config', 'demo_mconfig'),
    entry_points=set_entry_points(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    install_requires=_install_requires,
    extras_require=_extras_require,
)
