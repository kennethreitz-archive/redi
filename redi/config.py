# -*- coding: utf-8 -*-

"""
redi.config
~~~~~~~~~~~

This module contains the redi configuration.

"""


from redis import Redis

import jsonpickle


encoder =  jsonpickle.encode
decoder = jsonpickle.decode
str_codec = 'utf8'
block_timeout = 10



def init(host='localhost', port=6379, db=0):
    """Configures module-level redis instance."""

    global redis
    redis = Redis(host=host, port=port, db=db)


init()