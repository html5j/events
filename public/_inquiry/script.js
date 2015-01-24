/**
 * /inquiry/script.js
 *
 */


///////////////////////////////////////////////////////
// event handler for form

// send inquiry result for profile
$("#profile form").on("submit", function(ev) {
    ev.preventDefault();
    $.ajax({
      "url": location.pathname + "profile",
      "type": "POST",
      "data": {
        "uuid": getUUID(),
        "business": $(this).find("input[name=business_category]").val(),
        "occupation": $(this).find("input[name=occupation_category]").val(),
        "how_to_know": $(this).find("input[name=how_to_know]").val(),
        "how_often": $(this).find("input[name=how_often]").val(),
        "sex": $(this).find("input[name=sex]").val(),
        "generation": $(this).find("input[name=generation]").val()
      },
      "success": function(res){
        location.hash = "#session-selection";
      }
    });
  });


// session selection (view change only)
$("#session-selection").find("form")
  .on("submit", function(ev) {
    ev.preventDefault();
    var id = $(this).find("select option:selected").val();
    location.hash = "#"+id;
  });

// send inquiry result for each session
  $("form.session-inquiry").on("submit", function(ev) {
    ev.preventDefault();
    $.ajax({
      "url": location.pathname + "session",
      "type": "POST",
      "data": {
        "uuid": getUUID(),
        "room": $(this).data("room"),
        "title": $(this).data("sessionname"),
        "impression": $(this).find("input[name=impression]").val(),
        "freetext": $(this).find("textarea[name=impression-text]").val()
      },
      "success": function(res){
        location.href = "./thx/";
      }
    });
  });


//////////////////////////////////////////////////
// utilities

var uuid = (function(){
  var S4 = function() {
    return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
  }   
  return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4() +S4());
})();

var getUUID = function() {
  var key = location.pathname + "/uuid";
  if(!localStorage.getItem( key )) {
    localStorage.setItem( key, uuid );
  }
  return localStorage.getItem( key )
}

var UUID = (function(){
  var key = location.pathname + "/uuid";
  return localStorage.getItem( key );
}());

var changeView = function(){
  // init view
  $(".inquiry-components").hide();

  var hash = location.hash;

  if(hash === "" || hash === "#") {
    $("#profile").show();
  } else {
    $(hash).show();
  }
}

window.onhashchange = changeView;

// init
(function(){
  if(UUID){
    // UUID 登録済み
    location.hash = "#session-selection";
  } else {
    // UUID 無し
    location.hash = "#";
  }
  changeView(location.hash);
}());
