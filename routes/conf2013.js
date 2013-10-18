var sponsors = require('../model/sponsors')
	, speakers = require('../model/speakers')

// Helper functions
function show_logos(arr) {
	var _header = '<ul class="list-unstyled list-inline">'
		, _body = '<li><a class="thumbnail" href="{{href}}"><img src="{{img_url}}" alt="{{alt}}"></a>'
		, _footer = '</ul>'

	var ret = [];

	ret.push(_header);

	arr.forEach(function(obj){
		ret.push(
			_body.replace("{{href}}", obj.href)
				.replace("{{img_url}}", obj.img_url)
				.replace("{{alt}}", obj.alt)
		)
	})

	ret.push(_footer)

	return ret.join("\n")
}

function show_profiles(obj){
	var _body = [
		'<section class="speaker">', 
	    '<h2 id="{{speaker_id}}"><a href="{{speaker_url}}">{{name}}</a></h2>',
	    '<p class="affiliation">{{affiliation}}</p>',
	    '<p class="image"><img src="{{img_url}}" alt="{{img_alt}}"></p>',
	    '<div class="description">{{description}}</div>',
	  	'</section>'
  	].join("\n");

  	var ret = []

  	for(var key in obj) if(obj.hasOwnProperty(key)){
  		ret.push(_body
  			.replace("{{speaker_id}}", key)
  			.replace("{{speaker_url}}", obj[key].url)
  			.replace("{{name}}", obj[key].name)
  			.replace("{{affiliation}}", obj[key].affiliation)
  			.replace("{{img_url}}", obj[key].img_url)
  			.replace("{{img_alt}}", obj[key].name)
  			.replace("{{description}}", obj[key].description)
  		)
  	}

  	return ret.join("\n")
}

/*
 * GET home page.
 */

exports.index = function (req, res) {
  res.render("2013/index", {
  	id: "index"
  	, title : "HTML5 Conference 2013"	
  	, sponsors: sponsors
  	, show_logos: show_logos
  });
};

exports.sessions = function (req, res) {
  res.render("2013/sessions", {
  	id: "sessions"
  	, title: "セッション | HTML5 Conference 2013"
  });
};

exports.speakers = function (req, res) {
  res.render("2013/speakers", {
  	id: "speakers"
  	, title: "スピーカー | HTML5 Conference 2013" 
  	, speakers: speakers
  	, show_profiles: show_profiles
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