# -*- coding: utf-8 -*-

"""
redi.models
~~~~~~~~~~~

This module contains the configuration of redi.

"""

from redis import Redis

ENCODING = 'utf8'


def init(host='localhost', port=6379, db=0):
    """Configures module-level redis instance."""

    global redis
    redis = Redis(host=host, port=port, db=db)


init()