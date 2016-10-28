var Parliamentary = React.createClass({
    redirect: function(){
        location.href = '/parliamentary/profile/' + this.props.p.code;
    },
    render: function(){
        return(
            <div className="col-md-3 col-sm-50 hero-feature" style={{'minHeight':'600px', 'cursor': 'pointer'}} onClick={this.redirect} >
                <div className="thumbnail" >
                    <img src={this.props.p.url_photo} style={{'width':'100%'}} alt="" />
                    <div className="caption">
                        <h3>{this.props.p.salutation} {this.props.p.name}</h3>
                        <div className="info-p">
                            <h4>{this.props.p.acronym_party} / {this.props.p.state.slug}</h4>
                            <p><strong>Fone: </strong> <br/>{this.props.p.parliamentary.phone}</p>
                            <p><strong>Email: </strong> <br/>{this.props.p.email}</p>
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
  <Parliamentarians  url='/api/v1/identification?format=jsonp&limit=200'/>,
  document.getElementById('to-render')
);
