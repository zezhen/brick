import brick, triage, bconfig, util
import traceback, copy

def execute(config, query, args, fetcher):

	tabid = args['tabid']
	if not tabid or tabid not in ['native_topdiffsection', 'native_topdiffcampaign', 'native_topdiffadvertiser']:
		return brick._execute(config, query, args, fetcher)
	else:
		return _execute(config, query, args)

def _execute(config, param, args):
	param.update(args)

	start = int(util.get(args, 'start', util.day_start(util.today())))
	now = util.datetime2epic(util.today(param['timezone']))
	end = min(now, int(util.get(args, 'end', now)))

	start = util.timestamp2datetime(start)
	end = util.timestamp2datetime(end)

	return {'today':triage.query_topdiffspender(config, start, end, param)}