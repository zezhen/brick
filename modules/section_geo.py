def preexecute(appconfig, query, args):
	sid = args.get('sid')	
	if sid != 'all':
		field = 'section'
		query['filters'] = field
		args[field] = args['sid']
	return (query, args)