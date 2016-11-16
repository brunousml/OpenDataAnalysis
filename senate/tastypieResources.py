from django.forms.models import model_to_dict
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from .models import *


class StateResource(ModelResource):
    class Meta:
        queryset = State.objects.all()
        resource_name = 'state'


class MatterResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                      'parliamentary', verbose_name='parliamentary')

    class Meta:
        queryset = Matter.objects.all()
        resource_name = 'matter'
        filtering = {
            'parliamentary': ALL_WITH_RELATIONS
        }


class CommissionResource(ModelResource):
    parliamentary = fields.ToManyField('senate.tastypieResources.ParliamentaryResource',
                                       'parliamentary', verbose_name='parliamentary')

    class Meta:
        queryset = Commission.objects.all()
        resource_name = 'commission'
        filtering = {
            'parliamentary': ALL_WITH_RELATIONS
        }


class ExpenseResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                       'parliamentary', verbose_name='parliamentary')

    class Meta:
        queryset = Expenses.objects.all()
        resource_name = 'expense'
        filtering = {
            'parliamentary': ALL_WITH_RELATIONS
        }


class MandateResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                       'parliamentary', verbose_name='parliamentary')

    legislature = fields.ToManyField('senate.tastypieResources.LegislatureResource',
                                       'legislature', verbose_name='legislature', null=True)

    exercise = fields.ToManyField('senate.tastypieResources.ExerciseResource',
                                     'exercise', verbose_name='exercise', null=True)

    alternate = fields.ToManyField('senate.tastypieResources.AlternateResource',
                                  'alternate', verbose_name='alternate', null=True)

    state = fields.ToOneField('senate.tastypieResources.StateResource',
                                   'state', verbose_name='state', null=True, full=True)

    class Meta:
        queryset = ActualMandate.objects.all()
        resource_name = 'mandate'
        filtering = {
            'parliamentary': ALL_WITH_RELATIONS
        }

    def append_object(self, object, field, bundle):
        objects = object.objects.filter(actual_mandate=bundle.obj.id)
        for obj in objects:
            bundle.data[field].append(model_to_dict(obj))

        return bundle

    def dehydrate(self, bundle):
        bundle = self.append_object(Legislature, 'legislature', bundle)
        bundle = self.append_object(Exercise, 'exercise', bundle)
        bundle = self.append_object(Alternate, 'alternate', bundle)
        return bundle


class ReportResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                      'parliamentary', verbose_name='parliamentary')

    commission = fields.ToOneField('senate.tastypieResources.CommissionResource',
                                   'commission', verbose_name='commission', full=True)

    matter = fields.ToOneField('senate.tastypieResources.MatterResource',
                               'matter', verbose_name='matter', full=True)

    class Meta:
        queryset = Report.objects.all()
        resource_name = 'report'
        filtering = {
            'parliamentary': ALL_WITH_RELATIONS
        }


class ParliamentaryIdentificationResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                      'parliamentary', verbose_name='parliamentary', full=True)

    state = fields.ToOneField('senate.tastypieResources.StateResource',
                              'state', verbose_name='state', full=True)

    class Meta:
        queryset = ParliamentaryIdentification.objects.all()
        resource_name = 'identification'
        filtering = {
            'code': ALL_WITH_RELATIONS
        }


class ParliamentaryResource(ModelResource):
    natural_state = fields.ToOneField(StateResource, 'natural_state', verbose_name='natural_state', null=True,
                                      full=True)

    class Meta:
        queryset = Parliamentary.objects.all()
        resource_name = 'parliamentary'
        filtering = {
            'code': ALL_WITH_RELATIONS
        }

    def append_object(self, object, field, bundle):
        objects = object.objects.filter(parliamentary=bundle.obj.id)
        for obj in objects:
            bundle.data[field].append(model_to_dict(obj))

        return bundle

    def append_matters(self, bundle):
        return self.append_object(Matter, 'matters', bundle)

    def append_commissions(self, bundle):
        return self.append_object(Commission, 'commissions', bundle)

    def append_reports(self, bundle):
        return self.append_object(Report, 'reports', bundle)
