var Reports = React.createClass({
    getInitialState: function() {
        return {
          reports: []
        }
    },

    componentDidMount: function() {
        $.ajax({
          url: '/api/v1/report/',
          dataType: "jsonp",
          cache: false,
          success: function(data) {
            this.setState({reports: data.objects});
            $('#loading').hide();
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    },

    componentWillMount:function(){
        return true;
    },

    render: function(){
        var reports = this.state.reports.map(
            function(report, current){
                return <Report r={report} key={report.id} />
            }
        );

        return <div>{reports}</div>;
    }
});

var Report = React.createClass({
    render: function(){
        return (
            <div className='reports'>
                <h5>{this.props.r.type_description} na {this.props.r.commission.name} no {this.props.r.commission.house}</h5>
            </div>
        )
    }
});

var Commissions = React.createClass({
    getInitialState: function() {
        return {
          commissions: []
        }
    },

    componentDidMount: function() {
        $.ajax({
          url: '/api/v1/commission/?parliamentary__code=' + this.props.code,
          dataType: "jsonp",
          cache: false,
          success: function(data) {
            this.setState({commissions: data.objects});
            $('#loading').hide();
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    },

    componentWillMount:function(){
        return true;
    },

    render: function(){
        var commissions = this.state.commissions.map(
            function(commission, current){
                return <Commission c={commission} key={commission.id} />
            }
        );

        return <div>{commissions}</div>;
    }
});

var Commission = React.createClass({
    render: function(){
        return (
            <div className='commission'>
                <h5><b>{this.props.c.code} - {this.props.c.participation_description} em {this.props.c.name}</b> <small> {this.props.c.house} {this.props.c.date_start}</small></h5>

            </div>
        )
    }
});

var Matters = React.createClass({
    getInitialState: function() {
        return {
          matters: []
        }
    },

    componentDidMount: function() {
        $.ajax({
          url: '/api/v1/matter/?identification__code=' + this.props.code,
          dataType: "jsonp",
          cache: false,
          success: function(data) {
            this.setState({matters: data.objects});
            $('#loading').hide();
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    },

    componentWillMount:function(){
        return true;
    },

    redirect: function(){
        location.href = '/parliamentary/profile/' + this.props.p.code;
    },

    render: function(){
        var matters = this.state.matters.map(
            function(matter, current){
                return <Matter m={matter} key={matter.id} />
            }
        );

        return <div>{matters}</div>;
    }
});

var Matter = React.createClass({

    getInitialState: function() {
        return {
          display_description: false
        }
    },

    toggleDescription: function(){
        this.setState({display_description: !this.state.display_description});
    },

    render: function(){
        var style_description = (this.state.display_description) ? {'display': 'block'}:{'display': 'none'};
        return (
            <div className='matter'>
                <h5><b>{this.props.m.subtype} {this.props.m.code}</b><small> - {this.props.m.house} {this.props.m.year}</small></h5>

                <p><a href="javascript:false" onClick={this.toggleDescription}> Leia o texto + </a></p>
                <p style={style_description}  >{this.props.m.entry}</p>
            </div>
        )
    }
});

var Parliamentary = React.createClass({
    render: function(){
        return(
            <div className='tt'>
                <div className="col-md-3 col-sm-50 hero-feature" style={{'minHeight':'600px', 'cursor': 'pointer'}} >
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

                <div className="col-lg-8">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            Relatórios
                        </div>
                        <div className="panel-body">
                            <Reports code={this.props.p.code} />
                        </div>
                    </div>
                </div>

                <div className="col-lg-4">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            Matérias
                        </div>
                        <div className="panel-body">
                            <Matters code={this.props.p.code} />
                        </div>
                    </div>
                </div>

                <div className="col-lg-8">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            Comissões
                        </div>
                        <div className="panel-body">
                            <Commissions code={this.props.p.code} />
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

  componentWillMount:function(){
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

var url = '/api/v1/identification?code=' + $('#code').html();
ReactDOM.render(
  <Parliamentarians  url={url}/>,
  document.getElementById('to-render')
);
