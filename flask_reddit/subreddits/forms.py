# -*- coding: utf-8 -*-
"""
"""
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

class SubmitForm(Form):
    name = TextField('Name', [Required()])
    desc = TextAreaField('Description of this subreddit.', [Required()])
