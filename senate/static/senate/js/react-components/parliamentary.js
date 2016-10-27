var Parliamentary = React.createClass({
    render: function(){
        console.log(this.props.p);
        return(
            <div className="col-md-3 col-sm-6 hero-feature" >
                <div className="thumbnail" style={{'width': '250px', 'height': '600px'}}>
                    <img src={this.props.p.identification.url_photo} alt="" />
                    <div className="caption">
                        <h3>{this.props.p.identification.name}</h3>
                        <div className="info-p">
                            <ul>
                                <li><strong>Cargo</strong>: {this.props.p.identification.salutation}</li>
                                <li><strong>Materias: </strong>: {this.props.p.matters.length}</li>
                                <li><strong>Comissoes: </strong>: {this.props.p.commissions.length}</li>
                                <li><strong>Relatórios: </strong>: {this.props.p.reports.length}</li>
                            </ul>
                            <h4>Contatos:</h4>
                            <p><strong>Telefone: </strong>: {this.props.p.phone}</p>
                            <p><strong>Email: </strong>: {this.props.p.identification.email}</p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

var Parliamentarians = React.createClass({

  getInitialState: function() {
    return {
      parliamentarians: []
    }
  },

  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: "jsonp",
      cache: false,
      success: function(data) {
        this.setState({parliamentarians: data.objects});
        $('#loading').hide();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  componentWillount:function(){
    return true;
  },

  render: function() {

    var parliamentarians = this.state.parliamentarians.map(
                function(parliamentary, current){
                    return <Parliamentary p={parliamentary} key={parliamentary.id} />
            });

    var style = {'margin': '0 auto', 'maxWidth':'50%','textAlign': 'center'}

    return (
        <div className="row">
            <div id="loading" style={style} className="col-lg-20">
               <p>Aguarde enquanto processo sua solicitaçao.</p>
                <img src="/static/senate/img/loading.gif"  />
            </div>


            {parliamentarians}
        </div>
    )
  }
});

ReactDOM.render(
  <Parliamentarians  url='http://localhost:8000/api/v1/parliamentary?format=jsonp&limit=100'/>,
  document.getElementById('to-render')
);
