#!/usr/bin/env python

# scaffolding to call shell commands
from subprocess import check_output
from shlex import split
cmd = lambda s: check_output(split(s)).strip().decode()

from setuptools import setup

# package metadata
name = "datesieve"
version = cmd('sh ./version.sh describe')
author = "Anton Semjonov"
email = "anton@semjonov.de"
github = "https://github.com/ansemjo/%s" % name

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    url=github,
    scripts=[name],
    python_requires='>3',
    install_requires=['python-dateutil'],
)
