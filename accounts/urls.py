from django.urls import path
from . import views
from drawa import views as a_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('quit/', views.quit, name='quit'),
    path('<str:username>/profile/', views.profile, name='profile'),
    path('<str:username>/update/', views.update, name='update'),
    # path('<str:username>/password/', views.change_password, name='change_password'),
    path('calander/', views.calander, name = 'calander'),
    path('interest/', views.interest, name = 'interest'),
]
 