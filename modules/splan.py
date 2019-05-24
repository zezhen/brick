
import os, pytz
import util
from datetime import datetime

# var dict = {'action':'splan','start':startTime,'end':endTime,'ids':ids,'objtype':obj_type};

CMD='java -Xmx8192m -cp /home/y/lib/jars/curveball_ffl_tools-jar-with-dependencies.jar -Dlogback.configurationFile=file:/home/y/conf/curveball_ffl_tools/logback.xml yahoo.budget.tools.DataLoader /home/y/conf/curveball_ffl_tools/tools.properties'

def load_hbase(colo,action,start,end,ids,args):
	cmds = CMD.split(' ')
	cmds.append(colo);
	cmds.append(action)
	cmds.append(start)
	cmds.append(end)
	cmds.append(ids)
	ret=util.shell(cmds)
	ret=ret.split('\n')[-1]

	ret = util.str_to_json(ret)
	offset = util.total_seconds(pytz.timezone(args['timezone']).utcoffset(datetime.utcnow()))
	for item in ret:
		values = item['value']
		for value in values:
			value['cacheId'] = str(int(value['cacheId']) + offset)

	return ret

def execute(appconfig, page, args):

	offset = util.total_seconds(pytz.timezone(args['timezone']).utcoffset(datetime.utcnow()))

	start = str(int(util.get(args, 'start', util.day_start(util.today()))) - offset)
	now = util.datetime2epic(util.today('UTC'))
	end = str(min(now, int(util.get(args, 'end', now))) - offset)

	ids=args['id'].split(',')
	objtype = '256' if 'campaign' == args['type'] else '257'

	ids = [_id + "_" + objtype for _id in ids]
	
	try:
		colo = appconfig.get("hbase", "hbase")
	except:
		colo = 'blue_prod' 

	keys = ",".join(ids)

	if args.get('analysis') == "true":
		rets = load_hbase(colo, 'analysis', start, end, keys, args)
	else:
		rets = load_hbase(colo, 'cache', start, end, keys, args)

	return {'splan': rets}
