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
            text: 'Date (UTC)'
        }
    }],
    yAxis:[{
        title: {
           text: 'Budget'
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
            	pointFormat: "{point.y}"
            }
        }
    },
    tooltip: {
        crosshairs: true,
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
		// var grid = '<div class="row display output-item">';
		// grid += '<div class="display col-md-12">'
		var grid = '<div id="splan_' + i + '"></div>';
		// grid += '</div>';
		// grid += '</div>';
		$('#' + chart.id).append(grid);

		var item = cache[i];
		console.log(item);
		var id = item['id'];
		var type = item['type'];
		var messages = item['value'];
		for(var j in messages) {
			var msg = messages[j];
			var time = parseInt(msg.cacheId) * 1000;
			spends.push([time, msg.dailySpend]);
			caps.push([time, msg.dailyCap]);
			throttleRates.push({x:time, y:msg.trate, z:1, color:color(msg.trate), msg:msg, do_click:do_click(cache)});
		}
		TEMPLATE.series[0].data = caps;
		TEMPLATE.series[1].data = spends;
		TEMPLATE.series[2].data = throttleRates;
		TEMPLATE.title.text = id + " Budget, Spend & Throttle Rate";

		$('#splan_' + i).highcharts(TEMPLATE);
	}

}
