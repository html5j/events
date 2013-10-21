var sponsors = require('../model/sponsors')
	, speakers = require('../model/speakers')
	, sessions = require('../model/sessions')
	, helper = require('../helper/helper.js')		


var models = {
	"sponsors": sponsors,
	"sessions": sessions,
	"speakers": speakers
}

/*
 * GET home page.
 */

exports.index = function (req, res) {
  res.render("2013/index", {
  	id: "index"
  	, title : "HTML5 Conference 2013"	
  	, sponsors: sponsors
  	, show_sponsorlogos: helper.show_sponsorlogos
  });
};

exports.sessions = function (req, res) {
  res.render("2013/sessions", {
  	id: "sessions"
  	, title: "セッション | HTML5 Conference 2013"
  	, session_html: helper.show_sessions(sessions, speakers)
  });
};

exports.speakers = function (req, res) {
  res.render("2013/speakers", {
  	id: "speakers"
  	, title: "スピーカー | HTML5 Conference 2013" 
  	, speakers: speakers
  	, profiles_html: helper.show_profiles
  });
};

exports.access = function (req, res) {
  res.render("2013/access", {
  	id: "access"
  	, title: "会場・アクセス | HTML5 Conference 2013"
  });
};

exports.faq = function (req, res) {
  res.render("2013/faq", {
  	id: "faq"
  	, title: "よくある質問 | HTML5 Conference 2013"
  });
};


// json api
/////////////////////////////////////////////////////
exports.api = function(req, res){
	res.setHeader('Content-Type', 'application/json; charset=UTF-8')

	var model = req.params.model

	if(models.hasOwnProperty(model)) {
		res.end(JSON.stringify(models[model]));
	} else {
		res.send(404, "File not Found")
		res.end()
	}
}