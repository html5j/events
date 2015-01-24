
/*
 * inquiry page.
 */

var fs = require('fs');
var DB = require('../model/inquiry/db.js');

var inqObj = {};
inqObj['20150125'] = JSON.parse(fs.readFileSync( __dirname + "/../model/inquiry/20150125.json", "utf8"));

var dbs = {};
dbs['20150125'] = new DB('20150125');


exports.index_get = function (req, res) {
  var date = req.params.date;
  if(inqObj[date]) {
    res.render("inquiry/index", inqObj[date]);
  } else {
    res.status(404);
    res.type('txt').send('Not found');
  }
};

exports.thx = function (req, res) {
  var date = req.params.date;

  if(inqObj[date]) {
    res.render("inquiry/thx", inqObj[date]);
  } else {
    res.status(404);
    res.type('txt').send('Not found');
  }
}

exports.set_profile = function(req, res) {
  var date = req.params.date;

  if(dbs[date]) {
    dbs[date].setProfile(req.body, function() {
      res.status(200);
      res.type('txt').send('ok');
    });
  } else {
    res.status(404);
    res.type('txt').send('Not found');
  }
}

exports.set_session = function(req, res) {
  var date = req.params.date;

  if(dbs[date]) {
    dbs[date].setSession(req.body, function() {
      res.status(200);
      res.type('txt').send('ok');
    });
  } else {
    res.status(404);
    res.type('txt').send('Not found');
  }
}

