var conditions = conditions || {};
conditions.general = (function () {

    function processResponse(response, errorBar, onSuccess, shouldHide=true) {
        if (!response) {
            errorBar.html('Internet connection error.');
            errorBar.show();
            return;
        }
        if (response.error) {
            errorBar.html(response.error);
            errorBar.show();
            return;
        }
        if (shouldHide) {
            errorBar.hide();
        }
        if (onSuccess) {
            onSuccess(response);
        }
    }
    
    function parse_query_string(query) {
        var vars = query.split("&");
        var query_string = {};
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            var key = decodeURIComponent(pair[0]);
            var value = decodeURIComponent(pair[1]);
            // If first entry with this name
            if (typeof query_string[key] === "undefined") {
                query_string[key] = decodeURIComponent(value);
                // If second entry with this name
            } else if (typeof query_string[key] === "string") {
                var arr = [query_string[key], decodeURIComponent(value)];
                query_string[key] = arr;
                // If third or later entry with this name
            } else {
                query_string[key].push(decodeURIComponent(value));
            }
        }
        return query_string;
    }
    
    function getUrlParameters() {
        var query = window.location.search.substring(1);
        return parse_query_string(query);
    }

    function formatDate(dateInHours) {
        var hours = ('' + dateInHours % 24).padStart(2, '0');
        dateInHours = parseInt(dateInHours / 24);
        var days = ('' + dateInHours % 30).padStart(2, '0');
        dateInHours = parseInt(dateInHours / 30);
        var months = ('' + dateInHours % 12).padStart(2, '0');
        dateInHours = parseInt(dateInHours / 12);
        var years = ('' + dateInHours).padStart(4, '0');
        return '' + days + '.' + months + '.' + years + ' ' + hours + ':00:00';
    }

    function sortByDate(array, field) {
        array.sort(function(a,b){
          return new Date(a[field]) - new Date(b[field]);
        });
    }

    return {
        processResponse: processResponse,
        getUrlParameters: getUrlParameters,
        formatDate: formatDate,
        sortByDate: sortByDate
    };
})();
