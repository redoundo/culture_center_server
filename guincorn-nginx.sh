#!/bin/bash
gunicorn -w 1 --bind 172.31.32.74:8077 wsgi:flask_app
nginx