
import brick, splan

def nrt_metric_process(query, args):
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

def throttle_rate_process(query, args):
	otype = args.get('type')

	if 'campaign' == otype:
		args['type'] = '\"256\"'
	elif 'advertiser' == otype:
		args['type'] = '\"257\"'
	else:	# section
		args['type'] = '' # useless

	return (query, args)

def execute(appconfig, page, args):

	is_section = (args.get('type') == 'section')

	if args['tabid'] == 'splan' and not is_section:
		return splan.execute(appconfig, page, args)

	if args['tabid'] == 'throttlerate' and not is_section:
		return brick.execute(appconfig, page, args, throttle_rate_process)		

	return brick.execute(appconfig, page, args, nrt_metric_process)
