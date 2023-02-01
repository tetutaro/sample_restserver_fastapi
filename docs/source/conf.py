#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import Dict, Optional, Any
import os
import sys

from sphinx_pyproject_poetry import SphinxConfig

sys.path.insert(0, os.path.abspath("../.."))
config = SphinxConfig("../../pyproject.toml", globalns=globals())
project = config.name


def linkcode_resolve(
    domain: str,
    info: Dict[str, Any],
) -> Optional[str]:
    if domain != "py":
        return None
    if not info["module"]:
        return None
    filename = info["module"].replace(".", "/")
    if filename == "backend":
        filename += "/__init__.py"
    elif not filename.endswith(".py"):
        filename += ".py"
    return (
        "https://github.com/tetutaro/sample_restserver_fastapi/"
        f"blob/main/{filename}"
    )
