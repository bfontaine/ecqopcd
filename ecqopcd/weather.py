# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import os
import xmltodict
from urllib import urlopen

__day_names = {
    'Auj': 'Aujourd’hui',
    'Lun': 'Lundi',
    'Mar': 'Mardi',
    'Mer': 'Mercredi',
    'Jeu': 'Jeudi',
    'Ven': 'Vendredi',
    'Sam': 'Samedi',
    'Dim': 'Dimanche',
}

SUNNY = 100
MOSTLY_SUNNY = 95
CLOUDY = 80
MOSTLY_CLOUDY = 60
MIST = 30
STORMY = 15

# condition -> indice on 100. The higher the better
conditions = {
    'ensoleillé': SUNNY,
    'globalement ensoleillé': MOSTLY_SUNNY,
    'globalement couvert': MOSTLY_CLOUDY,
    'nuageux': CLOUDY,
    'risque de pluie': MIST,
    'pluie fine': MIST,
    'risque d\'orages': STORMY,
}


def get_condition_indice(condition):
    return conditions.get(condition.lower(), 50)


def get_day_name(short):
    return __day_names.get(short, short)


class PreviMeteoClient():

    def __init__(self, api_key):
        if not api_key:
            raise Exception("You need a previmeteo.com API key.")
        self.base_url = 'http://api.previmeteo.com/%s/ig/api' % api_key

    def weather(self, city='paris,FR', language='fr'):
        p = urlopen('%s?weather=%s&hl=%s' % (self.base_url, city, language))
        xml = xmltodict.parse(p.read())['xml_api_reply']['weather']
        curr = xml['current_conditions']
        return {
            'city': xml['forecast_information']['city']['@data'],
            'current': {
                'condition': curr['condition']['@data'],
                'temperature': curr['temp_c']['@data'],
                'humidity': curr['humidity']['@data'],
                'wind': curr['wind_condition']['@data'],
            },
            'forecast': [  # today + 3 days after
                {
                    'day': get_day_name(fc['day_of_week']['@data']),
                    'low': int(fc['low']['@data']),
                    'high': int(fc['high']['@data']),
                    'condition': fc['condition']['@data'],
                } for fc in xml['forecast_conditions']
            ]
        }


def defaultClient():
    return PreviMeteoClient(os.getenv('PREVIMETEO_KEY'))
