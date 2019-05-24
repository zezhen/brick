
import util
from datetime import datetime, timedelta
import calendar, pytz

CMPGN_ADV_DIFF_TEMPLATE = 'select convert_tz(max(date_sub(time, interval -5 minute)), "UTC", "{timezone}") as time, t.id, sum(t.today_spend) as today_spend, sum(t.ystd_spend) as ystd_spend, sum(t.lastwk_spend) as lastwk_spend, sum(t.today_click) as today_click, sum(t.ystd_click) as ystd_click, sum(t.lastwk_click) as lastwk_click, sum(t.today_imp) as today_imp, sum(t.ystd_imp) as ystd_imp, sum(t.lastwk_imp) as lastwk_imp, sum(t.today_serve) as today_serve, sum(t.ystd_serve) as ystd_serve, sum(t.lastwk_serve) as lastwk_serve, sum(t.today_spend) - sum(t.ystd_spend) as dod_delta, sum(t.today_spend) - sum(t.lastwk_spend) as wow_delta, sum(t.today_spend) - sum(t.ystd_spend) + sum(t.today_spend) - sum(t.lastwk_spend) as dodwow_delta {advertiser} from ( ({today_query}) union ({ystd_query}) union ({lastwk_query}) ) as t group by 2 {advertiser} order by dodwow_delta {desc} limit {topn}'

TODAY_TEMPLATE = 'select time, {type} as id, {sign} spend as today_spend, 0 as ystd_spend, 0 as lastwk_spend, {sign} click as today_click, 0 as ystd_click, 0 as lastwk_click, {sign} impression as today_imp, 0 as ystd_imp, 0 as lastwk_imp, {sign} serve as today_serve, 0 as ystd_serve, 0 as lastwk_serve {advertiser} from {table} where time = "{time}" and {type} > 0 and track = "{track}"'
YEST_TEMPLATE = 'select time, {type} as id, 0 as today_spend, {sign} spend as ystd_spend, 0 as lastwk_spend, 0 as today_click, {sign} click as ystd_click, 0 as lastwk_click, 0 as today_imp, {sign} impression as ystd_imp, 0 as lastwk_imp, 0 as today_serve, {sign} serve as ystd_serve, 0 as lastwk_serve {advertiser} from {table} where time = "{time}" and {type} > 0 and track = "{track}"'
LASTWK_TEMPLATE = 'select time, {type} as id, 0 as today_spend, 0 as ystd_spend, {sign} spend as lastwk_spend, 0 as today_click, 0 as ystd_click, {sign} click as lastwk_click, 0 as today_imp, 0 as ystd_imp, {sign} impression as lastwk_imp, 0 as today_serve, 0 as ystd_serve, {sign} serve as lastwk_serve {advertiser} from {table} where time = "{time}" and {type} > 0 and track = "{track}"'

SECTION_DIFF_TEMPLATE = 'select convert_tz(max(date_sub(time, interval -5 minute)), "UTC", "{timezone}") as time, t.id as id, sum(t.today_spend) as today_spend, sum(t.ystd_spend) as ystd_spend, sum(t.lastwk_spend) as lastwk_spend, sum(t.today_click) as today_click, sum(t.ystd_click) as ystd_click, sum(t.lastwk_click) as lastwk_click, sum(t.today_imp) as today_imp, sum(t.ystd_imp) as ystd_imp, sum(t.lastwk_imp) as lastwk_imp, sum(t.today_serve) as today_serve, sum(t.ystd_serve) as ystd_serve, sum(t.lastwk_serve) as lastwk_serve, sum(t.today_spend) - sum(t.ystd_spend) as dod_delta, sum(t.today_spend) - sum(t.lastwk_spend) as wow_delta {advertiser} from ( (select max(time) as time, {type} as id, sum(spend) as today_spend, 0 as ystd_spend, 0 as lastwk_spend, sum(click) as today_click, 0 as ystd_click, 0 as lastwk_click, sum(impression) as today_imp, 0 as ystd_imp, 0 as lastwk_imp, sum(serve) as today_serve, 0 as ystd_serve, 0 as lastwk_serve {advertiser} from {table} where time > convert_tz("{today_start}", "{timezone}", "UTC") and time <= convert_tz("{today_end}", "{timezone}", "UTC") and {type} > 0 and track="{track}" group by {type}) union (select max(time) as time, {type} as id, 0 as today_spend, sum(spend) as ystd_spend, 0 as lastwk_spend, 0 as today_click, sum(click) as ystd_click, 0 as lastwk_click, 0 as today_imp, sum(impression) as ystd_imp, 0 as lastwk_imp, 0 as today_serve, sum(serve) as ystd_serve, 0 as lastwk_serve {advertiser} from {table} where time > convert_tz("{ystd_start}", "{timezone}", "UTC") and time <= convert_tz("{ystd_end}", "{timezone}", "UTC") and {type} > 0 and track="{track}" group by {type}) union (select max(time) as time, {type} as id, 0 as today_spend, 0 as ystd_spend, sum(spend) as lastwk_spend, 0 as today_click, 0 as ystd_click, sum(click) as lastwk_click, 0 as today_imp, 0 as ystd_imp, sum(impression) as lastwk_imp, 0 as today_serve, 0 as ystd_serve, sum(serve) as lastwk_serve {advertiser} from {table} where time > convert_tz("{lastwk_start}", "{timezone}", "UTC") and time <= convert_tz("{lastwk_end}", "{timezone}", "UTC") and {type} > 0 and track="{track}" group by {type}) ) as t group by 2 order by wow_delta, dod_delta {desc} limit {topn} '

