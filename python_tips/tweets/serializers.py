from rest_framework import serializers
from .models import Tweets

class CreateTweeetSerializers(serializers.ModelSerializer):
    """
    THESE ARE PARAMETERS GOTTEN FROM TWEETS MODELS TO HELP IN THE VALIDATION AND SAVING
    OF TWEETS TO DATABASE
    """
    class Meta:
        model = Tweets
        Fields = "__all__"

    def create(self):
        serializer


class TweetsSerializers(serializers.ModelSerializer):
    """
    DISPLAYS TWEETS USING TWEETS MODELS 

    ARGS:
            ALL PAARAMETERS ADD IN THE FIELDS SECTION
            ARE DISPLAYED ON THE API
    """
    class Meta:
        model = Tweets
        fields = "__all__"


class SearchSerailizers(serializers.Serializer):
    """
    TAKES IN USER QUERY ARGUMENTS AND SUPPLYS IT TO THE
    VIEW FUNCTION FOR COMPREHENSIVE DATABASE SEARCH FOR SIMILARITIES 
    """

    query = serializers.CharField(required= True, max_length = 200)

class TwitterAuthSerializer(serializers.Serializer):
    """Handles serialization of twitter related data"""
    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()

class ReTweetSerializer(serializers.Serializer):
    """
    A FORM FIELD THAT TAKES IN THE ID OF THE TWEET 
    POST AND AND THE DEFAULT ACTION WHICH IS RETWEET
    """
    tweets_id = serializers.IntegerField(required = True)
