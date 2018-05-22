var conditions = conditions || {};
conditions.account = (function () {

    function signin(email, password) {
        conditions.server.sendRequest('login', {email: email, password: password}, function(response) {
            var signinError = $('#signin-error');
            conditions.general.processResponse(response, signinError, function(response) {
                window.localStorage.setItem('token', response.token);
                window.localStorage.setItem('email', response.email);
                window.localStorage.setItem('role', response.role);
                window.localStorage.setItem('organization_id', response.organization_id);
                $('#signin').modal('hide');
                updateButtons();
            });
        })
    }

    function signup(email, password) {
        conditions.server.sendRequest('signup', {email: email, password: password}, function(response) {
            var signupError = $('#signup-error');
            conditions.general.processResponse(response, signupError, function(response) {
                signin(email, password);
                $('#signup').modal('hide');
            });
        });
    }

    function isSignedIn() {
        var token = getToken();
        return token != null && token !== undefined && token != '';
    }

    function getToken() {
        return window.localStorage.getItem('token');
    }

    function getEmail() {
        return window.localStorage.getItem('email');
    }

    function isAdmin() {
        return window.localStorage.getItem('role') === 'admin';
    }

    function getOrganization() {
        return window.localStorage.getItem('organization_id');
    }


    function updateButtons() {
        $('#sign-welcome').html($('#sign-welcome-template').html() + ', ' + getEmail());
        if (isSignedIn()) {
            $('.signed-in').show();
            $('.unsigned-in').hide();
            // $('#signin-button').hide();
            // $('#signup-button').hide();
            // $('#signout-button').show();
            // $('#sign-welcome').show();
        } else {
            // $('#signin-button').show();
            // $('#signup-button').show();
            // $('#signout-button').hide();
            // $('#sign-welcome').hide();
            $('.signed-in').hide();
            $('.unsigned-in').show();
        }

        $('.admin-func').hide();
        $('.manager-func').hide();
        if (isSignedIn()) {
            if (isAdmin()) {
                $('.admin-func').show();
            } else {
                $('.manager-func').show();
            }
        }
    }

    function init() {
        $('#signin-form').submit(function(e) {
            e.preventDefault();
            conditions.account.signin($('#signin-email').val(), $('#signin-password').val());
        });
        $('#signup-form').submit(function(e) {
            e.preventDefault();
            conditions.account.signup($('#signup-email').val(), $('#signup-password').val());
        });
        $('#signout-button').click(function(e) {
            window.localStorage.setItem('token', '');
            window.localStorage.setItem('email', '');
            window.localStorage.setItem('organization_id', '');
            updateButtons();
            window.location.href = '/';
        });
        updateButtons();
    }

    function changeActiveStatus(user_id, status, errorId) {
        var data = {'user_id': user_id, 'active': status};
        conditions.server.sendAuthorizedRequest('change-status', conditions.account.getToken(), data, function (response) {
            var errorBox = $(errorId);
            conditions.general.processResponse(response, errorBox);
        });
    }

    return {
        init: init,
        signin: signin,
        signup: signup,
        getToken: getToken,
        isSignedIn: isSignedIn,
        getOrganization: getOrganization,
        changeActiveStatus: changeActiveStatus,
        updateButtons: updateButtons
    };
})();
