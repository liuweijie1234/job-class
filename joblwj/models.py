# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.


class SelectScript(models.Model):
    scriptname = models.CharField(max_length=50)
    scriptcontent = models.CharField(max_length=50)

    def __str__(self):
        return self.scriptname
