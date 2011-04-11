# -*- coding: utf-8 -*-

"""
redi.config
~~~~~~~~~~~

This module contains the redi configuration.

"""


from redis import Redis as RedisClient

from .packages import jsonpickle


encoder =  jsonpickle.encode
decoder = jsonpickle.decode
namespace_delimiter = ':'
str_codec = 'utf8'
block_timeout = 10



def init(host='localhost', port=6379, db=0, password=None, r=None):
    """Configures module-level redis instance."""

    global redis

    if r is not None:
        redis = r
    else:
        redis = RedisClient(host=host, port=port, db=db, password=password)


init()
