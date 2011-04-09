# -*- coding: utf-8 -*-

import redi



from redis import Redis

v = redi.value('png')

v.value = 'me'

print repr(v.value)
# v.expire(6)

v.delete()

print repr(v.value)