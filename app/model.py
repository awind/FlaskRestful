from app import app, ma, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from functools import wraps
from flask import jsonify, request

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return jsonify({'status': 'fail', 'msg': 'expired token'})
        except BadSignature:
            return jsonify({'status': 'fail', 'msg': 'useless token'})
        kwargs['userid'] = data['id']
        return func(*args, **kwargs)
    return wrapper


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=1440*31*60):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username','id')


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    author = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('books', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, title, author, user_id):
        self.title = title
        self.author = author
        self.user_id = user_id

    def __repr__(self):
        return '<Book %s>' % self.title


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'title')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)
