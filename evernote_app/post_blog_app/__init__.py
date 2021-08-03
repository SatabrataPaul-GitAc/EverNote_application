from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


web_app = Flask(__name__)
web_app.config['SECRET_KEY']="693eab612231fb67ae2f206f38dac69d"
web_app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db = SQLAlchemy(web_app)
bcrypt_obj = Bcrypt(app=web_app)
login_manager = LoginManager(web_app)
login_manager.login_view="login_page"
login_manager.login_message_category="warning"

web_app.config['MAIL_SERVER']='smtp.gmail.com'
web_app.config['MAIL_PORT']=587
web_app.config['MAIL_USE_TLS']=True
web_app.config['MAIL_USERNAME']=os.environ.get('email_user')
web_app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')

print(web_app.config['MAIL_USERNAME'])
print(web_app.config['MAIL_PASSWORD'])

mail=Mail(web_app)

from post_blog_app import routes
