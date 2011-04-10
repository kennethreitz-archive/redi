# -*- coding: utf-8 -*-

"""
redi.ext
~~~~~~~~

This module contains extra stuff.

"""


from . import config
from .utils import is_collection



def expand_key(key):
    """Expands tupled keys."""

    if is_collection(key):
        key = config.namespace_delimiter.join(key)

    return key


def auto_type(key, redis=None, default=None):
    """Returns datatype instance"""

    if redis is None:
        redis = config.redis

