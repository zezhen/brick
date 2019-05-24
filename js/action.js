
function load_config(config) {
    navigations = config.navigations;
    navigations.forEach(function(navigation) {
        insert('nav_', navigation);
        var navid = navigation.id;

        if(!('layouts' in navigation)) {
            // nav dropdown
            return;
        }

        var divid = 'layout_' + navid;

        var layouts = navigation.layouts;
        layouts.forEach(function(module) {
            module['navid'] = navid;
            insert(divid, module);
        });

        var outputdiv = 'output_' + navid;
        var button_id = 'button_' + navid;
        insert_button(divid, button_id, function() {
            $("#"+outputdiv).html("");
            $('#{0}'.format(button_id)).addClass('disabled');

            // insert button group
            var bgid = 'button_group'
            insert_button_group(outputdiv, {'id': bgid, 'navid': navid});

            // insert tab content div
            var tabsid = 'tabs_' + navid
            insert_div(outputdiv, tabsid);

            var tabs = navigation.tabs;
            var requiredTabs = getParameterByName('tabs');
            if(!isEmpty(requiredTabs)) {
                requiredTabs = new Set(requiredTabs.split(','));
            } else {
                requiredTabs = null;
            }
            tabs.forEach(function(tab) {
                if(requiredTabs != null && ! requiredTabs.has(tab.id))
                {
                    return;
                }
                // insert each tab div
                tab['type'] = 'rtab';
                tab['navid'] = navid;
                tab['bgid'] = bgid;
                insert(tabsid, tab);

                var tabid = get_id_w_navid(tab);
                $("#" + tabid).addClass("hide");
                
                var showtab = getParameterByName('tab');
                if(isEmpty(showtab) && tab.id == navid || tab.id == showtab) {
                    $("#" + tabid).removeClass("hide");
                }
                
                // prepare request parameters
                var dict = {'action': navid};
                layouts.forEach(function(module) {
                    var value = get_value(module);
                    dict[module.id] = verify(module, value, button_id);
                });
                dict['timezone'] = get_timezone();
                dict['tabid'] = tab.id;
                
                function query0() {
                    if(! isEmpty(tab.customized)) {
                        try {
                            load_script("js/{0}.js".format(tab.customized), function() {
                                var param = get_param(tab.customized);
                                if(! isEmpty(param)) {
                                     $.extend(dict, param);
                                }
                                _query(dict, tab, button_id);   
                            });
                        } catch(err) {
                            console.log(err);
                        }
                    } else {
                        _query(dict, tab, button_id);
                    }
                    $('#' + tabid).html("<img src='images/loading_spinner.gif' style:'text-align:center'/>");                    
                }

                query0();
                if(tab['refresh'] > 0) {
                    setInterval(function(){
                        if($('#pan_' + navid).hasClass('active')) {
                            query0();
                        }
                    }, tab['refresh'] * 1000);
                }
            });
        });
        insert_div(divid, outputdiv);
    });
}

function _query(dict, tab, button_id) {
    var args = encodeMap(dict);
    var tabid = get_id_w_navid(tab);

    query(args, function(result) {
        $('#' + tabid).html("");
        console.log(result);
        
        // batch insert div for better performance
        var div_array = [];
        tab.charts.forEach(function(chart) {
            div_array.push(get_div(chart.id));
        });
        insert_content(tabid, div_array.join(""));

        tab.charts.forEach(function(chart) {
            _show(chart, result[tab.id]);
        });
        
        $('#' + button_id).removeClass('disabled');
    });
}

function _show(chart, result) {
    if(! isEmpty(chart.render)) {
        load_script("js/{0}.js".format(chart.render), function() {
            show(chart, result);
        });
        return;
    }

    var metrics = chart.metrics;
    if("table" == chart.type) {
        draw_table(chart, result.today, chart.id);
    } else if("true" == chart.dodwow) {

        // batch insert div for better performance
        var div_array = [];
        var dodchartdiv = "{0}_dod".format(chart.id);
        div_array.push(get_div(dodchartdiv, "col-md-6 chart-space-md"));
        var wowchartdiv = "{0}_wow".format(chart.id);
        div_array.push(get_div(wowchartdiv, "col-md-6 chart-space-md"));
        insert_content(chart.id, div_array.join(""));

        var today = get_data(metrics, result.today);
        var ystd = get_data(metrics, result.ystd);
        var lastwk = get_data(metrics, result.lastwk);
        
        draw(chart, dodchartdiv, today, ystd, null);
        draw(chart, wowchartdiv, today, null, lastwk);

    } else {
        var today = get_data(metrics, result.today);
        draw(chart, chart.id, today);
    }
}

function get_timezone() {
    var timezone = $('.timezone > .btn.active').text().trim()
    if(isEmpty(timezone) || timezone == "EST") {
        timezone = "America/New_York";
    } else if(timezone == "LOCAL") {
        timezone = jstz.determine().name();
    }
    return timezone;
}

function verify(comp, value, button_id) {
    var divid = "{0}_{1}".format(comp.id, comp.navid);
    if(isEmpty(value) && "true" == comp.required) {
        $("#" + divid).addClass('errorClass')
        $('#' + button_id).removeClass('disabled');
        throw new Error("{0} must be provided.".format(comp.name));
    }

    $("#" + divid).removeClass('errorClass')
    switch(comp.type) {
        case 'datetimepicker':
        case 'datepicker':
            if(comp.id == 'start') {
                return fillStartTime(value)
            } else {
                return fillCurrentTime(value)
            }
        default:
            return getDefaultIfEmpty(value, 'all').toLowerCase();
    }
    return value.toLowerCase();
}