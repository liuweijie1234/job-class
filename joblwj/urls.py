# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.tasks),
    url(r'^dev-guide/$', views.record)
)
