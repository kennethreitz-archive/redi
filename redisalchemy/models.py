#!/usr/bin/env python
# -*- coding: utf-8 -*-


import config


__all__ = ('RList', 'RString', 'RSet')


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



class RList(BaseRedis):
    """Redis list of awesomeness."""

    def __init__(self, key):
        super(RList, self).__init__()
        self.key = key
        self._po = []

    def __repr__(self):
        return '<redis-list {0}>'.format(self.key)

    def __getitem__(self, i):
        pass

    def append(self, value):
        pass

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




class RString(BaseRedis):
    """Redis string of awesomeness."""

    def __init__(self, key):
        super(RString, self).__init__()
        pass


class RSet(BaseRedis):
    """Redis string of awesomeness."""

    def __init__(self, key):
        super(RSet, self).__init__()
        pass


def RSomething(object):
    """Transforms into whatever it needs to be."""
    pass



def BaseRedis(object):

    redis = config.redis

    def __init__(self
        super(BaseRedis, self).__init__()):
        self._po = None

    def __to_redis(self):
        pass

    def _