var conditions = conditions || {}
conditions.products = (function () {

    function init() {
        conditions.server.sendAuthorizedRequest('products', conditions.account.getToken(), null, function (response) {
            $('#product-template').tmpl(response.products).appendTo('#products-list');
        });
    }

    return {
        init: init
    };
})();
