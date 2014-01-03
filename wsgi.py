#!/usr/bin/env python

import sys
sys.path.insert(0, '/home/louyang/webapps/flask_reddit')

from werkzeug.debug import DebuggedApplication
from flask_reddit import app # as application

application = DebuggedApplication(app, True)

