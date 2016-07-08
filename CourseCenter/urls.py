"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.staticfiles.views import serve

from Center import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^download$', views.download),
    url(r'^upload$', views.upload),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^view/course$', views.view_course),
    url(r'^view/course_source$', views.view_course_source),
    url(r'^add/task$', views.add_task),

    url(r'^(?P<path>.*\.[\w]*)$', serve),
]
