
/*
 * GET home page.
 */

exports.index = function (req, res) {
  res.render("2013/index", {
  	id: "index"
  	, title : "HTML5 Conference 2013"	
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