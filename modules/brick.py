
import bconfig, util
import copy
from datetime import datetime, timedelta
import pytz, traceback
import importlib
import threading
import re

SQL_TEMPLATE = 'select {fields} from {table} where time >= convert_tz("{start}", "{timezone}", "Etc/UTC") and time < convert_tz("{end}", "{timezone}", "Etc/UTC") {conditions} {groupby} {orderby} {sort} {limit}'

HIVE_TEMPLATE = 'select {fields} from {table} where {partition} >= "{start}" and {partition} < "{end}" {conditions} {groupby} {orderby} {sort} {limit}'

SQL_JOIN_TEMPLATE = '''
					select {fields} from 
						(select {raw_fields_t1} from {table1} 
						where time >= convert_tz("{start}", "{timezone}", "Etc/UTC") 
							and time < convert_tz("{end}", "{timezone}", "Etc/UTC") 
							{conditions_t1} 
						{groupby_t1}) {table1}
						
						join
						
						(select {raw_fields_t2} from {table2} 
						where
							1 = 1
							{conditions_t2} 
						{groupby_t2}) {table2}
						
						on {table1}.{join_field_t1} = {table2}.{join_field_t2}
					where
						1 = 1
						{conditions}
					{groupby}
					{orderby} {sort}
					{limit}
					'''


class api(object):
	
	def execute(self, appconfig, query, args):
		url = query['url'].format(**args)
		yca = query.get('yca')
		return util.fetch_api_data(appconfig, url, yca)

