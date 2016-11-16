from __future__ import unicode_literals

from django.db import models

from OpenDataAnalysis import settings


class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.slug


class Parliamentary(models.Model):
    natural_state = models.ForeignKey(State, null=True)
    code = models.IntegerField()
    birth_date = models.DateField(null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=100, null=True)
    fax = models.CharField(max_length=100, null=True)
    open_data_url = models.URLField(null=True)

    def __unicode__(self):
        id = ParliamentaryIdentification.objects.get(parliamentary=self)
        return unicode(id.name)


class Expenses(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)

    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    kind = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=20)
    document = models.CharField(max_length=50)
    date = models.DateField(max_length=20)
    value = models.CharField(max_length=200)

    def __unicode__(self):
        return "Parlimanetary_id: " + str(self.parliamentary.id) + " - Description: " + self.kind


class Matter(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)

    code = models.IntegerField()
    house_slug = models.SlugField()
    house = models.CharField(max_length=100)
    subtype_slug = models.SlugField()
    subtype = models.CharField(max_length=100)
    number = models.CharField(max_length=50)
    year = models.IntegerField()
    entry = models.TextField()

    def __unicode__(self):
        return self.entry


class Commission(models.Model):
    parliamentary = models.ManyToManyField(Parliamentary)

    code = models.IntegerField()
    slug = models.SlugField()
    name = models.CharField(max_length=200)
    house = models.CharField(max_length=200)
    participation_description = models.CharField(max_length=200)
    start_date = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.name


class Report(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)
    matter = models.ForeignKey(Matter)
    commission = models.ForeignKey(Commission)

    type_description = models.CharField(max_length=100)
    date_designation = models.DateField()
    menu = models


class ParliamentaryIdentification(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)
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


class ActualMandate(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)
    code = models.IntegerField()
    participation_description = models.CharField(max_length=100)

    state = models.ForeignKey(State, null=True)

    def __unicode__(self):
        return str(self.code)


class Legislature(models.Model):
    actual_mandate = models.ForeignKey(ActualMandate, null=True)

    number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return str(self.number)


class Exercise(models.Model):
    actual_mandate = models.ForeignKey(ActualMandate, null=True)

    code = models.IntegerField()
    start_date = models.DateField()

    end_date = models.DateField(null=True)
    abbreviation_cause_expulsion = models.CharField(max_length=10, null=True)
    description_cause_expulsion = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return str(self.code)


class Alternate(models.Model):
    actual_mandate = models.ForeignKey(ActualMandate, null=True)

    participation_description = models.CharField(max_length=100)
    code = models.IntegerField()
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return str(self.code)


class PoliticalParty(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    code = models.IntegerField()
    membership_date = models.DateField()

    def __unicode__(self):
        return str(self.code)


class Responsibility(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)

    commission = models.ForeignKey(Commission, null=True)
    code = models.IntegerField()
    description = models.CharField(max_length=200)
    start_date = models.DateField()

    def __unicode__(self):
        return self.description


class OtherInformation(models.Model):
    parliamentary = models.ForeignKey(Parliamentary, null=True)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    url = models.URLField()

    def __unicode__(self):
        return self.description
