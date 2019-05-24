import brick, splan

def preexecute_nrt_oda(query, args):
	otype = args.get('type')
	if 'campaign' == otype:
		field = 'campaign_id'
	args[field] = args['id']
	return (query, args)

def preexecute_nrt(query, args):
	otype = args.get('type')

	if 'campaign' == otype:
		table = '5m_cmp_spend'
		field = 'cmp_id'
	elif 'advertiser' == otype:
		table = '5m_cmp_spend'
		field = 'adv_id'
	else:	# section
		table = '5m_section'
		field = 'section'

	query['table'] = table
	query['filters'] = field
	query['fields'] += ',' + field
	query['groupby'] += ',' + field

	args[field] = args['id']

	return (query, args)

def preexecute_throttlerate(query, args):
	otype = args.get('type')

	if 'campaign' == otype:
		args['type'] = '"256"'
	elif 'advertiser' == otype:
		args['type'] = '"257"'
	else:	# section
		args['type'] = '' # useless

	return (query, args)

def preexecute_advchanges(query, args):
	start, end, timezone = util.parseTime(args)
	offset = util.getOffsetSeconds(start, timezone)
	start -= offset
	
	offset_seconds = 0
	if args.get('offsetdate') == 'yesterday':
		offset_seconds = util.total_seconds(timedelta(days=1))
	elif args.get('offsetdate') == 'lastweek':
		offset_seconds = util.total_seconds(timedelta(days=7))
	start -= offset_seconds
	
	args['start'] = start

	return (query, start)

def preexecute(appconfig, query, args):
	tabid = args['tabid']
	try:
		return eval('preexecute_' + tabid)(query, args)
	except:
		return (query, args)

def returnEmpty():
	return {'today': []}

def execute_splan(appconfig, query, args, fetcher):
	_type = args.get('type').lower()
	return splan.execute(appconfig, query, args, fetcher) if _type in ('campaign', 'advertiser') else returnEmpty()

def execute_nrt(appconfig, query, args, fetcher):
	return brick._execute(appconfig, query, args, fetcher)

def execute_throttlerate(appconfig, query, args, fetcher):
	_type = args.get('type').lower()
	return brick._execute(appconfig, query, args, fetcher) if _type in ('campaign', 'advertiser', '"256"', '"257"') else returnEmpty()

def execute_advchanges(appconfig, query, args, fetcher):
	_type = args.get('type').lower()
	return brick._execute(appconfig, query, args, fetcher) if _type in ('advertiser') else returnEmpty()	

def execute_nrt_oda(appconfig, query, args, fetcher):
	_type = args.get('type').lower()
	return brick._execute(appconfig, query, args, fetcher) if _type in ('campaign') else returnEmpty()


def execute(appconfig, query, args, fetcher):
	
	tabid = args['tabid']
	try:
		return eval('execute_' + tabid)(appconfig, query, args, fetcher)
	except:
		return returnEmpty()

def postexecute(appconfig, query, args, data):
	tabid = args['tabid']
	try:
		return eval('postexecute_' + tabid)(appconfig, query, args, data)
	except:
		return data

def postexecute_advchanges(appconfig, query, args, data):
	for item in data:
		item['time'] = item.pop('txnDate') / 1000;
	return data
