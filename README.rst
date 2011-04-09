Redi: Redis Awesomeness
=======================

**Warning:** this may or may not be a good idea.

I'm certainly not an efficiency expert. I just want to be able to do things easily.


Features
--------

- Pythonic interface to Redis keys/values.
- Everything is automatically serialized to JSON. This is configurable.


Ideas
-----

- Offer limited type-specific search.



Example usage ::

    import redi

    metadata = redi.value('dashboard:metadata')

    metadata.append(dict(blah='blah'))
    metadata.append(someobject)

    # students.contain('value')
    #


    # students.any_contain('value')
    #

    # students.any_contain_any('value')
    # list of lists
    # list of dicts (keys)


    #for (i, student) in enumerate(students):
    #    students[i] = srcub(student)


