from flask import Flask, request, jsonify
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy
import linked_list





# app
app = Flask(__name__)

#configuration to use local file as a database
#config acts liek a dictioanry so we need to add keys to connect to our database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALECHMY_TRACK_MODIFICATIONS"] = False


# configure sqlite3 enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

db = SQLAlchemy(app)
now = datetime.now()

#models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost")

class BlogPost(db.Model):
    __tablename__ = "BlogPost"
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

#db.create_all()
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"], 
        address = data["address"], 
        phone = data["phone"], 
         )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():

    #query gives us the the use in ascending order
    users = User.query.all()
    all_users_ll = linked_list.Linked_list()
    #use insert_at_beginning to add the users from query with ascending order, so the last user will be the head of the  list
    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
                
            }
        )
    return jsonify(all_users_ll.to_list())

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    #query gives us the the use in ascending order
    users = User.query.all()
    all_users_ll = linked_list.Linked_list()
    for user in users:
        
            all_users_ll.insert_at_end({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
                
            })
        
    return jsonify(all_users_ll.to_list())

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all() #descending höchste ID ganz oben
    all_users_ll = linked_list.Linked_list()
    # node[data.id]-->node[data.id]-->node
    for user in users:
        all_users_ll.insert_beginning(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,    
        })
    user = all_users_ll.get_user_by_id(user_id)
    return jsonify(user), 200
        
    

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)
