$(function () {
	if ($(".following-activity").length) {
		$.get("/js_templates/following_activity.html", function (template) {
			request("/users/activity/following/", function (activity) {
				$(".following-activity").html($.tmpl(template, {activity: activity}));
			});
		});
	}
});
