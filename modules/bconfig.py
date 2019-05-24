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
startTimeMR = {
    'id': 'start',
    'name': 'Start Time',
    'placeholder': 'required',
    'type': 'dateminutepicker',
    'required': 'true',
}
endTimeMR = {
    'id': 'end',
    'name': 'End Time',
    'placeholder': 'required',
    'type': 'dateminutepicker',
    'required': 'true',
}
oid = {
    'id': 'id',
    'name': 'ID',
    'type': 'field',
    'placeholder': 'required',
    'required': 'true',
}
sid = {
    'id': 'sid',
    'name': 'Section ID',
    'type': 'field',
    'placeholder': 'optional',
}
siteids = {
    'id': 'siteids',
    'name': 'Site IDs',
    'type': 'field',
    'placeholder': '140540,140550',
}
otype = {
    'id': 'type',
    'name': 'Object Type',
    'items': 'Campaign,Advertiser,Section',
    'type': 'dropdown',
}
# make it invisible to user, default value is today
# yesterday and lastweek can be set via url parameter
offset = {
    'id': 'offsetdate',
    'name': 'Offset Date',
    'items': 'today,yesterday,lastweek',
    'type': 'dropdown',
    'hidden': 'true'
}

testCluster = {
    'name': 'Test Cluster',
    'id': 'testCluster',
    'type': 'group',
    'data': [{
        'id': 'env1',
        'name': 'native_ads.serving.csp.searcher.',
        'items': 'prod,cd,beta',
        'type': 'dropdown'
    }, {
        'id': 'colo1',
        'name': '.',
        'items': 'bf1,gq1,ne1,ir2,tp2,sg3',
        'type': 'dropdown',
    }, {
        'id': 'cluster1',
        'name': '.',
        'items': 'cluster1,cluster2,cluster3,cluster4,cluster5',
        'type': 'dropdown',
    }],
}

