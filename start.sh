#!/bin/sh
gunicorn -w 4 application:app -b $FLASK_RUN_HOST:5000
