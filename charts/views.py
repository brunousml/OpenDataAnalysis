import urllib2
import xmltodict

from django.shortcuts import render


def index(request):
    return render(request, 'charts/base_2.html')


def senadores(request):
    return render(request, 'charts/senadores.html')


def pecs(request):
    data = getXML('http://www.senado.leg.br/rss/projetospecssenadores.xml')
    context = {
        'channel': data['rss']['channel'],
        'data': data
    }
    return render(request=request, template_name='charts/pecs.html', context=context)


def getUpdates(request):
    return False


def getXML(url):
    file = urllib2.urlopen(url)
    data = file.read()
    file.close()

    return xmltodict.parse(data)
