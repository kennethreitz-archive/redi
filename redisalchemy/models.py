#!/usr/bin/env python
# -*- coding: utf-8 -*-


import config

import jsonpickle







class BaseRedis(object):

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


    @staticmethod
    def to_python(o):
        try:
            return jsonpickle.decode(o)
        except ValueError:
            return o




class SubList(object):
    """Lists within Redis values."""

    def __init__(self):
        pass


class SubDict(object):
    """Dicts within Redis values."""

    def __init__(self):
        pass


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

    @property
    def value(self):
        v = self.redis.get(self.key)
        return self.to_python(v)

    @value.setter
    def value(self, value):
        v = self.to_redis(value)
        self.redis.set(self.key, v)

        return v

    def type(self):
        v = self.redis.get(self.key)
        v = self.to_python(v)


class Rset(BaseRedis):
    """Redis string of awesomeness."""

    def __init__(self, key):
        super(Rset, self).__init__()
        pass


class Rsomething(object):
    """Transforms into whatever it needs to be."""
    pass



