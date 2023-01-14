#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""start backend server at local machine in debug mode
"""
import uvicorn


def main() -> None:
    """invoke FastAPI using uvicorn"""
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
