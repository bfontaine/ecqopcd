# -*- coding: UTF-8 -*-

"""
Redis-based mini DB with weather forecasts and pollution indices from the last
hour.
"""

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
    redis.set('data.pollution.json', json.dumps(p.indices()))
    redis.set('data.weather.json', weather.defaultClient().weather())
    redis.set('data.last_fetch', int(time.time()))


def pollution():
    return json.loads(redis.get('data.pollution.json') or 'null')


def weather():
    return json.loads(redis.get('data.weather.json') or 'null')
