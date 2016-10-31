
import urllib2
import xmltodict

from django.shortcuts import render


def index(request):
    return render(request, 'senate/index.html')


def parliamentarians(request):
    context = {'title': 'Lista de Parlamentares'}
    return render(request=request, template_name='senate/parliamentarians.html', context=context)
    # return render(request=request, template_name='senate/parliamentarians.html', context=context)


def parliamentary_profile(request, code):
    context = {
        'code': code,
        'title': 'Perfil Parlamentar'
    }
    return render(request=request, template_name='senate/parliamentary_profile.html', context=context)


def pecs(request):
    data = getXML('http://www.senado.leg.br/rss/projetospecssenadores.xml')
    context = {
        'channel': data['rss']['channel'],
        'data': data,
        'title': 'Lista de PECs no Senado Federal'
    }
    return render(request=request, template_name='senate/pecs.html', context=context)

def getXML(url):
    file = urllib2.urlopen(url)
    data = file.read()
    file.close()

    return xmltodict.parse(data)
