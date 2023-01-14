#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""revoke FastAPI using uvicorn
"""
import uvicorn


def main() -> None:
    """revoke FastAPI using uvicorn"""
    kwargs = {
        "app": "backend.api:app",
        "host": "0.0.0.0",
        "port": 8930,
        "reload": True,
    }
    uvicorn.run(**kwargs)
    return


if __name__ == "__main__":
    main()
