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

    d = redi.value('dashboard:metadata'):

    d.append(dict(blah='blah'))
    d.append([1,2,3,4])


    students = redi.list('dashboard:students'):

    print students[3].get('last_name')

    for s_found in students.find('reitz'):
        do_something(s_found)


