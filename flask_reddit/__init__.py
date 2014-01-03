#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Written by:
Lucas Ou-Yang -- http://codelucas.com
Jason Tanner -- http://jasontanner.herokuapp.com
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
