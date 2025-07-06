#!/usr/bin/env python
# coding: utf-8

import os
from os.path import join as pjoin
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))

from setuptools import setup
from setupbase import combine_commands
from setupbase import create_cmdclass
from setupbase import ensure_targets
from setupbase import install_npm

nb_path = pjoin(HERE, "src", "binars", "nbextensions", "static")

# Files that should exist after a successful build
jstargets = [
    pjoin(nb_path, "index.js"),
]

package_data_spec = {
    "evidently": [
        "nbextension/static/*.*js*",
        "nbextension/static/*.*woff2*",
        "legacy/ui/assets/*",
        "legacy/ui/assets/static/css/*",
        "legacy/ui/assets/static/js/*",
        "legacy/ui/assets/static/img/*",
        "ui/service/assets/*",
        "ui/service/assets/static/css/*",
        "ui/service/assets/static/js/*",
        "ui/service/assets/static/img/*",
    ]
}

data_files_spec = [
    ("share/jupyter/nbextensions/bina", nb_path, "*.js"),
    ("share/jupyter/nbextensions/bina", nb_path, "*.woff2")
    ("etc/jupyter/nbextensions/bina", HERE, "bina.json")
]

cmdclass = create_cmdclass("jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec)
cmdclass["jsdeps"] = combine_commands(
    install_npm(os.path.join(HERE, "ui"), build_cmd="build"),
    ensure_targets(jstargets),
)
setup_args = dict(
    cmdclass=cmdclass,
    author_email="junocence@gmail.com",
    long_description=(Path(__file__).parent / "README.md").read_text("utf8"), # FIGURE THIS OUT #
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
            # FIGURE THIS OUT TOO #
        ] 
)