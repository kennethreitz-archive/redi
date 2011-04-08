# -*- coding: utf-8 -*-

import redisalchemy as ra


student = ra.Rvalue('dashboard:student')
# print student.value

student.value = {'hi': 'bye'}


student.value['face'] = 'book'
# student.value.append('hi')



print student.value