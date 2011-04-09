Redi: Redis Awesomeness
=======================

Redi is Redis that's ready for Python. It's powered by redis-py, and it's awesome.

Essentially, **redi** allows you to interact with your Redis datatypes as if they were native Python objects.


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


Advanced
--------

- The de/serializing interface is completely overridable. You swap JSON out with YAML w/ two lines of code.
- You can use blocking pops with configurable timeouts.


Roadmap
-------

- Polish
- Add Sets (maybe)
- SHIP IT
- Tests
- Documentation


License
-------

::

    Copyright (c) 2011, Kenneth Reitz <me@kennethreitz.com>

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.