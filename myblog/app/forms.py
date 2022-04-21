from io import StringIO
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError, Length
from app.models import User
import re
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeated Password', validators=[DataRequired(), EqualTo('password')])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Register')

    def username_validate(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def email_validate(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def password_strength(self,password):
        if(len(password)<7):
            raise ValidationError('Weak password. Too short')
        elif not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password) or re.search("\s", password) :
            raise ValidationError('Password must contain lowercase letter, uppercase letter, number 0-9 and no space')
class ProfileEditingForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    aboutMe = TextAreaField('About me', validators=[Length(min=0, max=200)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')

    def __init__(self, orignal_username, original_email, *args, **kwargs):
        super(ProfileEditingForm,self).__init__(*args,**kwargs)
        self.original_username = orignal_username
        self.original_email = original_email
    def validate_username(self,username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError('Username exist, please chose a different one')
    def validate_email(self,email):
        if email.data != self.original_email:
            user = User.query.filter_by(email = self.email.data).first()
            if user is not None:
                raise ValidationError('Email exist, please chose a different one')
    
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
class PostingForm(FlaskForm):
    post = TextAreaField('Type here',validators=[DataRequired(),Length(min=1,max=200)])
    submit = SubmitField('Submit')