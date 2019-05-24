import brick, triage, bconfig, util
import traceback, copy

def execute(config, action, args):
	tabid = args['tabid']
	if not tabid or tabid not in ['native_topdiffsection', 'native_topdiffcampaign', 'native_topdiffadvertiser']:
		return brick.execute(config, action, args)
	else:
		return _execute(config, action, args)


def _execute(config, action, args):
	navigation = bconfig.load_config(action)

	if navigation['id'] == 'brick':
		return {'error': 'no action for %s' % (page)}

	tabs = navigation['tabs']
	ret = {}
	try:
		for tab in tabs:
			tabid = util.get(args, 'tabid', None)
			if tabid and tabid != tab['id']:
				continue

			param = copy.deepcopy(tab['data'])
			ret[tab['id']] = process_tab(config, args, param)
	except Exception as e:
		print "[ERROR]", e
		traceback.print_exc()

	return ret

def process_tab(config, args, param):
	param.update(args)

	start = int(util.get(args, 'start', util.day_start(util.today())))
	now = util.datetime2epic(util.today(param['timezone']))
	end = min(now, int(util.get(args, 'end', now)))

	start = util.timestamp2datetime(start)
	end = util.timestamp2datetime(end)

	return {'today':triage.query_topdiffspender(config, start, end, param)}

