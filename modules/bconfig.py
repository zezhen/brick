startTime = {
    'id': 'start',
    'name': 'Start Time',
    'placeholder': 'optional',
    'type': 'datetimepicker',
    }
endTime = {
    'id': 'end',
    'name': 'End Time',
    'placeholder': 'optional',
    'type': 'datetimepicker',
    }
startTimeR = {
    'id': 'start',
    'name': 'Start Time',
    'placeholder': 'required',
    'type': 'datetimepicker',
    'required': 'true',
    }
endTimeR = {
    'id': 'end',
    'name': 'End Time',
    'placeholder': 'required',
    'type': 'datetimepicker',
    'required': 'true',
    }
startDateR = {
    'id': 'start',
    'name': 'Date1',
    'placeholder': 'required',
    'type': 'datepicker',
    'required': 'true',
    }
endDateR = {
    'id': 'end',
    'name': 'Date2',
    'placeholder': 'required',
    'type': 'datepicker',
    'required': 'true',
    }
oid = {
    'id': 'id',
    'name': 'ID',
    'type': 'field',
    'placeholder': 'required',
    'required': 'true',
    }
otype = {
    'id': 'type',
    'name': 'Object Type',
    'items': 'Campaign,Advertiser,Section',
    'type': 'dropdown',
    }
help = {'id': 'help', 'type': 'html', 'file': 'help.html'}

gemini = {
    'id': 'gemini',
    'name': 'Gemini',
    'type': 'navtab',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'gemini',
        'name': 'Gemini',
        'refresh': 300,
        'data': {'fields': 'time,mb_spend,mb_spend_usd,ss_spend_usd,bing_spend_usd,bing_only_spend'
                 , 'groupby': 'time', 'table': '5m_summary'},
        'charts': [{
            'id': 'chart_native',
            'title': 'Native Ads Near-realtime Spends',
            'type': 'timeseries',
            'stack': 'true',
            'metrics': [{
                'series': '5-min Non-USD Spends',
                'field': 'mb_spend - mb_spend_usd',
                'color': '#555555',
                'type': 'area',
                }, {
                'series': '5-min USD Spends',
                'field': 'mb_spend_usd',
                'color': '#7cb5ec',
                'type': 'area',
                }],
            }, {
            'id': 'chart_search',
            'title': 'Search Ads Near-realtime Spends',
            'type': 'timeseries',
            'stack': 'true',
            'metrics': [{
                'series': '5-min Curveball Spends',
                'field': 'ss_spend_usd',
                'color': '#555555',
                'type': 'area',
                }, {
                'series': '5-min Bing Spends',
                'field': 'bing_spend_usd',
                'color': '#7cb5ec',
                'type': 'area',
                }, {
                'series': '5-min Bing-only Spends',
                'field': 'bing_only_spend',
                'color': '#7cb5ec',
                'type': 'area',
                }],
            }],
        }, {
        'id': 'dodwow',
        'name': 'DoD/WoW',
        'refresh': 300,
        'data': {
            'fields': 'time,mb_spend,mb_spend_usd,ss_spend_usd,bing_spend_usd,bing_only_spend',
            'groupby': 'time',
            'table': '5m_summary',
            'dod': 'true',
            'wow': 'true',
            },
        'charts': [{
            'id': 'gemini_bing_dodwow',
            'title': 'Gemini + Bing Spends',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'mb_spend + ss_spend_usd + bing_spend_usd + bing_only_spend',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'native_dodwow',
            'title': 'Native Spends',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'mb_spend',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'search_dodwow',
            'title': 'Gemini Search Spends',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'ss_spend_usd',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'bing_dodwow',
            'title': 'Bing Spends',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'bing_spend_usd',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'bing_only_dodwow',
            'title': 'Bing Only Spends',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'bing_only_spend',
                'accumulation': 'true',
                'type': 'area',
                }],
            }],
        }, {
        'id': 'topsection',
        'name': 'Top Sections',
        'refresh': 300,
        'customized': 'topsection',
        'data': {
            'fields': 'time,section,spend,serve,impression,click',
            'groupby': 'time,section',
            'table': '5m_section',
            'filters': 'section',
            'dod': 'true',
            'wow': 'true',
            # 'fixed_condition': 'section in (select * from (select section from 5m_section where time >= convert_tz("{start}", "{timezone}", "Etc/UTC") and time < convert_tz("{end}", "{timezone}", "Etc/UTC") and track="mb" and section in ({section}) group by section order by sum(spend) desc limit 30) temp_table)',
            },
        'charts': [{
            'id': 'topsection_dodwow',
            'render': 'topsection',
            'type': 'timeseries',
            'arrangedby': 'section',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'spend',
                'accumulation': 'true',
                'type': 'line',
                }],
            }],
        }],
    }

