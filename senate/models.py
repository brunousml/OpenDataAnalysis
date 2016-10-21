from __future__ import unicode_literals

from django.db import models


class ParliamentaryIdentification(models.Model):
    identification = models.IntegerField()
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=400)
    gender = models.CharField(max_length=20)


class Parliamentary(models.Model):
    identification = models.ForeignKey(ParliamentaryIdentification)
