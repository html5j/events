(function() {
  'use strict';

  var $handler = $('.js-draw-handler'),
      $drawer = $('.js-drawer');

  $handler.on('click', function() {
    $drawer.toggleClass('is-open');
  });

  function randomOrder(selector) {
    if ($(selector).length === 0) {
      return;
    }
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
  randomOrder('.thumb-list.platinum');
  randomOrder('.thumb-list.gold');
  randomOrder('.thumb-list.silver');
  randomOrder('.thumb-list.bronze');
  randomOrder('.thumb-list.support');
  randomOrder('.thumb-list.media');
})();
