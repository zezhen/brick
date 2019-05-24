import brick, util

def execute(appconfig, query, args, fetcher):
	ret = {}

	date1 = int(util.get(args, 'start', util.day_start(util.today())))
	date2 = int(util.get(args, 'end', util.day_start(util.today())))
	args['start'] = date1
	args['end'] = date1 + 24 * 3600

	day1 = brick._execute(appconfig, query, args, fetcher)
	ret['today'] = day1['today']

	query['offset_minutes'] = (date1 - date2) / 60
	day2 = brick._execute(appconfig, query, args, fetcher)
	ret['ystd'] = day2['today']

	ret['lastwk'] = []

	return ret
