from django.core.management.base import BaseCommand

from data.OpenDataParliamentary import OpenDataParliamentaryBrJsonParser
from senate.models import Parliamentary, ParliamentaryIdentification, State, ActualMandate


def get_state(parser, node, field):
    state, create = State.objects.get_or_create(slug=parser.get_parliamentary_node_field(node, field))

    if create:
        state.save()

    return state


def get_parliamentary_identification(open_data):

    parliamentary_identification, create = ParliamentaryIdentification.objects.get_or_create(
        code=open_data.get_parliamentary_identity('CodigoParlamentar')
    )

    parliamentary_identification.name = open_data.get_parliamentary_identity('NomeParlamentar')
    parliamentary_identification.full_name = open_data.get_parliamentary_identity('NomeCompletoParlamentar')
    parliamentary_identification.gender = open_data.get_parliamentary_identity('SexoParlamentar')
    parliamentary_identification.salutation = open_data.get_parliamentary_identity('FormaTratamento')
    parliamentary_identification.url_photo = open_data.get_parliamentary_identity('UrlFotoParlamentar')
    parliamentary_identification.url_page = open_data.get_parliamentary_identity('UrlPaginaParlamentar')
    parliamentary_identification.email = open_data.get_parliamentary_identity('EmailParlamentar')
    parliamentary_identification.acronym_party = open_data.get_parliamentary_identity('SiglaPartidoParlamentar')
    parliamentary_identification.state = get_state(open_data, 'IdentificacaoParlamentar', 'UfParlamentar')

    parliamentary_identification.save()

    return parliamentary_identification


def get_parliamentary_actual_mandate(parliamentary):
    open_data = OpenDataParliamentaryBrJsonParser(parliamentary)

    actual_mandate = ActualMandate.objects.get_or_create(
        code=open_data.get_parliamentary_actual_mandate('CodigoMandato')
    )

    actual_mandate.state = get_state(open_data, 'MandatoAtual', 'UfParlamentar')

    return True


def save_parliamentary(el):
    open_data = OpenDataParliamentaryBrJsonParser()
    open_data.get_parliamentary(el['IdentificacaoParlamentar']['CodigoParlamentar'])

    # Identification
    p_identification = get_parliamentary_identification(open_data)

    # Actual Mandate
    # p_actual_mandate = get_parliamentary_actual_mandate(parliamentary)

    # Basic Information
    parliamentary, create = Parliamentary.objects.get_or_create(identification=p_identification)

    parliamentary.natural_state = get_state(open_data, 'DadosBasicosParlamentar', 'UfNaturalidade')
    parliamentary.address = open_data.get_parliamentary_basic_data('EnderecoParlamentar')
    parliamentary.phone = open_data.get_parliamentary_basic_data('TelefoneParlamentar')
    parliamentary.fax = open_data.get_parliamentary_basic_data('FaxParlamentar')
    parliamentary.birth_date = open_data.get_parliamentary_basic_data('DataNascimento')
    parliamentary.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        parliamentarians = OpenDataParliamentaryBrJsonParser.get_parliamentarians()
        for el in parliamentarians:
            self.stdout.write(
                self.style.SUCCESS(unicode(el[u'IdentificacaoParlamentar'][u'NomeCompletoParlamentar'])))
            save_parliamentary(el)
