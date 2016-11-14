from data.OpenDataRequests import OpenDataRequests


class OpenDataParliamentaryBrParser:
    def __init__(self):
        self.parliamentary = None
        pass

    @staticmethod
    def get_expenses():
        return OpenDataRequests.expenses_csv()

    @staticmethod
    def get_parliamentarians():
        open_data = OpenDataRequests.get_parliamentarians_json()
        return open_data[u'ListaParlamentarEmExercicio'][u'Parlamentares'][u'Parlamentar']

    def get_parliamentary(self, code):
        response = OpenDataRequests.get_parliamentary_json(code)
        self.parliamentary = response[u'DetalheParlamentar'][u'Parlamentar']
        return self.parliamentary

    def get_parliamentary_node_field(self, node, field):
        if node in self.parliamentary:
            if field in self.parliamentary[node]:
                return self.parliamentary[node][field]

        return None

    def get_parliamentary_identity(self, field):
        return self.get_parliamentary_node_field('IdentificacaoParlamentar', field)

    def get_parliamentary_actual_mandate(self, field):
        return self.get_parliamentary_node_field('MandatoAtual', field)

    def get_parliamentary_basic_data(self, field):
        return self.get_parliamentary_node_field('DadosBasicosParlamentar', field)