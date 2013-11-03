(function($) {

$.fn.wikiImageWidget = function (action, options) {

    return this.each(function () {
        var self = this;

        $.get('/js_templates/wiki_image_widget.html', function (template) {
            var widget = $($.tmpl(template, {}));
            var setImage = function (thumbUrl, imgUrl) {
                widget.find('.no-image').hide();
                widget.find('.selected-image img').attr('src', thumbUrl);
                $(self).val(imgUrl);
            };

            if ($(self).val()) setImage($(self).val(), $(self).data('url'));

            widget.find('.search-button').click(function () {
                var query = widget.find('input[name=query]').val();

                if (query) {
                    widget.find('.search-result').html($('<img>').attr('src', '/static/img/loading.gif').addClass('loading'));
                    widget.find('.search-result').load('/wiki/images/list/?query=' + query, function () {
                        widget.find('.search-result img').click(function () {
                            $(this).parent().children().removeClass('selected');
                            $(this).addClass('selected');

                            setImage($(this).attr('src'), $(this).data('url'));
                        });
                    });
                }
            });

            $(self).after(widget);
        });
    });
}

})(jQuery);
