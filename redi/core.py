# -*- coding: utf-8 -*-

"""
redi.core
~~~~~~~~~

This module contains the primary interface for redi.

Simple, eh?

"""



from .utils import is_collection
from . import config
from . import models



def _expand_key(key):
    """Expands tupled keys."""

    if is_collection(key):
        key = config.namespace_delimiter.join(key)

    return key



def value(key, redis=config.redis):
    """Return RedisValue instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """


    return models.RedisValue(_expand_key(key), redis=config.redis)



def list(key, redis=config.redis):
    """Return RedisList instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return models.RedisList(_expand_key(key), redis=config.redis)