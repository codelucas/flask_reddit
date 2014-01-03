#!/usr/bin/env python
"""
/shell.py will allow you to get a console and enter commands within your flask environment.
"""

import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'
