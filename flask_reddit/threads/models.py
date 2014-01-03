# -*- coding: utf-8 -*-
"""
"""
from flask_reddit import db
from flask_reddit.threads import constants as THREAD

class Thread(db.Model):
    """
    We will mimic reddit, with votable threads. Each thread may have either
    a body text or a link, but not both.
    """
    __tablename__ = 'threads_thread'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(THREAD.MAX_TITLE))
    body = db.Column(db.String(THREAD.MAX_BODY), default=None)
    link = db.Column(db.String(THREAD.MAX_LINK), default=None, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # upvotes = db.Column()
    # downvotes = db.Column()
    # comments = db.Column()

    status = db.Column(db.SmallInteger, default=THREAD.ALIVE)

    def __init__(self, title, body, link, user):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Thread %r>' % (self.title)

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return THREAD.STATUS[self.status]

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        pass

    def get_human_age(self):
        """
        returns a humanized version of the raw age of this thread
        in seconds, eg: 34 minutes ago versus 2040 seconds ago.
        """
        pass
