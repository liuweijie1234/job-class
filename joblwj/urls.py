# -*- coding: utf-8 -*-

from django.conf.urls import url

from joblwj import views

urlpatterns = (
    url(r'^$', views.tasks),
    url(r'^tasks/$', views.tasks),
    url(r'^record/$', views.record)
)
