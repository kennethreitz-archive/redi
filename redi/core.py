# -*- coding: utf-8 -*-

"""
redi.core
~~~~~~~~~

This module contains the primary interface for redi.

Simple, eh?
"""


from . import config, models, db, ext, utils


def key(key, redis=config.redis, default=None):
    """Return Redi Datatype instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    Optional `default` keyword sets default Redis datatype if no value
    exists.
    """

    return models.auto_type(
        utils.compress_key(key), redis=config.redis, default=default
)


def list_string(key, redis=config.redis):
    """Return RedisValue instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return models.RedisListString(utils.compress_key(key), redis=config.redis)


def dict_string(key, redis=config.redis):
    """Return RedisValue instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return models.RedisDictString(utils.compress_key(key), redis=config.redis)


def string(key, redis=config.redis):
    """Return RedisValue instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return models.RedisString(utils.compress_key(key), redis=config.redis)


def list(key, redis=config.redis):
    """Return RedisList instance for given key.
    Optional `redis` keyword argument sets Redis instance.
    """

    return models.RedisList(utils.compress_key(key), redis=config.redis)

# REDI.S!
s = ext.Objectify(rootkeys=ext.root_keys(), redis=config.redis)