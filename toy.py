# -*- coding: utf-8 -*-

import redisalchemy as ra

ra.config()

student = ra.Rvalue('dashboard:student')
print student.value

student.value = [1,2,3,4, '5']
print student.type
