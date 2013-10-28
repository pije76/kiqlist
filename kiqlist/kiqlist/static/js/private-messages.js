$(function () {
	var privateMessagesDiv = $('<div class="private-messages">');
	var onLoad = function () {
		var conversationDiv = privateMessagesDiv.find(".conversation");
		if (conversationDiv.length) {
			conversationDiv.scrollTop(conversationDiv[0].scrollHeight);
		}

		var startConversationFormDiv = privateMessagesDiv.find(".start-conversation-form");
		if (startConversationFormDiv.length) {
			startConversationFormDiv.ajaxForm("/pm/start_conversation/", function (user) {
				privateMessagesDiv.load("/pm/conversation/" + user.pk + "/", function () {
					onLoad();
				});
			});
		}

		privateMessagesDiv.find("a").click(function () {
			privateMessagesDiv.load($(this).attr("href"), function () {
				onLoad();
			});

			return false;
		});

		privateMessagesDiv.find("form").submit(function () {
		   $.ajax({
				url: $(this).attr("action"),
				type: "post",
				data: $(this).serialize(),
				success: function (response) {
					privateMessagesDiv.html(response);
					onLoad();
				}
			});
			return false;
		})
	};

	privateMessagesDiv.load("/pm/index/", function () {
		$(this).appendTo("body");
		onLoad();
	});

	$(".private-messages-link").click(function () {
		$(privateMessagesDiv).topPopup("show");

		return false;
	});

	function autoRefresh() {
		var addForm = privateMessagesDiv.find(".add-private-message-form");

		if (addForm.length) {
			$.get("/pm/conversation/" + addForm.find("*[name=to_user]").val() + "/", function (response) {
				var contentInput = addForm.find("*[name=content]");
				var content = contentInput.val();
				privateMessagesDiv.html(response);
				privateMessagesDiv.find(".add-private-message-form").find("*[name=content]").focus();
				privateMessagesDiv.find(".add-private-message-form").find("*[name=content]").val(content);
				onLoad();
			});
		}
	}

	setInterval(autoRefresh, 10000);

	route([
		{
			hash: /^#pm\/conversation\/(\d+)$/,
			action: function (userPk) {
				privateMessagesDiv.load("/pm/conversation/" + userPk + "/", function () {
					$(privateMessagesDiv).topPopup("show", {
						callback: function () {
							onLoad();
						}
					});
				});
			}
		}
	]);
});