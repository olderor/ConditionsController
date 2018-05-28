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
                $('.browse-product-info-button').click(function () {
                    conditions.product.open($(this).data('product-id'));
                });
                conditions.tracking_device.initAssignDeviceButtons();
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

    function open(product_id) {
        window.location.href = '/product?id=' + product_id
    }

    function reloadAddProductType() {
        var addProductTypeBox = $('#add-product-select-type');
        conditions.product_types.getOrganizationProductTypes(
            conditions.organization.getCurrentOrganizationId(), function (response) {
                var addProductError = $('#add-product-error');
                conditions.general.processResponse(response, addProductError, function (response) {
                    addProductTypeBox.html('');
                    $.each(response.product_types, function (index, item) {
                        addProductTypeBox.append(new Option(item.name, item.id));
                    });
                    addProductTypeBox.val(conditions.conditions.getProductTypeId());
                });
            });
    }

    function reloadAddProductOrganization() {
        var addOrganizationBox = $('#add-product-select-organization');
        conditions.organizations.getOrganizations(function (response) {
                addOrganizationBox.html('');
                $.each(response.organizations, function(index, item) {
                    addOrganizationBox.append(new Option(item.name, item.id));
                });
                addOrganizationBox.val(conditions.organization.getCurrentOrganizationId());
                addOrganizationBox.change(function () {
                    window.localStorage.setItem('organization_id', addOrganizationBox.val());
                    reloadAddProductType();
                });
                reloadAddProductType();
            });
    }

    function initAddProductForm(onDone) {
        $('#add-product-form').submit(function(e) {
            e.preventDefault();
            addProduct(
                $('#add-product-name').val(), $('#add-product-select-type').val(),
                $('#add-product-select-organization').val(),
                onDone);
        });
    }


    function initOrganization() {
        reloadProductsByOrganization();
        reloadAddProductOrganization();

        $('#add-product-select-organization').prop("disabled", true);
        initAddProductForm(reloadProductsByOrganization);
        conditions.tracking_device.initAssignDeviceForm(reloadProductsByOrganization);
    }

    function initProductType() {
        reloadProductsByProductType();
        reloadAddProductOrganization();
        $('#add-product-select-organization').prop("disabled", true);
        $('#add-product-select-type').prop("disabled", true);

        initAddProductForm(reloadProductsByProductType);
        conditions.tracking_device.initAssignDeviceForm(reloadProductsByProductType);
    }

    function init() {
        reloadProducts();
        reloadAddProductOrganization();

        initAddProductForm(reloadProducts);
        conditions.tracking_device.initAssignDeviceForm(reloadProducts);
    }

    return {
        init: init,
        initOrganization: initOrganization,
        initProductType: initProductType,
        open: open
    };
})();
