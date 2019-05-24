String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g,
        function (m, i) {
            return args[i];
        });
};

String.prototype.padLeft = function (width, c) {
    width -= this.length;
    if (width > 0) {
        return (new Array(width + 1).join(c)) + this;
    }
    return this;
};

String.prototype.padRight = function (width, c) {
    width -= this.length;
    if (width > 0) {
        return this + (new Array(width + 1).join(c));
    }
    return this;
};

Date.prototype.format = function(format) {
    var date = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S+": this.getMilliseconds()
    };
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (var k in date) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1
                    ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
        }
    }
    return format;
};



var Commons = function () {
    return { };
};


Commons.MILLIS_PER_SECOND = 1000;
Commons.MILLIS_PER_MINUTE = 60000;
Commons.MILLIS_PER_HOUR = 3600000;
Commons.MILLIS_PER_DAY = 86400000;
Commons.SECONDS_PER_MINUTE = 60;
Commons.SECONDS_PER_HOUR = 3600;
Commons.SECONDS_PER_DAY = 86400;

Commons.ET_OFFSET = -4 * Commons.MILLIS_PER_HOUR;



var Utils = function () {
    return { };
};


Utils.pruneResponse = function (result) {
    var data = result.split('\n');
    while (data.length > 0)
        if (data[0] == '')
            data.shift();
        else
            break;
    while (data.length > 0)
        if (data[data.length - 1] == '')
            data.pop();
        else
            break;
    return data;
};

Utils.pruneJsonResponse = function (result) {
    var data = Utils.pruneResponse(result);
    if (data.length == 0) {
        return null;
    }
    return JSON.parse(data[0]);
};

Utils.partDatetimeString = function (datetimeString) {
    if (typeof datetimeString === 'undefined') {
        return {
            dateString: '(N/A)',
            timeString: '(N/A)'
        }
    }
    return {
        dateString: datetimeString.substr(0, 10),
        timeString: datetimeString.substr(11, 8)
    };
};

Utils.partDatetime = function (datetime) {
    if (!datetime) {
        return Utils.partDatetimeString(undefined);
    }
    return Utils.partDatetimeString((new Date(datetime)).toISOString());
};



var Formatter = function () {
    return { };
};


Formatter.UNLIMITED_CURRENCY_VALUE = 1.0e10;
Formatter.UNLIMITED_CURRENCY_STRING = '(Inf)';
Formatter.EXPONENTIAL_CURRENCY_VALUE = 1.0e8;


Formatter.integer = function (integer) {
    integer = parseInt(integer);
    return integer.toString();
};

Formatter.number = function (number, precision) {
    number = parseFloat(number);
    return number.toFixed(precision);
};

Formatter.currency = function (currency) {
    currency = parseFloat(currency);
    if (currency < Formatter.UNLIMITED_CURRENCY_VALUE) {
        if (currency < Formatter.EXPONENTIAL_CURRENCY_VALUE) {
            return currency.toFixed(2);
        }
        else {
            return currency.toExponential(4);
        }
    }
    return Formatter.UNLIMITED_CURRENCY_STRING;
};

Formatter.datetime = function (datetime) {
    var padding = '0';
    var year = datetime.getFullYear().toString().padLeft(4, padding);
    var month = (datetime.getMonth() + 1).toString().padLeft(2, padding);
    var date = datetime.getDate().toString().padLeft(2, padding);
    var hours = datetime.getHours().toString().padLeft(2, padding);
    var minutes = datetime.getMinutes().toString().padLeft(2, padding);
    var seconds = datetime.getSeconds().toString().padLeft(2, padding);
    return '{0}-{1}-{2} {3}:{4}:{5}'.format(year, month, date, hours, minutes, seconds);
};



var Unformatter = function () {
    return { };
};


Unformatter.datetime = function (datetimeString) {
    var fields = datetimeString.replace(/[-: ]/g, ',').split(',');
    var year = parseInt(fields[0]);
    var month = parseInt(fields[1]) - 1;
    var date = parseInt(fields[2]);
    var hours = fields.length > 3 ? parseInt(fields[3]) : 0;
    var minutes = fields.length > 4 ? parseInt(fields[4]) : 0;
    var seconds = fields.length > 5 ? parseInt(fields[5]) : 0;
    return parseInt(Date.UTC(year, month, date, hours, minutes, seconds) / Commons.MILLIS_PER_SECOND);
};



var Wrapper = function () {
    return { };
};


Wrapper.UNKNOWN_TYPE_FORMAT = '<span class="label label-types label-types-unknown">U</span>';


Wrapper.keyedType = function (type, formats) {
    if ((typeof type === 'undefined') || !type) {
        return Wrapper.UNKNOWN_TYPE_FORMAT;
    }
    type = type.toUpperCase();
    if (type == 'NULL') {
        return Wrapper.UNKNOWN_TYPE_FORMAT;
    }
    return formats[type];
};

Wrapper.indexedType = function (index, formats) {
    if ((typeof index === 'undefined') || (index < 0) || (index >= formats.length)) {
        return Wrapper.UNKNOWN_TYPE_FORMAT;
    }
    return formats[index];
};

Wrapper.upperLiner = function(upperLine, lowerLine) {
    return '<span style="color: #666; font-size: 10px;">{0}</span><br /><span>{1}</span>'
            .format(upperLine, lowerLine);
};

Wrapper.lowerLiner = function(upperLine, lowerLine) {
    return '<span>{0}</span><br /><span style="color: #666; font-size: 10px;">{1}</span>'
            .format(upperLine, lowerLine);
};



// Highcharts global options.
Highcharts.setOptions({
    lang: {
        thousandsSep: ','
    }
});

var loading = function (div_id) {
    $('#' + div_id).html("<img src='/loading_spinner.gif' />");
}

