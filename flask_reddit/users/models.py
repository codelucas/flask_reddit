# -*- coding: utf-8 -*-
"""
"""
from flask_reddit import db
from flask_reddit.users import constants as USER

class User(db.Model):
    """
    """
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USER.MAX_USERNAME), unique=True)
    email = db.Column(db.String(USER.MAX_EMAIL), unique=True)
    password = db.Column(db.String(USER.MAX_PASSW))
    created_on = db.Column(db.DateTime, default=db.func.now())

    threads = db.relationship('threads.Thread', backref='user', lazy='dynamic')

    # upvotes = db.Column()
    # downvotes = db.Column()

    status = db.Column(db.SmallInteger, default=USER.ALIVE)
    role = db.Column(db.SmallInteger, default=USER.USER)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return USER.STATUS[self.status]

    def get_role(self):
        """
        analogous to above but for roles
        """
        return USER.ROLE[self.role]
