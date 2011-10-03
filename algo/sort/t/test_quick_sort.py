#!/usr/bin/env python

import unittest
import random

import lib.utils
import algo.sort.stability_chkr

class MergeSort(unittest.TestCase):
    modname = 'algo.sort.qsort'
    mod = lib.utils.fqdn_import(modname)
    sort_range = 10

    def testAscSort(self): 
        """ test ascending sort """
        elemlist = range(self.sort_range)
        backup_elemlist = list(elemlist)

        """ test asc sort without comparator """
        random.shuffle(elemlist)
        self.mod.do_sort(elemlist)
        self.assertEqual(elemlist, backup_elemlist)

        """ test asc sort with comparator """
        random.shuffle(elemlist)
        self.mod.do_sort(elemlist, cmprator=lambda x,y: (x - y))
        self.assertEqual(elemlist, backup_elemlist)

    def testAscSortRandPivot(self): 
        """ test ascending sort """
        elemlist = range(self.sort_range)
        backup_elemlist = list(elemlist)

        """ test asc sort without comparator """
        random.shuffle(elemlist)

        """ set random pivot option """
        self.mod.choose_random_pivot()

        """ test asc sort without comparator """
        self.mod.do_sort(elemlist)
        self.assertEqual(elemlist, backup_elemlist)

        """ test asc sort with comparator """
        random.shuffle(elemlist)
        self.mod.do_sort(elemlist, cmprator=lambda x,y: (x - y))
        self.assertEqual(elemlist, backup_elemlist)

    def testDescSort(self): 
        """ test descending sort """
        elemlist = range(self.sort_range)
        backup_elemlist = list(elemlist)
        random.shuffle(elemlist)
        self.mod.do_sort(elemlist, cmprator=lambda x,y: (y - x))
        self.assertNotEqual(elemlist, backup_elemlist)
        backup_elemlist.reverse()
        self.assertEqual(elemlist, backup_elemlist)
        
    def testDescSortRandPivot(self): 
        """ test descending sort """
        elemlist = range(self.sort_range)
        backup_elemlist = list(elemlist)
        random.shuffle(elemlist)

        """ set random pivot option """
        self.mod.choose_random_pivot()

        self.mod.do_sort(elemlist, cmprator=lambda x,y: (y - x))
        self.assertNotEqual(elemlist, backup_elemlist)
        backup_elemlist.reverse()
        self.assertEqual(elemlist, backup_elemlist)

if __name__ == "__main__":
    unittest.main()
