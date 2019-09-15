from flask import Flask, redirect, request, url_for

from flask_graphql import GraphQLView
from flask_cors import CORS
from flask_json import FlaskJSON
from flask_graphql_auth import GraphQLAuth
from oauthlib.oauth2 import WebApplicationClient
import requests
import json

from config import config
from schema import schema
from helpers.database import db_session
from api.user.models import User

config_name ="development"
# def create_app(config_name):
app = Flask(__name__)
CORS(app)
FlaskJSON(app)
GraphQLAuth(app)
app.config.from_object(config[config_name])
config[config_name].init_app(app)
# OAuth 2 client setup
# import pdb; pdb.set_trace()

client = WebApplicationClient(config[config_name].GOOGLE_CLIENT_ID)
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

@app.route("/")
def index():
    return '<a class="button" href="/login">Google Login</a>'

def get_google_provider_cfg():
    return requests.get(config[config_name].GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():

    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
# Find out what URL to hit to get tokens that allow you to ask for
# things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(
            config[config_name].GOOGLE_CLIENT_ID,
            config[config_name].GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    import pdb; pdb.set_trace()

    user = User(
        name=users_name, email=users_email
    )
    print(user)


    # return app
if __name__ == '__main__':
    app.run(ssl_context="adhoc")
