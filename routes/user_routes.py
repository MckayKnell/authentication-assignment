from flask import Blueprint, request

import controllers

users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def add_user():
    return controllers.add_user(request)


@users.route('/users', methods=['GET'])
def user_get_all():
    return controllers.user_get_all(request)


@users.route('/user/<user_id>', methods=['PUT'])
def user_update(user_id):
    return controllers.user_update(request, user_id)


@users.route('/user/delete/<user_id>', methods=['DELETE'])
def user_delete_by_id(user_id):
    return controllers.user_delete_by_id(request, user_id)