DATE_FORMAT=util.DATE_ISO

# def query_topdiffadvertiser(start, end, track, supply, vertical, device, pt, layout, dod, wow):
# 	param = {'topn': 1000, 'type': 'adv_id', 'table': '5m_cmp_spend', 'track': track, 
# 		'desc': '', 'advertiser': ''}
# 	return query_topdiffspender(start, end, track, supply, vertical, device, pt, layout, dod, wow, param)

# def query_topdiffcampaign(start, end, track, supply, vertical, device, pt, layout, dod, wow):
# 	param = {'topn': 1000, 'type': 'cmp_id', 'table': '5m_cmp_spend', 'track': track, 
# 		'desc': '', 'advertiser': ', adv_id'}
# 	return query_topdiffspender(start, end, track, supply, vertical, device, pt, layout, dod, wow, param)

# def query_topdiffsection(start, end, track, supply, vertical, device, pt, layout, dod, wow):
# 	param = {'topn': 1000, 'type': 'section', 'table': '5m_section', 'track': track, 
# 		'desc': '', 'advertiser': ''}
# 	return query_topdiffspender(start, end, track, supply, vertical, device, pt, layout, dod, wow, param)

def iterate_day(start, end, param, template):
	queries = []
	
	timezone = param['timezone']
	start_utc = util.time_convert(util.timestamp2datetime(start), timezone, "UTC")
	end_utc = util.time_convert(util.timestamp2datetime(end), timezone, "UTC")

	# start point should be subtracted
	param['sign'] = '-'
	param['time'] = start_utc.strftime(DATE_FORMAT)
	queries.append(template.format(**param))

	# resume the sign
	param['sign'] = ''
	day = util.day_end(start_utc)

	# loop every day end util end time
	day = day.replace(tzinfo=pytz.UTC)
	while day < end_utc:
		param['time'] = day.strftime(DATE_FORMAT)
		queries.append(template.format(**param))

		day += timedelta(days=1)
	
	# add end time point
	param['time'] = end_utc.strftime(DATE_FORMAT)
	queries.append(template.format(**param))
	
	return ") union (".join(queries)

def query_topdiffspender(config, start, end, param):
	today_start = calendar.timegm(start.timetuple())
	ystd_start = calendar.timegm((start - timedelta(days=1)).timetuple())
	lastwk_start = calendar.timegm((start - timedelta(days=7)).timetuple())

	db_end = util.query_end_time(param['table'], config, timezone = param['timezone'])
	end = min(end, db_end)
	today_end = calendar.timegm(end.timetuple()) / 900 * 900

	ystd_end = calendar.timegm((end - timedelta(days=1)).timetuple())
	lastwk_end = calendar.timegm((end - timedelta(days=7)).timetuple())

	param['today_start'] = util.time2str(today_start, DATE_FORMAT)
	param['ystd_start'] = util.time2str(ystd_start, DATE_FORMAT)
	param['lastwk_start'] = util.time2str(lastwk_start, DATE_FORMAT)
	param['today_end'] = util.time2str(today_end, DATE_FORMAT)
	param['ystd_end'] = util.time2str(ystd_end, DATE_FORMAT)
	param['lastwk_end'] = util.time2str(lastwk_end, DATE_FORMAT)

	fields = 'time,id,today_spend,ystd_spend,lastwk_spend,today_click,ystd_click,lastwk_click,today_imp,ystd_imp,lastwk_imp,today_serve,ystd_serve,lastwk_serve,dod_delta,wow_delta,dodwow_delta,adv'.split(',')
	
	tabid = param.get('tabid')
	if tabid == 'native_topdiffsection':
		command = SECTION_DIFF_TEMPLATE.format(**param)
	else:
		param['today_query'] = iterate_day(today_start, today_end, param, TODAY_TEMPLATE)
		param['ystd_query'] = iterate_day(ystd_start, ystd_end, param, YEST_TEMPLATE)
		param['lastwk_query'] = iterate_day(lastwk_start, lastwk_end, param, LASTWK_TEMPLATE)
		command = CMPGN_ADV_DIFF_TEMPLATE.format(**param)

	return util.fetch_data(config, fields, command, - util.total_seconds(timedelta(minutes=5)))
