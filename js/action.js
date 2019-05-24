
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
        insert_button(divid, button_id, function(event, auto) {
            $("#"+outputdiv).html("");
            $('#{0}'.format(button_id)).addClass('disabled');
            
            // insert button group
            var bgid = 'button_group'
            insert_button_group(outputdiv, {'id': bgid, 'navid': navid});

            // insert tab content div
            var tabsid = 'tabs_' + navid
            insert_div(outputdiv, tabsid);

            var tabs = navigation.tabs;
            // there may be multiple tabs under one navigation,
            // use 'showtabs' to control which can show, seperated by comma.
            var showtabs = getUrlParameterByName('showtabs');
            if(!isEmpty(showtabs)) {
                showtabs = new Set(showtabs.split(','));
            } else {
                showtabs = null;
            }
            tabs.forEach(function(tab, i) {
                if(showtabs != null && ! showtabs.has(tab.id))
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
                
                // by default, the tab with the id same as navigation id is active,
                // others are hidden. 'activetab' is to specify the tab at first impression
                var activetab = getUrlParameterByName('activetab');
                if(isEmpty(activetab) && tab.id == navid || tab.id == activetab || 'default' in tab || i == 0) {
                    $("#" + tabid).removeClass("hide");
                    $("#b_" + tabid).addClass("active");
                }
                
                // prepare request parameters
                var dict = {'action': navid};
                layouts.forEach(function(module) {
                    if (module.type == 'group') {
                        // show grouped modules in one group
                        module.data.forEach(function(component) {
                            var value = get_value(component);
                            dict[component.id] = updateParameterValue(tab, component, value, button_id, auto);
                        });
                    } else {
                        var value = get_value(module);
                        dict[module.id] = updateParameterValue(tab, module, value, button_id, auto);
                    }
                });
                var timezone = getUrlParameterByName('timezone');
                if(isEmpty(timezone)) {
                    timezone = get_timezone();
                }
                dict['timezone'] = timezone;
                dict['tabid'] = tab.id;
                function query0() {
                    if(! isEmpty(tab.customized)) {
                        try {
                            load_script("js/{0}.js".format(tab.customized), function() {
                                var param = get_param(tab.id);
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

                    // show tip if the user is querying hive due to slow response.
                    if ('sql' in tab && typeof(tab.sql) != 'string' && 'source' in tab.sql && tab.sql['source'] == 'hive') {
                        $('#' + tabid).append('<h5>Querying data from hive. This may take serveral minutes.</h5>');
                    }
                    $('#' + tabid).append("<img src='images/loading_spinner.gif' style:'text-align:center'/>");                    
                }

                query0();
                if(tab['refresh'] > 0) {
                    tab['refreshIntervalId'] = setInterval(function(){
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
            if(tab.show_onload == 'true') {
                $('#b_' + tabid).trigger('click');    
            }
            data = result[tab.id]
            if(! isEmpty(chart.databody)) {
                data = get_value_by_fields(data, chart.databody);
            }
            _show(chart, dict, data, tab.id);
        });
        
        $('#' + button_id).removeClass('disabled');
    });
}

function _show(chart, requestArgs, result, tabid) {
    if(! isEmpty(chart.render)) {
        load_script("js/{0}.js".format(chart.render), function() {
            show(chart, result);
        });
        return;
    }

    var metrics = chart.metrics;
    if("text" == chart.type) {
        draw_text(chart, result)
    } else if("iframe" == chart.type) {
        draw_iframe(chart, result);
    } else if("hyperlink" == chart.type) {
        draw_hyperlink(chart, result);
    } else if("table" == chart.type) {
        result = getDefaultIfKeyNotExist(result, 'today', result)
        draw_table(chart, requestArgs, result);
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
        
        draw_graph(chart, dodchartdiv, today, ystd, null);
        draw_graph(chart, wowchartdiv, today, null, lastwk);

    } else {
        var today = get_data(metrics, result.today);
        draw_graph(chart, chart.id, today);
    }
}

function get_timezone() {
    var timezone = $('#navddm_timezone > .timezone-option.active').text().trim()
    if(isEmpty(timezone) || timezone == "EST") {
        timezone = "America/New_York";
    } else if(timezone == "LOCAL") {
        timezone = jstz.determine().name();
    }
    return timezone;
}

function updateParameterValue(tab, comp, value, button_id, auto) {

    // if auto is true, this is an auto click, use the args in url as input.
    // if auto is undefined, this is a manually click, use the input values instead.
    if (auto == 'true') {
        value = getUrlParameterByName(comp.id);
        // update the placeholder of input-fields using the values args in url.
        if (!isEmpty(value) && comp.hidden != "true") {
            updateInputPlaceholder(value, comp);
        }
    }
    var divid = "{0}_{1}".format(comp.id, comp.navid);
    var navid = tab['navid'];
    // verify parameter values
    if(isEmpty(value) && "true" == comp.required) {
        // when using url to access the page, make the corresponding page active
        $('#pan_' + navid).removeClass('fade').addClass('active');
        // show errors
        $("#" + divid).addClass('errorClass');
        // hide the button group as well if any error occurs
        $('#button_group_' + navid).hide();
        $('#' + button_id).removeClass('disabled');
        throw new Error("{0} must be provided.".format(comp.name));
    }

    // if the end time is set by the user, disable refreshing the graph
    if (comp.id == 'end' && !isEmpty(value)) {
        if ('refreshIntervalId' in tab) {
            clearInterval(tab['refreshIntervalId']);
        }
        tab['refresh'] = 0;
    }

    $("#" + divid).removeClass('errorClass');
    $('#button_group_' + navid).show();
    switch(comp.type) {
        case 'dateminutepicker':
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