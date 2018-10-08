(function() {
  'use strict';

  var $handler = $('.js-draw-handler'),
      $drawer = $('.js-drawer');

  $handler.on('click', function() {
    $drawer.toggleClass('is-open');
  });
})();