native = {
    'id': 'native',
    'name': 'Native Triage',
    'type': 'navtab',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'native',
        'name': 'Native Supply',
        'data': {
            'fields': 'time,supply,spend,impression,click,serve,conversion'
                ,
            'groupby': 'time,supply',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="mb"',
            },
        'charts': [{
            'id': 'native_supply_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'supply',
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend',
                    'color': '#555555',
                    'type': 'line',
                    },
                {
                    'series': 'Click',
                    'field': 'click',
                    'color': '#555555',
                    'type': 'line',
                    },
                {
                    'series': 'Impression',
                    'field': 'impression',
                    'color': '#555555',
                    'type': 'line',
                    },
                {
                    'series': 'CTR',
                    'field': 'click * 100 / impression',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                {
                    'series': 'PPC',
                    'field': 'spend / click',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                {
                    'series': 'RPM',
                    'field': 'spend * 1000 / impression',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                ],
            }],
        }, {
        'id': 'native_vertical',
        'name': 'Native Vertical',
        'data': {
            'fields': 'time,vertical,spend,impression,click,serve,conversion'
                ,
            'groupby': 'time,vertical',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="mb"',
            },
        'charts': [{
            'id': 'native_vertical_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'vertical',
            'metrics': [{
                'series': 'Revenue',
                'field': 'spend',
                'color': '#555555',
                'type': 'line',
                }],
            }],
        }, {
        'id': 'native_device',
        'name': 'Native Device',
        'data': {
            'fields': 'time,device,spend,impression,click,serve,conversion'
                ,
            'groupby': 'time,device',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="mb"',
            },
        'charts': [{
            'id': 'native_device_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'device',
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend',
                    'color': '#555555',
                    'type': 'line',
                    },
                {
                    'series': 'Click',
                    'field': 'click',
                    'color': '#555555',
                    'type': 'line',
                    },
                {
                    'series': 'Impression',
                    'field': 'impression',
                    'color': '#555555',
                    'type': 'line',
                    },
                {
                    'series': 'CTR',
                    'field': 'click * 100 / impression',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                {
                    'series': 'PPC',
                    'field': 'spend / click',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                {
                    'series': 'RPM',
                    'field': 'spend * 1000 / impression',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                ],
            }],
        }, {
        'id': 'native_topdiffsection',
        'name': 'Native TopDiff Section',
        'data': {
            'topn': 1000,
            'type': 'section',
            'table': '5m_section',
            'track': 'mb',
            'desc': '',
            'advertiser': '',
            },
        'charts': [{
            'id': 'native_topdiffsection',
            'type': 'table',
            'fields': 'id,dod_delta,wow_delta,today_spend,ystd_spend,lastwk_spend,today_click,ystd_click,lastwk_click,today_imp,ystd_imp,lastwk_imp,today_serve,ystd_serve,lastwk_serve'
                ,
            'columns': 'ID,DoD<br/>Delta,WoW<br/>Delta,Today<br/>Rev,Ystd<br/>Rev,Lastwk<br/>Rev,Today<br/>Click,Ystd<br/>Click,Lastwk<br/>Click,Today<br/>Imp,Ystd<br/>Imp,Lastwk<br/>Imp,Today<br/>Serve,Ystd<br/>Serve,Lastwk<br/>Serve'
                ,
            'order': 'asc,1,2',
            'invisible': '',
            }],
        }, {
        'id': 'native_topdiffadvertiser',
        'name': 'Native TopDiff Advertiser',
        'data': {
            'topn': 1000,
            'type': 'adv_id',
            'table': '5m_cmp_spend_cumulative',
            'track': 'mb',
            'desc': '',
            'advertiser': '',
            },
        'charts': [{
            'id': 'native_topdiffadvertiser',
            'type': 'table',
            'fields': 'id,dod_delta,wow_delta,today_spend,ystd_spend,lastwk_spend,today_click,ystd_click,lastwk_click,today_imp,ystd_imp,lastwk_imp,today_serve,ystd_serve,lastwk_serve'
                ,
            'columns': 'ID,DoD<br/>Delta,WoW<br/>Delta,Today<br/>Rev,Ystd<br/>Rev,Lastwk<br/>Rev,Today<br/>Click,Ystd<br/>Click,Lastwk<br/>Click,Today<br/>Imp,Ystd<br/>Imp,Lastwk<br/>Imp,Today<br/>Serve,Ystd<br/>Serve,Lastwk<br/>Serve'
                ,
            'order': 'asc,1,2',
            'invisible': '',
            }],
        }, {
        'id': 'native_topdiffcampaign',
        'name': 'Native TopDiff Campaign',
        'data': {
            'topn': 1000,
            'type': 'cmp_id',
            'table': '5m_cmp_spend_cumulative',
            'track': 'mb',
            'desc': '',
            'advertiser': ', adv_id',
            },
        'charts': [{
            'id': 'native_topdiffcampaign',
            'type': 'table',
            'fields': 'id,dod_delta,wow_delta,today_spend,ystd_spend,lastwk_spend,today_click,ystd_click,lastwk_click,today_imp,ystd_imp,lastwk_imp,today_serve,ystd_serve,lastwk_serve,adv'
                ,
            'columns': 'ID,DoD<br/>Delta,WoW<br/>Delta,Today<br/>Rev,Ystd<br/>Rev,Lastwk<br/>Rev,Today<br/>Click,Ystd<br/>Click,Lastwk<br/>Click,Today<br/>Imp,Ystd<br/>Imp,Lastwk<br/>Imp,Today<br/>Serve,Ystd<br/>Serve,Lastwk<br/>Serve,Adv'
                ,
            'order': 'asc,1,2',
            'invisible': '15',
            }],
        }],
    }

