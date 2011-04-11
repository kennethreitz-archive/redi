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
        if len(key) < 2:
            keys.append(key)

    return keys


class Objectify(object):
    """Objects out of NOTHING!"""

    def __init__(self, rootkeys, redis=config.redis):
        super(Objectify, self).__init__()

        self.redis = redis
        self.rootkeys = rootkeys

        self.update()


    def __repr__(self):
        return repr(self.dict)


    def __getitem__(self, key):
        return getattr(self, key, None)

    @property
    def dict(self):
        d = self.__dict__
        del d['redis']

        return d

    def items(self):
        """Returns items within object."""
        return self.dict.items()


    def keys(self):
        """Returns keys within object."""
        return self.dict.keys()


    def update(self):
        for key in self.rootkeys:
            self.__dict__[key[-1]] = (
                models.auto_type(key[-1], redis=self.redis, o=True)
            )

        # keys = []

        # for key in self.redis.keys('*'):
        #     keys.append(key)
        # print keys




