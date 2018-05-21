var conditions = conditions || {};
conditions.products = (function () {

    function addProduct(name, product_type_id, organization_id, reloadProducts) {
        var data = {'product_type_id': product_type_id, 'name': name, 'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('add-product', conditions.account.getToken(), data, function (response) {
            var addProductError = $('#add-product-error');
            conditions.general.processResponse(response, addProductError, function(response) {
                $('#add-product').modal('hide');
                reloadProducts();
            });
        });
    }

    function reloadProducts(data) {
        conditions.server.sendAuthorizedRequest('products', conditions.account.getToken(), data, function (response) {
            var productsError = $('#products-error');
            conditions.general.processResponse(response, productsError, function(response) {
                var dataItems = response.products;
                for (var i = 0; i < dataItems.length; ++i) {
                    if (!dataItems[i]['tracking_device_id']) {
                        dataItems[i]['tracking_device_id'] = '';
                    }
                }
                $('#products-list').html($('#products-template').tmpl(dataItems));
            });
        });
    }

    function reloadProductsByProductType() {
        var data = {'product_type_id': conditions.conditions.getProductTypeId()};
        reloadProducts(data)
    }

    function reloadProductsByOrganization() {
        var data = {'organization_id': conditions.organization.getCurrentOrganizationId()};
        reloadProducts(data)
    }

    function getProductInfo(product_id, onDone) {
        var data = {'product_id': product_id};
        conditions.server.sendAuthorizedRequest('product/get', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function getProductId() {
        return conditions.general.getUrlParameters()['product'];
    }

    function reloadProductInfo() {
        getProductInfo(getProductId(), function (response) {
            var productsError = $('#products-error');
            conditions.general.processResponse(response, productsError, function (response) {
                var dataItems = response.product;
                $('#product-description').html($('#product-template').tmpl([dataItems]));
            }, false);
        });
    }

    function open(product_id) {
        window.location.href = '/product?id=' + product_id
    }

    function reloadAddProductType() {
        var addProductTypeBox = $('#add-product-type');
        conditions.product_types.getOrganizationProductTypes(
            conditions.organization.getCurrentOrganizationId(), function (response) {
                var addProductError = $('#add-product-error');
                conditions.general.processResponse(response, addProductError, function (response) {
                    addProductTypeBox.html();
                    $.each(response.product_types, function (index, item) {
                        addProductTypeBox.append(new Option(item.name, item.id));
                    });
                    addProductTypeBox.val(conditions.conditions.getProductTypeId());
                });
            });
    }

    function reloadAddProductOrganization() {
        var addOrganizationBox = $('#add-product-organization');
        conditions.organizations.getOrganizations(function (response) {
                addOrganizationBox.html();
                $.each(response.organizations, function(index, item) {
                    addOrganizationBox.append(new Option(item.name, item.id));
                });
                addOrganizationBox.val(conditions.organization.getCurrentOrganizationId());
                reloadAddProductType();
            });
    }

    function initOrganization() {
        reloadProductsByOrganization();
        reloadAddProductOrganization();

        $('#add-product-organization').prop("disabled", true);

        $('#add-product-form').submit(function(e) {
            e.preventDefault();
            addProduct(
                $('#add-product-name').val(), $('#add-product-type').val(),
                $('#add-product-organization').val(),
                reloadProductsByOrganization);
        });
    }

    function initProductType() {
        reloadProductsByProductType();
        reloadAddProductOrganization();
        $('#add-product-organization').prop("disabled", true);
        $('#add-product-type').prop("disabled", true);

        $('#add-product-form').submit(function(e) {
            e.preventDefault();
            addProduct(
                $('#add-product-name').val(), $('#add-product-type').val(),
                $('#add-product-organization').val(),
                reloadProductsByProductType);
        });
    }

    function init() {
        reloadProducts();
        $('#add-product-form').submit(function(e) {
            e.preventDefault();
            addProduct(
                $('#add-product-name').val(), $('#add-product-type').val(),
                $('#add-product-organization').val(),
                reloadProducts());
        });
    }

    return {
        init: init,
        initOrganization: initOrganization,
        initProductType: initProductType,
        open: open
    };
})();
