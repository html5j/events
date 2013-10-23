var _ = require('underscore')

// Helper functions
var Helper = {}

Helper.show_sponsorlogos = function(type, arr0, arr1, shuffle_flag) {
    var template = [
        '<ul class="list-unstyled list-inline">',
        '<% _.each(list, function(item) { %>',
            '<li><a class="thumbnail sponsor" id="sp-<%= item.id %>" data-sponsorid="<%= item.id %>" target="_blank" href="<%= item.href %>">',
            '<img width="<%= width %>" height="<%= height %>" src="/conference/2013/11/<%= item.img_url %>" alt="<%= item.alt %>">',
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

Helper.show_profile = function(obj){
    var obj_ = _.clone(obj);
    var desc = obj_.description;
    obj_.description = desc
        .replace(/@@@/g, "<p>")
        .replace(/\$\$\$/g, "<br>")


    var template = [
            '<div class="speaker">', 
            '<% if (obj.affiliation) { %><p class="affiliation"><%= obj.affiliation %><% } %>',
            '<% if (obj.img_url) { %><p class="image"><img width="100" src="/conference/2013/11/<%= obj.img_url %>" alt=""><% } %>',
            '<div class="description"><%= obj.description %></div>',
            '</div>',
    ].join("\n");

    var compiled = _.template(template);

    return compiled(obj_);
}

Helper.show_profiles = function(obj){
    var obj_ = _.clone(obj);

    _.each(obj_, function(o){
        var desc = o.description;
        o.description = desc
            .replace(/@@@/g, "<p>")
            .replace(/\$\$\$/g, "<br>")
            // .replace(/(https?:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)/g, "<a href='$1' target='_blank'>$1</a>")
            // .replace(/@it/g, "@%it")
            // .replace(/@([0-9a-zA-Z_-]+)/g, "<a href='https://twitter.com/$1' target='_blank'>@$1</a>")
            // .replace(/@%it/g, "@it")
    })


    var template = [
        '<% _.each( _.pairs(obj), function(item) { %>',
            '<% var speaker_id = item[0], speaker = item[1]; %>',
            '<section class="speaker" id="<%= speaker_id %>">', 
            '<h2><a href="./speaker/<%= speaker_id %>"><%= speaker.name %></a></h2>',
            // '<h2 id="<%= speaker_id %>"><a href="<%= speaker.url %>"><%= speaker.name %></a></h2>',
            '<% if (speaker.affiliation) { %><p class="affiliation"><%= speaker.affiliation %><% } %>',
            '<% if (speaker.img_url) { %><p class="image"><img width="100" src="/conference/2013/11/<%= speaker.img_url %>" alt=""><% } %>',
            '<div class="description"><%= speaker.description %></div>',
            '</section><hr>',
         '<% }); %>'
    ].join("\n");

    var compiled = _.template(template);

    return compiled(obj_);
}

Helper.show_sessions = function(sessions, speakers) {
    _.each(sessions, function(row){
        _.each(row.sessions, function(session){
            session.long = session.description.replace(/\$\$\$/g, "<br>")
            session.short = session.long.length > 45 ? session.long.substr(0, 45) + "...." : session.long;
        });
    });
    var template = [
        '<div class="table-responsive">',
        '<table class="table">',
        '<thead>',
        '  <tr>',
        '    <th scope="col">時間',
        '    <th scope="col">ルーム1A<br>(1F)',
        '    <th scope="col">ルーム2A<br>(2F)',
        '    <th scope="col">ルーム5A<br>(5F)',
        '    <th scope="col">ルーム5B<br>(5F)',
        '    <th scope="col">ルーム5C<br>(5F)',
        '    <th scope="col">ルーム6A<br>(6F)',
        '</thead>',

        '<% _.each(sessions, function(item) { %>',
        '<% if (item.type === "break") { %>',

            '<tr class="break active">',
            '<th class="time" scope="row"><%= item.time %></th>',
            '<td colspan="6"><%= item.text %></td>',

        '<% } else { %>',
        
            '<tr>',
            '<th class="time" scope="row"><%= item.time %></th>',

            '<% _.each(item.sessions, function(session) { %>',

                '<td class="session">',
                '  <h4 class="sesssion-title"><%= session.title %></h4>',
                '  <p class="session-speaker">',

                '<% var flag = false; %>',
                '<% _.each(session.speakers, function(id) { %>',
                    '<% if(flag) { %><br><% } %>',
                    '<% if(Speakers[id]) { %>',

                '    <a href="./speaker/<%= id %>">',
                '    <% if(Speakers[id].img_url) { %><img width="28" height="28" alt="" src="/conference/2013/11/<%= Speakers[id].img_url %>"><% } %>',
                '    <span class="name"><%= Speakers[id].name %></span>',
                '    </a>',

                '   <% if(Speakers[id].affiliation) { %><br><span class="affiliation"><%= Speakers[id].affiliation %></span><% } %>',
                    '<% } else { %>',
                    '<span>調整中</span>',
                    '<% } %>',
                    '<% flag = true; %>',

                '<% }); %>',

                '  <div class="session-desc">',
                '    <p><%= session.short %>',
                '    <p><a id="s<%= session.id %>" class="btn btn-default btn-xs session show-detail" data-sessionid="<%= session.id %>" data-description="<%= session.long %>" data-title="<%= session.title %>">詳細を見る</a>',
                '  </div>',
                // '  <hr>',
                // '  <div class="materials">',
                // '    <p><!--<span class="button">講演資料</span><span class="button">講演映像</span>--></p>',
                // '  </div>',
                '</td>',
            '<% }); %>',

        '<% } %>',
        '<% }); %>',

        '</table>',
        '</div>',
    ].join("\n")
    var compiled = _.template(template)

    return compiled({sessions: sessions, Speakers: speakers})
}


Helper.show_sessions_v = function(sessions, speakers) {

var rooms_ = [
  'ルーム1A (1F) ',
  'ルーム2A (2F) ',
  'ルーム5A (5F) ',
  'ルーム5B (5F) ',
  'ルーム5C (5F) ',
  'ルーム6A (6F) '
];
    _.each(sessions, function(row){
        _.each(row.sessions, function(session){
            session.desc = session.description.replace(/\$\$\$/g, "<br>")
        });
    });
    var template = [
        '<div class="sessions">',
        // '<table class="table">',
        // '<thead>',
        // '  <tr>',
        // '    <th scope="col">時間',
        // '    <th scope="col">ルーム1A<br>(1F)',
        // '    <th scope="col">ルーム2A<br>(2F)',
        // '    <th scope="col">ルーム5A<br>(5F)',
        // '    <th scope="col">ルーム5B<br>(5F)',
        // '    <th scope="col">ルーム5C<br>(5F)',
        // '    <th scope="col">ルーム6A<br>(6F)',
        // '</thead>',

        '<% _.each(sessions, function(item) { %>',
        '<% if (item.type === "break") { %>',

            '<div class="panel panel-default">',
                '<div class="panel-heading">',
                    '<%= item.time %>',
                '</div>',
                '<div class="panel-body break">',
                    '<%= item.text %>',
                '</div>',
            '</div>',

        '<% } else { %>',

            '<div class="panel panel-default">',
                '<div class="panel-heading">',
                    '<%= item.time %>',
                '</div>',
        
                '<div class="panel-body session">',
                '<ul class="list-group">',

                '<% var c = 0; %>',
                '<% _.each(item.sessions, function(session) { %>',
                    '<li class="list-group-item">',
                    '<p class="room"><span class="label label-default"><%= rooms[c] %></span></p>',

                    '<h4 class="sesssion-title" id="s<%= session.id %>"><%= session.title %></h4>',
                    '<p class="session-speaker">',

                    '<% var flag = false; %>',
                    '<% _.each(session.speakers, function(id) { %>',
                        '<% if(flag) { %><br><% } %>', 
                        '<% if(Speakers[id]) { %>',
                            '<a href="./speaker/<%= id %>">', 
                            '<% if(Speakers[id].img_url) { %><img width="96" alt="<%= Speakers[id].name %>" src="/conference/2013/11/<%= Speakers[id].img_url %>"><% } %>', 
                            '<span class="name"><%= Speakers[id].name %></span>', '    </a>', 
                            '<% if(Speakers[id].affiliation) { %><br><span class="affiliation"><%= Speakers[id].affiliation %></span><% } %>', 
                        '<% } else { %>',
                            '<span>調整中</span>',
                        '<% } %>',
                    '<% flag = true; %>',

                    '<% }); %>',

                    '<div class="session-desc">',
                        '<p><%= session.desc %>',
                    '</div>',
                // '  <hr>',
                // '  <div class="materials">',
                // '    <p><!--<span class="button">講演資料</span><span class="button">講演映像</span>--></p>',
                // '  </div>',
                    '</li>',
                    '<% c++; %>',
                '<% }); %>',
                '</ul>',
                '</div>',
            '</div>',
        '<% } %>',
        '<% }); %>',

        '</div>',
    ].join("\n")
    var compiled = _.template(template)

    return compiled({sessions: sessions, Speakers: speakers, rooms: rooms_})
}

module.exports = Helper;