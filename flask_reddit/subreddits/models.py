# -*- coding: utf-8 -*-
"""
All database abstractions for subreddits go in this file.
"""
from flask_reddit import db
from flask_reddit.subreddits import constants as SUBREDDIT
from flask_reddit.threads import Thread
from flask_reddit import utils
import datetime

class Subreddit(db.Model):
    """
    """
    __tablename__ = 'subreddits_subreddit'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(SUBREDDIT.MAX_NAME))
    desc = db.Column(db.String(SUBREDDIT.MAX_DESCRIPTION), default=None)

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
