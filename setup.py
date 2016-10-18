#!/usr/bin/env python
# coding: utf-8

import re
import os
from setuptools import setup
from setuptools import find_packages


HERE = os.path.dirname(__file__)


def get_version_number():
    """ Get the current module version. """
    # TODO: What should be the authoritative source of version numbers?
    find_version = re.compile(
        r"""__version__\s*=\s*[ubr]*(?:"([.0-9]+)"|'([.0-9]+)')""",
        re.IGNORECASE)
    try:
        with open(os.path.join(HERE, 'whichmodule', '__init__.py')) as init:
            for line in init.readlines():
                result = find_version.search(line)
                if result:
                    return result.group(1) or result.group(2)
    except Exception:
        # TODO: Maybe don't catch this error?
        pass
    return '0.0.0'


def get_packages():
    """ List of (sub)packages to install. """
    return find_packages('.', include=('whichmodule', ))


def setup_package():
    """ build and run setup. """

    setup(
        name='whichmodule',
        description='Find and list modules in the current python environment',
        author='fredrikhl',
        url='https://github.com/fredrikhl/which-module',
        version=get_version_number(),
        packages=get_packages(),
        scripts=['whichmodule.py'],
        #   entry_points={
        #       'console_scripts': [
        #           'whichmodule = whichmodule:main'
        #       ]
        #   },
        options={
            'build_scripts': {
                'executable': '/usr/bin/env python',
            },
        },
    )


if __name__ == "__main__":
    setup_package()
