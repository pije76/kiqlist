var element = null;

backgroundOverlay = function (action, options) {
    if (action == "enable") {
        if (element) return;

        element = $('<div id="background-overlay"/>');
        element.appendTo('body').show();
        element.click(function () {
            backgroundOverlay('disable');
        });
    }else if (action == "disable") {
        if (!element) return;

        element.remove();
        element = null;
    }else if (action == "bind") {
        if (!element) return;

        element.bind(options.event, options.callback);
    }
};
