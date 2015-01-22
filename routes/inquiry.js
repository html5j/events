
/*
 * inquiry page.
 */

var fs = require('fs');

var inqObj = {};
inqObj['20150125'] = JSON.parse(fs.readFileSync("./model/inquiry/20150125.json", "utf8"));


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
