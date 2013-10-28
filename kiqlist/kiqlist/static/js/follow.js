function followUserCallback() {
    _followUserCallback(true, this);
    return false;
}

function unfollowUserCallback() {
    _followUserCallback(false, this);
    return false;
}

function _followUserCallback(isFollow, element) {
    var userId = $(element).data('user-id');
    var url = "/users/";
    url += isFollow ? "follow" : "unfollow";
    url += '/' + userId + '/'
    $.getJSON(url, function (response) {
        if (response.error_code == 0) {
            toggleFollowLink($(element), isFollow);
        }else {
            message("error", response.error_message);
        }
    });
}

function toggleFollowLink(element, isFollow) {
    element.unbind('click');
    if (isFollow) {
        element.html('Unfollow');
        element.click(unfollowUserCallback);
    } else {
        element.html('Follow');
        element.click(followUserCallback);
    }
}