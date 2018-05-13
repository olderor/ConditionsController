var conditions = conditions || {}
conditions.account = (function () {

    function signin(email, password) {
        conditions.server.sendRequest('login', 'post', {email: email, password: password}, function(response) {
            if (!response) {
                // todo: show failed to sign in.
                return;
            }
            if (response.error) {
                // todo: show error.
                return;
            }
            $.cookie('token', response.token, {
                path: '/',
                secure: true
            });
            $.cookie('email', email, {
                path: '/',
                secure: true
            });
            conditions.server.sendRequest('login', 'post', response, null, 'https://127.0.0.1:5003/');
            $('#signin').modal('hide');
            updateButtons();
        })
    }

    function signup(email, password) {
        response = conditions.server.sendRequest('signup', 'post', {email: email, password: password});
        if (!response) {
            // todo: show failed to sign in.
            return;
        }
        if (response.error) {
            // todo: show error.
            return;
        }
        // todo: now log in.
    }

    function isSignedIn() {
        var token = getToken();
        return token != null && token !== undefined && token != '';
    }

    function getToken() {
        return $.cookie('token');
    }

    function getEmail() {
        return $.cookie('email');
    }

    function updateButtons() {
        $('#sign-welcome').html($('#sign-welcome-template').html() + ', ' + getEmail());
        if (isSignedIn()) {
            $('#signin-button').hide();
            $('#signup-button').hide();
            $('#signout-button').show();
            $('#sign-welcome').show();
        } else {
            $('#signin-button').show();
            $('#signup-button').show();
            $('#signout-button').hide();
            $('#sign-welcome').hide();
        }
    }

    function init() {
        $('#sigin-form').submit(function(e) {
            e.preventDefault();
            conditions.account.signin($('#signin-email').val(), $('#signin-password').val());
        });
        $('#sigup-form').submit(function(e) {
            e.preventDefault();
            conditions.account.signup($('#signup-email').val(), $('#signup-password').val());
        });
        $('#signout-button').click(function(e) {
            $.cookie('token', '');
            $.cookie('email', '');
            updateButtons();
        });
        updateButtons();
    }

    return {
        init: init,
        signin: signin,
        signup: signup,
        getToken: getToken,
        isSignedIn: isSignedIn
    };
})();
