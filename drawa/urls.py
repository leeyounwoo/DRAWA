from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:shoes_pk>/', views.shoes_detail, name='shoes_detail'),
    path('place/', views.place, name='place'),
    path('<int:shoes_pk>/reservation/', views.shoes_reservation, name='shoes_reservation'),
    path('<int:shoes_pk>/interesting/', views.interesting, name = 'interesting'),
]
