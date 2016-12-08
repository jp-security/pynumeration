import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY='secret!'
PROPAGATE_EXCEPTION=True
SQLALCHEMY_DATABASE_URI=('mysql://@localhost/enumeration')

port = 5000
localhost = '127.0.0.1'
