#!/usr/bin/env python
# coding: utf-8

"""
This file originates from the 'jupyter-packaging' package, and
contains a set of useful utilities for including npm packages
within a Python package.
"""
import functools
import io
import os 
import re 
import shlex 
from typing import Sequence
import subprocess 
import sys
from collections import defaultdict
from os.path import join as pjoin

# Placeholder MANIFEST (Update when directory content changes)
if os.path.exists("MANIFEST"):
    os.remove("MANIFEST")
    
import logging
from setuptools import command
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.develop import develop

# list2cmdline: quote each argv and join into a shell-safe string
import shlex 

if hasattr(shlex, "join"):
    list2cmdline = shlex.join
else:
    from shlex import quote
    def list2cmdline(cmd_list: Sequence[str]) -> str:
        return " ".join(quote(arg) for arg in cmd_list)

__version__ = "0.2.0"

# ---------------------------------------------------------------------------
# Base Variables
# ---------------------------------------------------------------------------

HERE = os.path.abspath(os.path.dirname(__file__))
is_repo = os.path.exists(pjoin(HERE, ".git"))
node_modules = pjoin(HERE, "node_modules")

SEPARATORS = os.sep if os.altsep is None else os.sep + os.altsep


npm_path = ":".join(
    [
        pjoin(HERE, "node_modules", ".bin"),
        os.environ.get("PATH", os.defpath),
    ]
) 

if "--npm" in sys.argv:
    print("Rebuild UI as requested")
    build_npm = True
    sys.argv.remove("--npm")
else:
    build_npm = False
    
# ---------------------------------------------------------------------------
# Public Functions
# ---------------------------------------------------------------------------

def get_version(file, name="__version__"):
    """Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]

def find_package(top=HERE):
    """
    Find the packages.
    """
    packages = []
    for d, dirs, _ in os.walk(top, followlinks=True):
        if os.path.exists(pjoin(d, "__init.py__")):
            packages.append(os.path.relpath(d, top).replace(os.path.sep, "."))
        elif d !=top:
            # Do not look for packages in subfolders if current is not a package
            dirs[:] = []
    return packages

def update_package_date(distribution):
    """ Update build_py options to get package_data changes """
    build_py = distribution.get_command_obj("build_py")
    build_py.finalize_options()
    
    
class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg

    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """
    
    def run(self):
        sys.exit("Aborting implicit building of eggs. Use `pip install .` " " to install from source.")
        
       # Work on this more as it expands. Thus far, this is a framework for the parts you pictured.