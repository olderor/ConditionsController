var conditions = conditions || {}
conditions.server = (function () {
    server_url = "https://127.0.0.1:5002/api/"

    function sendRequest(action, data, onDone, url=server_url) {
        console.log(action, data);
        $.ajax({
            url: url + action,
            type: 'post',
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
        }).fail(function() {
            if (onDone) {
                onDone(response);
            }
        }).always(function () {
            conditions.account.updateButtons();
        });
    }

    function sendAuthorizedRequest(action, token, data, onDone, url=server_url) {
        console.log(action, data);
        $.ajax({
            url: url + action,
            type: 'post',
            cache: false,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            cache: false,
            data: JSON.stringify(data),
            headers: {
                "Authorization": "Bearer " + token
            },
        }).done(function (response) {
            console.log(response);
            if (onDone) {
                onDone(response);
            }
        }).fail(function() {
            if (onDone) {
                onDone(response);
            }
        }).always(function () {
            conditions.account.updateButtons();
        });
    }

    return {
        sendRequest: sendRequest,
        sendAuthorizedRequest: sendAuthorizedRequest
    };
})();
