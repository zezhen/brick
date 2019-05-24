
import os, pytz
import util
from datetime import datetime, timedelta

# var dict = {'action':'splan','start':startTime,'end':endTime,'ids':ids,'objtype':obj_type};

CMD='java -Xmx8192m -cp /home/y/lib/jars/curveball_ffl_tools-jar-with-dependencies.jar -Dlogback.configurationFile=file:/home/y/conf/curveball_ffl_tools/logback.xml yahoo.budget.tools.DataLoader /home/y/conf/curveball_ffl_tools/tools.properties'

def load_hbase(colo,action,start,end,ids,offset):
	cmds = CMD.split(' ')
	cmds.append(colo);
	cmds.append(action)
	cmds.append(str(start))
	cmds.append(str(end))
	cmds.append(ids)
	ret=util.shell(cmds)
	ret=ret.split(b'\n')[-1]

	ret = util.str_to_json(ret)
	
	if (action == 'cache'):
		for item in ret:
			values = item['value']
			for value in values:
				value['cacheId'] = str(int(value['cacheId']) + offset)

	return ret

def execute(appconfig, query, args, fetcher):

	start, end, timezone = util.parseTime(args)
	offset = util.getOffsetSeconds(start, timezone)
	start, end = start - offset, end - offset

	offset_seconds = 0
	if args.get('offsetdate') == 'yesterday':
		offset_seconds = util.total_seconds(timedelta(days=1))
	elif args.get('offsetdate') == 'lastweek':
		offset_seconds = util.total_seconds(timedelta(days=7))
	start -= offset_seconds

	ids=args['id'].split(',')
	objtype = '256' if 'campaign' == args['type'] else '257'

	ids = [_id + "_" + objtype for _id in ids]
	
	try:
		colo = appconfig.get("hbase", "hbase")
	except:
		colo = 'blue_prod' 

	keys = ",".join(ids)

	if args.get('analysis') == "true":
		rets = load_hbase(colo, 'analysis', start, end, keys, offset)
	else:
		rets = load_hbase(colo, 'cache', start, end, keys, offset)

	return rets
