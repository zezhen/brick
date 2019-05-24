
import bconfig, util
import copy
from datetime import datetime, timedelta
import pytz, traceback

SQL_TEMPLATE = 'select {fields} from {table} where time >= convert_tz("{start}", "{timezone}", "Etc/UTC") and time < convert_tz("{end}", "{timezone}", "Etc/UTC") {conditions} {groupby} {orderby} {sort} {limit}'

def execute(appconfig, page, args, process=None):
	navigation = bconfig.load_config(page)

	if navigation['id'] == 'brick':
		return {'error': 'no action for %s' % (page)}

	tabs = navigation['tabs']
	ret = {}
	try:
		for tab in tabs:
			tabid = util.get(args, 'tabid', None)
			if tabid and tabid != tab['id']:
				continue

			query = copy.deepcopy(tab['data'])
			if process:
				query, args = process(query, args)

			ret[tab['id']] = process_tab(appconfig, args, query)
	except Exception as e:
		print "[ERROR]", e
		traceback.print_exc()

	return ret

def get_additional_conditions(args, query):
	conditions = []
	try:
		filters = query['filters'].split(',')
		for fileter in filters:
			if fileter not in args: continue
			conditions.append("%s in (%s)" % (fileter, args[fileter]))
	except:
		print '[WARN] skip filters.'
		pass

	if 'fixed_condition' in query:
		conditions.append(query['fixed_condition'])

	return "".join(map("".join, zip([" and "]*len(conditions), conditions)))

def process_tab(appconfig, args, query):

	ret = {}

	query['timezone'] = util.get(args, 'timezone', 'America/New_York')
	query['conditions'] = get_additional_conditions(args, query)

	start = int(util.get(args, 'start', util.day_start(util.today())))
	now = util.datetime2epic(util.today(query['timezone']))
	end = min(now, int(util.get(args, 'end', now)))

	# data point stored in endtime, 5 minutes offset
	offset_minutes = util.get(query, 'offset_minutes', -5)
	
	ret['today'] = fetch_data(appconfig, query, start, end, util.total_seconds(timedelta(minutes=offset_minutes)))
	strip_len = len(ret['today'])

	if 'true' == query.get('dod'):
		ret['ystd'] = fetch_data(appconfig, query, start, end, util.total_seconds(timedelta(days=1, minutes=offset_minutes)))[:strip_len]
	
	if 'true' == query.get('wow'):
		ret['lastwk'] = fetch_data(appconfig, query, start, end, util.total_seconds(timedelta(days=7, minutes=offset_minutes)))[:strip_len]

	return ret

def fetch_data(appconfig, query, start, end, offset):

	query = copy.deepcopy(query)

	query['start'] = util.time2str(start - offset, util.DATE_ISO)
	query['end'] = util.time2str(end - offset, util.DATE_ISO)

	groupby = query.get('groupby')
	fields = query['fields'].split(',')
	if groupby:
		query['fields'] = ",".join(map(lambda f: 'sum(%s)' % (f) if f not in groupby else f, fields))
		query['groupby'] = "group by " + groupby
	else:
		query['groupby'] = ""

	query['orderby'] = util.get(query, 'orderby', '', lambda x: 'order by ' + x)
	query['sort'] = util.get(query, 'sort', '')
	query['limit'] = util.get(query, 'limit', '', lambda x: 'limit ' + x)

	# support parameters in conditions
	query['conditions'] = query['conditions'].format(**query)

	sql = SQL_TEMPLATE.format(**query)

	offset += util.total_seconds(pytz.timezone(query['timezone']).utcoffset(datetime.utcnow()))
	return util.fetch_data(appconfig, fields, sql, offset)
	