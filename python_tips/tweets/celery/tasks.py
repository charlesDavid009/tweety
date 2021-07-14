from ___future__ import absolute_import, unicode_literals
from celery import shared_task


access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

@shared_task
def login():
    consumer_api_key = os.environ.get('TWITTER_API_KEY')
    consumer_api_secret_key = os.environ.get('TWITTER_CONSUMER_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

@shared_task
def get_tweets():
    api = authentication(access_token_key, access_token_secret)
    userID = 'python_tip'

    tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )

    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)

    for tweet in tweets:
        serializer = Tweets.objects.create(
            who_posted = tweet.username,
            tips = tweet.full_text,
            timestamp = tweet.created_at,
            link = tweet.link,
            likes = tweet.favorite_counts,
            retweet = tweet.retweet_counts,
            tweet_id = tweet.id
        )
        serializer.save()