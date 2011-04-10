#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Redi."""

import unittest
import os


import redi




class RediTestSuite(unittest.TestCase):
    """Redi test suite."""

    def setUp(self):


        redi.config.init(db=DB)




    def tearDown(self):

        redi.db.flush()

        assert len(redi.db.keys('*')) is 0


    def test_redi(self):

        a = redi.value('test')
        a.data = 'hi'


if __name__ == '__main__':

    DB = os.environ.get('REDI_TEST_DB_NUM', None)

    if DB is None:
        raise Exception('REDI_TEST_DB_NUM env must be set.')



    unittest.main()
