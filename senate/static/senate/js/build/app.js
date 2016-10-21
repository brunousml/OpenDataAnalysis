function renderPecs(){
     $.get('http://www.senado.leg.br/rss/projetospecssenadores.xml', function(data){
        var channel = data.find('channel');

        var item = channel.find('item');
        var title = item.find('title');

        console.log(title);
    }, 'xml');

     $.ajax({
        url: "http://www.senado.leg.br/rss/projetospecssenadores.xml",
        type: "GET",
        crossDomain: true,
        dataType: "xml",
        headers: {
            "Access-Control-Allow-Origin": "*",
        },
        success: function (data) {
            var channel = data.find('channel');
        },
        error: function (xhr, status) {
            alert("error");
        }
    });
}

function renderMaterias(){
    var limit = 0;
    $.get('http://legis.senado.leg.br/dadosabertos/materia/legislaturaatual?tramitando=S', function(data){
        var ListaMateriasLegislaturaAtual = $(data);
        ListaMateriasLegislaturaAtual.each(function(){
            var Materias = $(this).find('Materias');
            Materias.each(function(){
                var Materia = $(this).find('Materia');
                $('#ajax-content').html('');

                Materia.each(function(){
                    limit++;
                    if(limit > 50){
                        return false;
                    }
                    var IdentificacaoMateria = $(this).find('IdentificacaoMateria');
                    var UrlDetalheMateria = $(this).find('UrlDetalheMateria').text();

                    var CodigoMateria = IdentificacaoMateria.find('CodigoMateria').text();
                    var NumeroMateria = IdentificacaoMateria.find('NumeroMateria').text();

                    $.get(UrlDetalheMateria, function(data){
                        var Materia = $(data).find('Materia');//root
                        var DadosBasicosMateria = Materia.find('DadosBasicosMateria');
                        var IdentificacaoMateria = Materia.find('IdentificacaoMateria');

                        var EmentaMateria = DadosBasicosMateria.find('EmentaMateria').text();

                        var DescricaoSubtipoMateria = IdentificacaoMateria.find('DescricaoSubtipoMateria').text();
//                        var AnoMateria = IdentificacaoMateria.find('AnoMateria').text();

                        $('#ajax-content').append('<div><h2>'+ DescricaoSubtipoMateria +'</h2><p>'+ EmentaMateria +'</p></div>');
                    });
                });
            });
        });
    }, 'json');
}


function renderSenadores(){
    var table = '<div class="table-responsive"><table class="table">';

    $.get('http://legis.senado.leg.br/dadosabertos/senador/lista/atual ', function(data){
                    var identificacaoParlamentar = $(this).find('IdentificacaoParlamentar');
                    var CodigoParlamentar = identificacaoParlamentar.find('CodigoParlamentar').text();
                    var UrlFotoParlamentar = identificacaoParlamentar.find('UrlFotoParlamentar').text();
                    var NomeCompletoParlamentar = identificacaoParlamentar.find('NomeCompletoParlamentar').text();

                    var UrlPaginaParlamentar = identificacaoParlamentar.find('UrlPaginaParlamentar').text();
                    var EmailParlamentar = identificacaoParlamentar.find('EmailParlamentar').text();
                    var SiglaPartidoParlamentar = identificacaoParlamentar.find('SiglaPartidoParlamentar').text();
                    var UfParlamentar = identificacaoParlamentar.find('UfParlamentar').text();

                    var row = '<tr>';
                    row = row +'<td><img width=100 src="'+ UrlFotoParlamentar +'" /></td>';
                    row = row +'<td>'+ CodigoParlamentar +'</td>';
                    row = row +'<td>'+ NomeCompletoParlamentar +'</td>';
                    row = row +'<td>'+ SiglaPartidoParlamentar +'</td>';
                    row = row +'<td>'+ UfParlamentar +'</td>';
                    row = row +'<td>'+ EmailParlamentar +'</td>';
                    table = table + row;
                });
            });
        });

        table = table + '</table></div> ';
        $('#ajax-content').html(table);

    }, 'json');
}

$(document).ready(function(){
//    renderSenadores();
//    renderPecs();
});

