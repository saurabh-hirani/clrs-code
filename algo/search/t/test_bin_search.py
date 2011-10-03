#!/usr/bin/env python

import unittest
import random

import lib.utils
import algo.sort.stability_chkr

class BinSearch(unittest.TestCase):
    modname = 'algo.search.bin_search'
    mod = lib.utils.fqdn_import(modname)
    search_range = 20

    def testPresentElem(self): 
        elemlist = range(self.search_range)
        target_idx = random.randrange(0, self.search_range - 1, 1) 
        idx = self.mod.do_search(elemlist, elemlist[target_idx])
        self.assertEqual(idx, target_idx)

        target_idx = random.randrange(0, self.search_range - 1, 1) 
        idx = self.mod.do_search(elemlist, elemlist[target_idx],
                                 cmprator = lambda x,y: (x - y))
        self.assertEqual(idx, target_idx)

    def testNotPresentElem(self):
        elemlist = range(self.search_range)
        elem_not_present = self.search_range + 1
        idx = self.mod.do_search(elemlist, elem_not_present)
        self.assertEqual(idx, -1)

    def testPresentLeft(self):
        elemlist = [1] * 100
        leftmost_idx = 0
        idx = self.mod.do_search(elemlist, 1, strategy = 'left')
        self.assertEqual(idx, leftmost_idx)

        elemlist = range(self.search_range)
        target_idx = random.randrange(0, self.search_range - 3, 1) 
        target_elem = elemlist[target_idx]
        elemlist[target_idx:target_idx + 3] = [target_elem] * 3
        idx = self.mod.do_search(elemlist, target_elem, 
                                 strategy = 'left')
        self.assertEqual(idx, target_idx) 

    def testNotPresentLeft(self):
        elemlist = [1] * 100
        idx = self.mod.do_search(elemlist, 2, strategy = 'left')
        self.assertEqual(idx, -1)

    def testPresentRight(self):
        elemlist = [1] * 100
        rightmost_idx = 99
        idx = self.mod.do_search(elemlist, 1, strategy = 'right')
        self.assertEqual(idx, rightmost_idx)

        elemlist = range(self.search_range)
        target_idx = random.randrange(0, self.search_range - 3, 1) 
        target_elem = elemlist[target_idx]
        elemlist[target_idx:target_idx + 3] = [target_elem] * 3
        idx = self.mod.do_search(elemlist, target_elem, 
                                 strategy = 'right')
        self.assertEqual(idx, target_idx + 2) 

    def testNotPresentRight(self):
        elemlist = [1] * 100
        idx = self.mod.do_search(elemlist, 2, strategy = 'right')
        self.assertEqual(idx, -1)

if __name__ == "__main__":
    unittest.main()
