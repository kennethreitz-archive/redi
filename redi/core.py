# -*- coding: utf-8 -*-

"""
redi.core
~~~~~~~~~

This module is the core of redi. Simple, eh?

"""


from models import *
from .config import init, redis


def value(key, r=redis):
    return RedisValue(key, r=r)

def list(key, r=redis):
    return RedisList(key, r=r)