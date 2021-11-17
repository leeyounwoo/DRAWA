from django.urls import path
from . import views

app_name = 'drawa'

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('<int:shoes_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/wish/', views.wish, name='wish'),
    path('<int:draw_pk>/reserve/', views.reserve, name='reserve'),
    path('<int:draw_pk>/participate/', views.participate, name='participate'),
    path('info/', views.info, name='info'),
    path('<int:draw_pk>/mail/', views.mail, name='mail'),
    # path('place/', views.place, name='place'),
    path('<int:shoes_pk>/reservation/', views.shoes_reservation, name='shoes_reservation'),
    path('<int:shoes_pk>/interesting/', views.interesting, name = 'interesting'),
]
