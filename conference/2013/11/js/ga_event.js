$(function(){

$("a.sponsor").on("click",function(){

    var el = $(this);
    var id = el.attr("data-sponsorid") || "none";
    var url = el.attr("href") || "";

        // hostnameだけセットする。
        var hostname = url.match(/^http:\/\/([^/]+)/)[1] || "unknown";

    _gaq.push(["_trackEvent", "sponsor", "view", hostname + " / " + id]);

});
$(".btn.session").on("click",function(){

    var el = $(this);
    var id = el.attr("id") || "unknown";

    _gaq.push(["_trackEvent", "session", "check", id]);

});

$("a.contact").on("click",function(){

    var el = $(this);
    var type = el.attr("data-contact-type") || "unknown";

    _gaq.push(["_trackEvent", "contact",type ]);

});

});