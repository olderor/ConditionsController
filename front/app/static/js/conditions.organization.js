var conditions = conditions || {}
conditions.organization = (function () {
    
    function changeActiveStatus(organization_id, status) {
        var data = {'organization_id': organization_id, 'active': status};
        conditions.server.sendAuthorizedRequest('organization/change-status', conditions.account.getToken(), data, function (response) {
            var organizationError = $('#organization-error');
            conditions.general.processResponse(response, organizationError);
        });
    }

    function addProductType(organization_id, name, description, image_url, expiration_date_length_hours) {
        var data = {'name': name, 'description': description, 'image_url': image_url,
            'expiration_date_length_hours': expiration_date_length_hours, 'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('organization/add-product-type', conditions.account.getToken(), data, function (response) {
            var addProductTypeError = $('#add-product-type-error');
            conditions.general.processResponse(response, addProductTypeError, function(response) {
                $('#add-product-type').modal('hide');
                reloadOrganizationProductTypes();
            });
        });
    }

    function registerManager(organization_id, email, password, name, description, image_url) {
        var data = {'name': name, 'description': description, 'image_url': image_url,
            'organization_id': organization_id, 'email': email, 'password': password};
        conditions.server.sendAuthorizedRequest('organization/register', conditions.account.getToken(), data, function (response) {
            var registerManagerError = $('#register-manager-error');
            conditions.general.processResponse(response, registerManagerError, function(response) {
                $('#register-manager').modal('hide');
                reloadOrganizationUsers();
            });
        });
    }

    function open(organization_id=getCurrentOrganizationId()) {
        window.location.href = '/organizations/get?id=' + organization_id
    }

    function getCurrentOrganizationId() {
        var id = conditions.general.getUrlParameters()['id'];
        if (id) {
            return id;
        }
        return conditions.account.getOrganization();
    }

    function getOrganizationInfo(organization_id, onDone) {
        var data = {'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('organization/get', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function getOrganizationProductTypes(organization_id, onDone) {
        var data = {'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('organization/product-types', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function getOrganizationUsers(organization_id, onDone) {
        var data = {'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('organization/users', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function reloadOrganizationProductTypes() {
        getOrganizationProductTypes(getCurrentOrganizationId(), function (response) {
            var organizationError = $('#organization-error');
            conditions.general.processResponse(response, organizationError, function (response) {
                var dataItems = response.product_types;
                for (var i = 0; i < dataItems.length; ++i) {
                    dataItems[i].expiration_date_length = conditions.general.formatDate(dataItems[i].expiration_date_length_hours);
                }
                $('#product-types-list').html($('#product-types-template').tmpl(dataItems));
            }, false);
        });
    }

    function reloadOrganizationUsers() {
        getOrganizationUsers(getCurrentOrganizationId(), function (response) {
            var organizationError = $('#organization-error');
            conditions.general.processResponse(response, organizationError, function (response) {
                var dataItems = response.users;
                $('#users-list').html($('#users-template').tmpl(dataItems));
                $('input.toggle:checkbox').bootstrapToggle();

                $('.active-user-toggle').change(function() {
                    conditions.account.changeActiveStatus($(this).data('user-id'), $(this).is(':checked'), '#organization-error')
                });
            }, false);
        });
    }

    function reloadOrganizationInfo() {
        getOrganizationInfo(getCurrentOrganizationId(), function (response) {
            var organizationError = $('#organization-error');
            conditions.general.processResponse(response, organizationError, function (response) {
                var dataItems = response.organization;
                $('#organization-description').html($('#organization-template').tmpl([dataItems]));
                $('input.toggle:checkbox').bootstrapToggle();

                $('.active-toggle').change(function() {
                    conditions.organization.changeActiveStatus($(this).data('organization-id'), $(this).is(':checked'))
                });
            }, false);
        });
    }
    
    function init() {
        reloadOrganizationInfo();
        reloadOrganizationProductTypes();
        reloadOrganizationUsers();

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

        $('#register-manager-form').submit(function(e) {
            e.preventDefault();
            registerManager(
                getCurrentOrganizationId(),
                $('#register-manager-email').val(),
                $('#register-manager-password').val(),
                $('#register-manager-name').val(),
                $('#register-manager-description').val(),
                $('#register-manager-image').val());
        });
    }

    return {
        init: init,
        changeActiveStatus: changeActiveStatus,
        getOrganizationInfo: getOrganizationInfo,
        open: open
    };
})();
