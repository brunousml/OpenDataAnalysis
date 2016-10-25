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
                                      'parliamentary', verbose_name='parliamentary')

    class Meta:
        queryset = Report.objects.all()
        resource_name = 'identification'


class ParliamentaryResource(ModelResource):
    commissions = fields.ToManyField(CommissionResource, 'commissions', verbose_name='commissions', null=True)
    natural_state = fields.ForeignKey(StateResource, 'state', verbose_name='natural_state', null=True, full=True)
    identification = fields.ForeignKey(ParliamentaryIdentificationResource, 'identification',
                                       verbose_name='identification', null=True)
    matters = fields.ManyToManyField(MatterResource, 'matters', verbose_name='matters', null=True, full=True)
    reports = fields.ManyToManyField(Report, 'reports', verbose_name='reports', null=True, full=True)

    class Meta:
        queryset = Parliamentary.objects.all()
        resource_name = 'parliamentary'

    def dehydrate(self, bundle):
        bundle = self.append_matters(bundle)
        bundle = self.append_commissions(bundle)
        bundle = self.append_reports(bundle)

        bundle.data['natural_state'] = model_to_dict(bundle.obj.natural_state)
        bundle.data['identification'] = model_to_dict(ParliamentaryIdentification.objects.get(parliamentary=bundle.obj.id))
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

