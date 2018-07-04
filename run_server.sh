#!/usr/bin/env bash
uwsgi --http-socket :6082 --gevent 4 --py-autoreload 1 --wsgi-file server.py
