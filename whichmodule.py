#!/usr/bin/env python
# encoding: utf-8
""" Look up and return file location of a module. """

from __future__ import unicode_literals, print_function, absolute_import

import argparse
import fnmatch
import imp
import importlib
import inspect
import os
import re
import sys


__version__ = '1.3.1'


def iter_dict(d):
    # PY2/3 compat
    try:
        return d.iteritems()
    except AttributeError:
        return d.items()


def get_suffix_data(filename):
    """ Fetches suffix data from the `filename` suffix. """
    for suffix in imp.get_suffixes():
        if filename[-len(suffix[0]):] == suffix[0]:
            return suffix
    return None


def get_paths():
    """ Gets a list of module paths, in search order. """
    return filter(os.path.isdir,
                  map(os.path.normcase,
                      map(os.path.abspath, sys.path[:])))


def get_modules(path):
    """ Gets a list of modules at a given path.

    :param str path:
        A directory to look up modules in.

    :returns dict:
        Returns a dictionary with modules in the given 'path'. The dictionary
        will contain items (<module>, <filename>), i.e. where the keys are
        module names from the path, and the values are the absolute path to the
        module file.

    """
    modules = {}
    module_name_re = re.compile(r'^[a-z_]\w*$', re.I)

    for basename in os.listdir(path):
        filename = os.path.join(path, basename)
        if os.path.isfile(filename):
            module, ext = os.path.splitext(os.path.basename(filename))
            suffix_data = get_suffix_data(filename)
            if not suffix_data:
                continue
            if module_name_re.match(module):
                #   if suffix_data[2] == imp.C_EXTENSION:
                #       # check that this extension can be imported
                #       try:
                #           __import__(name)
                #       except ImportError:
                #           continue
                modules[module] = filename
        elif (os.path.isdir(filename) and
              os.path.isfile(os.path.join(filename, "__init__.py"))):
            package = os.path.basename(filename)
            for module, fn in get_modules(filename).items():
                if module == '__init__':
                    module = package
                else:
                    module = package + '.' + module
                modules[module] = fn
    return modules


def expand_module_name(module_name):
    """ Returns the module name, and the packages it comes from.

    >>> expand_module_names('foo')
    ['foo']
    >>> expand_module_names('foo.bar')
    ['foo', 'foo.bar']
    """
    parts = module_name.split('.')
    return ['.'.join(parts[:i]) for i in range(1, len(parts) + 1)]


def join_modules(*module_dicts):
    """ Joins multiple module dicts that *may* contain conflicting names.

    The argument order dictates which modules will be filtered out. If the
    first dictionary contains a package or module 'foo', then no module 'foo'
    or module from a package 'foo' from later dictionaries will be included in
    the result.

    >>> _join_modules({'foo': '...', }, {'foo.bar': '...', 'baz': '...'})
    {'foo': '...', 'baz': '...'}

    :param list module_dicts:
        A list of dictionaries, each dictionary is a mapping of
        module_name -> filename.

    :return dict:
        A dictonary that maps module_name -> filename, where all conflicting
        modules have been removed.
    """
    # Join modules from multiple paths
    result = {}
    # Modules from other module sets.
    commited = set()
    for dict_ in module_dicts:
        # Modules from this set
        dict_names = set()
        for module in dict_.keys():
            names = expand_module_name(module)
            # If the module or the package it comes from has been seen
            # previously, it won't be importable
            if any(n in commited for n in names):
                continue
            dict_names.update(names)
            result[module] = dict_[module]
        commited.update(dict_names)
    return result


def get_module_file(module_name):
    """ Get the path to the source file for a given module. """
    # We could use other parts of the import system here to avoid actually
    # importing the file, but that's a bit messy to do for both PY2 and PY3.
    #
    # This solution is simple and gives us reasonally good support for python
    # version.
    module = importlib.import_module(module_name)
    return inspect.getsourcefile(module)


def _list_modules():
    module_dicts = []

    # Built-ins
    module_dicts.append(
        {m: None for m in sys.builtin_module_names})

    # Paths
    for path in get_paths():
        module_dicts.append(get_modules(path))

    # Join
    return join_modules(*module_dicts)


def _print_modules(modules, max_modules=0, max_depth=-1):
    # If depth, filter by number of parent packages
    if max_depth >= 0:
        modules = {k: v for k, v in iter_dict(modules)
                   if len(k.split('.')) <= max_depth + 1}

    # If no max_modules, include all modules
    if max_modules <= 0:
        max_modules = len(modules)

    print("Modules: {:d}".format(len(modules)))

    for m in sorted(modules.keys())[:max_modules]:
        print('  {!s}  ({!s})'.format(m, modules[m]))

    if len(modules) > max_modules:
        print('... and {:d} more'.format(len(modules) - max_modules))


class ListModulesAction(argparse.Action):
    """ An action that lists available python modules and exits.

    Usage:

    parser.add_argument('-o', '--option', help="Help")
    """

    default_help = """
        List modules and exit. Only modules matching a glob-like pattern
        '%(metavar)s' will be listed. The default pattern '%(const)s' will list
        all modules."""

    default_metavar = 'GLOB'

    def __init__(self, option_strings, dest,
                 type=None,
                 help=default_help,
                 metavar=default_metavar):
        super(ListModulesAction, self).__init__(
            option_strings=option_strings,
            dest=argparse.SUPPRESS,
            nargs='?',
            const='*',
            default=argparse.SUPPRESS,
            type=type,
            help=help,
            metavar=metavar)

    def __call__(self, parser, ns, opt_value, option_string=None):
        regex = re.compile(fnmatch.translate(opt_value))
        modules = {k: v
                   for k, v in iter_dict(_list_modules())
                   if regex.match(k)}

        print('Modules matching:', regex.pattern)
        depth = 0
        if opt_value != '*':
            depth = -1
        _print_modules(modules, max_depth=depth)
        parser.exit()


def edit(filename):
    """ Launch editor with file. """
    import subprocess

    editor = os.environ.get('EDITOR')
    if not editor:
        raise Exception(
            "Could not edit %r: No EDITOR environment variable set" %
            filename)

    try:
        subprocess.call([editor, filename])
    except OSError as e:
        raise Exception(
            "Could not edit %r (editor: %r): %s" %
            (filename, editor, e))


def main(inargs=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'module',
        help="Name of a module to look up")
    parser.add_argument(
        '-e', '--edit',
        action='store_true',
        default=False,
        help="Open the found module with $EDITOR")
    parser.add_argument(
        '-l', '--list',
        action=ListModulesAction)

    args = parser.parse_args(inargs)

    filename = get_module_file(args.module)
    print(filename)
    if args.edit:
        edit(filename)


if __name__ == '__main__':
    main()
