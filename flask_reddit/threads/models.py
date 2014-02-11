# -*- coding: utf-8 -*-
"""
"""
from flask_reddit import db
from flask_reddit.threads import constants as THREAD
from flask_reddit import utils
import datetime

thread_upvotes = db.Table('thread_upvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('thread_id', db.Integer, db.ForeignKey('threads_thread.id'))
)

comment_upvotes = db.Table('comment_upvotes',
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
    text = db.Column(db.String(THREAD.MAX_BODY), default=None)
    link = db.Column(db.String(THREAD.MAX_LINK), default=None)
    thumbnail = db.Column(db.String(THREAD.MAX_LINK), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # upvotes = db.Column()
    # downvotes = db.Column()
    comments = db.relationship('Comment', backref='thread', lazy='dynamic')

    status = db.Column(db.SmallInteger, default=THREAD.ALIVE)

    def __init__(self, title, text, link, user_id):
        self.title = title
        self.text = text
        self.link = link
        self.user_id = user_id

    def __repr__(self):
        return '<Thread %r>' % (self.title)

    def get_comments(self, order_by='timestamp'):
        """
        default order by timestamp
        return only top levels!
        """
        if order_by == 'timestamp':
            return self.comments.filter_by(depth=1).\
                order_by(db.desc(Comment.created_on)).all()[:500]
        else:
            return self.comments.filter_by(depth=1).\
                order_by(db.desc(Comment.created_on)).all()[:500]

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return THREAD.STATUS[self.status]

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        return (self.created_on - datetime.datetime(1970,1,1)).total_seconds()

    def pretty_date(self, typeof='created'):
        """
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated':
            return utils.pretty_date(self.updated_on)

    def comment_on(self):
        """
        when someone comments on this particular thread
        """
        pass

    def get_score(self):
        """
        return number of matching rows in thread_upvotes
        """
        pass


    def vote(self):
        """
        ins = thread_upvotes.insert(user_id=user.id, thread_id=self.id)
        db.engine.execute(ins)
        """
        pass

    def extract_thumbnail(self):
        """
        use reddit algorithm to extract thumbnail from link, grayscale it
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
    text = db.Column(db.String(THREAD.MAX_BODY), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads_thread.id'))

    parent_id = db.Column(db.Integer, db.ForeignKey('threads_comment.id'))
    children = db.relationship('Comment', backref=db.backref('parent',
            remote_side=[id]), lazy='dynamic')

    depth = db.Column(db.Integer, default=1) # start at depth 1

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # upvotes = db.Column(db.Integer)

    def __repr__(self):
        return '<Comment %r>' % (self.text[:25])

    def __init__(self, thread_id, user_id, text, parent_id=None):
        self.thread_id = thread_id
        self.user_id = user_id
        self.text = text
        self.parent_id = parent_id

    def set_depth(self):
        """
        call after initializing
        """
        if self.parent:
            self.depth = self.parent.depth + 1
            db.session.commit()

    def get_comments(self, order_by='timestamp'):
        """
        default order by timestamp
        """
        if order_by == 'timestamp':
            return self.children.order_by(db.desc(Comment.created_on)).all()[:500]
        else:
            return self.comments.order_by(db.desc(Comment.created_on)).all()[:500]

    def get_margin_left(self):
        """
        nested comments are pushed right on a page
        -15px is our default margin for top level comments
        """
        margin_left = 15 + ((self.depth-1) * 32)
        margin_left = min(margin_left, 680)
        return str(margin_left) + "px"

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        return (self.created_on - datetime.datetime(1970,1,1)).total_seconds()

    def pretty_date(self, typeof='created'):
        """
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated':
            return utils.pretty_date(self.updated_on)

    def vote(self, direction):
        """
        """
        pass

    def comment_on(self):
        """
        when someone comments on this particular comment
        """
        pass
