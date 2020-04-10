# Copyright (C) Takeshi Nakamura. All rights reserved.

import datetime

from django.db.models import F, Sum
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from ..models import Journal
from .shared import chart, date, value

INDEX_NUM = 7


def index(request):
    q = Journal.objects.filter(disabled=False)

    annual = q.values('year').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-year')[:INDEX_NUM]

    monthly = q.values('year', 'month').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-year', '-month')[:INDEX_NUM]

    weekly = q.values('year', 'month', 'week').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-year', '-month', '-week')[:INDEX_NUM]

    daily = q.values('date').annotate(
        income=Sum('income'), expense=Sum('expense'),
        balance=F('income')-F('expense')
    ).order_by('-date')[:INDEX_NUM]

    return render(request, 'money/reports/index.html', {
        'annual': annual, 'monthly': monthly, 'weekly': weekly, 'daily': daily,
    })


def show(request, id):
    q = Journal.objects.filter(disabled=False)

    start = request.GET.get('start', '1970-01-01')
    end = request.GET.get('end', '2100-12-31')

    q = q.filter(date__gte=start)
    q = q.filter(date__lte=end)

    summary = q.aggregate(
        income=Sum('income'), expense=Sum('expense'),
        asset=Sum('asset'), liability=Sum('liability'), equity=Sum('equity'),
        balance=Sum(F('income')-F('expense')),
        net=Sum(F('asset')-F('liability')),
    )

    incoming = q.exclude(income=0).values(
        'credit__id', 'credit__name'
    ).annotate(sum=Sum('income')).order_by('-sum')

    outgoing = q.exclude(expense=0).values(
        'debit__id', 'debit__name'
    ).annotate(sum=Sum('expense')).order_by('-sum')

    return render(request, 'money/reports/show.html', {
        'object': {'name': _('All')},
        'page': date.range_next_prev(start, end),
        'summary': summary, 'incoming': incoming, 'outgoing': outgoing,
        'data_doughnut_incoming': chart.data_doughnut_incoming(incoming),
        'data_doughnut_outgoing': chart.data_doughnut_outgoing(outgoing),
        'data_charts': _chart_data_lines(q, start, end, incoming, outgoing),
    })


def _chart_data_lines(query, start, end, incoming, outgoing):
    s = datetime.datetime.strptime(start, '%Y-%m-%d')
    e = datetime.datetime.strptime(end, '%Y-%m-%d')

    days = (e - s).days + 1

    data = {}

    if days >= 365:
        data['annual'] = {
            'balance': _chart_data_balance(query, 'year'),
            'asset': _chart_data_asset(query, 'year'),
            'incoming': _chart_data_incoming(incoming, query, 'year'),
            'outgoing': _chart_data_outgoing(outgoing, query, 'year'),
        }
    else:
        data['daily'] = {
            'balance': _chart_data_balance(query, 'date'),
            'asset': _chart_data_asset(query, 'year'),
            'incoming': _chart_data_incoming(incoming, query, 'date'),
            'outgoing': _chart_data_outgoing(outgoing, query, 'date'),
        }

    if days > 31:
        data['monthly'] = {
            'balance': _chart_data_balance(query, 'year', 'month'),
            'asset': _chart_data_asset(query, 'year', 'month'),
            'incoming': _chart_data_incoming(incoming, query, 'year', 'month'),
            'outgoing': _chart_data_outgoing(outgoing, query, 'year', 'month'),
        }

    if 365 * 5 >= days > 7:
        data['weekly'] = {
            'balance': _chart_data_balance(query, 'year', 'week'),
            'asset': _chart_data_asset(query, 'year', 'week'),
            'incoming': _chart_data_incoming(incoming, query, 'year', 'week'),
            'outgoing': _chart_data_outgoing(outgoing, query, 'year', 'week'),
        }

    return data


