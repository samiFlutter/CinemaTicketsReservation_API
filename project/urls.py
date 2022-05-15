
from django.contrib import admin
from django.urls import path
from tickets import views
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
]
