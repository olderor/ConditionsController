var conditions = conditions || {};
conditions.product_types = (function () {

    function addProductType(organization_id, name, description, image_url, expiration_date_length_hours) {
        var data = {'name': name, 'description': description, 'image_url': image_url,
            'expiration_date_length_hours': expiration_date_length_hours, 'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('add-product-type', conditions.account.getToken(), data, function (response) {
            var addProductTypeError = $('#add-product-type-error');
            conditions.general.processResponse(response, addProductTypeError, function(response) {
                $('#add-product-type').modal('hide');
                reloadOrganizationProductTypes();
            });
        });
    }

    function getOrganizationProductTypes(organization_id, onDone) {
        var data = {'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('product-types', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function reloadOrganizationProductTypes() {
        getOrganizationProductTypes(conditions.organization.getCurrentOrganizationId(), function (response) {
            var organizationError = $('#organization-error');
            conditions.general.processResponse(response, organizationError, function (response) {
                var dataItems = response.product_types;
                for (var i = 0; i < dataItems.length; ++i) {
                    dataItems[i].expiration_date_length = conditions.general.formatDate(dataItems[i].expiration_date_length_hours);
                }
                $('#product-types-list').html($('#product-types-template').tmpl(dataItems));

                $('.browse-conditions-button').click(function () {
                    conditions.conditions.open($(this).data('product-type-id'));
                });
            }, false);
        });
    }

    function init() {
        reloadOrganizationProductTypes();

        $('#add-product-type-form').submit(function(e) {
            e.preventDefault();
            var years = parseInt($('#add-product-type-expiration-date-length-years').val());
            var months = parseInt($('#add-product-type-expiration-date-length-months').val());
            var days = parseInt($('#add-product-type-expiration-date-length-days').val());
            var hours = parseInt($('#add-product-type-expiration-date-length-hours').val());
            var expiration_date_length_hours = ((years * 12 + months) * 30 + days) * 24 + hours;
            addProductType(
                getCurrentOrganizationId(),
                $('#add-product-type-name').val(),
                $('#add-product-type-description').val(),
                $('#add-product-type-image').val(),
                expiration_date_length_hours);
        });
    }

    function initProductType() {
        init();
        conditions.products.initProductType();
    }

    return {
        initOrganization: init,
        initProductType: initProductType,
        getOrganizationProductTypes: getOrganizationProductTypes
    };
})();
