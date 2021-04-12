"""Set up the version."""

import os


_version_major = 0
_version_minor = 1
_version_micro = ''
_version_extra = ''

# construct full version string
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)
__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ['Development Status :: 1 - Alpha',
               'Environment :: Console',
               'License :: OSI Approved :: BSD 3-Clause License',
               'Operating System :: Unix',
               'Programming Language :: Python']
NAME = 'rodney'
MAINTAINER = 'Olivier Mesnard'
MAINTAINER_EMAIL = 'mesnardo@gwu.edu'
DESCRIPTION = 'rodney: your assistant'
LONG_DESCRIPTION = """
rodney
======
Your assistant.

License
=======
rodney is licensed under the terms of the BSD 3-Clause license. See the
file "LICENSE" for information on the history of this software,
terms & conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.
All trademarks referenced herein are property of their respective holders.
Copyright (c) 2020-2021, Olivier Mesnard.
"""
URL = ''
DOWNLOAD_URL = ''
LICENSE = 'BSD 3-Clause'
AUTHOR = ''
AUTHOR_EMAIL = ''
PLATFORMS = 'Unix'
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ['rodney']
PACKAGE_DATA = {'rodney': ['data']}
REQUIRES = ['numpy', 'scipy']
