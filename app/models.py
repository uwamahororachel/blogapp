from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime



class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog',backref='user',lazy = 'dynamic')
    comments = db.relationship('Comment',backref='user',lazy = 'dynamic')
    # reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")
  
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}' 
class Blog(db.Model):
    

    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog = db.Column(db.String)
    category = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref='blog',lazy='dynamic')
    

    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls):
        blogs = Blog.query.all()
        return blogs

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment= db.Column(db.String(255))

    @classmethod
    def get_comments(cls,blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return comments


    
   

class Quotes:
    '''
    Quotes class to define Quotes Objects
    '''

    def __init__(self,author,quote):
       
        self.author=author
        self.quote= quote
      


