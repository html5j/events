
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
    res.render("inquiry/index_get", inqObj[date]);
  } else {
    res.status(404);
    res.type('txt').send('Not found');
  }
};

exports.index_post = function (req, res) {
  res.render("inquiry/index_post", {title: "dummy"});
}

exports.set_profile = function(req, res) {
  var date = req.params.date;

  res.status(200);
  res.type('txt').send('ok');

  //db.setProfile(req.params, function() {
  //  res.status(200);
  //  res.type('txt').send('ok');
  //});
}

exports.set_session = function(req, res) {
  var date = req.params.date;

  res.status(200);
  res.type('txt').send('ok');
  // db.setSession(req.params, function() {
  //   res.status(200);
  //   res.type('txt').send('ok');
  // });
}

