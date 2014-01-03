# -*- coding: utf-8 -*-
"""
"""
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])

class RegisterForm(Form):
    username = TextField('NickName', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])
    accept_tos = BooleanField('I accept the Terms of Service.', [Required()])
    recaptcha = RecaptchaField()

