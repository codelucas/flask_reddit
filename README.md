flask\_reddit
============

*I'm still working on this, but this project should be finished in an expected 1-2 weeks.*

**flask_reddit** is an extendable + minimalist [Reddit](http://reddit.com) clone built with flask.

We utilize: 
- `nginx` as the HTTP server  
- `gunicon` as the wsgi serer.
- `MySQL` for our database 
- `flask-sqlalchemy` as our ORM.
- `virtualenv` emcompasses everything. 
- `supervisord` makes sure our service never crashes.

And thats pretty much it!

All of the configutations are in this repository. Deployment instructions 
will be out soon.

Expected Features
-----------------
- threaded comments
- voting
- subreddits
- user karma
- rate limiting
- AJAX to smooth user actions


This build is missing one file. A `config.py` file in the currect directory. This
file contains application sensetive information but can be easily replicated for 
personal use.

Refer to the flask project configuration options to understand what to put in your own
config.py file.

This should be finished in 1-2 weeks! Feel free to `watch` or `star` my progress until then.
