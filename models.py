from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='posts', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True, cascade="all, delete-orphan")

    def is_liked_by_user(self, user_id):
        # Check if this post is liked by the current user
        return Like.query.filter_by(post_id=self.id, user_id=user_id).count() > 0

    def to_dict(self):
        post_dict = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "username": self.user.username,
            "likes_count": len(self.likes),
        }
        if self.user_id:
            post_dict["is_liked"] = self.is_liked_by_user(self.user_id)
        return post_dict

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)