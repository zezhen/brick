
function query(args, func) {
    console.log(args);
    $.get('/query?' + args, function(result) {
        func(result);
    });
}

function encodeMap(data) {
    return Object.keys(data).map(function(key) {
        return [key, data[key]].map(encodeURIComponent).join("=");
    }).join("&");
}

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

if (!String.prototype.formatObject) {
    String.prototype.formatObject = function() {
        var formatted = this;
        var obj = arguments[0];
        for (var key in obj) {
            formatted = formatted.replace("{" + key + "}", obj[key]);
        }
        return formatted;
    };
}

// Speed up calls to hasOwnProperty
var hasOwnProperty = Object.prototype.hasOwnProperty;

function isEmpty(obj) {

    // null and undefined are "empty"
    if (obj == null) return true;

    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }

    return true;
}

// function sleep(ms) {
//   return new Promise(resolve => setTimeout(resolve, ms));
// }

function getDefaultIfNaN(obj, _default) {
    return (obj == null || obj == "" || isNaN(obj)) ? _default : obj
}

function getDefaultIfEmpty(obj, _default) {
    return isEmpty(obj) ? _default : obj;
}

function getDefaultIfOutOfArray(array, i, _default) {
    return array == null || array.length <= i ? _default : array[i];
}

function getDefaultIfNotContain(map, key, _default) {
    return (key != null && key in map) ? map[key] : _default;
}

function getDefaultIfKeyNotExist(object, key, _default) {
    return (key != null && object[key] != undefined) ? object[key] : _default;
}

function getUrlParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function pad(n){return n<10 ? '0'+n : n}

function formatTime(timestamp){
    var d = new Date(timestamp);
    return pad(d.getUTCHours()) + ":" + pad(d.getUTCMinutes()) + ":" + pad(d.getUTCSeconds());
}

function formatDate(timestamp){
    var d = new Date(timestamp);
    return pad(d.getUTCMonth()+1) + '/' + pad(d.getUTCDate()) + " " + pad(d.getUTCHours()) 
    + ":" + pad(d.getUTCMinutes()) + ":" + pad(d.getUTCSeconds());
}

function color(rate) {
    if(rate >= 1) {
        return 'red';
    } else if(rate == 0) {
        return 'limegreen';
    } else if(rate >= 0.85) {
        return 'pink';
    } else {
        return 'lightgreen';
    }
}

function check_time(startTime, endTime) {

    if (! startTime || endTime && startTime > endTime) {
        return 'Please fill start/end time and start < end';
    }

    return null;
}

function check_null(value, name) {
    if (! value) {
        return name + ' is empty!';
    }
    return null;
}

function divide(num1, num2) {
    if(isNaN(num1) || isNaN(num2) || num2 == 0) {
        return 0;
    }
    return num1 / num2;
}

function load_header(force) {
    var header = getUrlParameterByName('header');
    if(force || header == 'true') {
        $('#header').load('index?page=header');
    }
}

function fillStartTime(time) {
    return fillCustomTime(time, getDayStart());
}

function fillCurrentTime(time){
    return fillCustomTime(time, Math.trunc(moment().toDate().getTime() / 1000));
}

function getDayStart() {
    var local_time = moment().startOf('day').format('YYYY-MM-DDTHH:mm:ss');
    return Math.trunc(moment.tz(local_time, 'UTC').toDate().getTime() / 1000);
}

function fillCustomTime(time, customTime) {
    if(isEmpty(time)) {
        return customTime;
    } else if (Number(time)){
        return parseInt(time);
    } else {
        return Math.trunc(moment.tz(time, 'UTC').toDate().getTime() / 1000);
    }
}

function clone(obj) {
    var copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}

function load_script(script_file, callback) {
    try {
        $.getScript(script_file)
            .done(function(module){
                //eval(module);
                console.log('load script {0} succeed.'.format(script_file))
                callback();
            })
            .fail(function( jqxhr, settings, exception ) {
                throw new Error(exception);
            });
    } catch(e) {
        console.log(e);
        callback();
    }
}

function get_value_by_fields(data, multiple_layer_fields_separated_by_dot) {
    return multiple_layer_fields_separated_by_dot.split('.').reduce((o, i) => o[i], data);
}

