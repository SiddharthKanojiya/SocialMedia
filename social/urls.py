"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from chatApp.views import chating,group_chat,createGroup
from videoApp.views import lobby,room,getToken

urlpatterns = [
    path('', include("dwitter.urls")),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    #Chat
    path('chating/',chating,name='chating'),
    path('group/',group_chat,name='group_chat'),
    #~~~~~~
    path('lobby',lobby,name="lobby"),
    path('room/',room,name="room"),
    path('getToken/',getToken,name="get_token"),
    path('creategroup/',createGroup,name="createGroup")
    
]
