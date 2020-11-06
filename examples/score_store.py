import os
import random
import hashlib
import operator 
from functools import reduce

from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

from utils import pprint


load_dotenv()

# init env variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
AUTHORIZATION_ENDPOINT = os.environ.get('AUTHORIZATION_ENDPOINT')
TOKEN_ENDPOINT = os.environ.get('TOKEN_ENDPOINT')

MY_ACTIVITY_URI = 'http://example.com/'

USER_ENDPOINT = 'https://reg.nti-contest.ru/api/user_info'
USER_TEAMS_ENDPOINT = 'https://reg.nti-contest.ru/api/user_team_info'
LIST_ACTIVITY_ENDPOINT = 'https://reg.nti-contest.ru/api/activity'
USER_ACTIVITY_ENDPOINT = 'https://reg.nti-contest.ru/api/user_external_activity'
TEAM_ACTIVITY_ENDPOINT = 'https://reg.nti-contest.ru/api/team_external_activity'

def _store_score(endpoint, payload):
    """
    Helper with logic of update for store score result for eny object
    """

    ext_activity = client.post(endpoint, json=payload)


    # if progress by current object and activity is exist, then - update
    if ext_activity.status_code == 542:
        pprint(ext_activity.json())

        ext_activity = list(
            filter(
                lambda a: a['activity']['id'] is payload['activity_id'],
                client.get(endpoint).json()
            )
        )
        if not ext_activity:
            raise Exception(
                f"ExternalActivity for current object and activity {payload['activity_id']} not found"
            )

        ext_activity = client.put(
            f"{endpoint}/{ext_activity.pop(0)['id']}",
            json=payload
        )
    return ext_activity

def store_user_score(user_id, activity_id, score=None):
    """
    Store user score
    """
    if not score:
        return None

    return _store_score(USER_ACTIVITY_ENDPOINT, payload={
            'user_id': user_id,
            'activity_id': activity_id,
            'code': hashlib.md5(
                f"{user_id}{activity_id}onti_external_activity".encode()
            ).hexdigest(),
            'score': score
        }
    )

def store_team_score(team_id, activity_id, score):
    """
    Store team score
    """
    if not score:
        return None

    return _store_score(TEAM_ACTIVITY_ENDPOINT, payload={
            'team_id': team_id,
            'activity_id': activity_id,
            'code': hashlib.md5(
                f"{team_id}{activity_id}onti_external_activity".encode()
            ).hexdigest(),
            'score': score
        }
    )

#####################
# Authorize section
#####################

# Step 1: get authrization url
client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, token_endpoint_auth_method='client_secret_post')
uri, state = client.create_authorization_url(AUTHORIZATION_ENDPOINT, redirect_uri=REDIRECT_URI)

# request redirect url from user
authorization_response = input(
    f'Go to "{uri}", approve app and enter authorization respones: '
)

# Step 2: change code to access/refresh_token
token = client.fetch_token(
    TOKEN_ENDPOINT, 
    authorization_response=authorization_response, 
    redirect_uri=REDIRECT_URI
)
print('Your token:')
pprint(token)


# Step 3: create api request
client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, token=token)


#####################
# Store score section
#####################

# get user info
user = client.get(USER_ENDPOINT).json()

# get teams
teams = client.get(USER_TEAMS_ENDPOINT).json()

# filter by accepted flag
teams = list(
            filter(
                lambda ut: ut['user_accept'] is 'accepted' and ut['owner_accept'] is 'accepted',
                [o[1] for o in teams['memberships'].items()]
            )
        ) + [o[1] for o in teams['teams'].items()]
print('User teams:')
pprint(teams)

# find my platform activity from user activities:
# - get all activity by every user profile
# - combine to flat list
# - filter by my platform url
try:
    own_activity = list(
        filter(
            lambda a: MY_ACTIVITY_URI in a['external_url'],
            reduce(
                lambda p_e, e: reduce(operator.add, zip(p_e, e)),
                [
                    client.get(
                        f"{LIST_ACTIVITY_ENDPOINT}?profile_id={profile['id']}&all=true"
                    ).json() for profile in user['profiles']
                ]
            )
        )
    ).pop(0)
except IndexError:
    raise Exception('Activity with need uri not found')

# save user progress by activity
user_activity = store_user_score(user['id'], own_activity['id'], score=99)
print('User activity progress:')
pprint(user_activity.json())



# get random team for save score
team = teams[random.randint(0, len(teams)-1)]
if not team:
    raise Exception('Teams for user not found')

# save team progress by activity
team_activity = store_team_score(team['id'], own_activity['id'], score=88)
print('Team activity progress:')
pprint(team_activity.json())