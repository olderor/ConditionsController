var conditions = conditions || {}
conditions.products = (function () {

    function init() {
        conditions.server.sendRequest('products', 'post', {token: conditions.account.getToken()}, function (response) {
            $('#product-template').tmpl(response.products).appendTo('#products-list');
        });
    }

    return {
        init: init
    };
})();
