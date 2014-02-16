# -*- coding: utf-8 -*-
"""
All database abstractions for subreddits go in this file.

I had to add the Subreddit model in manually via SQL, here were
my commands:

CREATE TABLE `subreddits_subreddit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `desc` varchar(3000) DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`admin_id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `subreddits_subreddit_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users_user` (`id`)
);

ALTER TABLE threads_thread ADD subreddit_id INT(11) DEFAULT 0;
alter table threads_thread drop subreddit_id;
alter table threads_thread add subreddit_id int(11) not null default 0;
insert into subreddits_subreddit (name, `desc`, admin_id) values('first_subreddit',
    'This is to get the sql up and running', 1);

ALTER TABLE threads_thread ADD CONSTRAINT threads_thread_ibfk_2 FOREIGN KEY (subreddit_id)
    references subreddits_subreddit(id);
"""
from flask_reddit import db
from flask_reddit.subreddits import constants as SUBREDDIT
from flask_reddit.threads.models import Thread
from flask_reddit import utils
import datetime

class Subreddit(db.Model):
    """
    """
    __tablename__ = 'subreddits_subreddit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(SUBREDDIT.MAX_NAME), unique=True)
    desc = db.Column(db.String(SUBREDDIT.MAX_DESCRIPTION))

    admin_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    threads = db.relationship('Thread', backref='subreddit', lazy='dynamic')
    status = db.Column(db.SmallInteger, default=SUBREDDIT.ALIVE)

    def __init__(self, name, desc, admin_id):
        self.name = name
        self.desc = desc
        self.admin_id = admin_id

    def __repr__(self):
        return '<Subreddit %r>' % (self.name)

    def get_threads(self, order_by='timestamp'):
        """
        default order by timestamp
        """
        if order_by == 'timestamp':
            return self.threads.order_by(db.desc(Thread.created_on)).\
                all()[:SUBREDDIT.MAX_THREADS]
        else:
            return self.threads.order_by(db.desc(Thread.created_on)).\
                all()[:SUBREDDIT.MAX_THREADS]

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return SUBREDDIT.STATUS[self.status]

    def get_age(self):
        """
        returns the raw age of this subreddit in seconds
        """
        return (self.created_on - datetime.datetime(1970, 1, 1)).total_seconds()

    def pretty_date(self, typeof='created'):
        """
        returns a humanized version of the raw age of this subreddit,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated':
            return utils.pretty_date(self.updated_on)
    """
    def add_thread(self, comment_text, comment_parent_id, user_id):
        if len(comment_parent_id) > 0:
            comment_parent_id = int(comment_parent_id)
            comment = Comment(thread_id=self.id, user_id=user_id,
                    text=comment_text, parent_id=comment_parent_id)
        else:
            comment = Comment(thread_id=self.id, user_id=user_id,
                    text=comment_text)

        db.session.add(comment)
        db.session.commit()
        comment.set_depth()
        return comment
    """
