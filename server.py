from flask import Flask, request, jsonify
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy


# app
app = Flask(__name__)

#configuration to use local file as a database
#config acts liek a dictioanry so we need to add keys to connect to our database
app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///sqlitedb.file"
app.config["SQLALECHMY_TRACK_MODIFICATIONS"] = 0


# configure sqlite3 enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreigb_keys=ON;")
        cursor.close()

db = SQLAlchemy(app)
now = datetime.now()


#models
class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost")