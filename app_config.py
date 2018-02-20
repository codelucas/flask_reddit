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

# Customize and add the blow if you'd like to use recaptcha. SSL is enabled
# by default and this is recaptcha v2: tap "I'm not a robot" checkbox instead
# of answering a riddle.
# Please see: https://www.google.com/recaptcha
RECAPTCHA_DATA_ATTRS = {'theme': 'light'}
RECAPTCHA_PUBLIC_KEY = 'YOUR KEY HERE'
RECAPTCHA_PRIVATE_KEY = 'YOUR PRIVATE KEY HERE'

BRAND = "reddit"
DOMAIN = "YOUR_DOMAIN_HERE"
ROOT_URL = "http://YOUR_URL_HERE"

STATIC_ROOT = "/path/to/your/static/root/"
STATIC_URL = ROOT_URL + "/static/"
