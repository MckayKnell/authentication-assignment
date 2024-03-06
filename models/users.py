
import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)

    auth = db.relationship('AuthTokens', back_populates='user', cascade='all,delete')

    def __init__(self, first_name, last_name, role, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.email = email
        self.password = password

    def get_new_user():
        return Users('', '', '', '', '')


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'email', 'first_name', 'last_name', 'role']


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
