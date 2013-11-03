var LifeList = function (options) {
	var goalsElementsByPk = {};
	var goalTemplateContent = null;
	var self = this;
	var renderGoalIndex = 0;

	var renderGoal = function (goal) {
		renderGoalIndex++

		var goalElement = $.tmpl(goalTemplateContent, $.extend({
			editable: options.editable
		}, goal, {index: renderGoalIndex}));

		goalElement.find(".short-info, .image").click(function () {
			options.container.children(".goal").removeClass("selected");
			options.container.children(".goal").find(".full-info").hide();
			options.container.children(".goal").find(".counters").hide();

			goalElement.addClass("selected");
			goalElement.find(".full-info").show();
			goalElement.find(".counters").show();

			goalElement.removeClass("clickable");

			return false;
		});

		attachGoalCountersListeners(goalElement.find(".counters"), goal);

		if (options.editable) {
			goalElement.find(".done-link").click(function () {
				options.formsContainers.done.load(options.urls.done.replace(":goal_pk", goal.pk), function () {
					$(this).topPopup("show");
				});
				return false;
			});
			goalElement.find(".edit-link").click(function () {
				options.formsContainers.edit.ajaxForm(options.urls.edit.replace(":goal_pk", goal.pk), function (newGoal) {
					self.edit(newGoal);

					options.formsContainers.edit.topPopup("hide");
				}, function () {
					options.formsContainers.edit.topPopup("show");
				});
				return false;
			});
			goalElement.find(".delete-link").click(function () {
				if (confirm("Are you sure?")) {
					request(options.urls.delete.replace(":goal_pk", goal.pk), function () {
						self.delete(goal.pk);
					});
				}
				return false;
			});
		}

		renderGoalComments(goalElement.find(".comments"), goal.pk, goal.fields.comments);

		goalElement.addClass("clickable");

		return goalElement;
	};

	this.add = function (goal) {
		goalsElementsByPk[goal.pk] = renderGoal(goal);
		goalsElementsByPk[goal.pk].appendTo(options.container);
	};

	this.edit = function (newGoal) {
		var goalElement = renderGoal(newGoal);
		goalsElementsByPk[newGoal.pk].replaceWith(goalElement);
		goalsElementsByPk[newGoal.pk] = goalElement;
	};

	this.delete = function (goalPk) {
		goalsElementsByPk[goalPk].remove();
	};

	this.isEditable = function () {
		return options.editable;
	};

	if (options.editable) {
		options.container.append('<div class="actions"><ul><li><a href="#" class="add-link">Add</a></li></ul></div>');
		$('h3', options.container).after(
            '<div class="filters">' +
                '<ul>' +
                    '<li><a href="#" id="ll-all-link" class="lifelist-link">All</a></li>' +
                    '<li><span class="lifelist-link">|<span></li>' +
                    '<li><a href="#" id="ll-done-link" class="lifelist-link">Done</a></li>' +
                '</ul>' +
            '</div>');

		options.formsContainers.add.ajaxForm(options.urls.add, function (newGoal) {
			self.add(newGoal);

			options.formsContainers.add.topPopup("hide");
		}, function () {
			options.container.find(".add-link").click(function () {
				options.formsContainers.add.topPopup("show");
				return false;
			});
		});
	}

	options.container.append(
        '<h3>My LifeList</h3>' +
        '<div class="filters">' +
            '<ul>' +
                '<li><a href="javascript:void(0);" id="ll-all-link" class="lifelist-link">All</a></li>' +
                '<li><span class="lifelist-link">|<span></li>' +
                '<li><a href="javascript:void(0);" id="ll-done-link" class="lifelist-link">Done</a></li>' +
            '</ul>' +
        '</div>'
    );

    $('#ll-all-link').click(function () {
        $('.goal', options.container).show();
        options.content.get(0).dispatchEvent(renderMasonryEvent);
    });

    $('#ll-done-link').click(function () {
        $('.goal', options.container).hide()
        $('.goal.done', options.container).show();
        options.content.get(0).dispatchEvent(renderMasonryEvent);
    });

	$.get(options.goalTemplateURL, function (response) {
		goalTemplateContent = response;

		request(options.urls.getList, function (goals) {
			for (var i = 0;  i < goals.length; ++i) {
				self.add(goals[i]);
			}
		});
	});
};
