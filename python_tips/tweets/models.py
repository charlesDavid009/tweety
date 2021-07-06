from django.db import models

# Create your models here.

class Tweets(models.Model):
    "craeting model to save tweets gotten from the apis to the database"
    who_posted = models.CharField(blank= False, null= False, max_length = 200)
    tips = models.TextField(blank=False, null= False)
    save_to_database = models.DateTimeField(auto_now_add= True)
    timestamp = models.CharField(blank = False, null= False, max_length = 200)
    link = models.UrlField(blank = True, null= True)
    likes = models.IntegerField(blank=True, null=True)
    retweets = models.IntegerField(blank=True, null=True)
    

