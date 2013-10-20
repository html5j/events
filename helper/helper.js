var _ = require('underscore')

// Helper functions
var Helper = {}

Helper.show_sponsorlogos = function(type, arr0, arr1, shuffle_flag) {
	var template = [
		'<ul class="list-unstyled list-inline">',
		'<% _.each(list, function(item) { %>',
			'<li><a class="thumbnail sponsor" data-sponsorid="<%= item.id %>" target="_blank" href="<%= item.href %>">',
			'<img width="<%= width %>" height="<%= height %>" src="<%= item.img_url %>" alt="<%= item.alt %>">',
			'</a>',
		'<% }); %>',
		'</ul>'
	].join("\n")

	var compiled = _.template(template)
	var width, height
	var list = _.union(arr0, arr1)

	if(shuffle_flag) {
		list = _.shuffle(list)
	}

	switch(type) {
		case "organizer": 
		case "main": 
			width = 250; height = 250;
			break;
		case "platinum":
			width = 200; height = 200;
			break;
		case "gold":
			width = 150; height = 150;
			break;
		default:
			width = 120; height = 120;
			break;
	}

	return compiled({list: list, width: width, height: height})
}

Helper.show_profiles = function(obj){
	var obj_ = {};

	_.each(obj, function(o){
		var desc = o.description;
		o.description = desc
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/@@@/g, "</p><p>")
			.replace(/\$\$\$/g, "<br/>")
			.replace(/(https?:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)/g, "<a href='$1' target='_blank'>$1</a>")
			.replace(/@it/g, "@%it")
			.replace(/@([0-9a-zA-Z_-]+)/g, "<a href='https://twitter.com/$1' target='_blank'>@$1</a>")
			.replace(/@%it/g, "@it")
	})


	var template = [
		'<% _.each( _.pairs(obj), function(item) { %>',
			'<% var speaker_id = item[0], speaker = item[1]; %>',
			'<section class="speaker">', 
		    '<h2 id="<%= speaker_id %>"><a href="<%= speaker.url %>"><%= speaker.name %></a></h2>',
		    '<p class="affiliation"><%= speaker.affiliation %></p>',
		    '<p class="image"><img width="100" src="<%= speaker.img_url %>" alt="<%= speaker.name %>"></p>',
		    '<div class="description"><%= speaker.description %></div>',
		  	'</section>',
		 '<% }); %>'
  	].join("\n");

  	var compiled = _.template(template);

  	return compiled(obj);
}

Helper.show_sessions = function(sessions, speakers) {
	_.each(sessions, function(row){
		_.each(row.sessions, function(session){
			session.description = session.description.replace(/\$\$\$/g, "<br>")
			console.log(session)
		});
	});
	var template = [
		'<div class="table-responsive">',
	    '<table class="table table-">',
	    '<thead>',
	    '  <tr>',
	    '    <th scope="col">時間',
	    '    <th scope="col">ルーム<br>(1F)<br>定員：360',
	    '    <th scope="col">ルーム<br>(2F)<br>定員：300',
	    '    <th scope="col">ルーム<br>(5F)<br>定員：120',
	    '    <th scope="col">ルーム<br>(5F)<br>定員：120',
	    '    <th scope="col">ルーム<br>(5F)<br>定員：360',
	    '    <th scope="col">ルーム<br>(6F)<br>定員：240',
	    '</thead>',

	    '<% _.each(sessions, function(item){ %>',
	    '<% if(item.type === "break") { %>',

	    	'<tr class="break active">',
        	'<th class="time" scope="row"><%= item.time %></th>',
        	'<td colspan="6"><%= item.text %></td>',
        	'</tr>',

	    '<% } else { %>',
		
			'<tr>',
	        '<th class="time" scope="row"><%= item.time %></th>',

	        '<% _.each(item.sessions, function(session) { %>',

	        	'<td class="session">',
	        	'  <h4 class="sesssion-title"><a href=""><%= session.title %></a></h4>',
	        	' <p class="session-speaker">',

	        	'<% _.each(session.speakers, function(id) { %>',
	        		'<% if(Speakers[id]) { %>',

	        	'    <span class="name"><%= Speakers[id].name %></span><br>',
	        	'    <span class="affiliation"><%= Speakers[id].affiliation %></span>',
	        		'<% } else { %>',
	        		'<span>調整中</span>',
	        		'<% } %>',

	        	'<% }); %>',

		        '  </p>',
		        '  <div class="session-desc">',
		        '    <p><%= session.description %></p>',
		        '  </div>',
		        '  <div class="materials">',
		        '    <p><!--<span class="button">講演資料</span><span class="button">講演映像</span>--></p>',
		        '  </div>',
		        '  <hr>',
		        '  <div class="toolbox">',
		        '    <p><a class="btn btn-default btn-xs session" data-sessionid="<%= session.id %>">',
		        '	  詳細を見る',
		        '	 </a></p>',
		        '  </div>',
		        '</td>',
		    '<% }); %>',
			'</tr>',

		'<% } %>',
	    '<% }); %>',

		'</table>',
		'</div>',
	].join("\n")
	var compiled = _.template(template)

	return compiled({sessions: sessions, Speakers: speakers})
}

module.exports = Helper;