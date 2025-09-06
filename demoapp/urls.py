# demoapp/urls.py
from django.urls import path
from demoapp import views

urlpatterns = [
    path('register/', views.register_view, name='register_view'),  # name must match
    path('login/', views.login_view, name='login_view'),
     path("logout/", views.logout_view, name="logout"),  
    
     path("home/", views.home_view, name="home"),  
    path("api/register/", views.api_register, name="api_register"),
    path("api/login/", views.api_login, name="api_login"),
]
