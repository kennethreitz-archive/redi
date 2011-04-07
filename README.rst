RedisAlchemy: Redis Awesomeness
===============================

**Warning:** this may or may not be a good idea.

I'm certianly not an efficiency expert. I just want to be able to do things easily.


Ideas
-----

- Offer limited type-specific search.
- Treat objects as dicts.
- Offer fileobject-like interface to values
    + useful for iterating


Everything should be serialized to JSON by default. Configurable.


Example usage ::

    from redisalchemy import RList, RSet, RString, search, find

    students = RList('dashboard:students')

    students.append(dict(blah='blah'))
    students.append(someobject)

    for (i, student) in enumerate(students):
        students[i] = srcub(student)


