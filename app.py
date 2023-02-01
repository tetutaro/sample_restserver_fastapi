#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""start backend server at local machine in debug mode
"""
from typing import NamedTuple

import uvicorn


class UnicornArgs(NamedTuple):
    app: str
    host: str
    port: int
    reload: bool


def main() -> None:
    """invoke FastAPI using uvicorn"""
    kwargs: UnicornArgs = UnicornArgs(
        app="backend.api:app",
        host="0.0.0.0",
        port=8930,
        reload=True,
    )
    uvicorn.run(**kwargs._asdict())
    return


if __name__ == "__main__":
    main()
