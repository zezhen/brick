
var datetimepicker_config = {
    format: 'yyyy-mm-ddThh:00',
    todayBtn: 1,
    autoclose: 1,
    minView: 'day',
    endDate: moment.utc().toDate(),
    language: 'en',
    datepicker: true,
    timepicker: false,
    hourStep: 1,
    // minuteStep: 15,
    inputMask: true
};

var datepicker_config = {
    format: 'yyyy-mm-ddT00:00',
    todayBtn: 1,
    autoclose: 1,
    endDate: moment.utc().toDate(),
    language: 'en',
    datepicker: true,
    dayStep: 1,
    inputMask: true
};

function get_value(component) {
    var id = "{0}_{1}".format(component['id'], component['navid']) ;
    switch(component['type']) {
        case 'datetimepicker':
        case 'datepicker':
        case 'field':
            return $('#{0}'.format(id)).val();
        case 'dropdown':
            return $('#{0} button:first'.format(id)).text();
        default:
            return null;
    }
}

function insert(divid, component) {
    switch(component['type']) {
        case 'datetimepicker':
            insert_datetimepicker(divid, component); break;
        case 'datepicker':
            insert_datepicker(divid, component); break;
        case 'dropdown':
            insert_dropdown(divid, component); break;
        case 'field':
            insert_field(divid, component); break;
        case 'navtab':
            var prefix = divid;
            if('navdropdown' in component) {
                divid = 'navddm_' + component.navdropdown;
            } else {
                divid = prefix + 'bar';
            }
            insert_navtab(divid, component); 
            insert_navcontent(prefix + 'content', component);
            break;
        case 'navdropdown':
            insert_navdropdown(divid + 'bar', component); break;
        case 'html':
            insert_html(divid, component); break;
        case 'button_group':
            insert_button_group(divid, component); break;
        case 'rtab':
            insert_rtab(divid, component); break;
        default:
            // console.log('unknown type ' + component['type']);
            break;
    }
}

function get_div(divid, additionalClass) {
    if(isEmpty(additionalClass)) {
        additionalClass="";
    }
    
    var div = '<div id="{0}" class="display {1}" cellspacing="0"></div>'.format(divid, additionalClass);
    return div;
}

function insert_div(insert_id, divid, additionalClass) {
    var div = get_div(divid, additionalClass);
    $('#' + insert_id).append(div);
}

function insert_content(insert_id, content) {
    $('#' + insert_id).append(content);
}

function insert_html(insert_id, html) {
    $('#' + insert_id).load(html.file);
}

function insert_navtab(insert_id, navdropdown) {
    var div = '<li class=""><a id="nav_{0}" href="#pan_{0}" data-toggle="tab">{1}</a>'.format(navdropdown.id, navdropdown.name);
    $('#' + insert_id).append(div);
}

function insert_navdropdown(insert_id, navtab) {
    var div = `<li id="nav_{0}" class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
          {1}<b class="caret"></b>
        </a>
        <ul id="navddm_{0}" class="dropdown-menu"></ul>
    </li>`.format(navtab.id, navtab.name);
    $('#' + insert_id).append(div);
}

function insert_navcontent(insert_id, navcontent) {
    // <div class="panel panel-default panel-top-fixed">
    // <div class="panel-body">
    var div = `<div class="tab-pane fade" id="pan_{0}">
        
          <div class="container" id="layout_{0}"></div>
        
    </div>`.format(navcontent.id);
    $('#' + insert_id).append(div);
}

function insert_datepicker(div, dt_picker) {
    var dtid = get_id_w_navid(dt_picker);
    var picker_layout = '<div class="input-field"><label for="{0}" class="control-label">{1}</label><input type="text" id="{0}" placeholder="{2}" /></div>'.format(dtid, dt_picker.name, getDefaultIfEmpty(dt_picker.placeholder,""))
    $('#' + div).append(picker_layout);
    $('#' + dtid).datepicker(datepicker_config);
}

