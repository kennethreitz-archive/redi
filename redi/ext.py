# -*- coding: utf-8 -*-

"""
redi.ext
~~~~~~~~

This module contains extra stuff.

"""


from . import config
from . import models
from .utils import is_collection, compress_key


TYPE_MAP = {
    'value': models.RedisListString,
    'string': models.RedisListString,
    'list': models.RedisList
}


def auto_type(key, redis=None, default=None):
    """Returns datatype instance"""

    if redis is None:
        redis = config.redis

    key = compress_key(key)

    if redis.exists(key):

        datatype = redis.type(key)

        return TYPE_MAP.get(datatype)(key, redis=redis)

    else:
        if default:
            try:
                return TYPE_MAP.get(default)(key, redis=redis)
            except KeyError:
                raise ValueError('Provide a valid default redis type.')

        return None

