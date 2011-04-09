#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
redi.models
~~~~~~~~~~~

This module contains most of the functionality of redi.

"""



from UserDict import DictMixin

from .utils import ListMixin, is_collection

from . import config



class BaseRedis(object):
    """Base Redis interface object. Provides Redis instance and
    datatype mapping."""


    def __init__(self, redis=config.redis):
        super(BaseRedis, self).__init__()
        self.redis = redis


    @staticmethod
    def to_redis(o):
        """Converts Python datatypes to Redis values."""

        if is_collection(o):
            return config.encoder(o)
        else:
            return o


    def to_python(self, o):
        """Converts Redis values to Python datatypes."""
        try:
            v = config.decoder(o)

            if isinstance(v, dict):
                return SubDict(v, self.save)

            elif is_collection(v):
                return SubList(v, self.save)

            else:
                return o

        except (ValueError, TypeError):
            try:
                return unicode(o, config.str_codec)
            except (UnicodeDecodeError, TypeError):
                return o



class RedisKey(BaseRedis):
    """Contains methods that can be applied to any Redis key."""

    def __init__(self, key, r=config.redis):
        super(RedisKey, self).__init__(redis=r)
        self.key = key


    def __repr__(self):
        return '<redis-key {0}>'.format(self.key)


    def delete(self):
        """Removes this key from Redis."""
        return self.redis.delete(self.key)


    def expire(self, s):
        """Expires this key from Redis in given seconds."""
        return self.redis.expire(self.key, s)



class RedisValue(RedisKey):
    """Redis value of awesomeness."""


    def __init__(self, key, r=config.redis):
        super(RedisValue, self).__init__(key, r=r)
        self.key = key


    def __repr__(self):
        return '<redis-value {0}>'.format(self.key)

    def save(self, value):
        v = self.to_redis(value)
        return self.redis.set(self.key, v)



    @property
    def data(self):
        v = self.redis.get(self.key)
        return self.to_python(v)


    @data.setter
    def data(self, value):
        self.save(value)


    @property
    def type(self):
        v = self.redis.get(self.key)
        return type(self.value)




class RedisList(RedisKey):
    """Redis list of awesomeness."""

    def __init__(self, key, r=config.redis):
        super(RedisList, self).__init__(key, r=r)
        self.key = key
        self.sync()

    def save(self, v, i):
        pass

    def __repr__(self):
        return '<redis-list {0}>'.format(self.key)


    def __getitem__(self, i):
        if not isinstance(i, slice(i).__class__):
            start = i
            stop = i
            single = True
        else:
            start = 0 if i.start is None else i.start
            stop = -1 if i.stop is None else i.stop
            single = False

        values = self.redis.lrange(self.key, start, stop)

        values = map(self.to_python, values)

        if single:
            values = values.pop()

        return values

    def __setitem__(self, i, value):
        v = self.to_python(value)
        return self.redis.lset(self.key, i, v)


    def __iter__(self):
        for v in self[:]:
            yield v

    def __len__(self):
        return self.redis.llen(self.key)


    def append(self, value, right=True):
        v = self.to_redis(value)

        if right:
            self.redis.rpush(self.key, v)
        else:
            self.redis.lpush(self.key, v)

    def rpush(self, value):
        self.append(value, right=True)

    def lpush(self, value):
        self.append(value, right=False)


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
        self.redis.delete(self.key)
        self.sync()






class SubList(ListMixin):
    """Lists within Redis values."""

    def __init__(self, l, writer):
        self.data = l
        self.writer = writer


    def write(self):
        """Writes List to Redis."""
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



class SubDict(DictMixin):
    """Dicts within Redis values."""

    def __init__(self, d, writer):
        self.data = d
        self.writer = writer


    def write(self):
        """Writes Dict to Redis."""

        self.writer(self.data)


    def __getitem__(self, item):
        return self.data.get(item)


    def __setitem__(self, k, v):
        self.data[k] = v
        self.write()


    def __repr__(self):
        return repr(self.data)

    def keys(self):
        return self.data.keys()





