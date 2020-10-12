import os

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

# Step 1: get authrization url
client = OAuth2Session(client_id, client_secret, token_endpoint_auth_method='client_secret_post')
uri, state = client.create_authorization_url(authorization_endpoint, redirect_uri=redirect_uri)

# request redirect url from user
authorization_response = input(
    f'Go to "{uri}", approve app and enter authorization respones: '
)

# Step 2: change code to access/refresh_token
token = client.fetch_token(
    token_endpoint, 
    authorization_response=authorization_response, 
    redirect_uri=redirect_uri
)
print('Your token:')
pprint(token)

# Step 3: create api request
client = OAuth2Session(client_id, client_secret, token=token)
resp = client.get('https://talent.kruzhok.org/api/user/')
print('User profile data:')
pprint(resp.json())