function insert_datetimepicker(div, dt_picker) {
    var dtid = get_id_w_navid(dt_picker);
    var picker_layout = '<div class="input-field"><label for="{0}" class="control-label">{1}</label><input type="text" id="{0}" placeholder="{2}" /></div>'.format(dtid, dt_picker.name, getDefaultIfEmpty(dt_picker.placeholder,""))
    $('#' + div).append(picker_layout);
    $('#' + dtid).datetimepicker(datetimepicker_config);
}

function insert_field(div, field) {
    var fid = get_id_w_navid(field);
    var field_layout = `<div class="input-field"> 
            <label for="{0}" class="control-label">{1}</label> 
            <input type="text" id="{0}" placeholder="{2}" /> 
            </div>`.format(fid, field.name, getDefaultIfEmpty(field.placeholder,""));
    $('#' + div).append(field_layout);
}

function insert_dropdown(div, dropdown) {
    var list = [];
    var first = null;
    dropdown.items.split(',').forEach(function(item) {
        var style = "";
        if(first == null) {
            style = 'style="font-weight: bold;"'
            first = item;
        }
        list.push('<li role="presentation"><a href="#" {1}>{0}</a></li>'.format(item, style));
    });

    var dpid = get_id_w_navid(dropdown);
    var dropdown_layout = `<div class="input-field"> 
      <label for="product" class="control-label">{1}</label>
      <div class="btn-group" id="{0}">
       <button type="button" class="btn btn-default">{2}</button>
       <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
        <span class="caret"></span> <span class="sr-only">Toggle Dropdown</span> </button> 
       <ul class="dropdown-menu" role="menu">
           {3}
       </ul>
      </div> 
     </div>`.format(dpid, dropdown.name, first, list.join(''));

    $('#' + div).append(dropdown_layout);

    $('#' + dpid + ' .dropdown-menu li').click(function () {
        var val = $(this).text();
         $('#' + dpid + ' button:first').text(val);
    });
}

function insert_button(div, id, callback) {
    var button = '<button class="btn btn-primary" data-loading-text="Querying" id="{0}">Submit</button>'.format(id);
    $('#' + div).append(button);
    $('#' + id).click(function () {
        callback();
    });
}

function insert_button_group(insert_id, button_group) {
    var bgid =get_id_w_navid(button_group);
    var bgroup = '<br /><div class="btn-group alignleft30" id="{0}" data-toggle="buttons"></div><hr />'.format(bgid);
    $('#' + insert_id).append(bgroup);
}

function insert_button_label(insert_id, button_label) {
    var blid = get_id_w_navid(button_label);
    var bldiv = '<label id="{0}" class="btn btn-default"><input type="radio">{1}</label>'.format(blid, button_label.name);
    $('#' + insert_id).append(bldiv);
}

function insert_rtab(insert_id, rtab) {
    var bgid = "{0}_{1}".format(rtab.bgid, rtab.navid);
    var rtabid = get_id_w_navid(rtab);

    insert_button_label(bgid, {'id':'b_' + rtab.id, 'navid': rtab.navid, 'name':rtab.name})

    insert_div(insert_id, rtabid);
    var blid = "{0}_{1}".format('b_' + rtab.id, rtab.navid);
    $('#' + blid).click(function() {

        // $("#{0} > label".format(bgid)).each(function(i){
        var labels = $(this).parent().children('label');
        labels.each(function(i) {
            var label = labels[i];
            $(label).removeClass('active');
        });
        $(this).removeClass('hide');
        $(this).addClass('active');

        // sleep 1 second waitting layout render
        setTimeout(function() {
            $("#{0} .highcharts-container".format(rtabid)).each(function(){
                var div = $(this).parent();
                var height = $(div).height();
                var width = $(div).width();
                // get highchart object
                $(div).highcharts().setSize(width, height, doAnimation = true);
            });
        }, 10);
        
        var tabs = $('#' + rtabid).parent().children('div');
        tabs.each(function(i) {
            var tab = tabs[i];
            $(tab).addClass('hide');
        });
        $('#' + rtabid).removeClass('hide');
    });
}

function insert_table(insert_id, table_id) {
    var table = '<table id="{0}" class="display output-graph" cellspacing="0" width="100%"></table>'.format(table_id);
    $('#' + insert_id).append(table);
}

function get_id_w_navid(comp) {
    return "{0}_{1}".format(comp.id, comp.navid);
}