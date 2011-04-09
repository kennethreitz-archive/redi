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



def _expand_key(key):
    """Expands tupled keys."""

    if is_collection(key):
        return config.namespace_delimiter.join(key)



def value(key, r=config.redis):
    """Return RedisValue instance for given key.
    Optional `r` keyword argument sets Redis instance.
    """

    return RedisValue(_expand_key(key), r=r)



def list(key, r=config.redis):
    """Return RedisList instance for given key.
    Optional `r` keyword argument sets Redis instance.
    """

    return RedisList(_expand_key(key), r=r)