def _chart_data_balance(query, *keys):
    q = query.values(*keys).annotate(
        data1=Sum('income'), data2=Sum('expense')
    ).order_by(*keys)

    l1 = _('Incoming')
    l2 = _('Outgoing')

    return {
        'normal': _chart_data_2lines(q, False, l1, l2,*keys),
        'accumulated': _chart_data_2lines(q, True, l1, l2, *keys),
    }


def _chart_data_asset(query, *keys):
    q = query.values(*keys).annotate(
        data1=Sum('asset'), data2=Sum('liability')
    ).order_by(*keys)

    l1 = _('Asset')
    l2 = _('Liability')

    return {
        'normal': _chart_data_2lines(q, False, l1, l2, *keys),
        'accumulated': _chart_data_2lines(q, True, l1, l2, *keys),
    }


def _chart_data_2lines(query, accumulated, label1, label2, *keys):
    data = {
        'datasets': [{
            'label': label1,
            'data': [],
            'radius': 2,
            'backgroundColor': 'rgba(153,255,51,0.4)',
            'borderWidth': 0,
            'borderColor': '#b2ff59',
            'hitRadius': 2,
        }, {
            'label': label2,
            'data': [],
            'radius': 2,
            'backgroundColor': 'rgba(255,153,0,0.4)',
            'borderWidth': 0,
            'borderColor': '#ffab40',
            'hitRadius': 2,
        }]
    }

    val_y1 = 0
    val_y2 = 0

    for x in query:
        val_x = _chart_data_val_x(x, *keys)
        val_y1 = x['data1'] + val_y1 if accumulated else x['data1']
        val_y2 = x['data2'] + val_y2 if accumulated else x['data2']

        if x['data1']:
            data['datasets'][0]['data'].append({'x': val_x, 'y': val_y1})

        if x['data2']:
            data['datasets'][1]['data'].append({'x': val_x, 'y': val_y2})

    return data


def _chart_data_incoming(label, query, *keys):
    q = query.values(
        *keys, 'credit__id', 'credit__name',
    ).annotate(sum=Sum('income')).order_by(*keys)

    return {
        'normal': _chart_data_stacked(label, q, False, 'credit', *keys),
        'accumulated': _chart_data_stacked(label, q, True, 'credit', *keys),
    }


def _chart_data_outgoing(label, query, *keys):
    q = query.values(
        *keys, 'debit__id', 'debit__name',
    ).annotate(sum=Sum('expense')).order_by(*keys)

    return {
        'normal': _chart_data_stacked(label, q, False, 'debit', *keys),
        'accumulated': _chart_data_stacked(label, q, True, 'debit', *keys),
    }


def _chart_data_stacked(label, query, accumulated, field, *keys):
    field_id = field + '__id'
    field_name = field + '__name'

    datasets = [{
        '_id': x[field_id],
        '_sum': 0,
        'label': x[field_name],
        'data': [],
        'radius': 2,
        'backgroundColor': chart.STACKED_COLOR[i % len(chart.STACKED_COLOR)],
        'borderWidth': 0,
        'borderColor': 'rgba(255,255,255,0.1)',
        'hitRadius': 2,
    } for i, x in enumerate(label)]

    data = {}

    for x in query:
        val_x = _chart_data_val_x(x, *keys)
        id = x[field_id]

        for y in datasets:
            if y['_id'] == id:
                if not val_x in data:
                    data[val_x] = {}

                data[val_x][id] = x['sum']

    for t, val in data.items():
        for d in datasets:
            id = d['_id']
            y = val[id] if id in val else 0
            offset = d['_sum'] if accumulated else 0

            d['data'].append({'t': t, 'y': y + offset})
            d['_sum'] += y

    return {'datasets': datasets}


def _chart_data_val_x(obj, *keys):
    l = len(keys)

    if keys[0] == 'date':
        return obj['date']
    elif len(keys) == 1:
        return obj['year']
    elif keys[1] == 'week':
        return '{}W{:02}'.format(obj['year'], obj['week'])

    return '{}-{:02}'.format(obj['year'], obj['month'])
