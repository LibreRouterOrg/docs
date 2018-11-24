#!/bin/sh

/usr/bin/xvfb-run /usr/bin/scribus-ng -g -ns -py generatepdf.py -- "$@"
