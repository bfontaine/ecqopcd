# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

"""
Redis-based mini DB with weather forecasts and pollution indices from the last
hour.
"""

import os
import redis
import json
import time

from redis.exceptions import ConnectionError

from firapria import pollution
import ecqopcd.weather as weather

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


def fetch_data():
    """
    Fetch external data and store it in redis
    """
    p = pollution.PollutionFetcher()
    w = weather.defaultClient().weather()
    redis.set('data.pollution.json', json.dumps(p.indices()))
    redis.set('data.weather.json', json.dumps(w))
    redis.set('data.last_fetch', int(time.time()))


def __get_key_or_null(k):
    if not redis.exists(k):
        fetch_data()
    return json.loads(redis.get(k) or 'null')


def get_pollution():
    return __get_key_or_null('data.pollution.json')


def get_weather():
    return __get_key_or_null('data.weather.json')


def get_last_fetch():
    return __get_key_or_null('data.last_fetch')
