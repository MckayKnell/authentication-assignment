from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from lib.authenticate import auth, auth_admin
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object


@auth_admin
def add_user(req):
    post_data = request.form if request.form else request.json

    new_user = Users.get_new_user()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    try:
        db.session.add(new_user)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create user'}), 400

    return jsonify({'message': 'user created', 'results': user_schema.dump(new_user)}), 201


@auth
def user_get_all(req):
    query = db.session.query(Users).all()

    return jsonify({'message': 'users found', 'results': users_schema.dump(query)}), 200


@auth_admin
def user_update(req, user_id):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    post_data = req.form if req.form else req.get_json()

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'user updated', 'result': user_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400


@auth_admin
def user_delete_by_id(req, user_id):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({'message': ' user does not found'}), 404
    try:
        db.session.delete(user_query)
        db.session.commit()
        return ({'message': 'user removed'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return ({'message': 'unable to delete user'}), 400
