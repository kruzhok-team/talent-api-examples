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

# Step 1: get token by client_id/client_secret
client = OAuth2Session(client_id, client_secret, token_endpoint_auth_method='client_secret_post')

token = client.fetch_token(token_endpoint, grant_type='client_credentials')
print('Your token:')
pprint(token)

# Step 2: create api request
client = OAuth2Session(client_id, client_secret, token=token)
resp = client.get('https://talent.kruzhok.org/api/user/')
print('User profile data:')
pprint(resp.json())