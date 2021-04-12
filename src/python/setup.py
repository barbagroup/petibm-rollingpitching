"""Set up package."""

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# Get version and release info.
version_file = os.path.join('rodney', 'version.py')
with open(version_file) as infile:
    exec(infile.read())

options = dict(name=NAME,
               maintainer=MAINTAINER,
               maintainer_email=MAINTAINER_EMAIL,
               description=DESCRIPTION,
               long_description=LONG_DESCRIPTION,
               url=URL,
               download_url=DOWNLOAD_URL,
               license=LICENSE,
               classifiers=CLASSIFIERS,
               author=AUTHOR,
               author_email=AUTHOR_EMAIL,
               platforms=PLATFORMS,
               version=VERSION,
               packages=PACKAGES,
               package_data=PACKAGE_DATA,
               include_package_data=True,
               requires=REQUIRES)


if __name__ == '__main__':
    setup(**options)
