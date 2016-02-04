from app import app, db, auth
from flask import request, g, jsonify, abort
from .model import User, Book, user_schema, users_schema, book_schema, books_schema, token_required


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/api/login', methods=['POST'])
@auth.login_required
def login():
    user = g.user
    token = user.generate_auth_token()
    return jsonify(username=user.username, token=token.decode('ascii'))


@app.route('/api/user', methods = ['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    user.save()
    return user_schema.jsonify(user)


@app.route('/api/user/<int:userid>', methods=['GET'])
@token_required
def get_user(userid):
    user = User.query.get(userid)
    if not user:
        abort(400)
    return user_schema.jsonify(user)


@app.route('/api/book', methods=['POST'])
@token_required
def create_book(userid):
    user = User.query.get(userid)
    if not user:
        abort(400)
    title = request.json['title']
    author = request.json['author']
    if title is None or author is None:
        abort(400)
    book = Book(title=title, author=author, user_id=userid)
    book.save()
    return jsonify(status="success")


@app.route('/api/book', methods=['GET'])
@token_required
def get_books(userid):
    user = User.query.get(userid)
    if not user:
        abort(400)
    books = user.books.all()
    result = books_schema.dump(books)
    return jsonify(books=result.data)


@app.route('/api/book/<int:bookid>', methods=['GET'])
@token_required
def get_book(userid, bookid):
    book = Book.query.filter_by(user_id=userid, id=bookid).first()
    if not book:
        abort(400)
    return book_schema.jsonify(book)


@app.route('/api/book/<int:bookid>', methods=['DELETE'])
@token_required
def delete_book(userid, bookid):
    book = Book.query.filter_by(user_id=userid, id=bookid).first()
    if not book:
        abort(400)
    book.delete()
    return jsonify(status='success')





