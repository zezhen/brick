
function stack_tooltip_formatter(xaixs, points) {
    var len = points.length;

    var htmls = ['<span style="font-size: 10px;">{0}</span><br />'
            .format(Highcharts.dateFormat('%A, %b %e, %H:%M', xaixs))];

    htmls.push('<table>');
    [0,1].forEach(function(s) {
        var sum = 0;
        for(var i = s; i < len; i += 2) {
            var metric = points[i];
            
            if(typeof(metric) != 'undefined') {
                htmls.push('<tr><td><span style="color:{0}">\u25CF</span> {1}</td><td style="text-align: right;"><b>{2}</b></td></tr>'
                            .format(metric.series.color, metric.series.options.id, Highcharts.numberFormat(metric.y, 2)));
                sum += metric.y;
            }
        }
        htmls.push('<tr><td>Total</td><td style="text-align: right; font-size: 18px;"><b>{0}</b></td></tr>'
                .format(Highcharts.numberFormat(sum, 2)));
    });

    htmls.push('</table>');
    return htmls.join("");
}

function dodwow_tooltip_formatter(xaixs, points) {
    
    var htmls = ['<span style="font-size: 10px;">{0}</span><br />'
            .format(Highcharts.dateFormat('%A, %b %e, %H:%M', xaixs))];

    htmls.push('<table>');

    // if points length is odd, then we suppose the metric per minutes and daily accumulated
    // are exist at same time, it cannot handle the scenario that show 4 metrics.
    var indexs = (points.length % 2 == 0) ? [0, 1] : [0];
    var step = indexs.length;

    indexs.forEach(function(i) {
        var currentP = points[i];
        
        htmls.push('<tr><td><span style="color:{0}">\u25CF</span> {1}</td><td colspan="2" style="text-align: right; font-size: 18px;"><b>{2}</b></td></tr>'
                        .format(currentP.series.color, currentP.series.options.id, Highcharts.numberFormat(currentP.y, 2)));
        
        for(var j = i + step; j < points.length; j += step) {
            var previousP = points[j];
            var nrtDiffsColor = '#333333';
            try {
                nrtDiffsColor= currentP.y > previousP.y
                    ? '#5cb85c'
                    : (currentP.y < previousP.y
                            ? '#d9534f'
                            : '#333333');
                htmls.push('<tr><td><span style="color:{0}">\u25CF</span> {1}</td><td style="text-align: right;"><b>{2}</b></td><td style="text-align: right; color: {3};">(<b>{4}</b>)</td></tr>'.format(previousP.series.color, previousP.series.options.id, Highcharts.numberFormat(previousP.y, 2), nrtDiffsColor, Highcharts.numberFormat(currentP.y - previousP.y, 2)));
            } catch(e) {
                console.log(e);
            }
            
        }
    });

    htmls.push('</table>');
    return htmls.join("");
}

function fit_chart(_title, _series, _yAxis, _formatter, _stacking) {
    return {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: _title
        },
        credits: {
            text: location.hostname,
            href: '#',
            enabled: false
        },
        exporting: {
            enabled: false
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%b %e',
                week: '%b %e',
                month: '%Y-%m',
                year: '%Y-%m-%e'
            },
            //maxZoom: Commons.MILLIS_PER_HOUR,
        },
        yAxis: _yAxis,
        tooltip: {
            shared: true,
            crosshairs: true,
            borderColor: '#333333',
            useHTML: true,
            formatter: function () {
                return _formatter(this.x, this.points);
            }
        },
        legend: {
            enabled: true,
            floating: true,
            x: 60,
            y: 35,
            align: 'left',
            layout: 'vertical',
            verticalAlign: 'top',
        },
        plotOptions: {
            area: {
                stacking: _stacking,
                fillOpacity: 0.3,
                lineWidth: 0.5,
                marker: {
                    enabled: false
                },
                shadow: false,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            },
            line: {
                stacking: _stacking,
                fillOpacity: 0.3,
                lineWidth: 2,
                marker: {
                    enabled: false
                },
                shadow: false,
                states: {
                    hover: {
                        lineWidth: 3
                    }
                },
                threshold: null
            }
        },
        series: _series
    };
}

function fit_yaxis(_yAxis, chart) {
    _yAxis.push(
        {
            title: {
                text: 'Minutes Amount'
            },
            min: 0
        }
    );

    _yAxis.push(
        {
            title: {
                text: 'Daily Accumulated Amount'
            },
            min: 0,
            opposite: true
        }
    );

}

