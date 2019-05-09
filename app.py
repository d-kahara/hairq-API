from flask import Flask

from flask_graphql import GraphGLView
from flask_cors import CORS
from flask_json import FlaskJSon

from config import config
from schema import schema


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    FlaskJSon(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.add_url_rule(
        'hairq',
        view_func=GraphGLView.as_view(
            'hairq',
            schema=schema,
            graphiql=True
        )
    )

    return app
