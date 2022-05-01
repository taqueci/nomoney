# Copyright (C) Takeshi Nakamura. All rights reserved.

import datetime

from django.core.paginator import Paginator
from django.db.models import CharField, F, Sum, Value
from django.db.models.functions import Concat
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_filters import OrderingFilter

from ..models import Journal, Tag
from .shared import account, chart, date, journal

INDEX_PER_PAGE = 20
INDEX_DEFAULT_SORT = '-date'
INDEX_DEFAULT_UNIT = 'annual'


class Filter(journal.Filter):
    sort = OrderingFilter(
        fields=(
            ('income', 'income'), ('expense', 'expense'),
            ('balance', 'balance'),
            ('year', 'year'), ('month', 'month'),
            ('week', 'week'), ('date', 'date'),
        )
    )


def index(request):
    n = request.GET.get('page')
    param = _index_query_param(request.GET.get('unit'))
    fields = param['fields']

    q = Journal.objects.available()

    q = q.values(*fields).annotate(
        label=param['label'],
        income=Sum('income', default=0), expense=Sum('expense', default=0),
        balance=F('income')-F('expense'),
    )

    q = Filter(_index_query_dict(request.GET, fields), queryset=q).qs

    paginator = Paginator(q, INDEX_PER_PAGE)

    return render(request, 'money/reports/index.html', {
        'page': paginator.get_page(n), 'total': paginator.count,
    })


def show(request, pk):  # pylint: disable=unused-argument
    start = request.GET.get('start') or '1970-01-01'
    end = request.GET.get('end') or '2100-12-31'

    q = Filter(request.GET, queryset=Journal.objects.available()).qs

    summary = q.aggregate(
        incomes=Sum('income', default=0), expenses=Sum('expense', default=0),
        assets=Sum('asset', default=0),
        liabilities=Sum('liability', default=0),
        balance=Sum(F('income')-F('expense'), default=0),
        net=Sum(F('asset')-F('liability'), default=0),
    )

    incomings = q.exclude(income=0).values(
        'credit__id', 'credit__name'
    ).annotate(sum=Sum('income', default=0)).order_by('-sum')

    outgoings = q.exclude(expense=0).values(
        'debit__id', 'debit__name'
    ).annotate(sum=Sum('expense', default=0)).order_by('-sum')

    tags = Tag.objects.all()
    grouped_accounts = account.grouped_objects()

    return render(request, 'money/reports/show.html', {
        'object': {'name': _('All')},
        'page': date.range_next_prev(start, end),
        'summary': summary, 'incomings': incomings, 'outgoings': outgoings,
        'data_doughnut_incoming': chart.data_doughnut_incoming(incomings),
        'data_doughnut_outgoing': chart.data_doughnut_outgoing(outgoings),
        'data_charts': _chart_data_lines(q, start, end, incomings, outgoings),
        'accounts': grouped_accounts, 'tags': tags,
    })


def _index_query_dict(data, fields):
    val = data.get('sort', INDEX_DEFAULT_SORT)
    params = []

    for x in val.split(','):
        if x == 'date':
            params.extend(fields)
        elif x == '-date':
            params.extend([f'-{x}' for x in fields])
        else:
            params.append(x)

    qd = data.copy()
    qd['sort'] = ','.join(params)

    return qd


def _index_query_param(unit):
    params = {
        'annual': {
            'fields': ('year', ), 'label': F('year')
        },
        'monthly': {
            'fields': ('year', 'month'),
            'label': Concat(
                F('year'), Value('-'), F('month'), output_field=CharField()
            )
        },
        'weekly': {
            'fields': ('year', 'week'),
            'label': Concat(
                F('year'), Value('-W'), F('week'), output_field=CharField()
            )
        },
        'daily': {
            'fields': ('year', 'date'), 'label': F('date')
        },
    }

    return params.get(unit, params[INDEX_DEFAULT_UNIT])


