import urllib2

from django.core.management.base import BaseCommand, CommandError
import json

from senate.models import Parliamentary, ParliamentaryIdentification, State


def getParliamentaryIdentification(parliamentary):
    parliamentary_identification = ParliamentaryIdentification.objects.filter(
        name=parliamentary[u'IdentificacaoParlamentar'][u'NomeParlamentar'])

    if not parliamentary_identification:
        # Get State
        state = State.objects.filter(slug=parliamentary[u'IdentificacaoParlamentar'][u'UfParlamentar'])
        if not state:
            state = State(slug=parliamentary[u'IdentificacaoParlamentar'][u'UfParlamentar'])
            state.save()
        else:
            state = state[0]

        # Create Parliamentary
        email = ''
        if 'EmailParlamentar' in parliamentary[u'IdentificacaoParlamentar']:
            email = parliamentary[u'IdentificacaoParlamentar'][u'EmailParlamentar']

        parliamentary_identification = ParliamentaryIdentification(
            identification=int(parliamentary[u'IdentificacaoParlamentar'][u'CodigoParlamentar']),
            name=parliamentary[u'IdentificacaoParlamentar'][u'NomeParlamentar'],
            full_name=parliamentary[u'IdentificacaoParlamentar'][u'NomeCompletoParlamentar'],
            gender=parliamentary[u'IdentificacaoParlamentar'][u'SexoParlamentar'],
            salutation=parliamentary[u'IdentificacaoParlamentar'][u'FormaTratamento'],
            url_photo=parliamentary[u'IdentificacaoParlamentar'][u'UrlFotoParlamentar'],
            url_page=parliamentary[u'IdentificacaoParlamentar'][u'UrlPaginaParlamentar'],
            email=email,
            acronym_party=parliamentary[u'IdentificacaoParlamentar'][u'SiglaPartidoParlamentar'],
            state=state,

        )
        parliamentary_identification.save()
    else:
        parliamentary_identification = parliamentary_identification[0]

    return parliamentary_identification


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

            p_identification = getParliamentaryIdentification(parliamentary)
            parliamentary = Parliamentary.objects.filter(identification=p_identification)

            parliamentary = Parliamentary(identification=p_identification)
            parliamentary.save()
