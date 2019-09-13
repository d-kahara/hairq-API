from sqlalchemy import (Column, String, Integer, Enum)
from flask_bcrypt import generate_password_hash

from helpers.database import Base
from utils.utility import StateType, ModelOperations


class User(Base, ModelOperations):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    state = Column(Enum(StateType), default='active')
    password_hash = Column(String, nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs['email']
        self.name = kwargs['name']
        self.password_hash = generate_password_hash(
            kwargs['password_hash']).decode('utf-8')

    def __repr__(self):
        return '<User {}>'.format(self.name)
