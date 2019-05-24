

function show(chart, result, ranking_keys, convert_title) {

    var metrics = chart.metrics;
    var arrangedKey = chart.arrangedby;

    var todayData = getArrangedData(result.today, metrics, arrangedKey);
    var ystdData = getArrangedData(result.ystd, metrics, arrangedKey);
    var lastwkData = getArrangedData(result.lastwk, metrics, arrangedKey);    

    var keys = isEmpty(ranking_keys) ? Object.keys(todayData) : ranking_keys(todayData);

    // batch insert div for better performance
    var div_array = [];
    var separate = false;
    keys.forEach(function(key) {
        metrics.forEach(function(metric) {
            var chartdiv = "{0}_{1}_{2}".format(chart.id, metric.series, key.replace(new RegExp("\\W+","gm"), "_"));
            // separate: draw dod and wow graphs separately
            if ('separate' in metric && metric.separate == 'true') {
                separate = true;
            }
            if (separate) {
                var dodchartdiv = "{0}_dod".format(chartdiv);
                div_array.push(get_div(dodchartdiv, "col-md-6 chart-space-md"));
                var wowchartdiv = "{0}_wow".format(chartdiv);
                div_array.push(get_div(wowchartdiv, "col-md-6 chart-space-md"));
            } else {
                div_array.push(get_div(chartdiv, "col-md-6 chart-space-md"));
            }
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
            
            var chartdiv = "{0}_{1}_{2}".format(chart.id, metric.series, key.replace(new RegExp("\\W+","gm"), "_"));
            var title = isEmpty(convert_title) ? 
                "{0}({1})".format(key, metric.series) : convert_title(key)
            var separate = ('separate' in metric && metric.separate == 'true') ? true : false;
            if (separate) {
                var dodchartdiv = "{0}_dod".format(chartdiv);
                var wowchartdiv = "{0}_wow".format(chartdiv);
                draw_graph({
                    'id': chart.id, 
                    'title': title,
                    'metrics':[metric]
                }, dodchartdiv, today, ystd, null);
                draw_graph({
                    'id': chart.id, 
                    'title': title,
                    'metrics':[metric]
                }, wowchartdiv, today, null, lastwk);
            } else {
                draw_graph({
                    'id': chart.id, 
                    'title': title,
                    'metrics':[metric]
                }, chartdiv, today, ystd, lastwk);
            }
            i++;
        });

    });


}
