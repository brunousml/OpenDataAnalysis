$(document).ready(function(){
    var table = '<div class="table-responsive"><table class="table">';

    $.get('http://legis.senado.leg.br/dadosabertos/senador/lista/atual ', function(data){
        var ListaParlamentarEmExercicio = $(data);
        ListaParlamentarEmExercicio.each(function(){
            var parlamentares = $(this).find('Parlamentares');
            parlamentares.each(function(){
                var parlamentar = $(this).find('Parlamentar');
                parlamentar.each(function(){
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
        $('#senadores').html(table);

    }, 'xml');

});