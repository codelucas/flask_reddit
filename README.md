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

Build Instructions
------------------

- Set up an instance of MySQL on your server. Note your username and password.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install mysql-server libmysqlclient-dev
```

- Set up an instance of nginx on your server. *I've provided the .conf scripts needed for our
servers in the `/server` directory.*

`sudo apt-get install nginx`

- Configure your nginx settings located in `flask_reddit/server/nginx.conf`.

- Add your settings into your global conf file located in `/etc/nginx/nginx.conf`

- Restart nginx to recognize your settings `sudo service nginx restart`

- Set up supervisord to monitor your project to make sure it never crashes.
Supervisor is also convenient for simply restarting/starting your project with ease.

`sudo apt-get install supervisor`

- When Supervisor is installed you can give it programs to start and watch by creating config 
files in the `/etc/supervisor/conf.d` directory. I've provided the conf file which we use
in the root directory of this repo as `supervisor.conf`. An example supervisor command 
would be running `supervisorctl restart YOUR_APP_NAME` to restart gunicorn and bring up new changes.

- Install [virtualenv](http://www.virtualenv.org/en/latest/virtualenv.html) and set up a project 
root where ever you want.

```bash
sudo apt-get install python-virtualenv;
cd /path/to/project;
virtualenv reddit-env;
cd reddit-env;
source bin/activate; # viola, you are now in an enclosed python workspace.
```

- Download the repository and  install all of the required python modules 
which this server uses.

```bash
git clone https://github.com/codelucas/flask_reddit.git;
cd flask_reddit;
pip install -r requirements.txt
```

- Due to sensitive configuration information, I have hidden my personal
`config.py` file in the gitignore. But, I have provided a clean and easy
to use config template in this repo named `app_config.py`. 

- **Fill out the `flask_reddit/app_config.py` file with your own information and then rename it to
`config.py` so flask recognizes it by using `mv app_config.py config.py`.**
Please be sure to fill out the mysql db settings similarly to how you set it up!, 
username, pass, etc

- Run the `kickstart.py` script to build the first user and subreddits.

`python2.7 kickstart.py`

- flask_reddit has tasks which must **occur on regular time intervals**. To make this
happen, we use the `crontab`, which is present on UNIX systems.

A crontab is a dash which allows you to specify what programs to run and how often.
I've provided flask_reddit's example crontab in the root directory as `jobs.cron`.

To view your current crontab, run `crontab -l`. To edit your crontab, run `crontab -e`.

- Paste the contents of `jobs.cron` into your crontab by running `crontab -e` and 
pasting! More directions are present in the `jobs.cron` file.

- Run the gunicorn server. You won't have to do this ever again if `supervisor` is set up
properly.

`sudo sh run_gunicorn.sh`

**Note that we have now deployed two servers: `nginx` and `gunicorn`. `nginx` is our
*internet facing* HTTP server on port 80 while `gunicorn` is our *wsgi server* which 
is serving up our flask python application locally. `nginx` reads client
requests and *decides* which requests to foreward to our `gunicorn` server. For example,
`nginx` serves static content like images very well but it forwards url routes 
to the homepage to gunicorn.**

For a full list of details, view our configs at `server/nginx.conf` and 
`server/gunicorn_config.py`.

*Note, for this build to work there are paths that you must change in the `wsgi.py` file, 
the server configs located in `server` directory and the `run_gunicorn.sh` file.*

*Refer to the flask project configuration options to understand what to put in your own
config.py file.*

Do not hesiate to <a href="http://codelucas.com">contact</a> me <Lucas Ou> for help or concerns.

