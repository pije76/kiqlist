function deleteStatus(statusPk, container) {
    $('#status' + statusPk).remove();
    container.get(0).dispatchEvent(renderMasonryEvent);
};

function renderStatus(status, options) {
    var editable = status.fields.user.pk === options.userPk;
    status.fields = $.extend({editable: editable}, status.fields);

    var statusElement = $.tmpl(options.template, status);

    if (editable) {
        statusElement.hover(function () {
            $(this).find(".delete").show().animate({ opacity: 1 }, 100);
        }, function () {
            $(this).find(".delete").animate({ opacity: 0 }, 100, function () {
                $(this).hide();
            });
        });

        statusElement.find(".delete").click(function () {
            request("/statuses/delete/" + status.pk + "/", function () {
                deleteStatus(status.pk, options.container);
            });

            return false;
        });
    }

    if (options.after) {
        $(statusElement).insertAfter(options.after);
    } else {
        options.container.append(statusElement);
    }
}

function addStatus(status, options) {
    renderStatus(status, options);
    options.container.masonry('reload');
}
