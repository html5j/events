var Sequelize = require('sequelize');

var inquiryDB = function(date) {
  this.sequelize = new Sequelize('sqlite://localhost/', {
    storage: __dirname + '/' + date + '.sqlite'
  });

  this.setTable();
}

inquiryDB.prototype.setTable = function(){
  this.Profile = this.sequelize.define('Profile', {
    'id': { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
    'uuid': { type: Sequelize.STRING, allowNull: false},
    'business': { type: Sequelize.STRING, allowNull: false},
    'occupation': { type: Sequelize.STRING, allowNull: false},
    'how_to_know': { type: Sequelize.STRING, allowNull: false},
    'how_often': { type: Sequelize.STRING, allowNull: false},
    'sex': { type: Sequelize.STRING, allowNull: false},
    'generation': { type: Sequelize.STRING, allowNull: false}
  });

  this.Session = this.sequelize.define('Session', {
    'id': { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
    'room': { type: Sequelize.STRING, allowNull: false},
    'title': { type: Sequelize.STRING, allowNull: false},
    'impression': { type: Sequelize.STRING, allowNull: false},
    'freetext': { type: Sequelize.STRING, allowNull: true},
    'uuid': { type: Sequelize.STRING, allowNull: false}
  });


  this.sequelize.sync();
}

inquiryDB.prototype.setProfile = function(obj, cb) {
  this.Profile.create({
    uuid: obj.uuid,
    business: obj.business,
    occupation: obj.occupation,
    how_to_know: obj.how_to_know,
    how_often: obj.how_often,
    sex: obj.sex,
    generation: obj.generation
  }).then(cb);
}

inquiryDB.prototype.setSession = function(obj, cb) {
  this.Profile.create({
    room: obj.room,
    title: obj.title,
    impression: obj.impression,
    freetext: obj.freetext,
    uuid: obj.uuid
  }).then(cb);
}

module.exports = inquiryDB;




// test
// var db = new inquiryDB('20150125');
// db.setProfile({uuid: "hoge"});
