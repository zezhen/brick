import json
import subprocess
import util
import bconfig

def get_color(text):
	return '#008000' if 'PASS' in text else '#8B0000' if 'FAIL' in text else '#000'

def parse_body(item):
	text = item['groupResult']
	return {
		'text': text,
		'color': get_color(text),
		'today': item['data']
	}

def parse_kpiGraph(query, args, data):
	latencyAbove140 = parse_latencyAbove140(args, query, data)
	acfPercentage = parse_acfPercentage(args, query, data)
	return {
		'latencyAbove140': {
			'text': latencyAbove140['text'],
			'color': latencyAbove140['color']
		},
		'acfPercentage': {
			'text': acfPercentage['text'],
			'color': acfPercentage['color']
		},
		'url': data['kpiGraph']
	}

def parse_latencyAbove140(query, args, data):
	for item in data['results']:
		if 'latencyAbove140' != item['metricGroup']: continue
		return parse_body(item)

def parse_acfPercentage(query, args, data):
	for item in data['results']:
		if 'acfPercentage' != item['metricGroup']: continue
		return parse_body(item)

def postexecute(appconfig, query, args, data):
	tabid = args['tabid']
	return eval('parse_' + tabid)(query, args, data)
