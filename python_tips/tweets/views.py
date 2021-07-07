from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsOwner
from django.conf import settings
from django.db.models import Q

from . models import *
import tweepy
import twitter
import os


# Create your views here.

class GetAllTweets(generics.ListAPIView):
    """
    GETS ALL PYTHON TIPS SAVE TO DATABASE IN ORDER OF POPULARITY

    ARGS:
            ORDERED BY AMMOUNTS OF LIKES
    """

    serializer_class= TweetsSerializers
    lookup = 'slug'
    permission_classes = []

    def get_queryset(self):
        slug =  self.request.GET.get("slug")
        qs = Tweets.objects.all()
        
        if slug is not None:
            or_lookup = (
                Q(tips__icontains=slug) |
                Q(tags_icontains=slug))
            qs = qs.filter(or_lookup).distinct().order_by('likes')
            return qs
        return qs.order_by('likes')


def authentication(access_token_key, access_token_secret):
    """
    validate_twitter_auth_tokens methods and helps tweepy access user's account
    """

    consumer_api_key = os.environ.get('TWITTER_API_KEY')
    consumer_api_secret_key = os.environ.get('TWITTER_CONSUMER_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_tweets():
    api = authentication(access_token_key, access_token_secret)
    userID= 'python_tip'

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
        return all_tweets




class CreateTweets(generics.CreateAPIView):
    """
    GETS TWEETS FROM API AND SAVE TO DATABASE

    ARGS: 
            USER MUST BE AUTHENTICATED 

    PARAMETERS:
                ALL FORM MODELS 
    """

    serializer_class = CreateTweetSerializer

    def create(self):
        tweets = get_tweets()
        for tweet in tweets:
            serializer = Tweets.objects.create(
                who_posted = tweet.username
                tips = tweet.full_text
                timestamp = tweet.created_at
                link = tweet.link
                likes = tweet.favorite_counts
                retweet = tweet.retweet_counts
            )
            serializer.save()


class SearchTweetView(viewss.ListAPIView):
    """
    TAKES IN QUERY AND MAKES A COMPREHENSIVE
    SEARCH THROUGH TWEETS STORED IN DATABASE.

    ARGS: 
            QUERY OF USER

    RESPONSES:
                GOES THROUGH THE TWEETS OBJECTS 
                AND SEARCHES FOR SIMILARITEIS TO QUERY
    """

    serializer_class = SearchSerializer

    def get_queryset(self):
        serializer