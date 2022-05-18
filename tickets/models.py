from ast import Str
from turtle import mode, title
from django.db import models
from django.forms import DateField



# to start wirking with signals  
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings 

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)

# start editing permissions  
from django.contrib.auth.models import User
class Post(models.Model):
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    title =models.CharField(max_length=50)
    body = models.TextField()

class Movie(models.Model):
    hall = models.CharField(max_length=10,)
    movie = models.CharField(max_length=10)
    date = models.DateField(max_length=10)
    

    def __str__(self) -> str:
        return self.movie
 
class Guest(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.name

class Reservation(models.Model):
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE,related_name='reservation')
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='reservation')


    def __str__(self) -> str:
        return str(self.guest) + ' '+str(self.movie)



