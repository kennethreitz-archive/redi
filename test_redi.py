#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Redi."""

import unittest
import os


import redi
import redis

DB = os.environ.get('REDI_TEST_DB_NUM', None)

if DB is None:
    raise Exception('hell no')

redi.config.init(db=DB)



class RediTestCase(unittest.TestCase):
    """Redi test cases."""

    def setUp(self):
        """Create simple data set with headers."""

        self.redis = redis.Redis(db=DB)




    def tearDown(self):
        """Teardown."""
        pass
        self.redis.flushdb()


    def test_redi(self):
        a = redi.value('test')
        a.data = 'hi'


if __name__ == '__main__':
    unittest.main()
