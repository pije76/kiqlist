$(function () {
	var notificationsTemplate = null;
    var seeMoreTemplate = null;
    var refreshTimer;

    function markAsRead(notification_pk) {
        request("/notifications/read/" + notification_pk + '/', function (){});
    }

    function markAsOld() {
        var pks = $('.new-notification').map(function () {
            return $(this).data('pk');
        }).get().join();

        if (pks.length > 0) {
            request('/notifications/mark_old?pks=' + pks, function () {
                $(".notifications-count").fadeOut(2000);
                $(".new-notification").switchClass("new-notification", "unread-notification", 2000);
            });
        }
    }

	function render(notifications, newCount) {
        var notificationsCount = $(".notifications-count"),
            notificationsList = $(".notifications-list ul"),
            newNotificationsRender = $.tmpl(notificationsTemplate, {notifications: notifications});

        if (!newCount) {
			notificationsCount.hide();

		}else {
			notificationsCount.show();
		}

        if (!notifications.length) {
            $('#see-more').hide();
            $('#no-notifications').show();
        } else {
            $('#see-more').show();
            $('#no-notifications').hide();
        }

		notificationsCount.html(newCount);
        $('.notifications-list ul li.notification').remove();
        notificationsList.prepend(newNotificationsRender);
        fadeNewNotifications();
	};

	function checkNew () {
		request("/notifications/new/", function (data) {
            render(data.notifications, data.count_new);

            $(".notifications-list .unread-notification").click(function () {
                var pk = $(this).data("pk");
                markAsRead(pk);
                return true;
            });
		});
	};

    function fadeNewNotifications() {
        if ($(".notifications-list").is(':visible')) {
            markAsOld();
        }
    }

	$.get("/js_templates/notifications.html", function (template) {
		notificationsTemplate = template;

		$(".notifications-link").click(function () {
            clearInterval(refreshTimer);
            refreshTimer = setInterval(checkNew, 5000);


			if ($(".notifications-list").is(':visible')) {
                $(".notifications-list").hide();
				return false;
            }

			$(".notifications-list").show();
            fadeNewNotifications();

            return false;
		});

        $.get("/js_templates/see_more_notifications.html", function (smTemplate) {
            seeMoreTemplate = smTemplate;

            $('#see-more').click(function () {
                request('/notifications/all/', function (allNotifications) {
                    $(".notifications-list").hide();
                    var seeMoreInfoPopup = $('.see-more-info');
                    seeMoreInfoPopup.html($.tmpl(seeMoreTemplate, {notifications: allNotifications}));
                    seeMoreInfoPopup.topPopup("show");
                });
                return false;
            });

            checkNew();
        });

		refreshTimer = setInterval(checkNew, 5000);
	});
});
