# -*- coding: utf-8 -*-
"""
"""
from flask_reddit import db
from flask_reddit.threads import constants as THREAD


thread_upvotes = db.Table('thread_upvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('thread_id', db.Integer, db.ForeignKey('threads_thread.id'))
)

thread_downvotes = db.Table('thread_downvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('thread_id', db.Integer, db.ForeignKey('threads_thread.id'))
)

comment_upvotes = db.Table('comment_upvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('threads_comment.id'))
)

comment_downvotes = db.Table('comment_downvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('threads_comment.id'))
)

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

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # upvotes = db.Column()
    # downvotes = db.Column()
    comments = db.relationship('Comment', backref='thread', lazy='dynamic')

    status = db.Column(db.SmallInteger, default=THREAD.ALIVE)

    def __init__(self, title, body, link, user_id):
        self.title = title
        self.body = body
        self.link = link
        self.user_id = user_id

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
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        pass

    def comment_on(self):
        """
        when someone comments on this particular thread
        """
        pass

class Comment(db.Model):
    """
    This class is here because comments can only be made on threads,
    so it is contained completly in the threads module.

    Note the parent_id and children values. A comment can be commented
    on, so a comment has a one to many relationship with itself.

    Backrefs:
        A comment can refer to its parent thread with 'thread'
        A comment can refer to its parent comment (if exists) with 'parent'
    """
    __tablename__ = 'threads_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(THREAD.MAX_BODY), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads_thread.id'))

    parent_id = db.Column(db.Integer, db.ForeignKey('threads_comment.id'))
    children = db.relationship('Comment', backref='parent', lazy='dynamic')
    depth = db.Column(db.Integer, default=1) # start at depth 1

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # upvotes = db.Column(db.Integer)
    # downvotes = db.Column(db.Integer)

    def __repr__(self):
        return '<Comment %r>' % (self.body[:25])

    def __init__(self, thread_id, comment_id, user_id, body):
        self.thread_id = thread_id
        self.user_id = user_id
        self.body = body

    def get_age(self):
        """
        returns the raw age of this comment in seconds
        """
        pass

    def get_human_age(self):
        """
        returns a humanized version of the raw age of this comment,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        pass

    def comment_on(self):
        """
        when someone comments on this particular comment
        """
        pass


