# -*- coding: utf-8 -*-

"""
redi.db
~~~~~~~

This module contains simple mappings to

"""

from . import config


def flush(redis=None):
    """Flushes Redis database."""

    if redis is None:
        redis = config.redis

    return redis.flushdb()

def keys(search, redis=None):
    """Flushes Redis database."""

    if redis is None:
        redis = config.redis

    return redis.keys(search)

