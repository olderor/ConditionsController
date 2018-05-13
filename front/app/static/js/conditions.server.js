var conditions = conditions || {}
conditions.server = (function () {
    server_url = "https://127.0.0.1:5002/api/"

    function sendRequest(action, type, data, onDone, url=server_url) {
        console.log(action, type, data);
        $.ajax({
            url: url + action,
            type: type,
            cache: false,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            cache: false,
            data: JSON.stringify(data)
        }).done(function (response) {
            console.log(response);
            if (onDone) {
                onDone(response);
            }
        }).fail(function (e) {
            console.log(e);
        });
    }

    return {
        sendRequest: sendRequest
    };
})();
