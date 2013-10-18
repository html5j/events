var sponsors = require('../model/sponsors')
	, speakers = require('../model/speakers')
	, sessions = require('../model/sessions')

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

function show_sessions(sessions, speakers) {
	//
	// クロージャ関数の宣言
	//////////////////////////////////////

	//
	// break timeの行を作るクロージャ
	//
	var _break = function(obj){
		var _header = '<tr class="break active">'
        var _body = '<th class="time" scope="row">{{time}}<td colspan="6">{{text}}'
		var ret = [];

		ret.push(_header)
		ret.push(_body
			.replace("{{time}}", obj.time)
			.replace("{{text}}", obj.text)
		)

		return ret.join("\n");
	}

	//
	// sessionの行を作るクロージャ
	//
	var _session = function(obj, speakers){
		var _header = [
			'<tr>',
        	'<th class="time" scope="row">{{time}}'
        ].join("\n")

        var _body_top = [
	        	'<td class="session">',
	        '  <h4 class="sesssion-title"><a href="">{{title}}</a></h4>',
	        ' <p class="session-speaker">'
	    ].join("\n")

	    var _body_middle = [
	        '    <span class="name">{{name}}</span><br>',
	        '    <span class="affiliation">{{affiliation}}</span>'
	    ].join("\n")

	    var _body_bottom = [
	        '  </p>',
	        '  <div class="session-desc">',
	        '    <p>{{description}}</p>',
	        '  </div>',
	        '  <div class="materials">',
	        '    <p><!--<span class="button">講演資料</span><span class="button">講演映像</span>--></p>',
	        '  </div>',
	        '  <hr>',
	        '  <div class="toolbox">',
	        '    <p><a class="btn btn-default btn-xs"><span class="glyphicon glyphicon-star"></span>見たい！</a></p>',
	        '  </div>'
        ].join("\n")

		var ret = [];

		ret.push(_header.replace("{{time}}", obj.time))

		obj.sessions.forEach(function(sess) {
			ret.push(_body_top.replace("{{title}}", sess.title))

			var first = true;
			sess.speakers.forEach(function(spk_id){
				var speaker = speakers[spk_id]
				if(first === false) ret.push("<br>")
				ret.push(_body_middle.replace("{{name}}", speaker.name).replace("{{affiliation}}", speaker.affiliation))
				first = false;
			})

			ret.push(_body_bottom.replace("{{description}}", sess.description))
		});

		return ret.join("\n");
	}


	//
	// session table生成
	////////////////////////////////////////////////////
	var _header = [
		'<div class="table-responsive">',
	    '<table class="table table-">',
	    '<thead>',
	    '  <tr>',
	    '    <th scope="col">時間',
	    '    <th scope="col">ルーム<br>(1F)<br>定員：360',
	    '    <th scope="col">ルーム<br>(2F)<br>定員：300',
	    '    <th scope="col">ルーム<br>(5F)<br>定員：120',
	    '    <th scope="col">ルーム<br>(5F)<br>定員：120',
	    '    <th scope="col">ルーム<br>(5F)<br>定員：360',
	    '    <th scope="col">ルーム<br>(6F)<br>定員：240',
	    '</thead>'
	].join("\n")

	var _footer = "</table>\n</div>"

	var ret = [];

	ret.push(_header)

	sessions.forEach(function(sess){
		if(sess.type === "break") {
			ret.push(_break(sess))
		} else {
			ret.push(_session(sess, speakers))
		}
	})

	ret.push(_footer);

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
  	, session_html: show_sessions(sessions, speakers)
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