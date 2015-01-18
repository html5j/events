/**
 * /inquiry/script.js
 *
 */

$(".inquiry-components").hide();

$("#profile").show()
  .find("form").on("click", function(ev) {
    ev.preventDefault();
    $(".inquiry-components").hide();
    $("#session-selection").show();
});

$("#session-selection").find("form")
  .on("submit", function(ev) {
    ev.preventDefault();
    var id = $(this).find("select option:selected").val();
    console.log(id);
    $(".inquiry-components").hide();
    $("#"+id).show();
  });