class sql(object):

	def execute(self, appconfig, query, args):
		ret = {}

		start, end, timezone = util.parseTime(args)

		self.parallel = util.get(query, 'parallel', 'false')
		self.threads = []
		query['timezone'] = timezone
		query['conditions'] = self.get_additional_conditions(args, query)

		offset_minutes = util.get(query, 'offset_minutes', 0)
		
		self.fetch_data(appconfig, query, args, start, end, util.total_seconds(timedelta(minutes=offset_minutes)), ret, 'today')

		if 'true' == query.get('dod'):
			self.fetch_data(appconfig, query, args, start, end, util.total_seconds(timedelta(days=1, minutes=offset_minutes)), ret, 'ystd')
		
		if 'true' == query.get('wow'):
			self.fetch_data(appconfig, query, args, start, end, util.total_seconds(timedelta(days=7, minutes=offset_minutes)), ret, 'lastwk')

		if self.parallel and len(self.threads) > 0:
			for t in self.threads:
				t.join()

		return ret

	def get_additional_conditions(self, args, query):
		conditions = []
		try:
			filters = query['filters'].split(',')
			for filter in filters:
				if filter not in args: continue
				conditions.append("%s in (%s)" % (filter, args[filter]))
		except:
			print('[WARN] skip filters.')
			pass

		if 'fixed_condition' in query:
			conditions.append(query['fixed_condition'])

		return "".join(map("".join, zip([" and "]*len(conditions), conditions)))
	
	def fetch_data(self, appconfig, query, args, start, end, offset, data, _type):
		if self.parallel == 'true':
			t = threading.Thread(target=self.fetch_data0, args = (appconfig, query, args, start, end, offset, data, _type))
			t.start()
			self.threads.append(t)
		else:
			self.fetch_data0(appconfig, query, args, start, end, offset, data, _type)

	def fetch_data0(self, appconfig, query, args, start, end, offset, data, _type):

		query = copy.deepcopy(query)

		dateformat = util.get(query, 'dateformat', util.DATE_ISO)
		query['dateformat'] = util.convert_date_format(dateformat)
			
		# timezone_switch_aware_offset is used to make time align in graph
		adjusted_offset = util.timezone_switch_aware_offset(start, offset, query['timezone'])
		groupby = query.get('groupby')
		fields = query['fields'].split(',')
		if groupby:
			query['fields'] = ",".join(map(lambda f: 'sum(%s) as %s' % (f,f) if(f not in groupby and not re.match(" as ", f, re.IGNORECASE)) else f, fields))
			query['groupby'] = "group by " + groupby
		else:
			query['groupby'] = ""

		query['orderby'] = util.get(query, 'orderby', '', lambda x: 'order by ' + x)
		query['sort'] = util.get(query, 'sort', '')
		query['limit'] = util.get(query, 'limit', '', lambda x: 'limit ' + x)

		# support parameters in conditions
		query['conditions'] = query['conditions'].format(**query)

		query['partition'] = util.get(query, 'partition', 'ds')
		
		# support parameters to join 2 tables
		join = util.get(query, 'join', None)
		join_to = None
		if join:
			join_to = util.get(join, 'join_to', None)
			if join_to:
				query['table1'] = util.get(query, 'table', None)
				query['groupby_t1'] = "group by " + util.get(join, 'groupby', '')
				query['conditions_t1'] = self.get_additional_conditions(args, join)
				query['raw_fields_t1'] = ",".join(map(lambda f: 'sum(%s) as %s' % (f,f) if(f not in query['groupby_t1'] and not re.match(" as ", f, re.IGNORECASE)) else f, join['raw_fields'].split(',')))
				query['join_field_t1'] = util.get(join, 'on', None)
				
				query['table2'] = util.get(join_to, 'table', None)
				query['groupby_t2'] = "group by " + util.get(join_to, 'groupby', '')
				query['conditions_t2'] = self.get_additional_conditions(args, join_to)
				query['raw_fields_t2'] = ",".join(map(lambda f: 'sum(%s) as %s' % (f,f) if(f not in query['groupby_t2'] and not re.match(" as ", f, re.IGNORECASE)) else f, join_to['raw_fields'].split(',')))
				query['join_field_t2'] = util.get(join_to, 'on', None)
			
			
		offset_w_timezone = adjusted_offset + util.getOffsetSeconds(start, query['timezone'])
		if util.get(query, 'source', None) == 'hive':
			query['start'] = util.time_to_utc(start - offset, dateformat, query['timezone'])
			query['end'] = util.time_to_utc(end - offset, dateformat, query['timezone'])
			sql = HIVE_TEMPLATE.format(**query)
			res = util.fetch_hive_data(appconfig, fields, sql, offset_w_timezone)
		else:
			#query['start'] & query['end'] need to be in timezone-free format, 
			#because SQL_TEMPLATE will convert it to timezone-specific time
			query['start'] = util.time2str(start - offset, dateformat)
			query['end'] = util.time2str(end - offset, dateformat)
			if join and join_to:
				sql = SQL_JOIN_TEMPLATE.format(**query)
			else:
				sql = SQL_TEMPLATE.format(**query)
			res = util.fetch_sql_data(appconfig, fields, sql, offset_w_timezone)

		data[_type] = res


def _execute(appconfig, query, args, fetcher):
	return eval(fetcher)().execute(appconfig, query, args)

def execute(appconfig, page, args):
	navigation = bconfig.load_config(page)
	if navigation['id'] == 'brick':
		return {'error': 'no action for %s' % (page)}

	tabs = navigation['tabs']
	ret = {}
	
	try:
		module = importlib.import_module(page)
	except Exception as e:
		print(e)
		print('[INFO] no module %s function found' % (page))
		module = None

	try:
		for tab in tabs:
			tabid = util.get(args, 'tabid', None)
			if tabid and tabid != tab['id']: continue

			for fetcher in ['sql', 'api', 'hive']:
				if fetcher not in tab: continue

				query = copy.deepcopy(tab[fetcher])

				if module and hasattr(module, 'preexecute'):
					query, args = module.preexecute(appconfig, query, args)

				if module and hasattr(module, 'execute'):
					data = module.execute(appconfig, query, args, fetcher)
				else:
					data = _execute(appconfig, query, args, fetcher)

				if module and hasattr(module, 'postexecute'):
					data = module.postexecute(appconfig, query, args, data)

			ret[tabid] = data
			break
				
	except Exception as e:
		print("[ERROR]", e)
		traceback.print_exc()

	return ret
