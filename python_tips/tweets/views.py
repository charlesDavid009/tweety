from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics, views
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from django.conf import settings
from django.db.models import Q

from . models import *
from . serializers import *
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


"""
class SearchTweetView(views.ListAPIView):

    #TAKES IN QUERY AND MAKES A COMPREHENSIVE
    #SEARCH THROUGH TWEETS STORED IN DATABASE.

    #ARGS: 
    #        QUERY OF USER

    #RESPONSES:
                #GOES THROUGH THE TWEETS OBJECTS 
                #AND SEARCHES FOR SIMILARITEIS TO QUERY
    

    serializer_class = SearchSerializer

    def get_queryset(self):
        serializer
"""
class RetweetTweepyView(generics.CreateAPIView):
    """
    GETS THE TWEET ID OF THE OBJECTS AND RETWEETS THAT TWEETS THROUGH 
    AUTHENTICATED USER ACCOUNT USING THE TWEEPY RETWEET FUNCTIONALITY

    ARGS:
            TWEET'S ID 
            USER ID
    """
    serializer_class = RetweetSerializer

    def post(self):
        tweet_id = self.request.get('tweets_id')

        consumer_api_key = os.environ.get('TWITTER_API_KEY')
        consumer_api_secret_key = os.environ.get('TWITTER_CONSUMER_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        status = api.retweet(tweet_id)
        if status == '200' or status == "201":
            return Response({'Tweets has been successfully been tweeted'}, status = status.HTTP_200_OK)
        return status.error

