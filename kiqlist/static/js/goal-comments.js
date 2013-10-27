var goalCommentTemplateContent = null;
var renderGoalComment = function (goalComment) {
	return $.tmpl(goalCommentTemplateContent, goalComment.fields);
};

$.get("/js_templates/goal_comment.html", function (response) {
	goalCommentTemplateContent = response;
});

function renderGoalComments(container, goalPk, comments) {
    var addCommentForm = container.find(".add-comment-form");
    if (comments) {
		for (var j = 0; j < comments.length; ++j) {
			addCommentForm.before(renderGoalComment(comments[j]));
		}
	}

	if (window.IS_AUTHORIZED) {
		addCommentForm.ajaxForm("/goals/add_comment/" + goalPk + "/", function (goalComment) {
			addCommentForm.before(renderGoalComment(goalComment));
            addCommentForm.hide();
            addCommentForm.get(0).dispatchEvent(renderMasonryEvent);
		});
	}
}