search = {
    'id': 'search',
    'name': 'Search Triage',
    'type': 'navtab',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'search',
        'name': 'Search PostTP',
        'data': {
            'fields': 'time,impression,click,spend'
                ,
            'groupby': 'time',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="search"',
            'offset_minutes': 0
            },
        'charts': [{
            'id': 'search_posttp_spend',
            'title': 'Search PostTP Spend',
            'type': 'timeseries',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [{
                'series': 'Spends',
                'field': 'spend',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'search_posttp_click',
            'title': 'Search PostTP Click',
            'type': 'timeseries',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [{
                'series': 'Spends',
                'field': 'click',
                'accumulation': 'true',
                'type': 'area',
                }],
            }],
        }, {
        'id': 'search_supply',
        'name': 'Search Supply',
        'data': {
            'fields': 'time,supply,spend,click'
                ,
            'groupby': 'time,supply',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="search"',
            },
        'charts': [{
            'id': 'search_supply_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'supply',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'click',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend / click',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                ],
            }],
        }, {
        'id': 'search_device',
        'name': 'Search Device',
        'data': {
            'fields': 'time,device,spend,click,serve,conversion'
                ,
            'groupby': 'time,device',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="sm"',
            },
        'charts': [{
            'id': 'search_device_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'device',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'click',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Impression',
                    'field': 'serve',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'CTR',
                    'field': 'click * 100 / serve',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend / click',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                },
                {
                    'series': 'RPM',
                    'field': 'spend * 1000 / serve',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                ],
            }],
        }, {
        'id': 'bing_posttp',
        'name': 'Bing PostTP',
        'data': {
            'fields': 'time,spend,click'
                ,
            'groupby': 'time,supply',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="bing"',
            },
        'charts': [{
            'id': 'bing_revenue_dodwow',
            'type': 'timeseries',
            'title': 'Bing PostTP Spend',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend',
                    'color': '#555555',
                    'type': 'area',
                }
            ]},{
            'id': 'bing_click_dodwow',
            'type': 'timeseries',
            'title': 'Bing PostTP Click',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Click',
                    'field': 'click',
                    'color': '#555555',
                    'type': 'area',
                }
            ]},{
            'id': 'bing_ppc_dodwow',
            'type': 'timeseries',
            'title': 'Bing PostTP PPC',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'PPC',
                    'field': 'spend / click',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'area',
                },
                ],
            }],
        }],
    }

