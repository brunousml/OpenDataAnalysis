from __future__ import unicode_literals

from django.db import models

from OpenDataAnalysis import settings


class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.slug


class ParliamentaryIdentification(models.Model):
    state = models.ForeignKey(State, null=True, default=None)

    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=400)
    gender = models.CharField(max_length=20)

    salutation = models.CharField(max_length=100)
    url_photo = models.TextField()
    url_page = models.TextField()
    email = models.CharField(max_length=200, null=True)
    acronym_party = models.CharField(max_length=10, null=True, default=None)

    def __unicode__(self):
        return self.name


class Legislature(models.Model):
    number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.code


class Exercise(models.Model):
    code = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.code


class Alternate(models.Model):
    participation_description = models.CharField(max_length=100)
    code = models.IntegerField()
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.code


class ActualMandate(models.Model):
    legislature = models.ForeignKey(Legislature)
    alternates = models.ForeignKey(Alternate)
    exercises = models.ForeignKey(Exercise)

    state = models.ForeignKey(State)

    code = models.IntegerField()
    participation_description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.code


class Parliamentary(models.Model):
    identification = models.OneToOneField(ParliamentaryIdentification)
    actual_mandate = models.OneToOneField(ActualMandate, null=True, blank=True)

    birth_date = models.DateField(null=True)
    natural_state = models.ForeignKey(State, null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=100, null=True)
    fax = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return unicode(self.identification.name)
