;( function ( $ ) {
  'use strict';

  $( function () {
    var $el = $( '.conf2018s-pageNav' );
    var $list   = $el.find( 'ul' );
    var $opener = $el.find( '.conf2018s-pageNav__opener' );
    var modifier = 'conf2018s-pageNav--open';

    $opener.on( 'click', function () {
      $.when(
        $list.slideToggle( 200 )
      ).done( function () {
        if ( $list.is( ':visible') ) {
          $el.addClass( modifier );
        } else {
          $el.removeClass( modifier );
        }
        $list.removeAttr( 'style' );
      } );
    } );
  } );

  function randomOrder(selector) {
    var arr = [];
    $(`${selector} li`).each(function() {
      arr.push($(this));
    });
    arr.sort(function() {
      return Math.random() - Math.random();
    });
    $(selector).empty();
    arr.forEach(function(item) {
      $(selector).append(item);
    });
  }
  if ($('.conf2018s-inlineList').length !== 0) {
    randomOrder('.conf2018s-inlineList.platinum');
    randomOrder('.conf2018s-inlineList.gold');
    randomOrder('.conf2018s-inlineList.silver');
    randomOrder('.conf2018s-inlineList.bronze');
    randomOrder('.conf2018s-inlineList.support');
    randomOrder('.conf2018s-inlineList.media');
  }

} )( jQuery )
