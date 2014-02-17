flask\_reddit
=============

**flask_reddit** is an extendable + minimalist [Reddit](http://reddit.com) clone.

This was built so beginners who want a standard CRUD + reddit-like application
can quickly get to work.

We utilize: 
- `flask` as the web framework.
- `nginx` as the HTTP server  
- `gunicon` as the wsgi server.
- `MySQL` for our database 
- `flask-sqlalchemy` as our ORM.
- `bootstrap-journal` theme makes us beautiful.
- `virtualenv` emcompasses everything. 
- `supervisord` makes sure our service never crashes.

And thats pretty much it!

All of the configutations are in this repository. Deployment instructions 
will be out soon.

Features
--------
- threaded comments
- up voting
- subreddits
- user karma
- search
- rate limiting
- ajax form posting
- user profiles

This build is missing one file. A `config.py` file in the currect directory. This
file contains application sensetive information but can be easily replicated for 
personal use.

Refer to the flask project configuration options to understand what to put in your own
config.py file.

This should be finished in 1-2 weeks! Feel free to `watch` or `star` my progress until then.

Do not hesiate to <a href="http://codelucas.com">contact</a> me <Lucas Ou-Yang> for help or concerns.
