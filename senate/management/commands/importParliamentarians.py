import urllib2
import xmltodict

from django.core.management.base import BaseCommand, CommandError
import json

from senate.models import Parliamentary, ParliamentaryIdentification


class Command(BaseCommand):
    def getData(self, url):
        headers = {'Accept': 'Application/json'}
        req = urllib2.Request(url, None, headers)
        file = urllib2.urlopen(req)
        data = file.read()
        file.close()

        return json.loads(data)

    def handle(self, *args, **options):
        parliamentarians = self.getData('http://legis.senado.leg.br/dadosabertos/senador/lista/atual')
        for parliamentary in parliamentarians[u'ListaParlamentarEmExercicio'][u'Parlamentares'][u'Parlamentar']:
            self.stdout.write(
                self.style.SUCCESS(unicode(parliamentary[u'IdentificacaoParlamentar'][u'NomeCompletoParlamentar'])))

            newParliamentaryIdentification = ParliamentaryIdentification(
                identification=int(parliamentary[u'IdentificacaoParlamentar'][u'CodigoParlamentar']),
                name=parliamentary[u'IdentificacaoParlamentar'][u'NomeParlamentar'],
                full_name=parliamentary[u'IdentificacaoParlamentar'][u'NomeCompletoParlamentar'],
                gender=parliamentary[u'IdentificacaoParlamentar'][u'SexoParlamentar'],
            )
            newParliamentaryIdentification.save()

            newParliamentary = Parliamentary(identification=newParliamentaryIdentification)
            newParliamentary.save()
