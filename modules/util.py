import ujson
import os, pytz
from datetime import datetime, time, timedelta
import calendar
from decimal import Decimal
import re
from urllib.request import urlopen, Request

try:
    # sudo /usr/bin/python /usr/bin/easy_install mysql-connector
    from mysql.connector import connection
except:
    pass
        
DATE_FORMAT='%Y%m%d%H%M%S'
DATE_ISO='%Y-%m-%d %H:%M:%S'
TIME_FORMAT='%H:%M:%S'

def shell(cmds):
    import subprocess
    try:
        print(' '.join(cmds))
        output = subprocess.Popen(cmds, stdout=subprocess.PIPE).communicate()
        return output[0]
    except Exception as e:
        print('execute command failed.', cmds, e)

def fetch_api_data(appconfig, url, yca_role):
    print(url, yca_role)
    req = Request(url)
    if yca_role:
        import subprocess
        req.add_header('Y-RESTRICTED', 'RESTRICTED')
        req.add_header('Y-YBY', 'MARKETPLACE')
        yca_cert = "yca-cert-util --show %s | cut -d \" \" -f2" % (yca_role)
        req.add_header('Yahoo-App-Auth', subprocess.call(yca_cert, shell=True))

    resp = urlopen(req)
    # load function reads json from streaming data, which is different from loads
    return ujson.load(resp)

def fetch_hive_data(appconfig, fields, sql, offset):
    cmd='/bin/sh /home/y/bin/hive.sh "%s"' % (sql)
    res = shell(cmd.split(' '))
    if not res: return []
    ret = []
    records = res.decode('utf-8').split('\n')

    for record in records:
        if len(record) <= 0: continue
        rs = record.split('\t')
        item = {}
        for i, field in enumerate(fields):
            if i >= len(rs): break
            content = rs[i]
            if field in ('time', 'datestamp', 'timestamp', 'ds'):
                try:
                    content = datetime2epic(str2datetime(content, '%Y%m%d%H%M')) + offset
                    field = 'time'
                except:
                    pass
            item[field] = content
        ret.append(item)
    return ret
    
def fetch_sql_data(appconfig, fields, sql, offset):
    ret = []
    for rs in query_mysql(sql, appconfig):
        item = {}
        for i, field in enumerate(fields):
            if i >= len(rs): break
            content = rs[i]
            if isinstance(content, datetime):
                content = datetime2epic(content) + offset
            elif isinstance(content, Decimal):
                content = float(content)
            item[field] = content
        ret.append(item)
    return ret

def query_mysql(command, config):
    db_host = config.get("database", "db_host")
    db_user = config.get("database", "db_user")
    db_schema = config.get("database", "db_schema")
    return query_mysql0(command, db_host, db_user, db_schema)

def query_mysql0(command, _hostname="pmdb1.bud.cb.bf1.yahoo.com", _user="pmdb_ro", _schema="pmdb"):
    result, cnx, cursor = [], None, None
    try:
        cnx = connection.MySQLConnection(user = _user,
                                         host = _hostname,
                                         database = _schema,
                                         connection_timeout = 300)
        cursor = cnx.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
    except Exception as e:
        print("failed to open connection to mysql ", _hostname, e)
    finally:
        if(cursor):
            cursor.close()
        if(cnx):
            cnx.close()
    return result

def query_mysql1(command, _hostname="pmdb1.bud.cb.bf1.yahoo.com", _user="pmdb_ro", _schema="pmdb"):
    execution = "{client} -h{hostname} -u{user} {schema} -e'{statement}'"
    execution = execution.format(
            client="mysql",
            hostname=_hostname,
            user=_user,
            schema=_schema,
            statement=command)
    print(execution)
    result = os.popen(execution).read()
    return result

def convert_date_format(date_format_str_in_python_style):
    date_format_dict = {
        '%Y': 'yyyy',
        '%m': 'MM',
        '%d': 'dd',
        '%H': 'HH',
        '%M': 'mm'
    }
    return replace_by_dict(date_format_str_in_python_style, date_format_dict)

