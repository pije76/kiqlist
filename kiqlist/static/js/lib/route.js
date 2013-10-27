function route(data) {
    var listener = function () {
        for(var i = 0; i < data.length; ++i) {
            if ((result = data[i].hash.exec(location.hash)) != null) {
                data[i].action.apply(null, result.splice(1));
            }
        }
    };

    $(window).bind('hashchange', listener);
    $(document).ready(listener);
};
