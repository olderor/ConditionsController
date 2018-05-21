var conditions = conditions || {};
conditions.product = (function () {

    function getProductInfo(product_id, onDone) {
        var data = {'product_id': product_id};
        conditions.server.sendAuthorizedRequest('product/get', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function reloadProductInfo() {
        getProductInfo(getCurrentProductId(), function (response) {
            var productError = $('#product-error');
            conditions.general.processResponse(response, productError, function (response) {
                var dataItems = response.product;
                if (!dataItems['tracking_device_id']) {
                    dataItems['tracking_device_id'] = '';
                }
                $('#product-description').html($('#product-template').tmpl([dataItems]));
                conditions.tracking_device.initAssignDeviceButtons();
            });
        });
    }

    function open(product_id=getCurrentProductId()) {
        window.localStorage.setItem('product_id', product_id);
        window.location.href = '/products/get?id=' + product_id;
    }

    function getCurrentProductId() {
        var productIdBox = $('#product-id');
        if (productIdBox && productIdBox.val()) {
            return productIdBox.val()
        }
        return window.localStorage.getItem('product_id');
    }

    function init() {
        reloadProductInfo();
        conditions.tracking_device.initAssignDeviceForm(reloadProductInfo);
    }

    function initHome() {
        $('#get-product-info-home').submit(function (e) {
            e.preventDefault();
            reloadProductInfo();
            open($('#product-id').val());
        })
    }

    return {
        init: init,
        initHome: initHome,
        open: open
    };
})();
