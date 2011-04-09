#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Redi."""

import unittest
import os


import redi

DB = os.environ.get('REDI_TEST_DB_NUM', None)
redi.init(db=DB)



class TablibTestCase(unittest.TestCase):
    """Tablib test cases."""

    def setUp(self):
        """Create simple data set with headers."""

        pass


    def tearDown(self):
        """Teardown."""
        pass





if __name__ == '__main__':
    unittest.main()