def replace_by_dict(input, _dict):
    pattern = re.compile(r'(' + '|'.join(_dict.keys()) + r')')
    return pattern.sub(lambda x: _dict[x.group()], input)

def query_end_time(table, config, timezone):
    command = 'select convert_tz(max(time), "UTC", "%s") from %s' % (timezone, table)
    return query_mysql(command, config)[0][0] # [(datetime,)]

def str_to_json(_str):
    return ujson.loads(_str)

def json_to_str(_json):
    return ujson.dumps(_json)

def wrap_error(error):
  return json_to_str({'error' : error})

def day_start(dt, _from='UTC', _to='UTC'):
    dt = time_convert(dt.replace(tzinfo=None), _from, _to)
    ds = datetime.combine(dt.date(), time())
    return calendar.timegm(ds.timetuple())

def day_end(dt, _from='UTC', _to='UTC'):
    dt = time_convert(dt.replace(tzinfo=None), _from, _to)
    return datetime.combine(dt.date() + timedelta(days=1), time())

def time_convert(naive, _from='UTC', _to="America/New_York"):
    local = pytz.timezone(_from)
    local_dt = local.localize(naive, is_dst=False)
    to_dt = local_dt.astimezone(pytz.timezone(_to))
    return to_dt

def time_to_utc(time, format, _from='America/New_York'):
    local = pytz.timezone(_from)
    naive = datetime.fromtimestamp(time)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt.strftime(format)

def timestamp2datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp)

def time2str(timestamp, to_format):
    return datetime.utcfromtimestamp(timestamp).strftime(to_format)

def str2datetime(_str, from_format):
    return datetime.strptime(_str, from_format)

def str2time(_str, from_format):
    return calendar.timegm(datetime.strptime(_str, from_format).timetuple())

def datetime2epic(dt):
    return calendar.timegm(dt.timetuple())

def convert_format(_str, from_format, to_format):
    time = calendar.timegm(datetime.strptime(_str, from_format).timetuple())
    return datetime.fromtimestamp(time).strftime(to_format)

def today(_to='UTC'):
	return time_convert(datetime.utcnow(), _to=_to)

def now(_to='UTC'):
    return calendar.timegm(time_convert(datetime.utcnow(), _to=_to).timetuple())

def add(_dict, key, number):
    _dict[key] = (_dict[key] if key in _dict else 0) + number

def total_seconds(td):
    return int(float((td.microseconds +
                (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6)

def timezone_switch_aware_offset(timestamp, offset, timezone):
    utc_date = timestamp2datetime(timestamp)
    target_date = timestamp2datetime(timestamp - offset)
    return total_seconds(time_convert(utc_date, timezone, 'UTC') - time_convert(target_date, timezone, 'UTC'))

def get_track(product):
    product = product.lower()
    if 'mb' == product or 'native' == product:
        return 'mb'
    elif 'sm' == product or 'search' == product:
        return 'sm'
    else:
        return 'unknown'

def wrap_quotes(items, sep=','):
    if items == None or len(items) <= 0:
        return items
    return '"' + ('"' + sep + '"').join(items.split(sep)) + '"'

def validate_str(_str):
    return _str != None and len(_str) > 0

def parseEpicOrTime(_time):
    if len(str(_time)) > 10:
        return str(str2time(_time, DATE_FORMAT))
    else:
        return _time

def get(_dict, key, default_value, convert_func=None):
    return (convert_func(_dict[key]) if convert_func else _dict[key]) \
        if key in _dict and _dict[key] != '' else default_value

def parseTime(args):
    timezone = get(args, 'timezone', 'America/New_York')

    start = int(get(args, 'start', day_start(today())))
    now = datetime2epic(today(timezone))
    end = min(now, int(get(args, 'end', now)))

    return start, end, timezone

#get offset seconds between current timezone and UTC
#for DST timezone, it may varies
def getOffsetSeconds(epic, timezone):
    return total_seconds(pytz.timezone(timezone).utcoffset(timestamp2datetime(epic)))
