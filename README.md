# whichmodule

Find modules in the current python environment.


## Usage

```
usage: which-module [-h] [-l [GLOB]] module

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

````bash
$ whichmodule.py os.path
/usr/lib/python2.7/posixpath.py
```

List modules with globs:

```bash
$ which-module -l logging.*
Modules matching: 'logging\..*\Z(?ms)'
Modules: 2
  logging.config (/usr/lib/python2.7/logging/config.pyc)
  logging.handlers (/usr/lib/python2.7/logging/handlers.pyc)
```


## Caveats

Don't install with ``pip``! I haven't figured out how to prevent pip from
rewriting the shebang. The script needs to be executed with the
Python-executable of the environment you want to list packages for, so the
shebang needs to be ``#!/usr/bin/env python`` or equivalent.
