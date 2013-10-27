function attachGoalCountersListeners(element, goal) {
    var relist = element.find(".relist"),
        relistPopup = $('.count-popup', relist);
	if (goal.fields.user.pk != window.REQUEST_USER_PK) {
        relist.click(function () {
			var self = $(this);

			$(".relist-goal-form").ajaxForm("/goals/relist/" + goal.pk + "/", function (relistsCount) {
				self.find("span").html(relistsCount);

				$(".relist-goal-form").topPopup("hide");

				message("success", "The goal was added to your lifelist.");
			}, function () {
				$(".relist-goal-form").topPopup("show");
			});

			return false;
		});
		relist.addClass("clickable");
	}
    $('span', relist).hover(function () {
        relistPopup.show();
    }, function () {
        relistPopup.hide();
    });

    var like = element.find(".like"),
        likePopup = $('.count-popup', like);
    like.click(function () {
		var self = $(this);

		request("/goals/like/" + goal.pk + "/", function (likesCount) {
			self.find("span").html(likesCount);
		});

		return false;
	});
	like.addClass("clickable");
    $('span', like).hover(function () {
        likePopup.show();
    }, function () {
        likePopup.hide();
    });

    var comment = element.find(".comment");
    comment.click(function () {
        var goalForm = element.parent('.goal-card');
        var addCommentForm = goalForm.find('.add-comment-form');
        if (addCommentForm.is(':visible')) {
            addCommentForm.hide();
        } else {
            $('.goal-card .add-comment-form').hide();
            addCommentForm.show();
            addCommentForm.find('textarea').focus();
        }
    });
    comment.addClass("clickable");
}
