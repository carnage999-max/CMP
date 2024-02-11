from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.loginUser, name="signin"),
    path('signup', views.registerUser, name="signup"),
]

