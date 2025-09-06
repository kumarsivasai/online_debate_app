"""
URL configuration for projectfolder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import hello,kumar
from django.urls import path, include
from .views import register_view,login_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello, name='hello'),
    path('kumar/',kumar,name='kumar'),
    path('', include('demoapp.urls')),
      # Include URLs from demoapp
    
    #---------------------------------------------login system urls------------------------------------------------
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]







# this is for static and media files
if settings.DEBUG:
    
    urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)