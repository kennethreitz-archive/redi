# -*- coding: utf-8 -*-

import redi

v = redi.value('png')

# with open('kr.png', 'rb') as f:
    # v.value = f.read()
    # f.write(v.value)
# unicode(v.value)

v.value = 'hi'

# print type(v.value)
print v.value

# print repr(v.value)
# print unicode(v.value)