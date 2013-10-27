var doneGoalTemplateContent = null;

$.get("/js_templates/done_goal.html", function (response) {
	doneGoalTemplateContent = response;
});

function loadGoals(url, container, justDone) {
	request(url, function (goals) {
        $.tmpl(doneGoalTemplateContent, goals).appendTo(container);

        for (var i = 0; i < goals.length; ++i) {
            var gCard = $(container.find(".goal-card").get(i));
            addGoalFormListeners(goals[i], gCard);
            renderGoalComments(gCard, goals[i].pk, goals[i].fields.comments);
        }

        var containerElement = container.get(0);
        containerElement.removeEventListener('kiqlistRenderMasonry', renderMasonryHandler, false);
        containerElement.addEventListener('kiqlistRenderMasonry', renderMasonryHandler, false);
        containerElement.dispatchEvent(renderMasonryEvent);
	});
}


function loadMostPopularDoneGoals(container) {
	loadGoals("/goals/done/list/", container, true);
}

function addGoalFormListeners(goal, goalCard) {
    if (window.IS_AUTHORIZED) {
        var counters = $(".counters", goalCard);

        goalCard.hover(function () {
            counters.show();
        }, function () {
            counters.hide();
        });

        attachGoalCountersListeners(goalCard.find(".counters"), goal);
    }

    goalCard.find(".images img").click(function () {
        window.location.href = "#goal/" + goal.pk + "/view";
    });
}

function renderGoal(goal, options) {
    var goalCard;
    $.tmpl(options.template, goal).appendTo(options.container);

    goalCard = $('#goal' + goal.pk);
    addGoalFormListeners(goal, goalCard);
    renderGoalComments(goalCard, goal.pk, goal.fields.comments);
}
