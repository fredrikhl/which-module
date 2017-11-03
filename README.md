# whichmodule

Find modules in the current python environment.


## Caveats

The script needs to be executed with the Python-executable of the environment
you want to list packages for, so the shebang needs to be ``#!/usr/bin/env
python`` or equivalent.


## Setup

Simply add the module to your ``$PATH`` in order to make it available in all python
environments:

```bash
$ echo 'export PATH="$PATH:/path/to/repo"' >> ~/.bashrc
```

> For this to work, the ``whichmodule.py`` script must be executable (``chmod +x
> whichmodule.py``), and the shebang must remain untouched (``#!/usr/bin/env
> python``).

If you install the script, you'll bind the script to the environment you install
it in:

```bash
$ virtualenv foo
$ source foo/bin/activate
(foo) $ pip install /path/to/repo
```

You can still make the script universally available for all environments with an
alias:

```bash
$ echo 'alias whichmodule.py="/usr/bin/env python /path/to/foo/bin/whichmodule.py"' >> ~/.bashrc
```


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


## Examples


Find a specific module:

```bash
$ whichmodule.py os.path
/usr/lib/python2.7/posixpath.py
```

```bash
(foo) $ whichmodule.py os.path
/path/to/foo/lib64/python2.7/posixpath.py
```


List modules with globs:

```bash
$ whichmodule.py -l logging.*
Modules matching: 'logging\..*\Z(?ms)'
Modules: 2
  logging.config (/usr/lib/python2.7/logging/config.pyc)
  logging.handlers (/usr/lib/python2.7/logging/handlers.pyc)
```
