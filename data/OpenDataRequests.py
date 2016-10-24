import json
import urllib2


class OpenDataRequests:
    def __init__(self):
        pass

    @staticmethod
    def request(url, headers):
        req = urllib2.Request(url, None, headers)
        file = urllib2.urlopen(req)
        data = file.read()
        file.close()

        return json.loads(data)

    @staticmethod
    def get_parliamentarians_json():
        return OpenDataRequests.request(
            'http://legis.senado.leg.br/dadosabertos/senador/lista/atual',
            {'Accept': 'Application/json'}
        )

    @staticmethod
    def get_parliamentary_json(code):
        return OpenDataRequests.request(
            'http://legis.senado.leg.br/dadosabertos/senador/' + code,
            {'Accept': 'Application/json'}
        )