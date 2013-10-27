$(function () {
	if ($(".search-by-tag-bar").length) {
		$(".search-by-tag-bar").ajaxForm("/tags/tag_form/", function (tag) {
			$(".search-by-tag-bar").hide();
			window.location = "/tags/search/" + tag;
		});
	}

	if ($(".top-tags").length) {
		$.get("/js_templates/top_tags.html", function (template) {
			request("/goals/top_tags/", function (topTags) {
				$(".top-tags").html($.tmpl(template, { topTags: topTags }));
			});
		});
	}
});
