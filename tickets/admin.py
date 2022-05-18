from django.contrib import admin
from .models import Guest,Movie, Post,Reservation
# Register your models here.

admin.site.register(Movie)
admin.site.register(Guest)
admin.site.register(Reservation)
# working on post author permissions  
admin.site.register(Post)
