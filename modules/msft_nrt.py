def preexecute(appconfig, query, args):
	siteids = args.get('siteids')
	if siteids == 'all':
		siteids = '140540,140550'
	
	if 'join' in query and 'join_to' in query['join']:
		field = 'site'
		query['join']['join_to']['filters'] = field
		args[field] = siteids
	return (query, args)