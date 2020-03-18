# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.


class SelectScript(models.Model):
    scriptname = models.CharField(max_length=50)
    scriptcontent = models.CharField(max_length=50)

    def __str__(self):
        return self.scriptname

class Doinfo(models.Model):
    businessname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    scriptname = models.ForeignKey(SelectScript, models.CASCADE)
    operatingtime = models.DateTimeField(auto_now_add=True)
    ipcount = models.IntegerField()
    status = models.CharField(max_length=100)
    scriptcontent = models.CharField(max_length=50)
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.businessname

    class Meta:
        ordering = ["-id"]


