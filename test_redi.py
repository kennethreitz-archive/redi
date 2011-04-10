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
        self.assertEqual(len(redi.db.keys('*')), 0)


    def test_value_as_dict(self):

        a = redi.dict_string('test')
        self.assertEqual(a.type, type(None))

        a.data = {}
        self.assertEqual(a.type, redi.models.SubDict)

        a['face'] = 'book'

        self.assertEqual(a['face'], 'book')
        self.assertEqual(a.get('face'), 'book')
        self.assertEqual(a.data['face'], 'book')
        self.assertEqual(a.data.get('face'), 'book')

        del a['face']
        self.assertEqual(a['face'], None)

        a.delete()
        self.assertEqual(a.data, None)


    def test_value_as_list(self):

        a = redi.list_string('test')


    def test_key_rename_unsafe(self):

        a = redi.string('rename_me')
        a.data = 'i am going to be renamed'
        success = a.rename('renamed', safe=False)

        b = redi.string('renamed')
        c = redi.string('rename_me')

        self.assertTrue(success)
        self.assertEqual(a.data, b.data)
        self.assertEqual(c.data, None)

        a.delete()
        b.delete()
        c.delete()


    def test_key_rename_unsafe_overwrite(self):

        a = redi.string('rename_me')
        a.data = 'i am going to be renamed'

        orig_value = a.data
        orig_key = a.key

        b = redi.string('exists')
        b.data = 'yes i do'

        success = a.rename('exists', safe=False)

        self.assertTrue(success)
        self.assertEqual(orig_value, a.data)
        self.assertNotEqual(a.key, orig_key)

        a.delete()
        b.delete()


    def test_key_rename_safe(self):

        a = redi.string('rename_me')
        a.data = 'i am going to be renamed'

        orig_value = a.data
        orig_key = a.key

        success = a.rename('exists', safe=True)

        self.assertTrue(success)
        self.assertEqual(orig_value, a.data)
        self.assertNotEqual(a.key, orig_key)

        a.delete()


    def test_key_rename_safe_overwrite(self):

        a = redi.string('rename_me')
        a.data = 'i am going to be renamed'

        orig_value = a.data
        orig_key = a.key

        b = redi.string('exists')
        b.data = 'yes i do'

        success = a.rename('exists', safe=True)

        self.assertFalse(success)
        self.assertEqual(orig_value, a.data)
        self.assertEqual(a.key, orig_key)

        a.delete()
        b.delete()



if __name__ == '__main__':

    DB = os.environ.get('REDI_TEST_DB_NUM', None)

    if DB is None:
        raise Exception('REDI_TEST_DB_NUM env must be set.')

    unittest.main()
