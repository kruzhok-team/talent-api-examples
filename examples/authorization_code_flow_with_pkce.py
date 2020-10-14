import os
from datetime import datetime

from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

from utils import pprint


load_dotenv()

# init env variables
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')
authorization_endpoint = os.environ.get('AUTHORIZATION_ENDPOINT')
token_endpoint = os.environ.get('TOKEN_ENDPOINT')

# code verfier for pkce flow, for more details:
# https://docs.authlib.org/en/latest/specs/rfc7636.html#using-code-challenge-in-client
pkce_params = {
    'code_verifer': 'iZzU6K55tpTgcobCxB4he2TeE6xGFXFYCEsSv8WQ8SyXjKBu',
    'code_challenge': 'ntS_qw7UCqoA9MPY8tO3PrAO1AkpIVYwOmlx-q0Iuec',
    'code_challenge_method': 'S256'
}

# Step 1: get authrization url
client = OAuth2Session(
    client_id,
    token_endpoint_auth_method=None,
    scope='openid',
)
uri, state = client.create_authorization_url(
    authorization_endpoint,
    redirect_uri=redirect_uri,
    code_challenge=pkce_params['code_challenge'],
    code_challenge_method=pkce_params['code_challenge_method'],
    nonce=datetime.now().timestamp()
)

# request redirect url from user
authorization_response = input(
    f'Go to "{uri}", approve app and enter authorization respones: '
)

# Step 2: change code to access/refresh_token
token = client.fetch_token(
    token_endpoint,
    client_secret=None,
    redirect_uri=redirect_uri,
    authorization_response=authorization_response,
    code_verifier=pkce_params['code_verifer'],
)
print('Your token:')
pprint(token)

# Step 3: create api request
client = OAuth2Session(client_id, client_secret, token=token)
resp = client.get('https://talent.kruzhok.org/api/user/')
print('User profile data:')
pprint(resp.json())