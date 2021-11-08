from django.urls import path
from . import views

app_name = 'drawa'

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('<int:shoes_pk>/', views.detail, name='detail'),
    # path('place/', views.place, name='place'),
    # path('<int:shoes_pk>/reservation/', views.shoes_reservation, name='shoes_reservation'),
    # path('<int:shoes_pk>/interesting/', views.interesting, name = 'interesting'),
]