def _chart_data_lines(query, start, end, incomings, outgoings):
    s = datetime.datetime.strptime(start, '%Y-%m-%d')
    e = datetime.datetime.strptime(end, '%Y-%m-%d')

    days = (e - s).days + 1

    data = {}

    if days >= 365:
        data['annual'] = {
            'balance': _chart_data_balance(query, 'year'),
            'asset': _chart_data_asset(query, 'year'),
            'incoming': _chart_data_incoming(incomings, query, 'year'),
            'outgoing': _chart_data_outgoing(outgoings, query, 'year'),
        }
    else:
        data['daily'] = {
            'balance': _chart_data_balance(query, 'date'),
            'asset': _chart_data_asset(query, 'date'),
            'incoming': _chart_data_incoming(incomings, query, 'date'),
            'outgoing': _chart_data_outgoing(outgoings, query, 'date'),
        }

    if days > 31:
        data['monthly'] = {
            'balance': _chart_data_balance(query, 'year', 'month'),
            'asset': _chart_data_asset(query, 'year', 'month'),
            'incoming': _chart_data_incoming(
                incomings, query, 'year', 'month'
            ),
            'outgoing': _chart_data_outgoing(
                outgoings, query, 'year', 'month'
            ),
        }

    if 365 * 5 >= days > 7:
        data['weekly'] = {
            'balance': _chart_data_balance(query, 'year', 'week'),
            'asset': _chart_data_asset(query, 'year', 'week'),
            'incoming': _chart_data_incoming(incomings, query, 'year', 'week'),
            'outgoing': _chart_data_outgoing(outgoings, query, 'year', 'week'),
        }

    return data


def _chart_data_balance(query, *keys):
    q = query.values(*keys).annotate(
        data1=Sum('income', default=0), data2=Sum('expense', default=0)
    ).order_by(*keys)

    label1 = _('Incoming')
    label2 = _('Outgoing')

    return {
        'normal': _chart_data_2lines(q, False, label1, label2, *keys),
        'accumulated': _chart_data_2lines(q, True, label1, label2, *keys),
    }


def _chart_data_asset(query, *keys):
    q = query.values(*keys).annotate(
        data1=Sum('asset', default=0), data2=Sum('liability', default=0)
    ).order_by(*keys)

    label1 = _('Asset')
    label2 = _('Liability')

    return {
        'normal': _chart_data_2lines(q, False, label1, label2, *keys),
        'accumulated': _chart_data_2lines(q, True, label1, label2, *keys),
    }


def _chart_data_2lines(query, accumulated, label1, label2, *keys):
    data = {
        'datasets': [{
            'label': label1,
            'data': [],
            'radius': 2,
            'backgroundColor': 'rgba(153,255,51,0.4)',
            'borderWidth': 1,
            'borderColor': '#b2ff59',
            'hitRadius': 2,
            'fill': True,
            'tension': 0.25,
        }, {
            'label': label2,
            'data': [],
            'radius': 2,
            'backgroundColor': 'rgba(255,153,0,0.4)',
            'borderWidth': 1,
            'borderColor': '#ffab40',
            'hitRadius': 2,
            'fill': True,
            'tension': 0.25,
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
    ).annotate(sum=Sum('income', default=0)).order_by(*keys)

    return {
        'normal': _chart_data_stacked(label, q, False, 'credit', *keys),
        'accumulated': _chart_data_stacked(label, q, True, 'credit', *keys),
    }


def _chart_data_outgoing(label, query, *keys):
    q = query.values(
        *keys, 'debit__id', 'debit__name',
    ).annotate(sum=Sum('expense', default=0)).order_by(*keys)

    return {
        'normal': _chart_data_stacked(label, q, False, 'debit', *keys),
        'accumulated': _chart_data_stacked(label, q, True, 'debit', *keys),
    }


def _chart_data_stacked(label, query, accumulated, field, *keys):
    # pylint: disable=too-many-locals

    field_id = field + '__id'
    field_name = field + '__name'

    datasets = [{
        '_id': x[field_id],
        '_sum': 0,
        'label': x[field_name],
        'data': [],
        'radius': 2,
        'backgroundColor': chart.STACKED_COLOR[i % len(chart.STACKED_COLOR)],
        'borderWidth': 1,
        'borderColor': 'rgba(255,255,255,0.1)',
        'hitRadius': 2,
        'fill': True,
        'tension': 0.25,
    } for i, x in enumerate(label)]

    data = {}

    for x in query:
        val_x = _chart_data_val_x(x, *keys)
        pk = x[field_id]

        for y in datasets:
            if y['_id'] == pk:
                if val_x not in data:
                    data[val_x] = {}

                data[val_x][pk] = x['sum']

    for t, val in data.items():
        for d in datasets:
            pk = d['_id']
            y = val[pk] if pk in val else 0
            offset = d['_sum'] if accumulated else 0

            d['data'].append({'x': t, 'y': y + offset})
            d['_sum'] += y

    return {'datasets': datasets}


def _chart_data_val_x(obj, *keys):
    if keys[0] == 'date':
        return obj['date']

    if len(keys) == 1:
        return obj['year']

    if keys[1] == 'week':
        return f'{obj["year"]}W{obj["week"]:02}'

    return f'{obj["year"]}-{obj["month"]:02}'
