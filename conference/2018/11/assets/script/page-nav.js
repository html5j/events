(function() {
  'use strict';

  var $handler = $('.js-draw-handler'),
      $drawer = $('.js-drawer');

  $handler.on('click', function() {
    $drawer.toggleClass('is-open');
  });

  // ハッシュによるフォーカス
  var currentFocus;
  $(window).on('hashchange', function (ev) {
    focusByHash();
  });
  focusByHash();

  function focusByHash() {
    if (location.hash) {
      if (currentFocus) {
        currentFocus.classList.remove('focus');
      }
      var focus = $(location.hash);
      if (focus.length !== 0) {
        focus[0].classList.add('focus');
        currentFocus = focus[0];
      }
    }
  }

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
