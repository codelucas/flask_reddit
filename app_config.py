#!/usr/bin/env python2.7
"""
app_config.py will be storing all the module configs.
Here the db uses mysql.
"""

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['your_email_here@email.com'])
SECRET_KEY = ''

SQLALCHEMY_DATABASE_URI = 'DATABASE://USERNAME:PASSWORD@localhost/YOUR_DB_NAME'
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = ""

# customize and add the blow if you'd like to use recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_OPTIONS = {'theme': 'white'}

BRAND = "reddit"
DOMAIN = "YOUR_DOMAIN_HERE"
ROOT_URL = "http://YOUR_URL_HERE"

STATIC_ROOT = "/path/to/your/static/root/"
STATIC_URL = ROOT_URL + "/static/"
