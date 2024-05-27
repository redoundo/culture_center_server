#!/bin/bash
gunicorn -w 1 --bind 0.0.0.0:8077 wsgi:flask_app
nginx