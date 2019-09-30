"""dig_chouti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index.html$', views.index),
    url(r'^authuser.html$', views.auth_user),
    url(r'^authlogin.html$', views.authlogin),
    url(r'^register.html$', views.register),
    url(r'^timeauth.html$', views.time_auth),
    url(r'^loginuot.html$', views.loginuot),
    url(r'^senddata.html$', views.article),
    url(r'^getarticle-(\d+).html$', views.getarticle),
    url(r'^get_link.html$', views.get_link),
    url(r'^upload_img.html$', views.upload_img),
    url(r'^vip.html$', views.vip),
    url(r'^viphome-(\d+).html$', views.viphome),
    url(r'^delviphome-(\d+)-(\d+).html$', views.delviphome),
    url(r'^ediviphome-(\d+)-(\d+).html$', views.ediviphome),
    url(r'^admin_profile.html$', views.admin_profile),
    url(r'^personal-(\d+).html$', views.personal),
    url(r'^auth_pwd.html$', views.auth_pwd),
    url(r'^favor.html$', views.favor),
    url(r'^comment.html$', views.comment),
]
