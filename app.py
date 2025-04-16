from requests_oauthlib import OAuth1Session
import webbrowser
from _datetime import datetime
import sys


TWEET_ID = 1904253134794596363
API_KEY = "my api key"
API_SECRET = "my api secret"


def get_request_token():
    """Obtains request token using PIN-based OAuth flow."""

    oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, callback_uri="oob")

    try:
        response = oauth.fetch_request_token("https://api.x.com/oauth/request_token")
        token = response.get("oauth_token")
        secret = response.get("oauth_token_secret")

        if token and secret:
            print("Request token obtained successfully!\n")
            return token, secret
        else:
            print("Failed to get request token: ", response)
            sys.exit(1)

    except Exception as e:
        print("Exception while fetching request token: ", e)
        sys.exit(1)


def authorize_user(request_token):
    """Uses request token to redirect user to complete authorization. Returns the authorization PIN."""

    webbrowser.open(f"https://api.x.com/oauth/authorize?oauth_token={request_token}")
    verifier = input("Enter the PIN: ")
    return verifier


def get_access_token(request_token, request_secret, verifier):
    """Uses request token and authorization PIN to obtain user's access token."""

    oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, resource_owner_key=request_token,
                          resource_owner_secret=request_secret, verifier=verifier)
    try:
        response = oauth.fetch_access_token("https://api.x.com/oauth/access_token")
        token = response.get("oauth_token")
        secret = response.get("oauth_token_secret")
        user_id = response.get("user_id")
        if token and secret and user_id:
            print("\nAccess token obtained successfully!\n")
            return token, secret, user_id

    except Exception as e:
        print("\nException while fetching access token:", e)
        sys.exit(1)


def like_tweet(access_token, access_secret, user_id):

    oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, resource_owner_key=access_token,
                          resource_owner_secret=access_secret, signature_type="auth_header")

    api_url = f"https://api.twitter.com/2/users/{user_id}/likes"
    headers = {"Content-Type": "application/json"}
    body = {"tweet_id": str(TWEET_ID)}

    try:
        response = oauth.post(api_url, json=body, headers=headers)

        if response.status_code == 200:
            print("Tweet liked successfully!")

        elif response.status_code == 429:
            print("Error 429: You've exceeded the limit of requests. Try again later")

            # Find the most restrictive rate limit to calculate limit reset date
            rate_ts = response.headers.get("x-rate-limit-reset")
            user_ts = response.headers.get("x-user-limit-24hour-reset")

            if rate_ts > user_ts:
                reset = rate_ts
            else:
                reset = user_ts

            # Change unix timestamps to datetime
            reset_date = datetime.fromtimestamp(float(reset)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\nRate limit resets at: {reset_date}")
        else:
            print(f"Request failed with status: {response.status_code}")

    except Exception as e:
        print(e)


# Obtain access token with 3-legged OAuth 1.0a flow

# 1.Obtain request token
request_token, request_secret = get_request_token()

# 2.Authorize the user
auth_pin = authorize_user(request_token)
if not auth_pin:
    sys.exit(1)

# 3.Obtain access token
access_token, access_secret, user_id = get_access_token(request_token, request_secret, auth_pin)

# make a POST request to like a tweet
like_tweet(access_token, access_secret, user_id)
