var conditions = conditions || {};
conditions.tracking_device = (function () {
    function assign(product_id, key, password, onDone) {
        var data = {'product_id': product_id, 'key': key, 'password': password};
        conditions.server.sendAuthorizedRequest('assign-device', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function addDevice(key, password) {
        var data = {'key': key, 'password': password};
        conditions.server.sendAuthorizedRequest('register-device', conditions.account.getToken(), data, function (response) {
            var registerDeviceError = $('#register-device-error');
            conditions.general.processResponse(response, registerDeviceError, function(response) {
                $('#register-device').modal('hide');
            });
        });
    }

    function initAssignDeviceButtons() {
        $('.add-tracking-device-button').click(function () {
            $('#assign-device-product-id').val($(this).data('product-id'));
            $('#assign-device').modal('show');
        });
    }

    function initAssignDeviceForm(onDone) {
        $('#assign-device-form').submit(function(e) {
            e.preventDefault();
            conditions.tracking_device.assign(
                $('#assign-device-product-id').val(),
                $('#assign-device-key').val(),
                $('#assign-device-password').val(),
                function (response) {
                    var assignDeviceError = $('#assign-device-error');
                    conditions.general.processResponse(response, assignDeviceError, function (response) {
                        onDone();
                        $('#assign-device').modal('hide');
                        $('#assign-device-product-id').val('');
                        $('#assign-device-key').val('');
                        $('#assign-device-password').val('');
                    });
                });
        });
    }

    function initBase() {
        $('#register-device-form').submit(function (e) {
            e.preventDefault();
            addDevice($('#register-device-key').val(), $('#register-device-password').val())
        })
    }

    return {
        assign: assign,
        initBase: initBase,
        initAssignDeviceForm: initAssignDeviceForm,
        initAssignDeviceButtons: initAssignDeviceButtons
    };
})();
