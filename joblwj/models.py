# -*- coding: utf-8 -*-
from django.db import models


class SelectScript(models.Model):
    scriptname = models.CharField(max_length=50)
    scriptcontent = models.CharField(max_length=50)

    def __str__(self):
        return self.scriptname

class Doinfo(models.Model):
    businessname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    scriptname = models.ForeignKey(SelectScript, models.CASCADE)
    scriptcontent = models.CharField(max_length=50)
    operatingtime = models.DateTimeField(auto_now_add=True)
    ipcount = models.IntegerField()
    details = models.CharField(max_length=200)
    Celeryid = models.IntegerField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.businessname

    class Meta:
        ordering = ["-id"]


