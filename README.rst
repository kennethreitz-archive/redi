RedisAlchemy: Redis Awesomeness
===============================

**Warning:** this may or may not be a good idea.

I'm certianly not an efficiency expert. I just want to be able to do things easily.


Ideas
-----

Everything should be serialized to JSON by default.


Example usage ::

    from redisalchemy import RList, RSet, RList, search, find

    students = RList('dashboard:students')

    students.append(dict(blah='blah'))
    students.appdend(someobject)

    for i, student in enumerate(students):
        students[i] = srcub(student)
