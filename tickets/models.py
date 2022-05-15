from ast import Str
from django.db import models
from django.forms import DateField

# Create your models here.


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