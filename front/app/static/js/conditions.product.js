var conditions = conditions || {};
conditions.product = (function () {
    var is_chart = false;
    var statuses = {};
    var con_ids = [];
    var last_date = null;
    var chart;

    function getProductInfo(product_id, onDone) {
        var data = {'product_id': product_id};
        conditions.server.sendAuthorizedRequest('product/get', conditions.account.getToken(), data, function (response) {
            onDone(response);
        });
    }

    function reloadProductInfo() {
        getProductInfo(getCurrentProductId(), function (response) {
            var productError = $('#product-error');
            conditions.general.processResponse(response, productError, function (response) {
                var dataItems = response.product;
                if (!dataItems['tracking_device_id']) {
                    dataItems['tracking_device_id'] = '';
                }
                $('#product-description').html($('#product-template').tmpl([dataItems]));
                conditions.tracking_device.initAssignDeviceButtons();
                if (!is_chart) {
                    is_chart = true;
                    initChart(dataItems.conditions, dataItems.tracking_statuses);
                }
                var qrcode = new QRCode("qrcode", {
                    text: getCurrentProductId(),
                    width: 128,
                    height: 128
                });
            });
        });
    }

    function open(product_id=getCurrentProductId()) {
        window.localStorage.setItem('product_id', product_id);
        window.location.href = '/products/get?id=' + product_id;
    }

    function getCurrentProductId() {
        var productIdBox = $('#product-id');
        if (productIdBox && productIdBox.val()) {
            return productIdBox.val()
        }
        return window.localStorage.getItem('product_id');
    }

    function addNewTracks(tracking_statuses) {
        conditions.general.sortByDate(tracking_statuses, 'date_recordered');
        for (var i = 0; i < con_ids.length; ++i) {
            for (var j = 0; j < tracking_statuses.length; ++j) {
                var status = tracking_statuses[j];
                var date = moment.utc(status.date_recordered);
                if (status.condition_id == con_ids[i]) {
                    statuses[con_ids[i]].push({
                        x: date.toDate(),
                        y: status.value
                    });
                }
                if (!last_date || last_date < date) {
                    last_date = date;
                }
            }
        }
        chart.render();
    }

    function initChart(cons, tracking_statuses) {
        var chartData = [];
        var stripLines = [];
        for (var i = 0; i < cons.length; ++i) {
            var color = "#" + ((1 << 24) * Math.random() | 0).toString(16);
            var condition = cons[i];
            if (condition.min_value) {
                stripLines.push({
                    label: condition.name + ": " + condition.min_value,
                    value: condition.min_value,
                    color: color,
                    labelFontColor: color
                });
            }
            if (condition.max_value) {
                stripLines.push({
                    label: condition.name + ": " + condition.max_value,
                    value: condition.max_value,
                    color: color,
                    labelFontColor: color
                });
            }
            statuses[condition.id] = [];
            con_ids.push(condition.id);

            chartData.push({
                type: "line",
                showInLegend: true,
                legendText: condition.name,
                dataPoints: statuses[condition.id],
                color: color
            });
        }
        chart = new CanvasJS.Chart('product-chart',{
            data: chartData,
            animationEnabled: false,
            axisY: {
                stripLines: stripLines,
                gridThickness: 0
            }
        });
        addNewTracks(tracking_statuses);

        var updateInterval = 1000;
        var updateChart = function () {
            var tracks_data = {'product_id': getCurrentProductId()};
            if (last_date) {
                tracks_data['from_date'] = last_date;
            }
            conditions.server.sendAuthorizedRequest('product/get-tracks', conditions.account.getToken(), tracks_data, function (response) {
                if (response && !response.error && response.product && response.product.tracking_statuses) {
                    addNewTracks(response.product.tracking_statuses);
                    $('#product-status-info').html(response.product.status)
                    $('#product-status-info').removeClass();
                    $('#product-status-info').addClass('status-' + response.product.status_en);
                }
            });
        };
        setInterval(function(){updateChart()}, updateInterval);
    }

    function init() {
        reloadProductInfo();
        conditions.tracking_device.initAssignDeviceForm(reloadProductInfo);
    }

    function initHome() {
        $('#get-product-info-home').submit(function (e) {
            e.preventDefault();
            getProductInfo($('#product-id').val(), function (response) {
                var productError = $('#product-error');
                conditions.general.processResponse(response, productError, function (response) {
                    open($('#product-id').val());
                });
            });
        })
    }

    return {
        init: init,
        initHome: initHome,
        open: open
    };
})();
