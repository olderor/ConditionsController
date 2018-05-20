var conditions = conditions || {}
conditions.organizations = (function () {

    function addOrganization(name, description, image_url) {
        var data = {'name': name, 'about': description, 'image_url': image_url};
        conditions.server.sendAuthorizedRequest('add-organization', conditions.account.getToken(), data, function (response) {
            var addOrganizationError = $('#add-organization-error');
            conditions.general.processResponse(response, addOrganizationError, function(response) {
                $('#add-organization').modal('hide');
                reloadOrgamizations();
            });
        });
    }

    function reloadOrgamizations() {
        conditions.server.sendAuthorizedRequest('organizations', conditions.account.getToken(), null, function (response) {
            var organizationsError = $('#organizations-error');
            conditions.general.processResponse(response, organizationsError, function(response) {
                dataItems = response.organizations;
                $('#organizations-list').html($('#organization-template').tmpl(dataItems));
                $('input.toggle:checkbox').bootstrapToggle();

                $('.active-toggle').change(function() {
                    conditions.organization.changeActiveStatus($(this).data('organization-id'), $(this).is(':checked'))
                });
                $('.show-organization-details-button').click(function () {
                    conditions.organization.open($(this).data('organization-id'));
                });
            });
        });
    }

    function init() {
        reloadOrgamizations();

        $('#add-organization-form').submit(function(e) {
            e.preventDefault();
            addOrganization($('#add-organization-name').val(), $('#add-organization-description').val(), $('#add-organization-image').val());
        });
    }

    return {
        init: init
    };
})();
