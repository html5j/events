
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes')
	, routes2013 = require('./routes/conf2013')
var http = require('http');
var path = require('path');

var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(express.favicon(__dirname + '/public/images/favicon2013.ico'));
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

// redirect to current year's page
app.get('/', routes.index);

// conference 2013
app.get('/conference/2013/11', routes2013.index)
app.get('/conference/2013/11/sessions', routes2013.sessions)
app.get('/conference/2013/11/speakers', routes2013.speakers)
app.get('/conference/2013/11/access', routes2013.access)
app.get('/conference/2013/11/faq', routes2013.faq)

// run server
app.listen(app.get('port'), function () {
  console.log('Express server listening on port ' + app.get('port'));
});
