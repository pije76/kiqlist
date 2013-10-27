function request(url, successCallback) {
	$.ajax(url, {
		dataType: "json",
		success: function (response) {
			if (response.error_code == 0) {
				successCallback(response.data);
			}else {
				message("error", response.error_message);
			}
		}
	});
};
