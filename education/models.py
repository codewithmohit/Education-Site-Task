from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone=models.CharField(max_length=10,default="")
    gender=models.CharField(max_length=10,default="")
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.user.username

class Ncert(models.Model):
    video=models.CharField(max_length=200,default="")
    def __str__(self):
        return self.video



    
