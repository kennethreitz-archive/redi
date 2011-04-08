# -*- coding: utf-8 -*-

import redisalchemy as ra


student = ra.Rvalue('dashboard:student')

student.value = {'hi': 'bye'}
raw_input()
student.value['face'] = 'book'

print student.value