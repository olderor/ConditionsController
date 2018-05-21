var conditions = conditions || {};
conditions.conditions = (function () {

    function addCondition(product_type_id, name, description, min_value, max_value) {
        var data = {'product_type_id': product_type_id, 'name': name, 'description': description,
        'min_value': min_value, 'max_value': max_value};
        conditions.server.sendAuthorizedRequest('add-condition', conditions.account.getToken(), data, function (response) {
            var addConditionError = $('#add-condition-error');
            conditions.general.processResponse(response, addConditionError, function(response) {
                $('#add-condition').modal('hide');
                reloadConditions();
            });
        });
    }

    function reloadConditions() {
        var data = {'product_type_id': getProductTypeId()};
        conditions.server.sendAuthorizedRequest('conditions', conditions.account.getToken(), data, function (response) {
            var conditionsError = $('#product-types-error');
            conditions.general.processResponse(response, conditionsError, function(response) {
                var dataItems = response.conditions;
                for (var i = 0; i < dataItems.length; ++i) {
                    if (!dataItems[i]['min_value']) {
                        dataItems[i]['min_value'] = '';
                    }
                    if (!dataItems[i]['max_value']) {
                        dataItems[i]['max_value'] = '';
                    }
                }
                $('#conditions-list').html($('#conditions-template').tmpl(dataItems));
            });
        });
    }

    function getProductTypeId() {
        return conditions.general.getUrlParameters()['product_type'];
    }

    function getProductTypeInfo(product_type_id, onDone) {
        var data = {'product_type_id': product_type_id};
        conditions.server.sendAuthorizedRequest('product-type/get', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function reloadProductTypeInfo() {
        getProductTypeInfo(getProductTypeId(), function (response) {
            var conditionsError = $('#product-types-error');
            conditions.general.processResponse(response, conditionsError, function (response) {
                var dataItems = response.product_type;
                $('#product-type-description').html($('#product-type-template').tmpl([dataItems]));
            }, false);
        });
    }

    function open(product_type) {
        window.location.href = '/product_types?product_type=' + product_type
    }

    function init() {
        reloadProductTypeInfo();
        reloadConditions();

        $('#add-condition-form').submit(function(e) {
            e.preventDefault();
            addCondition(getProductTypeId(),
                $('#add-condition-name').val(), $('#add-condition-description').val(),
                $('#add-condition-min-value').val(), $('#add-condition-max-value').val());
        });

        conditions.products.initProductType();
    }

    return {
        init: init,
        open: open,
        getProductTypeId: getProductTypeId
    };
})();
