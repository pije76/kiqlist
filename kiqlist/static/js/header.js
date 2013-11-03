$(function() {
	$("header li.user-link").not(".not-authorized").hover(function () {
		$("#user-dropdown").show();
	}, function(event) {
		if ($(event.toElement).attr("id") != "user-dropdown" && $(event.toElement).closest("#user-dropdown").length == 0)
			$("#user-dropdown").hide();
	});

	$("#user-dropdown").mouseleave(function (event) {
		$(this).hide();
	});
});

$(function() {
	$("header li.about-link").not(".not-authorized").hover(function () {
		$("#about-dropdown").show();
	}, function(event) {
		if ($(event.toElement).attr("id") != "about-dropdown" && $(event.toElement).closest("#about-dropdown").length == 0)
			$("#about-dropdown").hide();
	});

	$("#about-dropdown").mouseleave(function (event) {
		$(this).hide();
	});
});
