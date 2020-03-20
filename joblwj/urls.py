# -*- coding: utf-8 -*-
from django.conf.urls import url
from joblwj import views


urlpatterns = (
    url(r'^$', views.tasks),
    url(r'^tasks/$', views.tasks),
    url(r'^record/$', views.record),
    url(r'^host/update$', views.get_host),
    url(r'^execute/$', views.execute_script)
)
