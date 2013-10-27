(function($) {

var TOP_POPUP_ELEMENT = null;
var TOP_POPUP_ON_ANIMATE = false;

var getOrCreate = function (id) {
    var element = $('#' + id);

    if (element.length == 0) {
        element = $("<div id=\"" + id + "\"/>");
    }

    return element;
};

$.fn.topPopup = function (action, options) {
    return this.each(function () {
        if (TOP_POPUP_ON_ANIMATE)
            return;

        if (!action) action = 'show';

        var defaultOptions = {
            'position': 'center'
        };
        options = $.extend(defaultOptions, options);

        if (action == "hide" && TOP_POPUP_ELEMENT) {
            var popup = getOrCreate('top-popup');

            TOP_POPUP_ON_ANIMATE = true;
            popup.animate({
                top: "-="  + popup.outerHeight() + "px"
            }, 500, function () {
                popup.hide();
                $(TOP_POPUP_ELEMENT).unwrap();
                $(TOP_POPUP_ELEMENT).hide();
                backgroundOverlay('disable');

                TOP_POPUP_ELEMENT = null;

                if (options.callback) options.callback();
                TOP_POPUP_ON_ANIMATE = false;
            });
        }else if (action == 'show') {
            var show = function (element, callback) {
                TOP_POPUP_ELEMENT = element;

                var popup = getOrCreate('top-popup');

                $(element).wrap(popup);
                popup = $(element).parent();

                popup.width($(TOP_POPUP_ELEMENT).outerWidth());
                if (options.position == 'center') {
                    popup.css({ left: '50%', 'margin-left': - $(TOP_POPUP_ELEMENT).outerWidth() / 2 });
                }else if (options.position == 'right') {
                    popup.css({ right: '10px' });
                }

                $(TOP_POPUP_ELEMENT).show();
                popup.css('top', popup.css('top').replace('px', '') - popup.outerHeight());

                backgroundOverlay('enable');
                backgroundOverlay('bind', {
                    event: 'click',
                    callback: function () {
                        $(TOP_POPUP_ELEMENT).topPopup('hide');
                    }
                });

                popup.show();

                TOP_POPUP_ON_ANIMATE = true;
                popup.animate({
                    top: "+="  + popup.outerHeight() + "px"
                }, 500, function () {
                    if (callback) callback();
                    TOP_POPUP_ON_ANIMATE = false;
                });
            };

            if (TOP_POPUP_ELEMENT) {
                if (TOP_POPUP_ELEMENT == this)
                    return;

                var self = this;
                $(TOP_POPUP_ELEMENT).topPopup('hide', {
                    callback: function () {
                        show(self, options.callback);
                    }
                });
            }else {
                show(this, options.callback);
            }
        }
    });
}
})(jQuery);
