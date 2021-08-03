import os,secrets
from post_blog_app import web_app,mail
from PIL import Image
from flask_mail import Message
from flask import url_for,render_template

#The following function has the functionality of updating a user's profile picture. 
def save_profile_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(web_app.root_path,"static/profile_pic",picture_fn)
    output_size = (150,150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


#This function has a has the functionality of sending an email , when a user creates a account.
def welcome_email(user):
    msg = Message("Welcome to Evernote",sender="noreply@evernote.app.com",recipients=[user.email])
    msg.html = render_template("welcome_mail.html",name=user.username,link=url_for("login_page",_external=True))
    mail.send(msg)


#The following function sends an email to the user , for the password reset . 
def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",sender="noreply@evernote.app.com",recipients=[user.email])
    msg.html= f'''<h2>Please Click on the following link , to reset your passsword</h2>:<br> 
{url_for("reset_token",token=token,_external=True)}<br>

<h3>If you didn;t make this request , Ignore this mail . No Changes will be made</h3>
'''
    mail.send(msg)
    
