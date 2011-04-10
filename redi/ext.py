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
    'string': models.RedisString,
    'value': models.RedisString,

    'liststring': models.RedisListString,
    'list-string': models.RedisListString,
    'stringlist': models.RedisListString,
    'string-list': models.RedisListString,

    'dictstring': models.RedisDictString,
    'dict-string': models.RedisDictString,
    'stringdict': models.RedisDictString,
    'string-dict': models.RedisDictString,

    'list': models.RedisList
}



def auto_type(key, redis=None, default=None):
    """Returns datatype instance"""

    if redis is None:
        redis = config.redis

    key = compress_key(key)

    if redis.exists(key):

        datatype = redis.type(key)

        if datatype == 'string':
            test_string = models.RedisString(key).data

            if isinstance(test_string, dict):
                datatype = 'dict-string'
            elif isinstance(test_string, list):
                datatype = 'list-string'
            elif isinstance(test_string, basestring):
                datatype = 'string'
            elif isinstance(test_string, int):
                datatype = 'string'
            elif isinstance(test_string, float):
                datatype = 'string'

        return TYPE_MAP.get(datatype)(key, redis=redis)

    else:
        if default:
            try:
                return TYPE_MAP.get(default)(key, redis=redis)
            except KeyError:
                raise ValueError('Provide a valid default redis type.')

        return None

