var Parliamentary = React.createClass({
    render: function(){
        return(
            <div className="col-md-3 col-sm-20 hero-feature" style={{'height':'600px'}} >
                <div className="thumbnail" >
                    <img src={this.props.p.identification.url_photo} style={{'width':'100%'}} alt="" />
                    <div className="caption">
                        <h3>{this.props.p.identification.salutation} {this.props.p.identification.name}</h3>
                        <div className="info-p">
                            <h4>Contatos:</h4>
                            <p><strong>Telefone: </strong>: <br/>{this.props.p.phone}</p>
                            <p><strong>Email: </strong>: <br/>{this.props.p.identification.email}</p>
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
               <p>Estamos coletando dados públicos. Isto pode demorar alguns minutos.</p>
                <img src="/static/senate/img/loading.gif"  />
            </div>


            {parliamentarians}
        </div>
    )
  }
});

ReactDOM.render(
  <Parliamentarians  url='/api/v1/parliamentary?format=jsonp&limit=200'/>,
  document.getElementById('to-render')
);
