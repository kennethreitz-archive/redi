# -*- coding: utf-8 -*-

"""
redi.config
~~~~~~~~~~~

This module contains the redi configuration.

"""


from redis import Redis


ENCODING = 'utf8'



def init(host='localhost', port=6379, db=0):
    """Configures module-level redis instance."""

    global redis
    redis = Redis(host=host, port=port, db=db)


init()