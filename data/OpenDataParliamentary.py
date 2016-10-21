from data.OpenDataRequests import OpenDataRequests


class OpenDataParliamentaryBrJsonParser:
    def __init__(self, parliamentary=None):
        self.parliamentary_data = parliamentary

    @staticmethod
    def get_parliamentarians():
        open_data = OpenDataRequests.get_parliamentarians_json()
        return open_data[u'ListaParlamentarEmExercicio'][u'Parlamentares'][u'Parlamentar']

    def get_parliamentary_node(self, element):
        if element in self.parliamentary_data[u'IdentificacaoParlamentar']:
            return self.parliamentary_data[u'IdentificacaoParlamentar'][element]

        return None