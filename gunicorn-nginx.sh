#!/bin/bash
echo "nginx get started!!!"
nginx
echo "gunicorn start"
gunicorn -w 1 --bind 0.0.0.0:8077 wsgi:flask_app