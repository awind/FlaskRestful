# FlaskRestful
A simple restful api web app build with Flask . This demo app use [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth) to provide basic token auth and use [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) ORM Framework to privide database access.

> Please build with Python 3.4.x and MySQL Server 5.7.x

##Restful API List


| URL        | Method           | Description  |
| :-------------: |:-------------:| :-----:|
| /api/login    | POST 		| login method |
| /api/user     | POST       |   create new user |
| /api/user     | GET        |    get user info |
| /api/book     | POST       |    create book for authorize user |
| /api/book     | GET        |    get user's book list |
| /api/book/<bookid>     | GET        |    get user's book info |
| /api/book/<bookid>     | DELETE       |    delete book for authorize user |


## Libraries Used
+ [Flask](https://github.com/mitsuhiko/flask)
+ [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
+ [Flask-Marshmallow](https://github.com/marshmallow-code/flask-marshmallow)
+ [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth)

