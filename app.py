from flask import Flask

from flask_graphql import GraphQLView
from flask_cors import CORS
from flask_json import FlaskJSON
from flask_graphql_auth import GraphQLAuth

from config import config
from schema import schema
from helpers.database import db_session


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    FlaskJSON(app)
    GraphQLAuth(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.add_url_rule(
        '/hairq',
        view_func=GraphQLView.as_view(
            'hairq',
            schema=schema,
            graphiql=True
        )
    )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
