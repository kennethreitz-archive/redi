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
from .utils import ListMixin, is_collection



class BaseRedis(object):
    """Base Redis object. """

    redis = redis

    def __init__(self):
        super(BaseRedis, self).__init__()


    @staticmethod
    def to_redis(o):
        if hasattr(o, '__getitem__'):
            return jsonpickle.encode(o)
        else:
            return o


    def to_python(self, o):
        try:
            v = jsonpickle.decode(o)

            if isinstance(v, dict):
                return SubDict(v, self.save)

            elif is_collection(v):
                return SubList(v, self.save)

            else:
                return o

        except (ValueError, TypeError):
            return o




class SubList(ListMixin):
    """Lists within Redis values."""

    def __init__(self, l, writer):
        self.data = l
        self.writer = writer


    def write(self):
        self.writer(self.data)


    def _get_element(self, i):
        return self.data[i]


    def _set_element(self, i, value):
        self.data[i] = value
        self.write()

    def __len__(self):
        return len(self.data)

    def _resize_region(self, start, end, new_size):

        self.data[start:end] = [None] * new_size
        self.write()

    def _constructor(self, iter):
        return SubList(iter, self.writer)

    def __iter__(self):
        for item in self.data:
            yield item


class SubBytes(object):

    def __init__(self, bytes, writer):
        self.data = bytes
        self.writer = writer

    def write(self):
        self.writer(self.data)

class SubString(object):

    def __init__(self, unicodes, writer):
        self.data = unicodes
        self.writer = writer

    def write(self):
        self.writer(self.data)



class SubDict(DictMixin):
    """Dicts within Redis values."""

    def __init__(self, d, writer):
        self.data = d
        self.writer = writer
        # self.__dict__.update(d)


    def write(self):
        self.writer(self.data)


    def __getitem__(self, item):
        return self.data.get(item)


    def __setitem__(self, k, v):
        self.data[k] = v
        self.write()


    def __repr__(self):
        return repr(self.data)


class Rlist(BaseRedis):
    """Redis list of awesomeness."""

    def __init__(self, key):
        super(Rlist, self).__init__()
        self.key = key
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

