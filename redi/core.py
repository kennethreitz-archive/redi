# -*- coding: utf-8 -*-

"""
redi.core
~~~~~~~~~

This module contains the primary interface for redi.

Simple, eh?

"""


from . import config
from .models import *
from .utils import is_collection




def value(key, r=config.redis):
    """Return RedisValue instance for given key.
    Optional `r` keyword argument sets Redis instance.
    """

    if is_collection(key):
        key = config.namespace_delimiter.join(key)

    return RedisValue(key, r=r)



def list(key, r=config.redis):
    """Return RedisList instance for given key.
    Optional `r` keyword argument sets Redis instance.
    """

    if is_collection(key):
        key = config.namespace_delimiter.join(key)

    return RedisList(key, r=r)