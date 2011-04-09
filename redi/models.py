#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
redi.models
~~~~~~~~~~~

This module contains most of the functionality of redi.

"""



from UserDict import DictMixin


from .config import redis, ENCODER, DECODER, STR_ENCODING
from .utils import ListMixin, is_collection




class BaseRedis(object):
    """Base Redis interface object. Provides Redis instance and
    datatype mapping."""


    def __init__(self, redis=redis):
        super(BaseRedis, self).__init__()
        self.redis = redis


    @staticmethod
    def to_redis(o):
        """Converts Python datatypes to Redis values."""
        if is_collection(o):
            return ENCODER(o)
        else:
            return o


    def to_python(self, o):
        """Converts Redis values to Python datatypes."""
        try:
            v = DECODER(o)

            if isinstance(v, dict):
                return SubDict(v, self.save)

            elif is_collection(v):
                return SubList(v, self.save)

            else:
                return o

        except (ValueError, TypeError):
            try:
                return unicode(o, STR_ENCODING)
            except (UnicodeDecodeError, TypeError):
                return o



class RedisKey(BaseRedis):
    """Contains methods that can be applied to any Redis key."""

    def __init__(self, key, r=redis):
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

    def __init__(self, key, r=redis):
        super(RedisValue, self).__init__(key, r=r)
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




class RedisList(BaseRedis):
    """Redis list of awesomeness."""

    def __init__(self, key):
        super(RedisList, self).__init__()
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
        # self.__dict__.update(d)


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







