# -*- coding: latin-1 -*-
from data.OpenDataParliamentary import OpenDataParliamentaryBrParser
from senate.models import *
from StringCharsetHelper import StringCharset


class OpenDataParliamentariansParser(object):
    def dump(self):
        self.save_parliamentarians()  # first
        self.save_parliamentary_expenses()  # second

    def save_parliamentary_expenses(self):
        expenses = OpenDataParliamentaryBrParser.get_expenses()
        for expense in expenses:
            if len(expense) == 10 and expense[0] != "ANO":
                parli_ident = ParliamentaryIdentification.objects.filter(name=expense[02].decode("latin-1"))

                if len(parli_ident) > 0:
                    print (expense)
                    Expenses.objects.get_or_create(
                        parliamentary=parli_ident[0].parliamentary,
                        year=expense[0],
                        month=expense[1],
                        kind=StringCharset.latin_to_utf(expense[3]),
                        cpf_cnpj=expense[4],
                        document=StringCharset.latin_to_utf(expense[6]),
                        date=self.get_date(expense[7]),
                        value=expense[9]
                    )
        return expenses

    def get_date(self, date):
        # format date
        date = date.split('/')
        date = date[2] + '-' + date[1] + '-' + date[0]
        return date

    def save_parliamentarians(self):
        count = 0
        parliamentarians = OpenDataParliamentaryBrParser.get_parliamentarians()
        for el in parliamentarians:
            count += 1
            print count
            self.save(el)

        return parliamentarians

    def get_state(self, parser, node, field):
        state, create = State.objects.get_or_create(slug=parser.get_parliamentary_node_field(node, field))

        if create:
            state.save()

        return state

    def add_parliamentary_identification(self, open_data, parliamentary):
        parliamentary_identification = ParliamentaryIdentification.objects.get_or_create(
            parliamentary=parliamentary
        )
        parliamentary_identification = parliamentary_identification[0]
        parliamentary_identification.code = open_data.get_parliamentary_identity('CodigoParlamentar').decode('latin-1')
        parliamentary_identification.name = open_data.get_parliamentary_identity('NomeParlamentar')
        parliamentary_identification.full_name = open_data.get_parliamentary_identity('NomeCompletoParlamentar')
        parliamentary_identification.gender = open_data.get_parliamentary_identity('SexoParlamentar')
        parliamentary_identification.salutation = open_data.get_parliamentary_identity('FormaTratamento')
        parliamentary_identification.url_photo = open_data.get_parliamentary_identity('UrlFotoParlamentar')
        parliamentary_identification.url_page = open_data.get_parliamentary_identity('UrlPaginaParlamentar')
        parliamentary_identification.email = open_data.get_parliamentary_identity('EmailParlamentar')
        parliamentary_identification.acronym_party = open_data.get_parliamentary_identity('SiglaPartidoParlamentar')
        parliamentary_identification.state = self.get_state(open_data, 'IdentificacaoParlamentar', 'UfParlamentar')

        parliamentary_identification.save()

        return parliamentary_identification

    def add_legislature(self, leg, actual_mandate):
        legislature = Legislature.objects.get_or_create(
            number=leg['NumeroLegislatura'],
            actual_mandate=actual_mandate,
            start_date=leg['DataInicio'],
            end_date=leg['DataFim']
        )

        return legislature

    def add_alternates(self, alt, actual_mandate):
        alternate = Alternate.objects.get_or_create(
            code=alt['CodigoParlamentar'],
            actual_mandate=actual_mandate,
            participation_description=alt['DescricaoParticipacao'],
            name=alt['NomeParlamentar']
        )

        return alternate

    def add_exercises(self, exe, actual_mandate):
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

    def add_parliamentary_actual_mandate(self, open_data, parliamentary):
        actual_mandate = ActualMandate.objects.get_or_create(
            code=open_data.get_parliamentary_actual_mandate('CodigoMandato')
        )
        actual_mandate = actual_mandate[0]

        actual_mandate.parliamentary = parliamentary
        actual_mandate.state = self.get_state(open_data, 'MandatoAtual', 'UfParlamentar')
        actual_mandate.participation_description = open_data.get_parliamentary_actual_mandate('DescricaoParticipacao')
        actual_mandate.save()

        if 'MandatoAtual' in open_data.parliamentary:
            self.process_mandate_fields('MandatoAtual', open_data, actual_mandate)

        if 'UltimoMandato' in open_data.parliamentary:
            self.process_mandate_fields('UltimoMandato', open_data, actual_mandate)

        return actual_mandate

    def process_mandate_fields(self, node, open_data, actual_mandate):
        mandate = open_data.parliamentary[node]

        self.add_legislature(mandate['PrimeiraLegislaturaDoMandato'], actual_mandate)
        self.add_legislature(mandate['SegundaLegislaturaDoMandato'], actual_mandate)

        if 'Suplentes' in mandate:
            if len(mandate['Suplentes']['Suplente']) != 2:
                self.add_alternates(mandate['Suplentes']['Suplente'], actual_mandate)
            else:
                for alt in mandate['Suplentes']['Suplente']:
                    self.add_alternates(alt, actual_mandate)

        if 'Exercicios' in mandate:
            if (len(mandate['Exercicios']['Exercicio']) == 2 and 'CodigoExercicio' in mandate['Exercicios'][
                'Exercicio']) or (
                            len(mandate['Exercicios']['Exercicio']) == 3 and 'DataLeitura' in mandate['Exercicios'][
                        'Exercicio']):
                self.add_exercises(mandate['Exercicios']['Exercicio'], actual_mandate)
            else:
                for exe in mandate['Exercicios']['Exercicio']:
                    self.add_exercises(exe, actual_mandate)

    def add_parliamentary_political_party(self, open_data, parliamentary):
        party = open_data.parliamentary['FiliacaoAtual']['Partido']
        pp = PoliticalParty.objects.get_or_create(
            name=party['NomePartido'],
            slug=party['SiglaPartido'],
            code=party['CodigoPartido'],
            membership_date=open_data.parliamentary['FiliacaoAtual']['DataFiliacao'],
            parliamentary=parliamentary
        )

        return pp[0]

    def get_or_create_commissions(self, content, parliamentary):
        commission = {}
        for com in content:
            if type(content) == dict:
                ident = content
                com = {'DescricaoParticipacao': '', 'DataInicio': ''}
            else:
                ident = com.get('IdentificacaoComissao')

            if com.has_key('CodigoComissao'):
                commission = Commission.objects.get_or_create(
                    code=ident.get('CodigoComissao'),
                    slug=ident.get('SiglaComissao'),
                    name=ident.get('NomeComissao'),
                    house=ident.get('NomeCasaComissao'),
                    participation_description=com.get('DescricaoParticipacao'),
                    start_date=com.get('DataInicio'),
                )

                commission[0].parliamentary.add(parliamentary)
                commission[0].save()

            if len(content) == 5 and not content.has_key('DescricaoTipoRelator') and len(commission) > 0:
                return commission[0]

        return commission[0] if len(commission) > 0 else commission

    def get_or_create_matters(self, content, parliamentary):
        for mat in content:
            if mat == "EmentaMateria" or mat == "IdentificacaoMateria":
                mat = content
            ident = mat.get('IdentificacaoMateria')
            matter = Matter.objects.get_or_create(
                code=int(ident.get('CodigoMateria')),
                house_slug=ident.get('SiglaCasaIdentificacaoMateria'),
                house=ident.get('NomeCasaIdentificacaoMateria'),
                subtype_slug=ident.get('SiglaSubtipoMateria'),
                subtype=ident.get('DescricaoSubtipoMateria'),
                number=ident.get('NumeroMateria'),
                year=int(ident.get('AnoMateria')),
                entry=mat.get('EmentaMateria'),
                parliamentary=parliamentary
            )
        return matter[0]

    def get_or_create_reports(self, content, parliamentary):
        for rep in content:
            if type(content) == dict:
                rep = content
            matter = self.get_or_create_matters(rep.get('Materia'), parliamentary)
            commission = self.get_or_create_commissions(rep.get('IdentificacaoComissao'), parliamentary)
            report = Report.objects.get_or_create(
                parliamentary=parliamentary,
                matter=matter,
                commission=commission,
                type_description=rep.get('DescricaoTipoRelator'),
                date_designation=rep.get('DataDesignacao')
            )
        return report[0]

    def get_or_create_responsibility(self, content, parliamentary):
        for res in content:
            if type(content) == dict:
                res = content
            commission = self.get_or_create_commissions(res.get('IdentificacaoComissao'), parliamentary)
            responsibility = Responsibility.objects.get_or_create(
                parliamentary=parliamentary,
                commission=commission,
                code=res.get('CodigoCargo'),
                description=res.get('DescricaoCargo'),
                start_date=res.get('DataInicio')
            )
        return responsibility[0]

    def get_or_create_other_information(self, content, parliamentary):
        for oi in content:
            if type(content) == dict:
                oi = content
            other_information = OtherInformation.objects.get_or_create(
                parliamentary=parliamentary,
                name=oi.get('NomeServico'),
                description=oi.get('DescricaoServico'),
                url=oi.get('UrlServico')
            )
        return other_information[0]

    def save(self, el):
        open_data = OpenDataParliamentaryBrParser()
        open_data.get_parliamentary(el['IdentificacaoParlamentar']['CodigoParlamentar'])

        # Basic Information
        parliamentary, create = Parliamentary.objects.get_or_create(
            code=open_data.parliamentary['IdentificacaoParlamentar']['CodigoParlamentar'])

        parliamentary.natural_state = self.get_state(open_data, 'DadosBasicosParlamentar', 'UfNaturalidade')
        parliamentary.address = open_data.get_parliamentary_basic_data('EnderecoParlamentar')
        parliamentary.phone = open_data.get_parliamentary_basic_data('TelefoneParlamentar')
        parliamentary.fax = open_data.get_parliamentary_basic_data('FaxParlamentar')
        parliamentary.birth_date = open_data.get_parliamentary_basic_data('DataNascimento')
        parliamentary.open_data_url = open_data.parliamentary['UrlGlossario'] + \
                                      open_data.parliamentary['IdentificacaoParlamentar']['CodigoParlamentar']
        parliamentary.save()

        # Foreign Keys
        self.add_parliamentary_identification(open_data, parliamentary)
        self.add_parliamentary_actual_mandate(open_data, parliamentary)
        self.add_parliamentary_political_party(open_data, parliamentary)

        # Matter
        if open_data.parliamentary.has_key('MateriasDeAutoriaTramitando'):
            self.get_or_create_matters(open_data.parliamentary['MateriasDeAutoriaTramitando']['Materia'], parliamentary)


        # REMOVE COMMENTS BELLOW TO ACTIVE THAT INFORMATION TO PARLIAMENTARY PROFILE

        # if open_data.parliamentary.has_key('MembroAtualComissoes'):
        #     self.get_or_create_commissions(open_data.parliamentary['MembroAtualComissoes']['Comissao'], parliamentary)
        # if open_data.parliamentary.has_key('RelatoriasAtuais'):
        #     self.get_or_create_reports(open_data.parliamentary['RelatoriasAtuais']['Relatoria'], parliamentary)
        #
        # if open_data.parliamentary.has_key('CargosAtuais'):
        #     self.get_or_create_responsibility(open_data.parliamentary['CargosAtuais']['CargoAtual'], parliamentary)
        #
        # if open_data.parliamentary.has_key('OutrasInformacoes'):
        #     self.get_or_create_other_information(open_data.parliamentary['OutrasInformacoes']['Servico'], parliamentary)
