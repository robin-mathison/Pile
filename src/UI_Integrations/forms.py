from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import  InputRequired,Length, EqualTo

class registerform(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=3,max=10)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=3,max=10)])
    confirm_password = PasswordField('Retype_Password',validators=[InputRequired(),Length(min=3,max=10),EqualTo('Password')])
    Submit = SubmitField('Sign up')

class Loginform(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=3,max=10)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=3,max=10)])
    Submit = SubmitField('Sign in')


