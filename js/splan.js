//2:"DAY_START",
var M_TYPE = {0:"EVENT", 1:"DIFF", 3:"BOOTSTRAP", 4:"REPEAT", 5:"SMART", 7:'TOTAL', 8:'THROTTLE_RATE'};
var HEADER = "<tr><th>Time</th><th>ID</th><th>EVENT</th><th>DIFF</th><th>BOOTSTRAP</th><th>REPEAT</th><th>SMART</th><th>TOTAL</th><th>ThrottleRate</th></tr>"

var TEMPLATE = { 
    title: {
        text: 'Budget Spend and Throttle Rate'
    },
    xAxis: [{
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        },
        title: {
            text: 'Time'
        }
    }],
    yAxis:[{
        title: {
           text: 'Budget (Adv Currency)'
        },
        // endOnTick: false,
        // minPadding: 0.1,
        // maxPadding: 0.1,
        // min: 0
    },{
        title: {
           text: 'ThrottleRate'
        },
        opposite: true,
        // endOnTick: false,
        // minPadding: 0.01,
        // maxPadding: 0.00
       	//  max: 1.1,
      	// min: 0
    }],
    plotOptions: {
        bubble: {
            minSize: 1,
            maxSize: 5,
            tooltip: {
            	pointFormat: "{point.y:,.2f}"
            }
        },
        series: {
            point: {
                events: {
                    mouseOver: function () {
                        $('#cap_type').html(this.msg.capType);
                        $('#daily_cap').html(this.msg.dailyCap.toFixed(2));
                        $('#daily_spend').html(this.msg.dailySpend.toFixed(2));
                        $('#managed_by').html(this.msg.managedBy);
                        $('#pacing_type').html(this.msg.pacingType);
                        $('#previous_day_overspend').html(this.msg.previousDayOverspend);
                        $('#timezone').html(this.msg.timezone);

                        var track = this.msg.track;
                        switch (this.msg.track) {
                            case 'SM': 
                                track = 'Search';
                                break;
                            case 'MB':
                                track = 'Native';
                                break;
                        }
                        
                        $('#track').html(track);
                    },
                    mouseOut: function () {
                        // mouse out action
                    }
                }
            }
        }
    },
    tooltip: {
        crosshairs: true,
        pointFormatter: function() {
            var s = '';
            if (this.series.type == 'spline') {
                s += '<br/><span style="color:{0}">\u25CF</span> {1}: <b>{2}</b>'.format(this.color, this.series.name, Highcharts.numberFormat(this.y, 2, '.', ','));
            } else {
                s += '<b> {0}</b>'.format(Highcharts.numberFormat(this.y, 2, '.', ','));
            }
            return s;
        },
        shared: true
    },
    series: [
        { // spend series
            type: "spline",
            name: 'BudgetCap',
            lineWidth: 1,
            yAxis: 0,
            marker: {
                radius: 2
            }
        },
        { // spend series
            type: "spline",
            name: 'Spend',
            lineWidth: 1,
            yAxis: 0,
            marker: {
                radius: 2
            }
        },
        { // throttle rate series
            type: "bubble",
            name: 'Throttle Rate',
            yAxis: 1,
            events: {
                click: function(event) {
                    console.log(event.point.msg);
                }
            },
        }
    ],
    drilldown:{
        series:[]
    },
    chart: {
        zoomType : 'x',
        animation: Highcharts.svg,
        events: {
            load: function() {
            }
        }
    }
};

function do_click(data) {
    function click() {
        console.log(data);
    }
    return click;
}

function show(chart, cache) {
	console.log(cache);
	for(var i in cache) {
		var spends = [];
		var caps = [];
		var throttleRates = [];
		var grid = '<div id="splan_' + i + '"></div>';
		$('#' + chart.id).append(grid);

        var meta = `<div id="metadata_{0}" class="metadata" style="margin-top: 30px">
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Cap Type: </span><div id="cap_type"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Daily Cap: </span><div id="daily_cap"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Daily Spend: </span><div id="daily_spend"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Advertiser/Reseller: </span><div id="managed_by"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Pacing Type: </span><div id="pacing_type"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Previous Day Overspend: </span><div id="previous_day_overspend"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Time Zone: </span><div id="timezone"></div></div>
                        <div class="col-md-3 col-sm-6 col-xs-12"><span>Product Type: </span><div id="track"></div></div>
                    </div>
                    <div id="chart_{0}" style="margin-top: 30px"></div>`.format(i);

        $('#splan_' + i).append(meta);

		var item = cache[i];
		var id = item['id'];
		var type = item['type'];
		var messages = item['value'];
		for(var j in messages) {
			var msg = messages[j];
			var time = parseInt(msg.cacheId) * 1000;
			spends.push({x:time, y:msg.dailySpend, msg:msg});
			caps.push({x:time, y:msg.dailyCap, msg:msg});
			throttleRates.push({x:time, y:msg.trate, z:1, color:color(msg.trate), msg:msg, do_click:do_click(cache)});
		}
		TEMPLATE.series[0].data = caps;
		TEMPLATE.series[1].data = spends;
		TEMPLATE.series[2].data = throttleRates;
		TEMPLATE.title.text = id + " Budget, Spend & Throttle Rate";
		$('#chart_' + i).highcharts(TEMPLATE);
	}

}
