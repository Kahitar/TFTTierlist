from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from tierlist import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # One-to-many relationships
    tierlists = db.relationship('Tierlist', backref='author', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', 'admin:{self.is_admin}')"


class Tierlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='New Tierlist')
    is_public = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(
        db.DateTime, unique=True, nullable=True, default=datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comps = db.relationship('Comp', backref='tierlist', lazy=True)

    def __repr__(self):
        return f"Tierlist('Name: {self.name}', 'Public: {self.is_public}', 'Author: {self.author.username}', 'Last update: {self.last_updated}')"


class Comp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.Integer, nullable=False)
    sub_tier = db.Column(db.Integer, nullable=False)
    carries = db.Column(db.String(100), nullable=False)
    synergies = db.Column(db.String(100), nullable=False)
    lolchess = db.Column(db.String(200), nullable=False)
    chosen = db.Column(db.String(100), nullable=False)

    # Relationships
    list_id = db.Column(db.Integer, db.ForeignKey(
        'tierlist.id'), nullable=False)

    def __repr__(self):
        return f"Comp('ID: {self.id}', 'Carries: {self.carries}', 'Tier: {self.tier}.{self.sub_tier}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True)

    # One-to-many relationship between User and Post
    #    The 'user' in 'user.id' is lowercase here because SQLAlchemy automatically creates
    #    an object for the User class, which is named user.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
