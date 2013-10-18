var sponsors = require('../model/sponsors')

// Helper functions
function show_logos(arr) {
	var _header = '<ul class="list-unstyled list-inline">'
		, _footer = '</ul>'
		, _body = '<li><a class="thumbnail" href="{{href}}"><img src="{{img_url}}" alt="{{alt}}"></a>'
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