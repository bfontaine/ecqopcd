# -*- coding: UTF-8 -*-

import os
import xmltodict
from urllib import urlopen

__day_names = {
    u'Auj': u'Aujourd’hui',
    u'Lun': u'Lundi',
    u'Mar': u'Mardi',
    u'Mer': u'Mercredi',
    u'Jeu': u'Jeudi',
    u'Ven': u'Vendredi',
    u'Sam': u'Samedi',
    u'Dim': u'Dimanche',
}

SUNNY = 100
CLOUDY = 80
MOSTLY_CLOUDY = 60
MIST = 30

# condition -> indice on 100. The higher the better
conditions = {
    u'ensoleillé': SUNNY,
    u'globalement couvert': MOSTLY_CLOUDY,
    u'nuageux': CLOUDY,
    u'pluie fine': MIST,
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
