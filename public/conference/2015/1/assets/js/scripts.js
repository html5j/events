

;( function ( $ ) {
  
  'use strict';

  $( function () {

    var $el = $( '.conf2015s-pageNav' );
    var $list   = $el.find( 'ul' );
    var $opener = $el.find( '.conf2015s-pageNav__opener' );
    var modifier = 'conf2015s-pageNav--open';

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


} )( jQuery )

"2.js";
