$(function() {
    $('.sponsor-list').each(function() {
        var listItems = $(this).children('li').detach();
        var tmp = [];
        listItems.each(function() {
            tmp.push(this);
        });
        tmp.sort(function() {
            return Math.round(Math.random()) - 0.5;
        });
        for (var i = 0, len = tmp.length; i < len; i++) {
            $(this).append(tmp[i]);
        }
    }).css('display', 'block');
});

$(window).load(function(){
  var t = $("section#top-slide")
    , imgs = t.data("imgs").split(",")
    , folder = t.data("folder")
    , c = 0;

  var show_ = function(i){
    t.html("<figure><img class='shadow' src='"+folder+imgs[i]+"'></figure>").hide().fadeIn();
  }
  setInterval(function(){
    c = (c + 1) % imgs.length;
    t.find("img").fadeOut(function(){
      show_(c);
    })
  }, 7500);
  show_(c);
});
