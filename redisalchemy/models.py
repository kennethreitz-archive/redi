#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
redisalchemy.models
~~~~~~~~~~~~~~~~~~~

This module contains most of the functionality of redis.

"""



from UserDict import DictMixin

import jsonpickle

from .config import redis
from .utils import ListMixin



class BaseRedis(object):
    """Base Redis object. """

    redis = config.redis


    def __init__(self):
        super(BaseRedis, self).__init__()
        self._po = None


    @staticmethod
    def to_redis(o):
        if hasattr(o, '__getitem__'):
            return jsonpickle.encode(o)
        else:
            return o


    def to_python(self, o):
        try:
            v = jsonpickle.decode(o)

            if isinstance(v, list):
                return SubList(v)
            elif isinstance(v, dict):
                return SubDict(v, self.save)

        except ValueError:
            return o




class SubList(list):
    """Lists within Redis values."""

    def __init__(self, l):
        self.data = l


class SubDict(DictMixin):
    """Dicts within Redis values."""

    def __init__(self, d, writer):
        self.data = d
        self.writer = writer
        # self.__dict__.update(d)

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, k, v):
        self.data[k] = v
        self.writer(self.data)

    def __repr__(self):
        return repr(self.data)


class SubValue(object):
    """Redis Values"""
    pass



class Rlist(BaseRedis):
    """Redis list of awesomeness."""

    def __init__(self, key):
        super(Rlist, self).__init__()
        self.key = key
        self._po = []
        self.sync()

    def __repr__(self):
        return '<redis-list {0}>'.format(self.key)

    def __getitem__(self, i):
        pass

    def __len__(self):
        return len(self._po)

    def append(self, *values):
        for value in value:
            self._po.append(value)

    def lpop(self):
        return self.pop(right=False)

    def rpop(self):
        return self.pop(right=True)

    def pop(self, right=True):
        # pops redis datasaet, resyncs?
        return None

    def sort(self, direction):
        pass

    def sync(self):
        """Syncs dataset."""
        pass

    def delete(self):
        redis.delete(key)
        self.sync()


class Rvalue(BaseRedis):
    """Redis string of awesomeness."""

    def __init__(self, key):
        super(Rvalue, self).__init__()
        self.key = key

    def __repr__(self):
        return '<redis-value {0}>'.format(self.key)

    def save(self, value):
        v = self.to_redis(value)
        return self.redis.set(self.key, v)

    @property
    def value(self):
        v = self.redis.get(self.key)
        return self.to_python(v)


    @value.setter
    def value(self, value):
        self.save(value)

    @property
    def type(self):
        v = self.redis.get(self.key)
        return type(self.value)

