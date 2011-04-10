#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
redi.models
~~~~~~~~~~~

This module contains most of the functionality of redi.

"""

import uuid

from operator import itemgetter
from UserDict import DictMixin

from . import config
from .utils import ListMixin, is_collection, compress_key, expand_key

from clint.textui import colored




class RedisKey(object):
    """Contains methods that can be applied to any Redis key."""

    def __init__(self, key, redis=None):

        self.key = key

        if redis is None:
            self.redis = config.redis

        self.redis = redis
        self.uuid = uuid.uuid4().hex


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

        new_name = compress_key(new_name)

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

        namespace = expand_key(self.key) + ['*']

        key = compress_key(namespace)
        keys = self.redis.keys(key)

        for key in keys:
            yield key


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



class RedisString(RedisKey):
    """Redis String interface."""

    def __init__(self, key, redis=None):
        super(RedisString, self).__init__(key, redis=redis)

        self.key = key


    def __repr__(self):
        return '<redis-string {0}>'.format(self.key)


    @property
    def _raw(self):
        """Returns raw Redis data."""
        return self.redis.get(self.key)


    def save(self, value):
        """Saves current value to Database."""
        v = self.to_redis(value)
        return self.redis.set(self.key, v)


    @property
    def data(self):
        """Writes value to database."""
        v = self.redis.get(self.key)
        return self.to_python(v)


    @data.setter
    def data(self, value):
        """Writes value to database."""
        self.save(value)


    @property
    def type(self):
        return self.data.__class__


    def write(self):
        return self.data.write()


    def __getitem__(self, item):
        return self.data.__getitem__(item)


    def __setitem__(self, k, v):
        return self.data.__setitem__(k, v)


    def __delitem__(self, k):
        return self.data.__delitem__(k)



class RedisListString(RedisString, ListMixin):
    """Redis value of awesomeness."""


    def __init__(self, key, redis=None):
        super(RedisListString, self).__init__(key, redis=redis)
        self.key = key


    def __repr__(self):
        return '<redis-list-string {0}>'.format(self.key)


    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __setitem__(self, k, v):
        return self.data.__setitem__(k, v)

    def __delitem__(self, k):
        return self.data.__delitem__(k)

    def _get_element(self, i):
        return self.data._get_element(i)

    def _set_element(self, i, value):
        return self.data._set_element(i, value)

    def __len__(self):
        return self.data.__len__()

    def _resize_region(self, start, end, new_size):
        return self.data._resize_region(start, end, new_size)

    def _constructor(self, iter):
        return self.data._constructor(iter)


class RedisDictString(RedisString, DictMixin):
    """Redis value of awesomeness."""


    def __init__(self, key, redis=None):
        super(RedisDictString, self).__init__(key, redis=redis)
        self.key = key


    def __repr__(self):
        return '<redis-dict-string {0}>'.format(self.key)


    def get(self, item):
        return self.data.get(item)


    def keys(self):
        return self.data.keys()





class RedisList(RedisKey):
    """Redis list of awesomeness."""

    def __init__(self, key, redis=None):
        super(RedisList, self).__init__(key, redis=redis)
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

    def sorted_by(self, key, reverse=False ):

        return sorted(self, key=itemgetter(key), reverse=reverse)


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

    def __delitem__(self, k):
        del self.data[k]
        self.write()

    def __repr__(self):
        return repr(self.data)

    def keys(self):
        return self.data.keys()
