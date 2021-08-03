from datetime import date,datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from post_blog_app import db,login_manager,web_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column("id",db.Integer,primary_key=True)
    username = db.Column("uname",db.String(20),unique=True,nullable=False)
    email = db.Column("email_address",db.String(120),unique=True,nullable=False)
    image_file = db.Column("profile_pic",db.String(20),nullable=False,default="default.jpeg")
    password = db.Column("pwd",db.String(60),nullable=False)
    registered_on = db.Column("registered_on",db.Date,nullable=False,default=date.today)
    posts = db.relationship('Post',backref="author",lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(web_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(web_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"Users('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    title = db.Column("title",db.String(100),nullable=False)
    date_posted = db.Column("date",db.Date,nullable=False,default=date.today)
    content = db.Column("post_content",db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"