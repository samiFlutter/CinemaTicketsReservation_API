
from django.contrib import admin
from django.db import router
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewssets_movie)
router.register('reservations',views.viewssets_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    # 1
    path('django/jsonresponsenomodel/',views.no_rest_no_model),
    # 2
    path('django/jsonresponsefrommodel/',views.no_rest_from_model),
    # 3
    path('rest/fbvlist/',views.FBV_List),
    # 3.1
    path('rest/fbvpk/<int:pk>',views.FBV_pk),
    # 4
    path('rest/cbv',views.CBV_List.as_view()),
    # 4.1
    path('rest/cbv/<int:pk>',views.CBV_pk.as_view()),

     # 5
    path('rest/mixins',views.mixins_list.as_view()),
    # 5.1
    path('rest/mixins/<int:pk>',views.mixins_list.as_view()),
     # 6
    path('rest/generics',views.generics_list.as_view()),
    # 6.1
    path('rest/generics/<int:pk>',views.generics_pk.as_view()),
    
    # 7
    path('rest/viewsets/',include(router.urls)),
    # 8 find movie  
    path('fbv/findmovie',views.find_movie),
    # 9 new reservation 
    path('fbv/newreservation',views.new_reservation),
]
