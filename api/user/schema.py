import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from flask_graphql_auth import (create_access_token,
                                create_refresh_token)
from flask_bcrypt import check_password_hash

from api.user.models import User as UserModel
from utils.validators import verify_email, validate_empty_fields


class User(SQLAlchemyObjectType):
    """
        Autogenerated return type of a user
    """
    class Meta:
        model = UserModel
        exclude_fields = ('password_hash',)


class CreateUser(graphene.Mutation):
    """Mutation that creates a user."""

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password_hash = graphene.String(required=True)
    access_token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(User)

    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        user = UserModel(**kwargs)
        query = User.get_query(info)
        exact_email = query.filter(UserModel.email == user.email).first()
        exact_name = query.filter(UserModel.name == user.name).first()
        if exact_email:
            raise GraphQLError('This email already exists')

        if exact_name:
            raise GraphQLError('This username already exists')

        if not verify_email(user.email):
            raise GraphQLError('Invalid email format')
        user.save()

        return CreateUser(user=user, access_token=create_access_token(
                          kwargs['email']),
                          refresh_token=create_refresh_token(kwargs['email']))


class LoginUser(graphene.Mutation):

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        query = User.get_query(info)
        email = kwargs.get('email')
        password = kwargs.get('password')
        exact_user = query.filter(UserModel.email == email).first()
        if not verify_email(email):
            raise GraphQLError('Invalid email format')
        if not exact_user:
            raise GraphQLError('This email does not exist')
        if not check_password_hash(exact_user.password_hash, password):
            raise GraphQLError('Please check your login credentials')

        return LoginUser(access_token=create_access_token(
                        kwargs['email']),
                          refresh_token=create_refresh_token(kwargs['email']))


class Mutation(graphene.ObjectType):
    """
    Mutation to register a user
    """
    create_user = CreateUser.Field(
        description="Creates a new user with the arguments\
            \n- email: The email field of the user[required]\
            \n- name: The name field of a user[required]\
            \n- password_hash: The password field of a user[required]")

    login_user = LoginUser.Field(
        description="Logs in a user with the arguments\
            \n- email: The email field of the user[required]\
            \n- password: The password field of a user[required]")


class Query(graphene.ObjectType):
    """
        Query to get list of all users
    """
    all_users = graphene.List(
        User,
        description="Query that returns a list of all users")

    def resolve_all_users(self, info):
        query = User.get_query(info)
        users = query.filter(UserModel.state == 'active').all()
        return users
