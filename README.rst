Redi: Redis Awesomeness
=======================

**Warning:** this may or may not be a good idea. I am not an efficiency expert.

> I don't need it to be super efficient. I just want it to work easily without being incredibly stupid.


Features
--------

- Pythonic interface to Redis keys/values.
- Everything is automatically serialized to JSON. This is configurable.
- ^^ Including custom objects.
- Limited type-specific search.



Usage
-----

**Simple value interface.**

Resis Value as a List: ::

    import redi

    d = redi.value('haystack:metalist')

    d.append(dict(blah='blah'))
    d.append([1,2,3,4])

    # redis: "[{\"blah\": \"blah\"}, [1, 2, 3, 4]]"


Resis Value as a Dict: ::

    d = redi.value('haystack:metadict')

    d.data = {}

    d.data['timestamp'] = datetime.now().isoformat()
    d.data['values'] = [12, 82, 248.2]

    # redis: "{\"timestamp\": \"2011-04-09T03:39:03.204597\", \"values\": [12, 82, 248.2]}"


**Simple list interface.** ::


    students = redi.list('haystack:students')

    print students[3].get('last_name')
    del students[3]

    for s_found in students.find('reitz'):
        do_something(s_found)


