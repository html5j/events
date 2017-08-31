;( function ( $ ) {
  'use strict';

  $( function () {
    var $el = $( '.conf2017s-pageNav' );
    var $list   = $el.find( 'ul' );
    var $opener = $el.find( '.conf2017s-pageNav__opener' );
    var modifier = 'conf2017s-pageNav--open';

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
  if ($('.conf2017s-inlineList').length !== 0) {
    randomOrder('.conf2017s-inlineList.platinum');
    randomOrder('.conf2017s-inlineList.gold');
    randomOrder('.conf2017s-inlineList.silver');
    randomOrder('.conf2017s-inlineList.bronze');
    randomOrder('.conf2017s-inlineList.support');
    randomOrder('.conf2017s-inlineList.media');
  }

} )( jQuery )
