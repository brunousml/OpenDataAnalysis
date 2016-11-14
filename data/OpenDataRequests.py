import requests
import json
import urllib2
import csv


class OpenDataRequests:
    def __init__(self):
        pass

    @staticmethod
    def expenses_csv(year=2016):
        return OpenDataRequests.get_csv_into_list('http://www.senado.gov.br/transparencia/LAI/verba/' + str(year) + '.csv')

    @staticmethod
    def get_csv_into_list(url):
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content
            cr = csv.reader(decoded_content.splitlines(), delimiter=';')
            my_list = list(cr)
        return my_list

    @staticmethod
    def request_json(url, headers):
        req = urllib2.Request(url, None, headers)
        file = urllib2.urlopen(req)
        data = file.read()
        file.close()

        return json.loads(data)

    @staticmethod
    def get_parliamentarians_json():
        return OpenDataRequests.request_json(
            'http://legis.senado.leg.br/dadosabertos/senador/lista/atual',
            {'Accept': 'Application/json'}
        )

    @staticmethod
    def get_parliamentary_json(code):
        return OpenDataRequests.request_json(
            'http://legis.senado.leg.br/dadosabertos/senador/' + code,
            {'Accept': 'Application/json'}
        )