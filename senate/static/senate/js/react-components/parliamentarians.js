var Parliamentary = React.createClass({
    redirect: function(){
        location.href = '/parliamentary/profile/' + this.props.p.code;
    },
    render: function(){
        return(
            <div className="col-md-3 col-sm-20 hero-feature" style={{'height':'650px', 'cursor': 'pointer'}} onClick={this.redirect} >
                <div className="thumbnail" >
                    <img src={this.props.p.url_photo} style={{'width':'100%'}} alt="" />
                    <div className="caption">
                        <h3 className='name'>{this.props.p.salutation} {this.props.p.name}</h3>
                        <div className="info-p">
                            <h4 className='acronym'><b>Partido:</b>{this.props.p.acronym_party}</h4>
                            <p className="state"><b>Estado:</b> {this.props.p.state.slug}</p>
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
      parliamentarians: [],
      search_value: ''
    }
  },

  componentWillMount:function(){
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

  search: function(el){
        this.setState({search_value: el.target.value.toLowerCase()});
  },

  render: function() {

    var parliamentarians = this.state.parliamentarians.map(
                function(parliamentary, current){
                    var p = <li key={parliamentary.id}><Parliamentary p={parliamentary} key={parliamentary.id} /></li>;
                    if( this.state.search_value.length == 0
                        || parliamentary.name.toLowerCase().indexOf(this.state.search_value) != -1
                            || parliamentary.acronym_party.toLowerCase().indexOf(this.state.search_value) != -1
                                || parliamentary.state.slug.toLowerCase().indexOf(this.state.search_value) != -1 ){

                        return p;
                    }
                }.bind(this)
    );

    var style = {'margin': '0 auto', 'maxWidth':'50%','textAlign': 'center'}

    return (
        <div className="row">
              <div className="col-lg-20">
                <strong> Busca: </strong>
                <input className="search " type="text" value={this.state.input_value}  onChange={this.search} placeholder="Renan" />
                <hr/>
              </div>

              <div id="loading" style={style} className="col-lg-20">
                   <p>Estamos coletando dados públicos. Isto pode demorar alguns minutos.</p>
                    <img src="/static/senate/img/loading.gif"  />
              </div>
              <ul style={{'listStyle': 'none','padding': '0'}} className="parliamentarians">
                {parliamentarians}
              </ul>
        </div>
    )
  }
});

ReactDOM.render(
  <Parliamentarians  url='/api/v1/identification?format=jsonp&limit=9999'/>,
  document.getElementById('to-render')
);
