// set EvertHandler for Modal Window
// (Session Detail will be shown)
///////////////////////////////////////////

$("td.session a.show-detail").on("click", function(e){
	var description = $(this).data("description")
		, title = $(this).data("title")
		, session_id = $(this).data("sessionid")

	var parent = $(this).parents("td.session")
		, speaker_html = parent.find(".session-speaker").html();

	speaker_html = speaker_html.replace(/28/g, "96")

	$("#session-modal .modal-title").text(title);
	$("#session-modal .modal-body").html(speaker_html)
		.append($("<div class='panel panel-default'>")
			.append($("<div class='panel-body'>").html(description)));

	$("#session-modal").modal('show')
})