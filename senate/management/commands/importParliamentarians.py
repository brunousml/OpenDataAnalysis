from django.core.management.base import BaseCommand

from data.OpenDataParliamentary import OpenDataParliamentaryBrJsonParser
from senate.models import Parliamentary, ParliamentaryIdentification, State, ActualMandate, Legislature, Alternate, \
    Exercise, PoliticalParty, Commission, Matters


def get_state(parser, node, field):
    state, create = State.objects.get_or_create(slug=parser.get_parliamentary_node_field(node, field))

    if create:
        state.save()

    return state


def add_parliamentary_identification(open_data, parliamentary):
    parliamentary_identification, create = ParliamentaryIdentification.objects.get_or_create(
        code=open_data.get_parliamentary_identity('CodigoParlamentar')
    )

    parliamentary_identification.parliamentary = parliamentary

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


def add_legislature(leg, actual_mandate):
    legislature = Legislature.objects.get_or_create(
        number=leg['NumeroLegislatura'],
        actual_mandate=actual_mandate,
        start_date=leg['DataInicio'],
        end_date=leg['DataFim']
    )

    return legislature


def add_alternates(alt, actual_mandate):
    alternate = Alternate.objects.get_or_create(
        code=alt['CodigoParlamentar'],
        actual_mandate=actual_mandate,
        participation_description=alt['DescricaoParticipacao'],
        name=alt['NomeParlamentar']
    )

    return alternate


def add_exercises(exe, actual_mandate):
    exercise = Exercise.objects.get_or_create(
        code=int(exe['CodigoExercicio']),
        actual_mandate=actual_mandate,
        start_date=exe['DataInicio']
    )

    if 'DataFim' in exe:
        exercise[0].end_date = str(exe['DataFim'])
        exercise[0].abbreviation_cause_expulsion = exe['SiglaCausaAfastamento']
        exercise[0].description_cause_expulsion = exe['DescricaoCausaAfastamento']

    return exercise


def add_parliamentary_actual_mandate(open_data, parliamentary):
    actual_mandate = ActualMandate.objects.get_or_create(
        code=open_data.get_parliamentary_actual_mandate('CodigoMandato')
    )
    actual_mandate = actual_mandate[0]

    actual_mandate.parliamentary = parliamentary
    actual_mandate.state = get_state(open_data, 'MandatoAtual', 'UfParlamentar')
    actual_mandate.participation_description = open_data.get_parliamentary_actual_mandate('DescricaoParticipacao')
    actual_mandate.save()

    if 'MandatoAtual' in open_data.parliamentary:
        process_mandate_fields('MandatoAtual', open_data, actual_mandate)

    if 'UltimoMandato' in open_data.parliamentary:
        process_mandate_fields('UltimoMandato', open_data, actual_mandate)

    return actual_mandate


def process_mandate_fields(node, open_data, actual_mandate):
    mandate = open_data.parliamentary[node]

    add_legislature(mandate['PrimeiraLegislaturaDoMandato'], actual_mandate)
    add_legislature(mandate['SegundaLegislaturaDoMandato'], actual_mandate)

    if 'Suplentes' in mandate:
        if len(mandate['Suplentes']['Suplente']) != 2:
            add_alternates(mandate['Suplentes']['Suplente'], actual_mandate)
        else:
            for alt in mandate['Suplentes']['Suplente']:
                add_alternates(alt, actual_mandate)

    if 'Exercicios' in mandate:
        if (len(mandate['Exercicios']['Exercicio']) == 2 and 'CodigoExercicio' in mandate['Exercicios'][
            'Exercicio']) or (
                        len(mandate['Exercicios']['Exercicio']) == 3 and 'DataLeitura' in mandate['Exercicios'][
                    'Exercicio']):
            add_exercises(mandate['Exercicios']['Exercicio'], actual_mandate)
        else:
            for exe in mandate['Exercicios']['Exercicio']:
                add_exercises(exe, actual_mandate)


def add_parliamentary_political_party(open_data, parliamentary):
    party = open_data.parliamentary['FiliacaoAtual']['Partido']
    pp = PoliticalParty.objects.get_or_create(
        name=party['NomePartido'],
        slug=party['SiglaPartido'],
        code=party['CodigoPartido'],
        membership_date=open_data.parliamentary['FiliacaoAtual']['DataFiliacao'],
        parliamentary=parliamentary
    )

    return pp[0]


def add_parliamentary_commissions(open_data, parliamentary):
    if 'MembroAtualComissoes' in open_data.parliamentary:
        commissions = open_data.parliamentary['MembroAtualComissoes']['Comissao']
        for com in commissions:
            ident = com['IdentificacaoComissao']
            commission = Commission.objects.get_or_create(
                code=ident['CodigoComissao'],
                slug=ident['SiglaComissao'],
                name=ident['NomeComissao'],
                house=ident['NomeCasaComissao'],
                participation_description=com['DescricaoParticipacao'],
                start_date=com['DataInicio'],
            )

            commission[0].parliamentary.add(parliamentary)
            commission[0].save()


def add_parliamentary_matters(open_data, parliamentary):
    if 'MateriasDeAutoriaTramitando' in open_data.parliamentary:
        mats = open_data.parliamentary['MateriasDeAutoriaTramitando']['Materia']
        for mat in mats:
            if mat == "EmentaMateria":
                mat = mats
            ident = mat['IdentificacaoMateria']
            matter = Matters.objects.get_or_create(
                code=int(ident['CodigoMateria']),
                house_slug=ident['SiglaCasaIdentificacaoMateria'],
                house=ident['NomeCasaIdentificacaoMateria'],
                subtype_slug=ident['SiglaSubtipoMateria'],
                subtype=ident['DescricaoSubtipoMateria'],
                number=ident['NumeroMateria'],
                year=int(ident['AnoMateria']),
                entry=mat['EmentaMateria'],
                parliamentary=parliamentary
            )


def save_parliamentary(el):
    open_data = OpenDataParliamentaryBrJsonParser()
    open_data.get_parliamentary(el['IdentificacaoParlamentar']['CodigoParlamentar'])

    # Basic Information
    parliamentary, create = Parliamentary.objects.get_or_create(
        code=open_data.parliamentary['IdentificacaoParlamentar']['CodigoParlamentar'])

    parliamentary.natural_state = get_state(open_data, 'DadosBasicosParlamentar', 'UfNaturalidade')
    parliamentary.address = open_data.get_parliamentary_basic_data('EnderecoParlamentar')
    parliamentary.phone = open_data.get_parliamentary_basic_data('TelefoneParlamentar')
    parliamentary.fax = open_data.get_parliamentary_basic_data('FaxParlamentar')
    parliamentary.birth_date = open_data.get_parliamentary_basic_data('DataNascimento')
    parliamentary.save()

    # Foreign Keys
    add_parliamentary_identification(open_data, parliamentary)
    add_parliamentary_actual_mandate(open_data, parliamentary)
    add_parliamentary_political_party(open_data, parliamentary)
    add_parliamentary_commissions(open_data, parliamentary)
    add_parliamentary_matters(open_data, parliamentary)


class Command(BaseCommand):
    def handle(self, *args, **options):
        parliamentarians = OpenDataParliamentaryBrJsonParser.get_parliamentarians()
        for el in parliamentarians:
            log_txt = unicode(
                el[u'IdentificacaoParlamentar'][u'CodigoParlamentar'] + ' - ' + el[u'IdentificacaoParlamentar'][
                    u'NomeCompletoParlamentar'])

            self.stdout.write(self.style.SUCCESS(log_txt))
            save_parliamentary(el)
