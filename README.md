# whichmodule

Find modules in the current python environment.


## Setup

The script needs to be executed with the Python-executable of the environment
you want to list packages for.

You can make the script work in multiple python environments and across multiple
python versions by executing it with ``/usr/bin/env python``.


### ``PATH``

Simply add the module to your ``$PATH``:

```bash
$ echo 'export PATH="$PATH:/path/to/repo"' >> ~/.bashrc
```

> For this to work, the ``whichmodule.py`` script must be executable (``chmod +x
> whichmodule.py``), and the shebang must remain untouched (``#!/usr/bin/env
> python``).


### alias

Make an alias that executes the script with ``/usr/bin/env python``:

```bash
$ echo 'alias whichmodule.py="/usr/bin/env python /path/to/repo/whichmodule.py"' >> ~/.bashrc
```


### Install with setup script

You can install the script in whatever environment you need:

```bash
$ virtualenv foo
$ source foo/bin/activate
(foo) $ pip install /path/to/repo
(foo) $ # or
(foo) $ python /path/to/repo/setup.py install
```

> Note that this will rewrite the shebang, so running
> ``/path/to/foo/bin/whichmodule.py`` will always target that environment. You
> can still use it from other environments with ``/usr/bin/env python
> /path/to/foo/bin/whichmodule.py``, or set that up as an alias in bash.


## Usage

```
usage: whichmodule.py [-h] [-l [GLOB]] module

Look up and return file location of a module.

positional arguments:
  module                Name of a module to look up

optional arguments:
  -h, --help            show this help message and exit
  -l [GLOB], --list [GLOB]
                        List modules and exit. Only modules matching a glob-
                        like pattern 'GLOB' will be listed. The default
                        pattern '*' will list all modules.
```


The default behaviour is to look up and show the path to certain modules:

```bash
$ whichmodule.py os.path
/usr/lib/python2.7/posixpath.py
```

```bash
(foo) $ whichmodule.py os.path
/path/to/foo/lib64/python2.7/posixpath.py
```

```bash
$ whichmodule.py sys
Traceback (most recent call last):
  …
TypeError: <module 'sys' (built-in)> is a built-in module
```


With the ``-l`` switch, you can search for modules by [glob patterns].

You could look up submodules of the ``logging`` module:

```bash
$ whichmodule.py -l logging.*
Modules matching: 'logging\..*\Z(?ms)'
Modules: 2
  logging.config (/usr/lib/python2.7/logging/config.pyc)
  logging.handlers (/usr/lib/python2.7/logging/handlers.pyc)
```

Or look up which packages provides a ``config`` module or sub-package:

```bash
$ whichmodule.py -l *.config
Modules matching: '.*\.config\Z(?ms)'
Modules: 9
  ansible.cli.config  (/usr/lib/python2.7/site-packages/ansible/cli/config.py)
  ansible.config  (/usr/lib/python2.7/site-packages/ansible/config/__init__.pyc)
  distutils.command.config  (/usr/lib64/python2.7/distutils/command/config.py)
  distutils.config  (/usr/lib64/python2.7/distutils/config.py)
  flake8.options.config  (/usr/lib/python2.7/site-packages/flake8/options/config.py)
  logging.config  (/usr/lib64/python2.7/logging/config.py)
  mercurial.config  (/usr/lib64/python2.7/site-packages/mercurial/config.py)
  setuptools.config  (/usr/lib/python2.7/site-packages/setuptools/config.py)
  tox.config  (/usr/lib/python2.7/site-packages/tox/config.py)
```

  [glob patterns]: https://docs.python.org/3/library/fnmatch.html
