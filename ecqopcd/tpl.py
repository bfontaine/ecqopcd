# -*- coding: UTF-8 -*-

"""
templates helpers
"""

import db


def forecast_icon(condition):
    """
    return an icon for a forecast condition. This is HTML code and thus should
    not be escaped in the template.
    """
    base_code = '<i class="ss-icon">&#x%s;</i>'

    # TODO
    return base_code % '2600' # sun


def pollution_class(indice):
    # TODO
    return 'good'


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


def tpl_vals():
    last_fetch = db.get_last_fetch()
    return {
        'pollution': tpl_pollution(),
        'weather': tpl_weather(),
        'last_fetch': last_fetch,
        'answer': 'peut-être', # TODO
    }
