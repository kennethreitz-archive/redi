#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
redi.models
~~~~~~~~~~~

This module contains most of the functionality of redi.

"""



from UserDict import DictMixin

from . import config
from .ext import expand_key
from .utils import ListMixin, is_collection

from clint.textui import colored



class BaseRedis(object):
    """Base Redis interface object. Provides Redis instance and
    datatype mapping."""


    def __init__(self, redis=None):
        super(BaseRedis, self).__init__()

        if redis is None:
            self.redis = config.redis

        self.redis = redis


    @staticmethod
    def to_redis(o):
        """Converts Python datatypes to Redis values."""

        # don't serialize internal datatype classesf
        if isinstance(o, SubList) or isinstance(o, SubDict):
            o = o.data

        return config.encoder(o)


    def to_python(self, o):
        """Converts Redis values to Python datatypes."""
        try:
            v = config.decoder(o)

            if isinstance(v, dict):
                return SubDict(v, self.save)

            elif is_collection(v):
                return SubList(v, self.save)

            try:
                if not isinstance(v, float):
                    return int(v)
            except ValueError:
                pass

            try:
                if not isinstance(v, int):
                    return float(v)
            except ValueError:
                pass

            return v

        except (ValueError, TypeError):
            try:
                return unicode(o, config.str_codec)
            except (UnicodeDecodeError, TypeError):
                return o

    def save(self, *args):
        pass



class RedisKey(BaseRedis):
    """Contains methods that can be applied to any Redis key."""

    def __init__(self, key, redis=None):
        super(RedisKey, self).__init__(redis=redis)

        self.key = key


    def __repr__(self):
        return '<redis-key {0}>'.format(self.key)


    def delete(self):
        """Removes this key from Redis."""
        return self.redis.delete(self.key)


    def expire(self, s):
        """Expires this key from Redis in given seconds."""
        # TODO: Accept datetime for expire_at

        return self.redis.expire(self.key, s)


    def rename(self, new_name, safe=True):
        """Renames this key."""

        new_name = expand_key(new_name)

        if safe:
            if self.redis.renamenx(self.key, new_name):
                self.key = new_name
                return True
            return False
        else:
            self.redis.rename(self.key, new_name)
            self.key = new_name
            return True


    @property
    def children(self):
        """Lists all children of current key."""

        keys = self.redis.keys('{0}*'.format(self.key))

        for key in keys:
            yield key



class RedisValue(RedisKey):
    """Redis value of awesomeness."""


    def __init__(self, key, redis=None):
        super(RedisValue, self).__init__(key, redis=redis)

        self.key = key


    @property
    def _raw(self):
        return self.redis.get(self.key)


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

    def __init__(self, key, redis=None):
        super(RedisList, self).__init__(key, redis=redis)
        # print r.db
        # print self.redis
        self.key = key



    def __repr__(self):
        return '<redis-list {0}>'.format(self.key)


    @property
    def _raw(self):
        for v in self.redis.lrange(self.key, 0, -1):
            yield v


    def save(self, value, i=None):
        """Save list."""

        self[i] = value


    def __getitem__(self, i):
        is_single = not isinstance(i, slice)

        if is_single:
            value = self.redis.lindex(self.key, i)
            values = self.to_python(value)
            try:
                values.i = i
            except AttributeError:
                pass


        else:
            start = 0 if i.start is None else i.start
            stop = -1 if i.stop is None else i.stop

            values = self.redis.lrange(self.key, start, stop)
            values = map(self.to_python, values)

            for i in range(start, start+len(values)):
                try:
                    values[i].i = i
                except AttributeError:
                    pass


        return values


    def __setitem__(self, i, value):
        v = self.to_redis(value)
        return self.redis.lset(self.key, i, v)


    def __delitem__(self, i):

        for value in self[i]:
            self.redis.lrem(self.key, value)


    def __iter__(self):
        for v in self[:]:
            yield v


    def __len__(self):
        return self.redis.llen(self.key)


    def __contains__(self, value):
        i = self.index(value)
        return (i is not None)


    def insert(self, index, value, before=True):

        refvalue = self[index]
        where = 'BEFORE' if before else 'AFTER'

        return self.redis.linsert(self.key, where, refvalue, value)


    def index(self, value):
        """Returns first found index of given value."""

        for i, v in enumerate(self):
            try:
                if value.__dict__ == v.__dict__:
                    return i
            except AttributeError:
                if value == v:
                    return i


    def append(self, value, right=True):
        v = self.to_redis(value)

        if right:
            return self.redis.rpush(self.key, v)
        else:
            return self.redis.lpush(self.key, v)


    def extend(self, values):
        for value in values:
             v = self.to_redis(value)
             self.append(v)

    def rpush(self, value):
        """Redis RPUSH."""
        return self.append(value, right=True)


    def lpush(self, value):
        """Redis LPUSH."""
        return self.append(value, right=False)


    def lpop(self):
        """Redis LPOP."""
        return self.pop(right=False)


    def rpop(self):
        """Redis RPOP."""
        return self.pop(right=True)


    def pop(self, right=True):
        """Redis (R|L)POP."""

        if right:
            v = self.redis.lpop(self.key)
        else:
            v = self.redis.rpop(self.key)


        return self.to_python(v)


    def brpop(self, timeout=config.block_timeout):
        """Redis BRPOP."""
        return self.bpop(timeout, right=True)


    def blpop(self, timeout=config.block_timeout):
        """Redis BLPOP."""
        return self.bpop(timeout, right=False)


    def bpop(self, timeout=config.block_timeout, right=True):
        """Redis B(R|L)POP."""

        if right:
            v = self.redis.brpop(self.key, timeout)
        else:
            v = self.redis.blpop(self.key, timeout)

        try:
            return self.to_python(v[1])
        except TypeError:
            return None


    def find(self, *search):
        """FINDS ALL TEH THINGS."""

        for item in self._raw:
            for s in search:
                if callable(s):
                    if s(item):
                        yield item
                else:
                    if s in item:
                        yield self.to_python(item)



class SubList(ListMixin):
    """Lists within Redis values."""

    def __init__(self, l, writer):
        self.data = l
        self.writer = writer
        self.i = None


    def write(self):
        """Writes List to Redis."""
        if self.i is not None:
            self.writer(self.data, self.i)
        else:
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
        self.i = None

    def write(self):
        """Writes Dict to Redis."""
        if self.i is not None:
            self.writer(self.data, self.i)
        else:
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