compareCluster = {
    'name': 'Compare Cluster',
    'id': 'compareCluster',
    'type': 'group',
    'data': [{
        'id': 'env2',
        'name': 'native_ads.serving.csp.searcher.',
        'items': 'prod,cd,beta',
        'type': 'dropdown',
    }, {
        'id': 'colo2',
        'name': '.',
        'items': 'bf1,gq1,ne1,ir2,tp2,sg3',
        'type': 'dropdown',
    }, {
        'id': 'cluster2',
        'name': '.',
        'items': 'cluster2,cluster1,cluster3,cluster4,cluster5',
        'type': 'dropdown',
    }],
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
        'refresh': 150,
        'sql': {
            'fields': 'time,mb_spend,mb_spend_usd',
                 'groupby': 'time',
                 'table': '5m_summary',
                 'offset_minutes': -5
            },
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
            }],
        }, {
        'id': 'dodwow',
        'name': 'DoD/WoW',
        'refresh': 150,
        'sql': {
            'fields': 'time,mb_spend,mb_spend_usd',
            'groupby': 'time',
            'table': '5m_summary',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5
            },
        'charts': [{
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
            }],
        }, {
        'id': 'section_whitelist',
        'name': 'Whitelist Sections',
        'refresh': 150,
        'customized': 'topsection',
        'sql': {
            'fields': 'time,section,spend,serve,impression,click',
            'groupby': 'time,section',
            'table': '5m_section',
            'filters': 'section',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5,
            },
        'charts': [{
            'id': 'section_whitelist_dodwow',
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
        'sql': {
            'fields': 'time,supply,spend,impression,click,serve'
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
                    'series': 'Serve',
                    'field': 'serve',
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
        'sql': {
            'fields': 'time,vertical,spend,impression,click,serve'
                ,
            'groupby': 'time,vertical',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="mb"',
            'offset_minutes': -5,
            },
        'charts': [{
            'id': 'native_vertical_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'vertical',
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
                    'series': 'Serve',
                    'field': 'serve',
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
        'id': 'native_device',
        'name': 'Native Device',
        'sql': {
            'fields': 'time,device,spend,impression,click,serve'
                ,
            'groupby': 'time,device',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="mb"',
            'offset_minutes': -5,
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
                    'series': 'Serve',
                    'field': 'serve',
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
        'sql': {
            'topn': 1000,
            'type': 'section',
            'table': '5m_section',
            'track': 'mb',
            'desc': 'desc',
            'advertiser': '',
            'offset_minutes': -5,
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
        'sql': {
            'topn': 5000,
            'type': 'adv_id',
            'table': '5m_cmp_spend_cumulative',
            'track': 'mb',
            'desc': 'desc',
            'advertiser': '',
            'offset_minutes': -5,
            },
        'charts': [{
            'id': 'native_topdiffadvertiser_latencyDescription',
            'type': 'text',
            'prefix': 'Data in this table has 15-minute latency as it is from Grid'
            },{
            'id': 'native_topdiffadvertiser',
            'type': 'table',
            'fields': 'id,dod_delta,wow_delta,tot_3day_spend,today_spend,ystd_spend,lastwk_spend,today_click,ystd_click,lastwk_click,today_imp,ystd_imp,lastwk_imp,today_serve,ystd_serve,lastwk_serve'
                ,
            'columns': 'ID,DoD<br/>Delta,WoW<br/>Delta,3DaysTotal</br>Rev,Today<br/>Rev,Ystd<br/>Rev,Lastwk<br/>Rev,Today<br/>Click,Ystd<br/>Click,Lastwk<br/>Click,Today<br/>Imp,Ystd<br/>Imp,Lastwk<br/>Imp,Today<br/>Serve,Ystd<br/>Serve,Lastwk<br/>Serve'
                ,
            'order': 'desc,3',
            'invisible': '',
            'links': {
                'id': {
                    'url': 'https://gemini.yahoo.com/internal/advertiser/{id}/campaigns'
                },
                'dod_delta': {
                    'url': 'https://moneywatcher.gemini.yahoo.com/?page=objid&showtabs=splan,advchanges&id={id}&start={start}&end={end}&timezone={timezone}&type=advertiser&offsetdate=yesterday'
                },
                'wow_delta': {
                    'url': 'https://moneywatcher.gemini.yahoo.com/?page=objid&showtabs=splan,advchanges&id={id}&start={start}&end={end}&timezone={timezone}&type=advertiser&offsetdate=lastweek'
                }
            }
            }],
        }, {
        'id': 'native_topdiffcampaign',
        'name': 'Native TopDiff Campaign',
        'sql': {
            'topn': 5000,
            'type': 'cmp_id',
            'table': '5m_cmp_spend_cumulative',
            'track': 'mb',
            'desc': 'desc',
            'advertiser': ', adv_id',
            'offset_minutes': -5
            },
        'charts': [{
            'id': 'native_topdiffcampaign_latencyDescription',
            'type': 'text',
            'prefix': 'Data in this table has 15-minute latency as it is from Grid'
            },{
            'id': 'native_topdiffcampaign',
            'type': 'table',
            'fields': 'id,dod_delta,wow_delta,tot_3day_spend,today_spend,ystd_spend,lastwk_spend,today_click,ystd_click,lastwk_click,today_imp,ystd_imp,lastwk_imp,today_serve,ystd_serve,lastwk_serve,adv'
                ,
            'columns': 'ID,DoD<br/>Delta,WoW<br/>Delta,3DaysTotal</br>Rev,Today<br/>Rev,Ystd<br/>Rev,Lastwk<br/>Rev,Today<br/>Click,Ystd<br/>Click,Lastwk<br/>Click,Today<br/>Imp,Ystd<br/>Imp,Lastwk<br/>Imp,Today<br/>Serve,Ystd<br/>Serve,Lastwk<br/>Serve,Adv'
                ,
            'order': 'desc,3',
            'invisible': '15',
            'links': {
                'id': {
                    'url': 'https://gemini.yahoo.com/internal/advertiser/{adv}/campaign/{id}'
                },
                'dod_delta': {
                    'url': 'https://moneywatcher.gemini.yahoo.com/?page=objid&showtabs=splan&id={id}&start={start}&end={end}&timezone={timezone}&type=campaign&offsetdate=yesterday'
                },
                'wow_delta': {
                    'url': 'https://moneywatcher.gemini.yahoo.com/?page=objid&showtabs=splan&id={id}&start={start}&end={end}&timezone={timezone}&type=campaign&offsetdate=lastweek'
                }
            }

            }],
        }],
    }

native_posttp = {
    'id': 'native_posttp',
    'name': 'Native PostTP',
    'type': 'navtab',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'native_posttp',
        'name': 'Native PostTP',
        'sql': {
            'fields': 'time,impression,click,spend',
            'groupby': 'time',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="native"',
            'offset_minutes': 0
            },
        'charts': [{
            'id': 'native_posttp_spend',
            'title': 'Native PostTP Spend',
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
            'id': 'native_posttp_click',
            'title': 'Native PostTP Click',
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
        'id': 'native_supply_posttp',
        'name': 'Native Supply PostTP',
        'sql': {
            'fields': 'time,supply,spend,click',
            'groupby': 'time,supply',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="native"',
            },
        'charts': [{
            'id': 'native_supply_dodwow',
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
                }],
            }],
        }, {
        'id': 'native_vertical_posttp',
        'name': 'Native Vertical PostTP',
        'sql': {
            'fields': 'time,vertical,spend,click'
                ,
            'groupby': 'time,vertical',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="native"',
            'offset_minutes': -5,
            },
        'charts': [{
            'id': 'native_vertical_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'vertical',
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
                }],
            }]
        }, {
        'id': 'native_device_posttp',
        'name': 'Native Device PostTP',
        'sql': {
            'fields': 'time,device,spend,click'
                ,
            'groupby': 'time,device',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="native"'
            },
        'charts': [{
            'id': 'native_device_dodwow',
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
                    'series': 'PPC',
                    'field': 'spend / click',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                }],
            }],
        }],
    }

