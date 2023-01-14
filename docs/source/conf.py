#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

from sphinx_pyproject_poetry import SphinxConfig

sys.path.insert(0, os.path.abspath("../.."))
config = SphinxConfig("../../pyproject.toml", globalns=globals())
project = config.name
release = config.version