objid = {
    'id': 'objid',
    'name': 'Cmpgn/Adv/Section',
    'type': 'navtab',
    'layouts': [startTime, endTime, oid, otype],
    'tabs': [{
        'id': 'objid',
        'name': 'NRT Metric',
        'data': {
            'fields': 'time,spend,serve,impression,click',
            'groupby': 'time',
            'table': '5m_cmp_spend',
            'filters': 'cmp_id',
            'dod': 'true',
            'wow': 'true',
            },
        'charts': [{
            'id': 'obj_nrt_spend',
            'title': 'NRT Spend',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Spends',
                'field': 'spend',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'obj_nrt_click',
            'title': 'NRT Click',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Clicks',
                'field': 'click',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'obj_nrt_imp',
            'title': 'NRT Impression',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Impressions',
                'field': 'impression',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'obj_nrt_serve',
            'title': 'NRT Serve',
            'type': 'timeseries',
            'dodwow': 'true',
            'metrics': [{
                'series': 'Serves',
                'field': 'serve',
                'accumulation': 'true',
                'type': 'area',
                }],
            }],
        }, {
        'id': 'splan',
        'name': 'PostTP',
        'data': 'fetch from hbase',
        'charts':[{
            'id': 'spend_plans',
            'render': 'splan'
            }],
        }, {
        'id': 'throttlerate',
        'name': 'Throttle Rate',
        'data': {
            'fields': 'time,id,type,throttle_rate,message_type,throttle_type,colo',
            'table': 'throttle_rate',
            'filters': 'id,type',
            'orderby': 'time'
            },
        'charts': [{
            'id': 'throttlerate',
            'type': 'table',
            'fields': 'time,id,throttle_rate,throttle_type,colo,message_type',
            'columns': 'Time,Id,Throttle Rate,Throttle Type,Primary Colo,Message Type',
            'order': 'desc,0'
            }]
        }],
    }

labs = {'id': 'labs', 'name': 'More', 'type': 'navdropdown'}

oda = {
    'id': 'oda',
    'name': 'NRT Estimated ODA',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime],
    }

son = {
    'id': 'son',
    'name': 'Search On Native',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime],
    'tabs': [{
        'id': 'son',
        'name': 'SoN DoD/WoW',
        'data': {
            'fields': 'time,son_spend',
            'groupby': 'time',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': 0
        },
        'charts': [{
                'id': 'son_spend',
                'title': 'Search On Native Revenue',
                'type': 'timeseries',
                'dodwow': 'true',
                'granularity': 15,
                'metrics': [{
                    'series': 'Spends',
                    'field': 'son_spend',
                    'accumulation': 'true',
                    'type': 'area',
                }],
        }],
    }]

}

topspender = {
    'id': 'topspender',
    'name': 'Top Spender',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTimeR, endTime],
    'tabs': [{
        'id': 'topspender',
        'name': 'Top Spender',
        'debug': 1,
        'data': {
            'fields': 'cmp_id,adv_id,track,spend,serve,impression,click'
                ,
            'groupby': 'cmp_id,track',
            'table': '5m_cmp_spend',
            'fixed_condition': 'cmp_id not in (-99999, -88888)',
            'orderby': 'sum(spend)',
            'sort': 'desc',
            'limit': '100',
            },
        'charts': [{
            'id': 'topspender_table',
            'type': 'table',
            'fields': 'cmp_id,adv_id,track,spend,click,impression,serve'
                ,
            'columns': 'Campaign,Advertiser,Product,Spend,Click,Impression,Serve'
                ,
            'order': 'desc,3',
            'invisible': '',
            }],
        }]
}

dodcomparison = {
    'id': 'dodcomparison',
    'name': 'DoD Comparison',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startDateR, endDateR],
    'render': 'triage',
    'tabs': [{
        'id': 'dodcomparison',
        'name': 'DoD Comparison',
        'data': {
            'fields': 'time,product_type,spend,impression,click'
                ,
            'groupby': 'time,product_type',
            'table': 'posttp_revenue_triage'
            },
        'charts': [{
            'id': 'dod_comparison',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'product_type',
            'granularity': 15,
            'metrics': [{
                'series': 'Revenue',
                'field': 'spend',
                'color': '#555555',
                'type': 'area',
                }],
            }],
        }]
}

help = {
    'id': 'help',
    'name': 'Help',
    'type': 'navtab',
    'layouts': [help],
    }

page_config = {'id': 'brick', 'navigations': [
    gemini,
    native,
    search,
    objid,
    labs,
    dodcomparison,
    topspender,
    son,
    help,
    ]}

def load_config(page):
    if not page:
        return page_config
    navigations = page_config['navigations']
    for navigation in navigations:
        if page == navigation['id']:
            return navigation
    return page_config
