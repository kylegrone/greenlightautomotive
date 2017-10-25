from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Upload(models.Model):
    pic = models.ImageField("Image", upload_to="images/")    
    upload_date=models.DateTimeField(auto_now_add =True)
    
class Channels(models.Model):
    channel = models.CharField(max_length="2000")
    advisor = models.ForeignKey(User)
    guest_user = models.CharField(max_length="2000")
    chat_dt = models.DateTimeField(auto_now_add=True)