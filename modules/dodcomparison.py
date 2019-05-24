import brick, util



def execute(appconfig, page, args):
	ret = {}

	date1 = int(util.get(args, 'start', util.day_start(util.today())))
	date2 = int(util.get(args, 'end', util.day_start(util.today())))
	args['start'] = date1
	args['end'] = date1 + 24 * 3600

	def process(query, args):
		query['offset_minutes'] = (date1 - date2) / 60 - 5
		return (query, args)

	day1 = brick.execute(appconfig, page, args)
	ret['today'] = day1['dodcomparison']['today']

	day2 = brick.execute(appconfig, page, args, process)
	ret['ystd'] = day2['dodcomparison']['today']

	ret['lastwk'] = []

	return {'dodcomparison': ret}
