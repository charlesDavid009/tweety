from ___future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def login():
    consumer_api_key = os.environ.get('TWITTER_API_KEY')
    consumer_api_secret_key = os.environ.get('TWITTER_CONSUMER_SECRET')
    access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
