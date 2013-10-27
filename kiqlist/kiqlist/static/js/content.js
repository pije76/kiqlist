var contentTemplates = null;

$.get("/js_templates/content_template.html", function (response) {
    contentTemplates = response;
});

function renderComponent(component, options) {
    switch (component.type) {
        case "goal":
            renderGoal(component, options);
            break;
        case "status":
            renderStatus(component, options);
            break;
    }
}

function extendOptions(options, container) {
    $.extend(options, {
        template: contentTemplates,
        container: container
    });
}

function loadContent(url, container, options) {
    request(url, function (data) {
        var i;
        extendOptions(options, container);
        window.STATUS_OPTS = options;

        for (i = 0; i < data.length; i++) {
            renderComponent(data[i], options);
        }

        container.get(0).addEventListener('kiqlistRenderMasonry', renderMasonryHandler, false);
        container.get(0).dispatchEvent(renderMasonryEvent);
    });
}