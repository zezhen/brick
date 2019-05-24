

function show(chart, result, ranking_keys, convert_title) {

    var metrics = chart.metrics;
    var arrangedKey = chart.arrangedby;

    var todayData = getArrangedData(result.today, metrics, arrangedKey);
    var ystdData = getArrangedData(result.ystd, metrics, arrangedKey);
    var lastwkData = getArrangedData(result.lastwk, metrics, arrangedKey);    

    var keys = isEmpty(ranking_keys) ? Object.keys(todayData) : ranking_keys(todayData);

    // batch insert div for better performance
    var div_array = [];
    keys.forEach(function(key) {
        metrics.forEach(function(metric) {
            var chartdiv = "{0}_{1}_{2}".format(chart.id, metric.series, key);
            div_array.push(get_div(chartdiv, "col-md-6 chart-space-md"));
        });
    });
    insert_content(chart.id, div_array.join(""));

    keys.forEach(function(key) {
        var i = 1;
        metrics.forEach(function(metric) {
            
            // 0 is time, i is specified metric
            var today = todayData[key].map(function(item) {
                return [item[0], item[i]];
            });
            var ystd = (key in ystdData) ? ystdData[key].map(function(item) {
                return [item[0], item[i]];
            }) : null;
            var lastwk = (key in lastwkData) ? lastwkData[key].map(function(item) {
                return [item[0], item[i]];
            }) : null;
            
            var chartdiv = "{0}_{1}_{2}".format(chart.id, metric.series, key);
            var title = isEmpty(convert_title) ? 
                "{0}({1})".format(key, metric.series) : convert_title(key)
            draw({
                'id': chart.id, 
                'title': title,
                'metrics':[metric]
            }, chartdiv, today, ystd, lastwk);

            i++;
        });

    });


}
