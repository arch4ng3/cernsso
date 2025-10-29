from flask import Flask, redirect, session, url_for, render_template
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
import requests
import json
import os

# Based on the official Authlib example for Google:
# https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py

app = Flask(__name__)

load_dotenv()

CONF_URL = 'https://auth.cern.ch/auth/realms/cern/.well-known/openid-configuration'
LOGOUT_URL = 'https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/logout'
API_ACCESS_URL = "https://auth.cern.ch/auth/realms/cern/api-access/token"

oauth = OAuth()
oauth.register(
    'sso',
    client_id=os.environ["SSO_CLIENT_ID"],
    client_secret=os.environ["SSO_CLIENT_SECRET"],
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid'}
)
oauth.init_app(app)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/hidden')
def hidden():
    user = session.get('user')
    return render_template('hidden.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.sso.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.sso.authorize_access_token()
    user = oauth.sso.parse_id_token(token)
    # Use the user object for authorization (e.g. check user roles)
    session['user'] = user

    # TODO check for a role, redirect to a different page
    # if 'XXX' in user['XXX']:
    #  return redirect(url_for('hidden'))

    return redirect(url_for('homepage'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("{}?redirect_uri={}".format(
        LOGOUT_URL,
        url_for('homepage', _external=True))
    )


@app.route('/apitest')
def apitest():
    # TODO Use client credentials on an API endpoint
    client_id = os.environ["SSO_CLIENT_ID"],
    client_secret = os.environ["SSO_CLIENT_SECRET"]
    audience = "auth-test-api"
    api_endpoint = "https://auth-test-api.web.cern.ch"
    grant_type = "XXXX"

    # Form the API Token request
    api_token_request = requests.post(
        API_ACCESS_URL,
        data={
            # TODO Fill in the post body based on the docs in the README
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    # Have a look in the logs to see what is returned
    print(api_token_request.json())
    # Select the correct part of the response to use to call the API
    token = api_token_request.json()['XXXXX']

    # Call the downstream API
    api_response = requests.get(
        "{0}/ProtectedMessage/".format(api_endpoint),
        headers={"Authorization": "Bearer {}".format(token)}
    )
    print(api_response.json())
    # In real life we would want to do something interesting with the response
    return redirect(url_for('homepage'))


app.secret_key = os.urandom(24)
app.run(port=5000)

if __name__ == "__main__":
    # no need to re-import os here; it's already imported at top
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
