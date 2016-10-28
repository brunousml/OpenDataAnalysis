from django.forms.models import model_to_dict
from tastypie import fields
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


class CommissionResource(ModelResource):
    parliamentary = fields.ToManyField('senate.tastypieResources.ParliamentaryResource',
                                       'parliamentary', verbose_name='parliamentary')

    class Meta:
        queryset = Commission.objects.all()
        resource_name = 'commission'


class ReportResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                      'parliamentary', verbose_name='parliamentary')

    class Meta:
        queryset = Report.objects.all()
        resource_name = 'report'


class ParliamentaryIdentificationResource(ModelResource):
    parliamentary = fields.ToOneField('senate.tastypieResources.ParliamentaryResource',
                                      'parliamentary', verbose_name='parliamentary', full=True)

    state = fields.ToOneField('senate.tastypieResources.StateResource',
                              'state', verbose_name='state', full=True)

    class Meta:
        queryset = ParliamentaryIdentification.objects.all()
        resource_name = 'identification'


class ParliamentaryResource(ModelResource):
    natural_state = fields.ToOneField(StateResource, 'natural_state', verbose_name='natural_state', null=True, full=True)

    class Meta:
        queryset = Parliamentary.objects.all()
        resource_name = 'parliamentary'

    def dehydrate(self, bundle):
        # bundle.data['natural_state'] = model_to_dict(bundle.obj.natural_state)
        return bundle

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
