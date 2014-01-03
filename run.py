#!/usr/bin/env python

"""
/run.py will be used to launch the web server.
"""

from flask_reddit import app
app.run(debug=True)
