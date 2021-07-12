from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView, TwitterSocialAuthView

urlpatterns = [
    path('twitter/', TwitterSocialAuthView.as_view()),


]
