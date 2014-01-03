#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Written by:
Lucas Ou-Yang -- http://codelucas.com
Jason Tanner -- http://jasontanner.herokuapp.com
"""
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.users.views import mod as users_module
app.register_blueprint(users_module)

@app.route("/")
def hello():
    return render_template('base.html'

if __name__ == "__main__":
    app.run()
