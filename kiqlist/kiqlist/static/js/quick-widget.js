$(function () {
	$("#quick-widget a").click(function () {
		$(".quick-widget-forms").topPopup("show");
        return false;
	});

	$(".quick-widget-forms .tabs .tab a").click(function () {
		$(this).parent().parent().children().removeClass("active");
		$(this).parent().addClass("active");
		$(".quick-widget-forms").find(".tab-content").hide();

		if ($(this).parent().hasClass("goal-tab")) {
			$(".quick-widget-forms").find(".add-goal-form").show();
		}

		if ($(this).parent().hasClass("status-tab")) {
			$(".quick-widget-forms").find(".add-status-form").show();
		}

		return false;
	});

	$(".quick-widget-forms").find(".add-goal-form").ajaxForm("/goals/add/", function (newGoal) {
		if (window.LIFELIST && window.LIFELIST.isEditable()) {
			window.LIFELIST.add(newGoal);
		}

		$(".quick-widget-forms").topPopup("hide");
	});

	$(".quick-widget-forms").find(".add-status-form").ajaxForm("/statuses/add/", function (newStatus) {
		if (window.STATUS_OPTS) {
			addStatus(newStatus, window.STATUS_OPTS);
		}

		$(".quick-widget-forms").topPopup("hide");
	});

	$(".quick-widget-forms .tabs .tab:first a").click();
});
