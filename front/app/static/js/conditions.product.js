var conditions = conditions || {};
conditions.product = (function () {
    var is_chart = false;
    var statuses = {};

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

    function initChart(cons, tracking_statuses) {
        var data = [];
        var stripLines = [];
        conditions.general.sortByDate(tracking_statuses, 'date_recordered');
        for (var i = 0; i < cons.length; ++i) {
            var color = "#"+((1<<24)*Math.random()|0).toString(16);
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
            var dataPoints = [];
            for (var j = 0; j < tracking_statuses.length; ++j) {
                var status = tracking_statuses[j];
                if (status.condition_id == condition.id) {
                    dataPoints.push({
                        x: new Date(status.date_recordered),
                        y: status.value
                    });
                }
            }
            statuses[condition.id] = dataPoints;
            data.push({
                type: "line",
                showInLegend: true,
                legendText: condition.name,
                dataPoints : dataPoints,
                color: color
            })
        }
        var chart = new CanvasJS.Chart('product-chart',{
            data: data,
            axisY: {
                stripLines: stripLines,
                gridThickness: 0
            }
        });
        chart.render();

        var updateInterval = 1000;
        var updateChart = function () {
            chart.render();	
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
            reloadProductInfo();
            open($('#product-id').val());
        })
    }

    return {
        init: init,
        initHome: initHome,
        open: open
    };
})();
