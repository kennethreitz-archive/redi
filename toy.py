# -*- coding: utf-8 -*-

import redi

student = redi.Rvalue('dashboard:student')

print student.value

student.value = {'hi': 'bye'}
student.value['face'] = 'book'

print student.value