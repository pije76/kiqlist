(function($) {

$.fn.ajaxForm = function (url, successFormCallback, callback) {
    return this.each(function () {
        var self = this;
        var attachSubmitListener = function () {
            $(self).find('form').submit(function () {
                var url = $(this).attr('action');
                var type = $(this).attr('method') || 'POST';

                $.ajax({
                    url: url,
                    type: type,
                    data: $(this).serialize(),
                    success: function (response) {
                        if (typeof(response) == "string") {
                            $(self).html(response);
                            attachSubmitListener();
                        }else {
                            if (response.error_code == 0) {
                                successFormCallback(response.data);
                            }else {
                                message('error', response.error_message);
                            }

                            $(self).load(url, function () {
                                attachSubmitListener();
                            });
                        }
                    },
                    error: function () {
                        message('error', "Something wrong happened. We are working to fix the problem. Pleast try later.");
                    }
                });

                return false;
            });
        };

        $(this).load(url, function (responseText, textStatus) {
            if (textStatus == 'success') {
                attachSubmitListener();
                if (callback) callback();
            }else if (textStatus == 'error') {
                message('error', "Something wrong happened. We are working to fix the problem. Pleast try later.");
            }
        });
    });
};

})(jQuery);
