from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
import email_validator
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,email,EqualTo,ValidationError
from post_blog_app.models import User


class registration_form(FlaskForm):
        username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
        email = StringField('Email Adddress',
                validators=[DataRequired(),email(message="Not a valid email address")])
    
        password = PasswordField('Password',validators=[DataRequired()])

        confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(),EqualTo('password',message="Password doesn't match")])

        submit = SubmitField('Sign Up')

        def validate_username(self,username):
                user = User.query.filter_by(username=username.data).first()
                if user:
                        raise ValidationError("This username is already taken !! Choose a different one .")

        def validate_email(self,email):
                user = User.query.filter_by(email=email.data).first()
                if user:
                        raise ValidationError("This email is already taken !! Choose a different one .")
        


class login_form(FlaskForm):
    email = StringField('Email Adddress',
            validators=[DataRequired(),email(message="Not a Valid Email Address",granular_message="Valid Email")])
    password = PasswordField('Enter password',validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class account_update_form(FlaskForm):
        username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
        email = StringField('Email Adddress',
                validators=[DataRequired(),email(message="Not a valid email address")])

        profile_pic = FileField("Update Profile Picture",validators=[FileAllowed(["png","jpg","jpeg"])])
    
        submit = SubmitField('Update')

        def validate_username(self,username):
                if(username.data != current_user.username):
                        user = User.query.filter_by(username=username.data).first()
                        if user:
                                raise ValidationError("This username is already taken !! Choose a different one .")

        def validate_email(self,email):
                if(email.data != current_user.email):
                        user = User.query.filter_by(email=email.data).first()
                        if user:
                                raise ValidationError("This email is already taken !! Choose a different one .")
                
class post_form(FlaskForm):
        title = StringField('Title',validators=[DataRequired()])
        content = TextAreaField("Content",validators=[DataRequired()])
        submit = SubmitField("Post")


class request_reset_form(FlaskForm):
        email = StringField('Email Adddress',
                validators=[DataRequired(),email(message="Not a valid email address")])
        submit = SubmitField("Request Password Reset")

        def validate_email(self,email):
                user = User.query.filter_by(email=email.data).first()
                if user is None:
                        raise ValidationError("No Account exists with this email . Please Create One !")

class password_reset_form(FlaskForm):
        password = PasswordField('New Password',validators=[DataRequired()])

        confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(),EqualTo('password',message="Password doesn't match")])

        submit = SubmitField("Reset Password")