function get_data(metrics, raw_data) {
    var data = [];
    raw_data.sort(function(a, b) {
        return a.time - b.time;
    });
    raw_data.forEach(function(item) {
        ret = []
        ret.push(item.time);
        var i = 0;
        metrics.forEach(function(metric) {
            var field = metric.field;
            var isFormula = field.match(/[^+/*()-]+/g).length > 1;
            var value = isFormula ? calculate_formula(item, field) : item[field];
            ret.push(value);
            i ++;
        });
        data.push(ret);
    });
    return data;
}

// this is the performance bottleneck
function calculate_formula0(item, _formula) {
    var body = {};
    var i = 1;
    Object.keys(item).forEach(function(key) {
        var newkey = 'A' + i;
        var pattern = "(\\s|-|\\+|^|\\*|\\/){0}(\\s|-|\\+|$|\\*|\\/)".format(key);
        _formula = _formula.replace(new RegExp(pattern, 'g'), newkey);
        body[newkey] = {'value': item[key]};
        i += 1;
    });
    var resid = 'R1';
    body[resid] = {'formula': _formula}
    $('#calx_div').calx({'data' : body});
    var value = $('#calx_value').val();
    $('#calx_div').calx('destroy')
    return parseFloat(value);
}

function parseCalculationString(s) {
  // --- Parse a calculation string into an array of numbers and operators
  var calculation = [], current = '';
  for (var i = 0, ch; ch = s.charAt(i); i++) {
    if ('^*/+-'.indexOf(ch) > -1) {
      if (current == '' && ch == '-') {
        current = '-';
      } else {
        calculation.push(current.trim(), ch);
        current = '';
      }
    } else {
      current += s.charAt(i);
    }
  }
  if (current != '') {
    calculation.push(current.trim());
  }
  return calculation;
}

function calculate_formula(item, formula) {
  var calc = parseCalculationString(formula);
  // --- Perform a calculation expressed as an array of operators and numbers
  function parse(v) {
    var ret = (isFloat(parseFloat(v)) || isInt(parseInt(v))) ? v : item[v];
    return ret;
  }
  var ops = ['^', '*', '/', '+', '-'],
    opFunctions = [
      function(a, b) {  
        return Math.pow(parse(a), parse(b));
      },

      function(a, b) {
        return parse(a) * parse(b)
      },

      function(a, b) {
        var bb = parse(b);
        if (bb < 1e-5 && bb > -1e-5) {
           return 0.0;
        }
        return parse(a) / parse(b)
      },

      function(a, b) {
        return parse(a) + parse(b)
      },

      function(a, b) {
        return parse(a) - parse(b)
      }
    ],
    newCalc = [],
    currentOp;
  for (var i = 0; i < ops.length; i++) {
    for (var j = 0; j < calc.length; j++) {
      if (calc[j] == ops[i]) {
        currentOp = opFunctions[i];
      } else if (currentOp) {
        newCalc[newCalc.length - 1] = currentOp(newCalc[newCalc.length - 1], calc[j]);
        currentOp = null;
      } else {
        newCalc.push(calc[j]);
      }
    }
    calc = newCalc;
    newCalc = [];
  } 
  if (calc.length > 1) {
    console.log('Error: unable to resolve calculation');
    return calc;
  } else {
    return calc[0];
  }
}

function getArrangedData(data, metrics, arrangingKey) {
    var ret = {};
    data.forEach(function(item) {
        var arrKey = item[arrangingKey];
        if(!(arrKey in ret)) {
            ret[arrKey] = [];
        }

        ret[arrKey].push(get_data(metrics, [item])[0]);
    });
    return ret;
}

function isInt(n){
    return Number(n) === n && n % 1 === 0;
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}

function updateDateTimePicker(timezone) {
    var dateTimeConfig = getDateTimePickerConfig(timezone);
    config.navigations.forEach(function(navigation){
        if(!('layouts' in navigation)) {
            // nav dropdown
            return;
        }
        var navid = navigation.id;
        $("#start_" + navid).datetimepicker('remove');
        $("#end_" + navid).datetimepicker('remove');
        $("#start_" + navid).datetimepicker(dateTimeConfig);
        $("#end_" + navid).datetimepicker(dateTimeConfig);
    }); 
}

function isNumeric(num){
    return !isNaN(num)
}

// convert epoch time to iso format yy-mm-ddThh:mm
function epicToISODate(value) {
    var date = new Date(value * 1000).toISOString().substring(0, 16);
    return date;
}

function updateInputPlaceholder(value, component) {
    var id = get_id_w_navid(component);
    switch(component['type']) {
        case 'dropdown':
            $('#' + id + ' > button:first').html(value);
            break;
        case 'dateminutepicker':
        case 'datetimepicker':
        case 'datepicker':
            value = epicToISODate(value);
        case 'field':
            $('#' + id).attr('value', value);
            break;
        default:
            break;
    }
}
