var conditions = conditions || {};
conditions.organization = (function () {
    
    function changeActiveStatus(organization_id, status) {
        var data = {'organization_id': organization_id, 'active': status};
        conditions.server.sendAuthorizedRequest('organization/change-status', conditions.account.getToken(), data, function (response) {
            var organizationError = $('#organization-error');
            conditions.general.processResponse(response, organizationError);
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
        window.localStorage.setItem('organization_id', organization_id);
        window.location.href = '/organizations/get?id=' + organization_id;
    }

    function getCurrentOrganizationId() {
        return window.localStorage.getItem('organization_id');
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

    function getOrganizationUsers(organization_id, onDone) {
        var data = {'organization_id': organization_id};
        conditions.server.sendAuthorizedRequest('organization/users', conditions.account.getToken(), data, function (response) {
            onDone(response);
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
        conditions.product_types.initOrganization();
        reloadOrganizationUsers();

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

        conditions.products.initOrganization();
    }

    return {
        init: init,
        changeActiveStatus: changeActiveStatus,
        getOrganizationInfo: getOrganizationInfo,
        open: open,
        getCurrentOrganizationId: getCurrentOrganizationId
    };
})();
