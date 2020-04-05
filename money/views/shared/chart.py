# Copyright (C) Takeshi Nakamura. All rights reserved.

DOUGHNUT_COLOR = (
    '#ff4081', # 02
    '#448aff', # 06
    '#69f0ae', # 10
    '#ffd740', # 14
    '#e040fb', # 03
    '#40c4ff', # 07
    '#b2ff59', # 11
    '#ffab40', # 15
    '#ff5252', # 01
    '#536dfe', # 05
    '#64ffda', # 09
    '#ffff00', # 13
    '#7c4dff', # 04
    '#18ffff', # 08
    '#eeff41', # 12
    '#ff6e40', # 16
)


def data_doughnut_incoming(query):
    data = {
        'labels': [],
        'datasets': [{
            'data': [],
            'backgroundColor': DOUGHNUT_COLOR,
	    'hoverBackgroundColor': DOUGHNUT_COLOR
        }]
    }

    for x in query:
        data['labels'].append(x['credit__name'])
        data['datasets'][0]['data'].append(x['sum'])

    return data


def data_doughnut_outgoing(query):
    data = {
        'labels': [],
        'datasets': [{
            'data': [],
            'backgroundColor': DOUGHNUT_COLOR,
	    'hoverBackgroundColor': DOUGHNUT_COLOR
        }]
    }

    for x in query:
        data['labels'].append(x['debit__name'])
        data['datasets'][0]['data'].append(x['sum'])

    return data
