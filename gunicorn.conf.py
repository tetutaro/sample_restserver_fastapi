#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Gunicorn configurations for Docker container
"""
from typing import List, Optional
import os

# Current Directory
chdir: str = "/app"
# WSGI Application
wsgi_app: str = "backend.api:app"
# Daemon Mode
daemon: bool = False
# Server Socket
bind: str = "0.0.0.0:8930"
# Worker Processes
workers: int = 1
threads: int = 1
cpu_count: Optional[int] = os.cpu_count()
if cpu_count is not None:
    workers = 2 * cpu_count + 1
    threads = 2 * cpu_count + 1
worker_class: str = "uvicorn.workers.UvicornWorker"
# Environment Variables
raw_env: List[str] = ["WSGI_SERVER=gunicorn"]
# Debugging
relead: bool = False
