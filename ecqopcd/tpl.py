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


def forecast_icon(condition):
    """
    return an icon for a forecast condition. This is HTML code and thus should
    not be escaped in the template.
    """
    v = w.get_condition_indice(condition)
    return '<i class="ss-icon">&#x%s;</i>' % __icons.get(v)


def pollution_class(indice):
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
    while len(pollution) < 3:
        pollution.append(None)
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
    high = w[day]['high']
    low = w[day]['low']
    wt = get_condition_indice(w[day]['condition'])
    words = {-1: 'non', 0: 'peut-&ecirc;tre', 1: 'oui'}

    # very bad conditions
    if high < 0 or p >= 78 or wt <= 35:
        return words[-1]

    # good conditions
    if p <= 65 and wt > 45:
        return words[1]

    # maybe
    return words[0]


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
