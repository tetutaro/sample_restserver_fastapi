#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Gunicorn configurations for Docker container
"""
import os

# Current Directory
chdir = "/app"
# WSGI Application
wsgi_app = "backend.api:app"
# Daemon Mode
daemon = False
# Server Socket
bind = "0.0.0.0:8930"
# Worker Processes
workers = 2 * os.cpu_count() + 1
threads = 2 * os.cpu_count() + 1
worker_class = "uvicorn.workers.UvicornWorker"
# Environment Variables
raw_env = ["WSGI_SERVER=gunicorn"]
# Debugging
relead = False
