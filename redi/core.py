# -*- coding: utf-8 -*-

"""
redi.core
~~~~~~~~~

This module contains the primary interface for redi.

Simple, eh?

"""


from . import config, models, db, ext


def value(key, redis=config.redis):
    """Return RedisValue instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """


    return models.RedisValue(ext.expand_key(key), redis=config.redis)



def list(key, redis=config.redis):
    """Return RedisList instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return models.RedisList(ext.expand_key(key), redis=config.redis)


def key(key, redis=config.redis):
    """Return Redi Dattype instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return ext.auto_type(key, redis=config.redis)