
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes')
    , routes2013 = require('./routes/conf2013')
    , inquiry = require('./routes/inquiry')
var http = require('http');
var path = require('path');
var fs = require('fs')


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

if(process.env.AUTH==="BASIC") {
    var acc = JSON.parse(fs.readFileSync(__dirname+'/passwords/basic.json'))
    app.all('/conference/2013/11/*', express.basicAuth(function (user, pass) {
        return user === acc.user && pass === acc.password;
    }));
}
// redirect to current year's page
app.get('/', routes.index);

// conference 2013
app.get('/conference/2013/11/', routes2013.index);
app.get('/conference/2013/11/sessions', routes2013.sessions);
app.get('/conference/2013/11/sessions_v', routes2013.sessions_v);
app.get('/conference/2013/11/speakers', routes2013.speakers);
app.get('/conference/2013/11/access', routes2013.access);
app.get('/conference/2013/11/volunteer', routes2013.volunteer);
app.get('/conference/2013/11/offering', routes2013.offering);
app.get('/conference/2013/11/faq', routes2013.faq);
app.get('/conference/2013/11/booth', routes2013.booth);
app.get('/conference/2013/11/guide', routes2013.guide);

app.get('/conference/2013/11/speaker/:speaker_id', routes2013.speaker);
app.get('/conference/2013/11/api/:model', routes2013.api);
app.get('/conference/2013/11/questionnaire', routes2013.questionnaire);

// inquiry
app.get('/inquiry/:date', inquiry.index_get);
app.post('/inquiry/:date', inquiry.index_post);

app.post('/inquiry/:date/profile', inquiry.set_profile);
app.post('/inquiry/:date/session', inquiry.set_session);

// run server
app.listen(app.get('port'), function () {
    console.log('Express server listening on port ' + app.get('port'));
});


// temporary use
// app.all('/meetup/46/*', express.basicAuth(function(user, password) {
//   return user === 'html5j' && password === 'goemon';
// }));
