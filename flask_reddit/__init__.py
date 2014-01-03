#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Written by:
Lucas Ou-Yang -- http://codelucas.com
Jason Tanner -- http://jasontanner.herokuapp.com
"""
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

IS_DEBUG = True
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from flask_reddit.users.views import mod as users_module
app.register_blueprint(users_module)

from flask_reddit.threads.views import mod as threads_module
app.register_blueprint(threads_module)

@app.route("/")
def hello():
    return render_template('home.html')

app.debug = IS_DEBUG
if __name__ == "__main__":
    print 'We are running flask via main()'
    app.run()
