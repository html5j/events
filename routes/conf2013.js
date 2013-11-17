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
    , title: "セッションテーブル | HTML5 Conference 2013"
    , speakers: speakers
    , session_html: helper.show_sessions(sessions, speakers)
  });
};

exports.sessions_v = function (req, res) {
  res.render("2013/sessions_v", {
    id: "sessions"
    , title: "セッションテーブル | HTML5 Conference 2013"
    , speakers: speakers
    , session_html: helper.show_sessions_v(sessions, speakers)
  });
};

exports.speakers = function (req, res) {
  res.render("2013/speakers", {
    id: "speakers"
    , title: "スピーカーのみなさん | HTML5 Conference 2013"
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

exports.volunteer = function (req, res) {
  res.render("2013/volunteer", {
    id: "volunteer"
    , title: "ボランティアスタッフ募集 | HTML5 Conference 2013"
  });
};

exports.offering = function (req, res) {
  res.render("2013/offering", {
    id: "offering"
    , title: "各種募集 | HTML5 Conference 2013"
  });
};

exports.faq = function (req, res) {
  res.render("2013/faq", {
    id: "faq"
    , title: "よくある質問・注意事項 | HTML5 Conference 2013"
  });
};

exports.booth = function (req, res) {
  res.render("2013/booth", {
    id: "booth"
    , title: "展示ブース | HTML5 Conference 2013"
  });
};

exports.speaker = function(req, res) {
  var speaker_id = req.params.speaker_id;

  res.render("2013/speaker", {
    id: "speaker",
    spaeker_id: speaker_id,
    speaker: speakers[speaker_id],
    show_profile: helper.show_profile,
    title: "スピーカー: "+ speakers[speaker_id].name + " | HTML5 Conference 2013"
  })
}

// json api
/////////////////////////////////////////////////////
exports.api = function(req, res){
  res.setHeader('Content-Type', 'application/json; charset=UTF-8');

  var model = req.params.model

  if(models.hasOwnProperty(model)) {
    res.end(JSON.stringify(models[model]));
  } else {
    res.send(404, "File not Found")
    res.end()
  }
}
