# -*- coding: UTF-8 -*-

"""
Redis-based mini DB with weather forecasts and pollution indices from the last
hour.
"""

import os
import redis
import json
import time

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


def __ensure_key_exist(k):
    if not redis.exists(k):
        fetch_data()


def get_pollution():
    k = 'data.pollution.json'
    __ensure_key_exist(k)
    return json.loads(redis.get(k) or 'null')


def get_weather():
    k = 'data.weather.json'
    __ensure_key_exist(k)
    return json.loads(redis.get(k) or 'null')


def get_last_fetch():
    k = 'data.last_fetch'
    __ensure_key_exist(k)
    return redis.get(k)
