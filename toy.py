# -*- coding: utf-8 -*-

import redi


class Test(object):
    def __init__(self, y='heim'):
        self.x = 'hi'
        self.y = y

# meta = redi.value('dashboard:metadata')

# meta.data = {}
# meta.data.update(dict(blah='blah'))
# meta.data.update(dict(face='book'))
# meta.data.update(dict(fuck='the world'))
# # meta.data.append([1,2,3,4])


stack = redi.list(('stack', 'this'))


# stack.append(Test())
# stack.append([1,2,3,4])
# stack.append('imma be bytes')

# print len(stack)

# for item in stack:
    # print item
    # print type(item)

# stack[11] = {'f': 'u'}
# stack.append({'f': 'u'})

a = Test()
if 1:
    # pass
    stack.delete()
    stack.append('cheese')
    stack.append('bobo')
    stack.append('chia pets')
    stack.append(4)
    # print '\o/'
# print stack[:]

print list(stack.find('ch'))
# stack.insert(1, 2)

# print '-----'
# print a in stack


# print type(stack[0])

# print stack[:][0]
# print stack.index(1)
# print stack[2]
del stack[:]
# print len(stack)

# print stack[:]
# print len(stack)
# print stack.pop()
# print len(stack)