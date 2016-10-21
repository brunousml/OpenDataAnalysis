from __future__ import unicode_literals

from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.slug


class ParliamentaryIdentification(models.Model):
    identification = models.IntegerField()
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=400)
    gender = models.CharField(max_length=20)
    salutation = models.CharField(max_length=100)
    url_photo = models.TextField()
    url_page = models.TextField()
    email = models.CharField(max_length=200, null=True)
    acronym_party = models.CharField(max_length=10, default=None)
    state = models.ForeignKey(State, null=True, default=None)

    def __unicode__(self):
        return self.name

class Parliamentary(models.Model):
    identification = models.ForeignKey(ParliamentaryIdentification)

    def __unicode__(self):
        return unicode(self.identification.name)
