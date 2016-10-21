from __future__ import unicode_literals

from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.slug


class ParliamentaryIdentification(models.Model):
    code = models.IntegerField()
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


class Legislature(models.Model):
    number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class Exercise(models.Model):
    code = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class Alternate(models.Model):
    participation_description = models.CharField(max_length=100)
    code = models.IntegerField()
    name = models.CharField(max_length=200)


class ActualMandate(models.Model):
    alternates = models.ForeignKey(Alternate, unique=False)
    exercises = models.ForeignKey(Exercise, unique=False)
    state = models.ForeignKey(State)

    code = models.IntegerField()
    participation_description = models.CharField(max_length=100)


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
