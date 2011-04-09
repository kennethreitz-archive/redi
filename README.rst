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

- **Easy to import** ::

    import redi


- **Resis Value as a List** ::


    d = redi.value('haystack:metalist')

    d.append(dict(blah='blah'))
    d.append([1,2,3,4])

    # redis: "[{\"blah\": \"blah\"}, [1, 2, 3, 4]]"


- **Resis Value as a Dict** ::

    d = redi.value('haystack:metadict')

    d.data = {}

    d.data['timestamp'] = datetime.now().isoformat()
    d.data['values'] = [12, 82, 248.2]

    # redis: "{\"timestamp\": \"2011-04-09T03:39:03.204597\", \"values\": [  12, 82, 248.2]}"


- **Redis List as a List** ::


    >>> students = redi.list('haystack:students')

    >>> students[3]
    {'first': 'kenneth', 'last': 'unknown'}

    >>> students[3].update(last='reitz')

    >>> list(students.find('reitz'))
    [{'first': 'kenneth', 'last': 'reitz'}]



Installation
------------

To install redi, simply: ::

    $ pip install redi

Or, if you absolutely must: ::

    $ easy_install redi


But, you really shouldn't do that.



License
-------

The ISC License. ::

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


Contribute
----------

If you'd like to contribute, simply fork the repository, commit your changes to the develop branch (or branch off of it), and send a pull request. Make sure you add yourself to AUTHORS.



Advanced
--------

- The de/serializing interface is completely overridable. You can fully swap JSON out with YAML w/ two lines of code.
- You can use blocking pops with configurable timeouts.
- Namespace aware!


Roadmap
-------

- Polish
- Add Sets (maybe)
- SHIP IT
- Tests
- Documentation
