from django.urls import path, include
from .views import *

urlpatterns = [
    path('tweets/', GetAllTweets.as_view()),
    path('retweet/', RetweetTweepyView.as_view()),
    path('search', SearchSerailizers.as_view()),
]