# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

"""
templates helpers
"""

import db
import weather as w
from weather import get_condition_indice

__icons = {
    w.SUNNY: '3600',
    w.CLOUDY: '2601',
    w.MOSTLY_CLOUDY: 'F220',
    w.MIST: 'F225',
}

__i18n = {
    'no': 'non',
    'maybe': 'peut-être',
    'yes': 'oui',
}


def forecast_icon(condition):
    """
    return an icon for a forecast condition.
    """
    v = w.get_condition_indice(condition)
    return '&#x%s;' % __icons.get(v)


def pollution_class(indice):
    if indice == '?':
        return 'unknown'

    if indice < 45:
        return 'very-good'
    if indice < 60:
        return 'good'
    if indice < 70:
        return 'medium'
    if indice < 90:
        return 'bad'

    return 'very-bad'


def tpl_pollution():
    pollution = db.get_pollution()
    if len(pollution) < 3:
        pollution.append('?')
    return {
        'today': {
            'value': pollution[1],
            'class': pollution_class(pollution[1]),
        },
        'tomorrow': {
            'value': pollution[2],
            'class': pollution_class(pollution[2]),
        },
    }


def tpl_weather():
    weather = db.get_weather()
    today = weather['current']
    tomorrow = weather['forecast'][1]
    return {
        'city': weather['city'],
        'today': {
            'condition': today['condition'],
            'high': today['temperature'],
            'low': today['temperature'],
            'humidity': today['humidity'],
            'wind': today['wind'],
            'day': None,
            'icon': forecast_icon(today['condition']),
        },
        'tomorrow': {
            'condition': tomorrow['condition'],
            'high': tomorrow['high'],
            'low': tomorrow['low'],
            'humidity': None,
            'wind': None,
            'day': tomorrow['day'],
            'icon': forecast_icon(tomorrow['condition']),
        },
    }


def tpl_answer(p, w, day='tomorrow'):
    p = p[day]['value']
    high = int(w[day]['high'])
    low = int(w[day]['low'])
    wt = int(get_condition_indice(w[day]['condition']))
    words = {-1: 'no', 0: 'maybe', 1: 'yes'}

    # maybe
    w = 0

    if not isinstance(p, int) and wt > 40:
        # unknown pollution indice but good weather -> maybe
        w = 0
    # very bad conditions
    elif high < 0 or p >= 78 or wt <= 35:
        w = -1
    # good conditions
    elif p <= 65 and wt > 45:
        w = 1

    word = words[w]
    return {'class': word, 'text': __i18n.get(word, word)}


def tpl_vals():
    last_fetch = db.get_last_fetch()
    pollution = tpl_pollution()
    weather = tpl_weather()
    return {
        'pollution': pollution,
        'weather': weather,
        'last_fetch': last_fetch,
        'answer': tpl_answer(pollution, weather)
    }
