from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import Guest,Movie,Reservation

class MovieSerializer(serializers.ModelSerializer):
    class Meta :
        model = Movie
        fields = '__all__'

class ResevationSerializer(serializers.ModelSerializer):
    class Meta:
        model =Reservation
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta :
        model =Guest 
        fields = ['pk','reservation','name','mobile']