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