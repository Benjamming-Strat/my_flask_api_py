'''
This is Code from a Class on FreeCodeCamp called Datastructures for Pythondevelopers (w/ Flask)
 It is my first API. I have typed it on my own from the youtube video to understand the functionality.
'''


from tkinter import CASCADE
from typing import Hashable
from flask import Flask, request, jsonify, session
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy
import linked_list
import hastable
import random
import binarysearchtree
import custom_queue
import stack




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
    posts = db.relationship("BlogPost", cascade="all, delete") #if we delete a user by id it automatically deletes the row in table BlogPost because user.id has a constraint as foreign key

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
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@app.route("/user/<user_id>", methods=["POST"])
def create_all_blog_posts(user_id):
    data = request.get_json()
    user = User.query.filter_by(user_id)
    if not user:
        return jsonify({"Message": "User does not Exist"}), 400
    
    ht = hastable.Hashtable(10)
    ht.add_key_value("title" , data["title"])
    ht.add_key_value("body" , data["body"])
    ht.add_key_value("date" , now)
    ht.add_key_value("user_id" , user_id)

    new_blogpost = BlogPost(
        title = ht.get_value("title"),
        body = ht.get_value("body"),
        date = ht.get_value("date"),
        user_id = ht.get_value("user_id")
    )
    db.session.add(new_blogpost)
    db.session.commit()
    return jsonify({"Message": "New Blogpost created"}), 200

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_posts(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)
    bst = binarysearchtree.BinarySearchTree()
    for post in blog_posts:
        bst.insert(
            {
                "id":post.id,
                "title":post.title,
                "body":post.body,
                "user":post.user_id
            }
        )
    post = bst.search(blog_post_id)
    if not post:
        return jsonify({"message": "post not found"}), 400
    return jsonify(post)


@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()
    q = custom_queue.Queue()
    for post in blog_posts:
        q.enqueue(post)

    
    return_list = []
    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char) #ascii equivalent

        post.data.body = numeric_body
        return_list.append({"id" : post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_id": post.data.user_id})

    return jsonify(return_list), 200


@app.route("/blog_post/delete_last_10", methods=["DELETE"])
def delete_last_10():
    blog_posts = BlogPost.query.all()
    s = stack.Stack()
    for post in blog_posts:
        s.push(post)
    for _ in range(10):
        post_to_delete = s.pop()
        db.session.delete(post_to_delete.data) #pop returns a node, access data
        db.session.commit()
    return jsonify({"Message": "Success"})


if __name__ == "__main__":
    app.run(debug=True)
