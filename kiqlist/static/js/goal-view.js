$(function () {
	route([{
		hash: /^#goal\/(\d+)\/view$/,
		action: function (goalPk) {
			backgroundOverlay("enable");

			$("#goal-view").load("/goals/view/" + goalPk + "/", function() {
				var self = this;

				$(this).find(".images .next a").click(function() {
					$(self).find(".images .current.image").next().click();
					return false;
				});

				$(this).find(".images .prev a").click(function() {
					$(self).find(".images .current.image").prev().click();
					return false;
				});

				$(this).find(".images .image").click(function() {
					if (!$(this).next().hasClass("image")) {
						$(self).find(".images .next img").hide();
					} else {
						$(self).find(".images .next img").show();
					}

					if (!$(this).prev().hasClass("image")) {
						$(self).find(".images .prev img").hide();
					} else {
						$(self).find(".images .prev img").show();
					}

					$(self).find(".images .image").removeClass("current");
					$(this).addClass("current");
					$(this).children("img").css({ marginTop: - $(this).children("img").innerHeight() / 2 });
				});

				renderGoalComments($(this).find(".comments"), goalPk);

				$(this).find(".images .image:first").click();
				$(this).show();

				backgroundOverlay("bind", {
					event: "click",
					callback: function() {
						$("#goal-view").hide();
						window.location.hash = "";
					}
				});

				KeyboardJS.on("right", function() {
					$(self).find(".images .next a").click();
				});

				KeyboardJS.on("left", function() {
					$(self).find(".images .prev a").click();
				});

				$(".goal-links .report span").on("click", function(e) {
					if (confirm("Report this goal? Abuse of this feature will be punished.")) {
						$(this).text("Reported! Thanks.").addClass("reported").off("click")
						var url = $(this).data("url")
						console.log(url)
					}
				})

				gapi.plus.go();
			});

		}
	}]);
});