msft_nrt = {
    'id': 'msft_nrt',
    'name': 'MSFT NRT',
    'type': 'navtab',
    'layouts': [startTime, endTime, siteids],
    'render': 'triage',
    'tabs': [{
        'id': 'msft_vertical',
        'name': 'MSFT Vertical',
        'sql': {
            'fields': 'time,vertical,spend,impression,click,serve',
            'groupby': 'time,vertical',
            'table': 'revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'track="mb" and vertical in ("MICROSOFT", "MICROSOFT_EXCLUSIVE")',
            'offset_minutes': -5,
            },
        'charts': [{
            'id': 'msft_vertical_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'vertical',
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
                    'series': 'Serve',
                    'field': 'serve',
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
            },
            {
        'id': 'msft_site',
        'name': 'MSFT Site',
        'sql': {
            'fields': 'time,site,spend,impression,click,serve',
            'groupby': 'time,site',
            'table': '5m_section',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5,
            'join': {
                'raw_fields': 'time,section,spend,impression,click,serve',
                'groupby': 'time,section',
                'fixed_condition': 'track="mb"',
                'on': 'section',
                'join_to': {
                    'table': 'section_info',
                    'raw_fields': 'section,site,vertical',
                    'fixed_condition': 'vertical in ("microsoft", "microsoft_exclusive")',
                    'groupby': 'section,site,vertical',
                    'on': 'section'
                    }
                }
            },
        'charts': [{
            'id': 'msft_site_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'site',
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
                    'series': 'Serve',
                    'field': 'serve',
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
        }],
    }

search = {
    'id': 'search',
    'name': 'Search Triage',
    'type': 'navtab',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'bing_posttp',
        'name': 'Bing PostTP',
        'sql': {
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
    'layouts': [startTime, endTime, oid, otype, offset],
    'tabs': [{
        'id': 'splan',
        'name': 'PostTP',
        'sql': 'fetch from hbase',
        'charts':[{
            'id': 'spend_plans',
            'render': 'splan'
            }],
        }, {
        'id': 'throttlerate',
        'name': 'Throttle Rate',
        'sql': {
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
        }, {
        'id': 'nrt',
        'name': 'NRT Metric',
        'show_onload': 'true',
        'sql': {
            'fields': 'time,spend,serve,impression,click',
            'groupby': 'time',
            'table': '5m_cmp_spend',
            'filters': 'cmp_id',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5,
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
        'id': 'advchanges',
        'name': 'Advertiser Changes',
        'api': {
            'url': 'http://iws.gemini.yahoo.com:4080/mb_be/rest/auditlog?ai={id}&usd={start}&ued={end}',
            'yca': 'yahoo.moneyball.adbe.whitelist.gq1'
        },
        'charts':[{
            'id': 'advchanges',
            'type': 'table',
            'fields': 'time,entityType,entityId,entityAttr,oldValue,newValue,accountId,userUpdate'
                ,
            'columns': 'Time [UTC],Entity,Id,Changed,From,To,Advertiser,By'
                ,
            'order': 'desc,0',
            'invisible': '6',
            }],
        },{
        'id': 'nrt_oda',
        'name': 'NRT ODA',
        'sql': {
            'source': 'hive',
            'fields': 'nrt_15m_product_oda,datestamp',
            'groupby': 'datestamp',
            'filters': 'campaign_id',
            'table': 'mx3.product_oda_credit',
            'fixed_condition': 'test_flag=0',
            'partition': 'datestamp',
            'offset_minutes': 0,
            'dateformat': '%Y%m%d%H%M',
            'parallel': 'true'
            },
        'charts': [{
            'id': 'nrt_oda',
            'title': 'Campaign NRT ODA',
            'type': 'timeseries',
            'dodwow': 'false',
            'metrics': [{
                'series': 'Spends',
                'field': 'nrt_15m_product_oda',
                'accumulation': 'true',
                'type': 'area',
                }],
            },]
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
        'sql': {
            'fields': 'time,son_spend',
            'groupby': 'time',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
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

hive = {
    'id': 'hive',
    'name': 'Search Hive',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime],
    'tabs': [{
        'id': 'hive',
        'name': 'Search PostTP Hive',
        'sql': {
            'fields': 'ds,impressions,clicks,revenue_usd'
                ,
            'groupby': 'ds',
            'table': 'budget.posttp_revenue_triage_15m',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'product_type="search"',
            'offset_minutes': 0,
            'source': 'hive',
            'dateformat': '%Y%m%d%H%M',
            'parallel': 'true'
            },
        'charts': [{
            'id': 'search_posttp_spend',
            'title': 'Search PostTP Spend',
            'type': 'timeseries',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [{
                'series': 'Spends',
                'field': 'revenue_usd',
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
                'series': 'Clicks',
                'field': 'clicks',
                'accumulation': 'true',
                'type': 'area',
                }],
            }],
        }]
}

topcampaign = {
    'id': 'topcampaign',
    'name': 'Top Spend Campaigns',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTimeR, endTime],
    'tabs': [{
        'id': 'topcampaign',
        'name': 'Top Spend Campaigns',
        'debug': 1,
        'sql': {
            'fields': 'cmp_id,adv_id,track,spend,serve,impression,click'
                ,
            'groupby': 'cmp_id,adv_id,track',
            'table': '5m_cmp_spend',
            'fixed_condition': 'cmp_id not in (-99999, -88888)',
            'orderby': 'sum(spend)',
            'sort': 'desc',
            'limit': '100',
            'offset_minutes': -5
            },
        'charts': [{
            'id': 'topcampaign_table_latencyDescription',
            'type': 'text',
            'prefix': 'Data in this table has 15-minute latency as it is from Grid'
            },{
            'id': 'topcampaign_table',
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
        'sql': {
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

topsection = {
    'id': 'topsection',
    'name': 'Top Spend Sections',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTimeR, endTime],
    'tabs': [{
        'id': 'topsection',
        'name': 'Top Spend Sections',
        'customized': 'topsection',
        'sql': {
            'fields': 'time,section,spend,serve,impression,click',
            'groupby': 'time,section',
            'table': '5m_section',
            'filters': 'section',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5,
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
            }]
        }]
}

native_metrics = {
    'id': 'native_metrics',
    'type': 'navtab',
    'name': 'Native Ads Metrics',
    'navdropdown': 'labs',
    'layouts': [testCluster, compareCluster, startTimeMR, endTimeMR],
    'tabs': [{
        'id': 'kpiGraph',
        'name': 'KPI Graph',
        'show_onload': 'true',
        'api': {
            'url': "http://monitoring1.nads.bf1.yahoo.com:4080/moneyball_autobots/MetricBotGetJSON?testCluster=native_ads.serving.csp.searcher.{env1}.{colo1}.{cluster1}&compareCluster=native_ads.serving.csp.searcher.{env2}.{colo2}.{cluster2}&startTime={start}&endTime={end}",
        },
        'charts': [{
            'id': 'kpiGraphtext1',
            'type': 'text',
            'databody': 'latencyAbove140',
            'prefix': 'Latency Above 140: '
        },{
            'id': 'kpiGraphtext2',
            'type': 'text',
            'databody': 'acfPercentage',
            'prefix': 'ACF Percentage: '
        },{
            'id': 'hyperlink',
            'type': 'hyperlink',
            'description': 'KPI Graph Link',
        },{
            'id': 'iframe',
            'type': 'iframe',
            'suffix': '&noChrome=1'
        }]

    }, {
        'id': 'latencyAbove140',
        'name': 'Latency Above 140',
        'api': {
            'url': "http://monitoring1.nads.bf1.yahoo.com:4080/moneyball_autobots/MetricBotGetJSON?testCluster=native_ads.serving.csp.searcher.{env1}.{colo1}.{cluster1}&compareCluster=native_ads.serving.csp.searcher.{env2}.{colo2}.{cluster2}&startTime={start}&endTime={end}",
        },
        'charts': [{
            'id': 'latencyAbove140text',
            'type': 'text',
        }, {
            'id': 'latencyAbove140table',
            'type': 'table',
            'fields': '0,1,2,3,4',
            'columns': 'Time,TestCluster,CompareCluster,% Deviation,OK/not-OK'
        }]
    }, {
        'id': 'acfPercentage',
        'name': 'ACF Percentage',
        'api': {
            'url': "http://monitoring1.nads.bf1.yahoo.com:4080/moneyball_autobots/MetricBotGetJSON?testCluster=native_ads.serving.csp.searcher.{env1}.{colo1}.{cluster1}&compareCluster=native_ads.serving.csp.searcher.{env2}.{colo2}.{cluster2}&startTime={start}&endTime={end}",
        },
        'charts': [{
            'id': 'acfPercentagetext',
            'type': 'text',
        },{
            'id': 'acfPercentagetable',
            'type': 'table',
            'fields': '0,1,2,3,4'
                ,
            'columns': 'Time,TestCluster,CompareCluster,% Deviation,OK/not-OK'
        }]
    }]
}

section_geo = {
    'id': 'section_geo',
    'name': 'Geo Spend by Section',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime, sid],
    'render': 'triage',
    'tabs': [{
        'id': 'dodwow',
        'name': 'DoD/WoW',
        'sql': {
            'fields': 'time,spend,country_iso',
            'groupby': 'time,country_iso',
            'table': '5m_section_country',
            'fixed_condition': 'country_iso<>"NULL"',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5
            },
        'charts': [{
            'id': 'geo_spend_dodwow',
            'type': 'timeseries',
            'dodwow': 'true',
            'arrangedby': 'country_iso',
            'render': 'triage',
            'metrics': [{
                'series': 'spend',
                'field': 'spend',
                'separate': 'true',
                'accumulation': 'true',
                'type': 'area',
                }],
             }],
        }],
    }

section_adrank = {
    'id': 'section_adrank',
    'name': 'AdRank Spend by Section',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime, sid],
    'render': 'triage',
    'tabs': [{
        'id': 'dodwow',
        'name': 'DoD/WoW',
        'sql': {
            'fields': 'time,spend,adrank',
            'groupby': 'time,adrank',
            'table': '5m_section_adrank',
            'fixed_condition': 'adrank<>"NULL"',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5
            },
        'charts': [{
            'id': 'adrank_spend_dodwow',
            'type': 'timeseries',
            'dodwow': 'true',
            'arrangedby': 'adrank',
            'render': 'triage',
            'metrics': [{
                'series': 'spend',
                'field': 'spend',
                'separate': 'true',
                'accumulation': 'true',
                'type': 'area',
                }],
             }],
        }],
    }

native_cluster = {
    'id': 'native_cluster',
    'name': 'Native Spend by Cluster',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'clusterdodwow',
        'name': 'Cluster DoD/WoW',
        'sql': {
            'fields': 'time,spend,server_version',
            'groupby': 'time,server_version',
            'table': '5m_cluster_spend',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5
            },
        'charts': [{
            'id': 'cluster_spend_dodwow',
            'type': 'timeseries',
            'dodwow': 'true',
            'arrangedby': 'server_version',
            'render': 'triage',
            'metrics': [{
                'series': 'spend',
                'field': 'spend',
                'separate': 'true',
                'accumulation': 'true',
                'type': 'area',
                }],
             }],
        }, {
        'id': 'colododwow',
        'name': 'Colo DoD/WoW',
        'sql': {
            'fields': 'time,spend,colo',
            'groupby': 'time,colo',
            'table': '5m_cluster_spend',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': -5
            },
        'charts': [{
            'id': 'colo_spend_dodwow',
            'type': 'timeseries',
            'dodwow': 'true',
            'arrangedby': 'colo',
            'render': 'triage',
            'metrics': [{
                'series': 'spend',
                'field': 'spend',
                'separate': 'true',
                'accumulation': 'true',
                'type': 'area',
                }],
             }],
        }],
    }

dpa = {
    'id': 'dpa',
    'name': 'DPA',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'dpa',
        'name': 'DPA PostTP',
        'sql': {
            'fields': 'time,spend',
            'groupby': 'time',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'dpa_type != "NULL" and dpa_type != ""',
            'offset_minutes': 0
            },
        'charts': [{
            'id': 'dpa_posttp_spend',
            'title': 'DPA PostTP Spend',
            'type': 'timeseries',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [{
                'series': 'Spends',
                'field': 'spend',
                'accumulation': 'true',
                'type': 'area',
                }],
            }]
        },{
        'id': 'dpa_type',
        'name': 'DPA Type',
        'sql': {
            'fields': 'time,spend,dpa_type',
            'groupby': 'time, dpa_type',
            'table': 'posttp_revenue_triage',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'dpa_type != "NULL" and dpa_type != ""',
            'offset_minutes': 0
            },
        'charts': [{
            'id': 'dpa_type_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'dodwow': 'true',
            'arrangedby': 'dpa_type',
            'granularity': 15,
            'metrics': [{
                'series': 'Spends',
                'field': 'spend',
                'separate': 'true',
                'accumulation': 'true',
                'type': 'area',
                }],
            }]
        }]
    }

atlantis = {
    'id': 'atlantis',
    'name': 'Atlantis Spend',
    'type': 'navtab',
    'navdropdown': 'labs',
    'layouts': [startTime, endTime],
    'render': 'triage',
    'tabs': [{
        'id': 'atlantis_overview',
        'name': 'Overview',
        'sql': {
            'fields': 'time,spend_usd,clicks',
            'groupby': 'time',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'offset_minutes': 0
            },
        'charts': [{
            'id': 'atlantis_posttp_spend',
            'title': 'Atlantis Spend (Without Google)',
            'type': 'timeseries',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [{
                'series': 'Spends',
                'field': 'spend_usd',
                'accumulation': 'true',
                'type': 'area',
                }],
            }, {
            'id': 'atlantis_posttp_click',
            'title': 'Atlantis Click (With Google)',
            'type': 'timeseries',
            'dodwow': 'true',
            'granularity': 15,
            'metrics': [{
                'series': 'Click',
                'field': 'clicks',
                'accumulation': 'true',
                'type': 'area',
                }],
            }],
        }, {
        'id': 'atlantis_website_country',
        'name': 'Website Country',
        'sql': {
            'fields': 'time,website_country,spend_usd,clicks',
            'groupby': 'time,website_country',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'ad_provider!="Google"',
            },
        'charts': [{
            'id': 'atlantis_website_country_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'website_country',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                ],
            }],
        }, {
        'id': 'atlantis_device',
        'name': 'Device',
        'sql': {
            'fields': 'time,device_name,spend_usd,clicks',
            'groupby': 'time,device_name',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'ad_provider!="Google"'
            },
        'charts': [{
            'id': 'atlantis_device_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'device_name',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                }
                ],
            }],
        }, {
        'id': 'atlantis_ad_provider',
        'name': 'Ad Provider',
        'sql': {
            'fields': 'time,ad_provider,spend_usd,clicks',
            'groupby': 'time,ad_provider',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            },
        'charts': [{
            'id': 'atlantis_ad_provider_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'ad_provider',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                }
                ],
            }],
        }, {
        'id': 'atlantis_entry_point',
        'name': 'Entry Point',
        'sql': {
            'fields': 'time,named_entry_point_group,spend_usd,clicks',
            'groupby': 'time,named_entry_point_group',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'ad_provider!="Google"',
            },
        'charts': [{
            'id': 'atlantis_entry_point_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'named_entry_point_group',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                    },
                ],
            }],
        }, {
        'id': 'atlantis_market',
        'name': 'Market',
        'sql': {
            'fields': 'time,market_classification,spend_usd,clicks',
            'groupby': 'time,market_classification',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'ad_provider!="Google"'
            },
        'charts': [{
            'id': 'atlantis_market_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'market_classification',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                }
                ],
            }],
        }, {
        'id': 'atlantis_traffic_type',
        'name': 'Traffic Type',
        'sql': {
            'fields': 'time,x_traffic_type,spend_usd,clicks',
            'groupby': 'time,x_traffic_type',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'ad_provider!="Google"'
            },
        'charts': [{
            'id': 'atlantis_traffic_type_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'x_traffic_type',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                }
                ],
            }],
        }, {
        'id': 'atlantis_ginsu_partner',
        'name': 'Ginsu Partner',
        'sql': {
            'fields': 'time,ginsu_partner,spend_usd,clicks',
            'groupby': 'time,ginsu_partner',
            'table': 'atlantis_spend',
            'dod': 'true',
            'wow': 'true',
            'fixed_condition': 'ad_provider!="Google"'
            },
        'charts': [{
            'id': 'atlantis_ginsu_partner_dodwow',
            'render': 'triage',
            'type': 'timeseries',
            'arrangedby': 'ginsu_partner',
            'granularity': 15,
            'metrics': [
                {
                    'series': 'Revenue',
                    'field': 'spend_usd',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'Click',
                    'field': 'clicks',
                    'color': '#555555',
                    'type': 'line',
                },
                {
                    'series': 'PPC',
                    'field': 'spend_usd / clicks',
                    'color': '#555555',
                    'accumulation': 'false',
                    'type': 'line',
                }
                ],
            }],
        }],
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
    native_posttp,
    msft_nrt,
    search,
    objid,
    labs,
    dodcomparison,
    topcampaign,
    topsection,
    son,
    native_metrics,
    section_geo,
    section_adrank,
    native_cluster,
    dpa,
    atlantis,
    help
    ]}

def load_config(page):
    if not page:
        return page_config
    navigations = page_config['navigations']
    for navigation in navigations:
        if page == navigation['id']:
            return navigation
    return page_config

