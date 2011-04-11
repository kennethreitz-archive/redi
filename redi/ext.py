# -*- coding: utf-8 -*-

"""
redi.ext
~~~~~~~~

This module contains extra stuff.

"""


from . import config
from . import models
from .utils import is_collection, compress_key, expand_key





def root_keys(redis=config.redis):

    keys = []

    for key in map(expand_key, redis.keys('*')):
        keys.append(key[0])

    return keys


class TheSInRedis(object):
    """Objects out of NOTHING!"""

    def __init__(self, redis=config.redis):
        super(TheSInRedis, self).__init__()

        self.redis = redis
        self.update()

    def __getattribute__(self, key):
        if not key in ('redis', 'rootkeys', 'update', '__dict__'):
            self.update()

        return object.__getattribute__(self, key)

    def __repr__(self):
        return repr(self.dict)


    def __getitem__(self, key):
        return getattr(self, key, None)

    @property
    def dict(self):
        d = self.__dict__
        del d['redis']
        del d['rootkeys']

        return d

    def items(self):
        """Returns items within object."""
        return self.dict.items()


    def keys(self):
        """Returns keys within object."""
        return self.dict.keys()


    def update(self):
        for key in root_keys():
            self.__dict__[key] = (
                models.auto_type(key, redis=self.redis, default='key', o=True)
            )




