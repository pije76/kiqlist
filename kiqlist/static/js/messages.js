function message(tags, text) {
	var messageElement = $('#message-tmpl').tmpl({ tags: tags, text: text });

	messageElement.find('.close').click(function () {
		messageElement.remove();
		return false;
	});

	messageElement.animate({
		opacity: 0
	}, 10000, function () {
		$(this).remove();
	});

	messageElement.appendTo($('.messages'));
}