function fit_series(_series, chart, data) {
    var i = 1;

    var granularity = chart.granularity == 'undefined' ? 300 : chart.granularity * 60;
    chart.metrics.forEach(function(metric) {
        var values = [], sums = [], accumulated = 0;

        var previousTime = null;
        data.forEach(function(item) {
            var time = item[0] * 1000;
            if(previousTime == null) {
                previousTime = time;
            }
            while(time > previousTime + granularity * 1000) {
                previousTime += granularity * 1000;
                values.push([previousTime, 0]);
            }
            values.push([time, item[i]]);
            if(formatTime(time) == '00:00:00') {
               accumulated = 0;
            }
            accumulated += item[i];
            sums.push([time, accumulated]);
            previousTime = time;
        });
        i += 1;

        _series.push({
            type: metric.type,
            name: metric.series,
            id: metric.series,
            color: metric.color,
            tooltip: {
                valueDecimals: 2
            },
            data: values
        });

        var accumulated = ! (('accumulation' in metric) && metric['accumulation'] == 'false');
        var accumulated_metric = "Accmulated " + metric.series;
        _series.push({
            type: 'line',
            name: accumulated_metric,
            id: accumulated_metric,
            color: metric.color,
            yAxis: 1,
            visible: accumulated,
            tooltip: {
                valueDecimals: 2,
            },
            data: sums
        });
    });
}

function get_single_chart(chart, data, formatter) {
    var _series = [], _yAxis = [];
    fit_yaxis(_yAxis, chart);
    fit_series(_series, chart, data);
    var stacking = chart.stack == "true" ? 'normal' : null;
    return fit_chart(chart.title, _series, _yAxis, formatter, stacking);
}

function get_dod_wow_chart(chart, today, ystd, lastwk, formatter) {
    
    var _series = [], _yAxis = [];

    fit_yaxis(_yAxis, chart);

    var tchart = clone(chart);
    tchart.metrics.forEach(function(metric) {
        metric.color = "#555555";
        metric.series = "{0} {1}".format("Today", metric.series);
    });
    fit_series(_series, tchart, today);

    if(! isEmpty(ystd)) {
        var lchart = clone(chart);
        lchart.metrics.forEach(function(metric) {
            metric.color = "#7cb5ec";
            metric.series = "{0} {1}".format("Ystd ", metric.series);
        });
        fit_series(_series, lchart, ystd);
    }

    if(! isEmpty(lastwk)) {
        var lchart = clone(chart);
        lchart.metrics.forEach(function(metric) {
            metric.color = "#f7a35c";
            metric.series = "{0} {1}".format("LastWk ", metric.series);
        });
        fit_series(_series, lchart, lastwk);
    }

    var highchart = fit_chart(chart.title, _series, _yAxis, formatter);
    highchart.legend.enabled=false;
    return highchart;
}

function draw(chart, divid, today, ystd, lastwk) {

    var dod = ! isEmpty(ystd);
    var wow = ! isEmpty(lastwk);

    var hightchart;
    if(! (dod || wow)) {
        hightchart = get_single_chart(chart, today, stack_tooltip_formatter);
    } else {
        hightchart = get_dod_wow_chart(chart, today, ystd, lastwk, dodwow_tooltip_formatter); 
    }
    
    $("#"+divid).highcharts(hightchart);
    // chart.chart.renderTo=divid;
    // new Highcharts.Chart(chart)
}

function draw_table(chart, data, divid) {

    var tableid = divid + "_table";
    insert_table(divid, tableid);

    var fields = chart.fields.split(',');
    var columns = chart.columns.split(',');
    
    var _dataset = [];
    data.forEach(function(item) {
        var arr = [];
        fields.forEach(function(f) {
            var value = item[f];
            if(f == 'time') {
                value = formatDate(value);
            } else if(isFloat(value)) {
                value = value.toFixed(2);
            }
            arr.push(value);
        });
        _dataset.push(arr);
    });

    var _columns = [];
    columns.forEach(function(c) {
        _columns.push({'title': c});
    });

    var _order = [];
    try{
        var order = chart.order.split(',');
        var seq = order[0];
        order.slice(1).forEach(function(i){
            _order.push([i, seq]);
        });
    } catch(e){}
    

    var _invisible = [];
    try {
        chart.invisible.split(',').forEach(function(item) {
            _invisible.push(parseInt(item, 10));
        });
    } catch(e){}
    
    var _unsearchable = [];
    try {
        _unsearchable = chart.unsearchable.split(',').map(function(item) {
            return parseInt(item, 10);
        });
    } catch(e){}

    $('#'+tableid).empty();
    $('#'+tableid).DataTable( {
        data: _dataset,
        columns: _columns,
        destroy: true,
        dom: 'Bflrtip',
        buttons: [
            'copy', 'csv'
        ],
        columnDefs: [
            {
                "targets": _unsearchable,
                "visible": false,
                "searchable": false
            },
            {
                "targets": _invisible,
                "visible": false,
                "searchable": true
            }
        ],
        "iDisplayLength": 25,
        "order": _order
    } );
    
}