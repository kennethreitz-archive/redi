# -*- coding: utf-8 -*-

"""
redi.core
~~~~~~~~~

This module contains the primary interface for redi.

Simple, eh?

"""


from models import *
from .config import init, redis



def value(key, r=redis):
    """Return RedisValue instance for given key.
    Optional `r` keyword argument sets Redis instance.
    """

    return RedisValue(key, r=r)



def list(key, r=redis):
    """Return RedisList instance for given key.
    Optional `r` keyword argument sets Redis instance.
    """

    return RedisList(key, r=r)