# -*- coding: utf-8 -*-

import redi

from redis import Redis

v = redi.value('png')

print repr(v.value)