#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from setuptools import find_packages


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
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        packages=get_packages(),
        scripts=['whichmodule.py'],
        # We need to prevent setuptools from rewriting the shebang.
        # This script needs to run in the current python environment to be
        # helpful.
        options={
            'build_scripts': {
                'executable': '/usr/bin/env python',
            },
        },
    )


if __name__ == "__main__":
    setup_package()
