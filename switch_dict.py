#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest


class TestSwitch(unittest.TestCase):

    def test_if(self):
        """if での複数条件分岐"""
        key = 'a'
        if key == 'a':
            print 'a'
            self.assertEqual('a', key)
        elif key == 'b':
            print 'b'
            self.assertEqual('b', key)
        else:
            print 'other'
            self.assertNotIn(('a', 'b'), (key,))

    def test_dict(self):
        """dict での複数条件分岐"""
        key = 'a'

        def key_a(key):
            print 'a'
            self.assertEqual('a', key)

        def key_b(key):
            print 'b'
            self.assertEqual('b', key)

        def key_other(key):
            print 'other'
            self.assertNotIn(('a', 'b'), (key,))

        key_dict = {
            'a': key_a,
            'b': key_b
        }

        key_dict.get(key, key_other)(key)

if __name__ == '__main__':
    unittest.main()
